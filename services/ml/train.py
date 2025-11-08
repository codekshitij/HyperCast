#!/usr/bin/env python3
"""
Training Script for Weather LSTM Model

Trains the LSTM model on prepared sequences and saves the best model.
"""
import argparse
import sys
import json
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

from models.lstm_forecaster import create_model


def load_data(data_dir: Path):
    """Load training and validation data."""
    X_train = np.load(data_dir / 'X_train.npy')
    y_train = np.load(data_dir / 'y_train.npy')
    X_val = np.load(data_dir / 'X_val.npy')
    y_val = np.load(data_dir / 'y_val.npy')
    
    with open(data_dir / 'metadata.json', 'r') as f:
        metadata = json.load(f)
    
    return X_train, y_train, X_val, y_val, metadata


def train_epoch(model, train_loader, criterion, optimizer, device):
    """Train for one epoch."""
    model.train()
    total_loss = 0
    
    for X_batch, y_batch in train_loader:
        X_batch = X_batch.to(device)
        y_batch = y_batch.to(device)
        
        # Forward pass
        optimizer.zero_grad()
        outputs = model(X_batch)
        loss = criterion(outputs, y_batch)
        
        # Backward pass
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    return total_loss / len(train_loader)


def validate(model, val_loader, criterion, device):
    """Validate the model."""
    model.eval()
    total_loss = 0
    
    with torch.no_grad():
        for X_batch, y_batch in val_loader:
            X_batch = X_batch.to(device)
            y_batch = y_batch.to(device)
            
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)
            
            total_loss += loss.item()
    
    return total_loss / len(val_loader)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Train Weather LSTM model"
    )
    parser.add_argument(
        '--data-dir',
        type=str,
        default='/Users/kshitijmishra/weatherApp/data/processed',
        help='Directory containing training data'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='/Users/kshitijmishra/weatherApp/services/ml/models/checkpoints',
        help='Output directory for model checkpoints'
    )
    parser.add_argument(
        '--hidden-size',
        type=int,
        default=64,
        help='LSTM hidden size'
    )
    parser.add_argument(
        '--num-layers',
        type=int,
        default=2,
        help='Number of LSTM layers'
    )
    parser.add_argument(
        '--dropout',
        type=float,
        default=0.2,
        help='Dropout rate'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=2,
        help='Batch size'
    )
    parser.add_argument(
        '--epochs',
        type=int,
        default=100,
        help='Number of epochs'
    )
    parser.add_argument(
        '--lr',
        type=float,
        default=0.001,
        help='Learning rate'
    )
    parser.add_argument(
        '--patience',
        type=int,
        default=20,
        help='Early stopping patience'
    )
    return parser.parse_args()


def main() -> int:
    """Main training loop."""
    args = parse_args()
    
    # Setup device
    device = torch.device('mps' if torch.backends.mps.is_available() 
                         else 'cuda' if torch.cuda.is_available() 
                         else 'cpu')
    print(f"Using device: {device}")
    
    # Load data
    data_dir = Path(args.data_dir)
    if not data_dir.exists():
        print(f"Error: Data directory {data_dir} does not exist", file=sys.stderr)
        return 1
    
    print(f"\nLoading data from {data_dir}...")
    X_train, y_train, X_val, y_val, metadata = load_data(data_dir)
    
    print(f"Train samples: {len(X_train)}")
    print(f"Val samples: {len(X_val)}")
    print(f"Input shape: {X_train.shape}")
    print(f"Features: {metadata['n_features']}")
    
    # Convert to PyTorch tensors
    X_train = torch.FloatTensor(X_train)
    y_train = torch.FloatTensor(y_train)
    X_val = torch.FloatTensor(X_val)
    y_val = torch.FloatTensor(y_val)
    
    # Create data loaders
    train_dataset = TensorDataset(X_train, y_train)
    val_dataset = TensorDataset(X_val, y_val)
    
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False)
    
    # Create model
    print(f"\nCreating model...")
    model = create_model(
        input_size=metadata['n_features'],
        hidden_size=args.hidden_size,
        num_layers=args.num_layers,
        dropout=args.dropout
    )
    model = model.to(device)
    
    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")
    
    # Loss and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    
    # Training loop
    print(f"\nTraining for {args.epochs} epochs...")
    best_val_loss = float('inf')
    patience_counter = 0
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for epoch in range(args.epochs):
        train_loss = train_epoch(model, train_loader, criterion, optimizer, device)
        val_loss = validate(model, val_loader, criterion, device)
        
        print(f"Epoch {epoch+1}/{args.epochs} - "
              f"Train Loss: {train_loss:.6f}, Val Loss: {val_loss:.6f}")
        
        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            
            checkpoint = {
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'train_loss': train_loss,
                'val_loss': val_loss,
                'metadata': metadata,
                'model_config': {
                    'input_size': metadata['n_features'],
                    'hidden_size': args.hidden_size,
                    'num_layers': args.num_layers,
                    'dropout': args.dropout,
                }
            }
            
            torch.save(checkpoint, output_dir / 'best_model.pth')
            print(f"  → Saved best model (val_loss: {val_loss:.6f})")
        else:
            patience_counter += 1
            if patience_counter >= args.patience:
                print(f"\nEarly stopping after {epoch+1} epochs")
                break
    
    print(f"\n✓ Training complete!")
    print(f"Best validation loss: {best_val_loss:.6f}")
    print(f"Model saved to: {output_dir / 'best_model.pth'}")
    
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

