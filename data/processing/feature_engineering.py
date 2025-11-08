#!/usr/bin/env python3
"""
Feature Engineering for Weather Forecasting

Creates time-series sequences for LSTM training from processed weather data.
"""
import argparse
import sys
from pathlib import Path
from typing import Tuple

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import pickle


class WeatherFeatureEngineer:
    """Create features and sequences for LSTM training."""
    
    def __init__(self, sequence_length: int = 8, forecast_horizon: int = 8):
        """
        Initialize feature engineer.
        
        Args:
            sequence_length: Number of timesteps to use as input (default: 8 = 24h with 3h intervals)
            forecast_horizon: Number of timesteps ahead to predict (default: 8 = 24h ahead)
        """
        self.sequence_length = sequence_length
        self.forecast_horizon = forecast_horizon
        self.scaler = StandardScaler()
        self.feature_columns = None
        
    def prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare dataframe for feature engineering.
        
        Args:
            df: Raw time-series dataframe
            
        Returns:
            Cleaned dataframe with additional features
        """
        df = df.copy()
        
        # Ensure timestamp is datetime
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.sort_values('timestamp').reset_index(drop=True)
        
        # Remove any duplicate timestamps
        df = df.drop_duplicates(subset=['timestamp'], keep='first')
        
        # Add time-based features
        if 'timestamp' in df.columns:
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_year'] = df['timestamp'].dt.dayofyear
            df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
            df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
            df['day_sin'] = np.sin(2 * np.pi * df['day_of_year'] / 365)
            df['day_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365)
        
        # Fill missing values with forward fill then backward fill
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(method='ffill').fillna(method='bfill')
        
        return df
    
    def create_sequences(
        self,
        df: pd.DataFrame,
        fit_scaler: bool = True
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Create input-output sequences for LSTM.
        
        Args:
            df: Prepared dataframe
            fit_scaler: Whether to fit the scaler (True for training data)
            
        Returns:
            Tuple of (X, y, timestamps) where:
                X: Input sequences (n_samples, sequence_length, n_features)
                y: Target values (n_samples,)
                timestamps: Timestamps for each sample (n_samples,)
        """
        # Define feature columns (all numeric except timestamp-related)
        feature_cols = [col for col in df.columns 
                       if col not in ['timestamp', 'hour', 'day_of_year'] 
                       and df[col].dtype in [np.float64, np.float32, np.int64, np.int32]]
        
        self.feature_columns = feature_cols
        
        # Extract features
        features = df[feature_cols].values
        
        # Scale features
        if fit_scaler:
            features_scaled = self.scaler.fit_transform(features)
        else:
            features_scaled = self.scaler.transform(features)
        
        # Create sequences
        X, y, timestamps = [], [], []
        
        for i in range(len(df) - self.sequence_length - self.forecast_horizon + 1):
            # Input sequence
            X.append(features_scaled[i:i + self.sequence_length])
            
            # Target (temperature N steps ahead)
            target_idx = i + self.sequence_length + self.forecast_horizon - 1
            y.append(features_scaled[target_idx, 0])  # Assuming temperature is first column
            
            # Timestamp of the target
            if 'timestamp' in df.columns:
                timestamps.append(df.iloc[target_idx]['timestamp'])
        
        return np.array(X), np.array(y), np.array(timestamps)
    
    def save_scaler(self, filepath: Path):
        """Save the fitted scaler."""
        with open(filepath, 'wb') as f:
            pickle.dump(self.scaler, f)
    
    def load_scaler(self, filepath: Path):
        """Load a fitted scaler."""
        with open(filepath, 'rb') as f:
            self.scaler = pickle.load(f)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Create training sequences from weather data"
    )
    parser.add_argument(
        'input_file',
        type=str,
        help='Input parquet file with weather data'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='/Users/kshitijmishra/weatherApp/data/processed',
        help='Output directory for sequences'
    )
    parser.add_argument(
        '--sequence-length',
        type=int,
        default=8,
        help='Number of timesteps in input sequence (default: 8)'
    )
    parser.add_argument(
        '--forecast-horizon',
        type=int,
        default=8,
        help='Number of timesteps ahead to predict (default: 8)'
    )
    parser.add_argument(
        '--train-split',
        type=float,
        default=0.8,
        help='Fraction of data for training (default: 0.8)'
    )
    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()
    
    input_file = Path(args.input_file)
    if not input_file.exists():
        print(f"Error: {input_file} does not exist", file=sys.stderr)
        return 1
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load data
    print(f"Loading data from {input_file}...")
    df = pd.read_parquet(input_file)
    print(f"Loaded {len(df)} records")
    
    # Prepare features
    engineer = WeatherFeatureEngineer(
        sequence_length=args.sequence_length,
        forecast_horizon=args.forecast_horizon
    )
    
    df_prepared = engineer.prepare_data(df)
    print(f"Prepared data with {len(df_prepared.columns)} columns")
    
    # Create sequences
    print("Creating sequences...")
    X, y, timestamps = engineer.create_sequences(df_prepared, fit_scaler=True)
    
    if len(X) == 0:
        print("Error: Not enough data to create sequences", file=sys.stderr)
        print(f"Need at least {args.sequence_length + args.forecast_horizon} timesteps", file=sys.stderr)
        return 1
    
    print(f"Created {len(X)} sequences")
    print(f"  Input shape: {X.shape}")
    print(f"  Target shape: {y.shape}")
    
    # Split into train/val
    split_idx = int(len(X) * args.train_split)
    
    X_train, X_val = X[:split_idx], X[split_idx:]
    y_train, y_val = y[:split_idx], y[split_idx:]
    
    print(f"\nTrain: {len(X_train)} samples")
    print(f"Val: {len(X_val)} samples")
    
    # Save sequences
    print("\nSaving sequences...")
    np.save(output_dir / 'X_train.npy', X_train)
    np.save(output_dir / 'y_train.npy', y_train)
    np.save(output_dir / 'X_val.npy', X_val)
    np.save(output_dir / 'y_val.npy', y_val)
    
    # Save scaler
    engineer.save_scaler(output_dir / 'scaler.pkl')
    
    # Save metadata
    metadata = {
        'sequence_length': args.sequence_length,
        'forecast_horizon': args.forecast_horizon,
        'n_features': X.shape[2],
        'feature_columns': engineer.feature_columns,
        'train_samples': len(X_train),
        'val_samples': len(X_val),
    }
    
    import json
    with open(output_dir / 'metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"\n✓ Saved sequences and metadata to {output_dir}")
    
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

