"""
Inference Module for Weather Forecasting

Loads trained model and makes predictions.
"""
import pickle
from pathlib import Path
from typing import Optional, Dict

import numpy as np
import torch

from models.lstm_forecaster import create_model


class WeatherPredictor:
    """Wrapper for making weather predictions."""
    
    def __init__(self, model_path: Path, scaler_path: Path):
        """
        Initialize the predictor.
        
        Args:
            model_path: Path to trained model checkpoint
            scaler_path: Path to fitted scaler
        """
        self.device = torch.device('mps' if torch.backends.mps.is_available() 
                                  else 'cuda' if torch.cuda.is_available() 
                                  else 'cpu')
        
        # Load model
        checkpoint = torch.load(model_path, map_location=self.device)
        self.metadata = checkpoint['metadata']
        model_config = checkpoint['model_config']
        
        self.model = create_model(**model_config)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model = self.model.to(self.device)
        self.model.eval()
        
        # Load scaler
        with open(scaler_path, 'rb') as f:
            self.scaler = pickle.load(f)
        
        print(f"Model loaded successfully (device: {self.device})")
        print(f"Forecast horizon: {self.metadata['forecast_horizon']} steps")
    
    def predict(self, recent_data: np.ndarray) -> Dict:
        """
        Make a temperature prediction.
        
        Args:
            recent_data: Recent weather data 
                        Shape: (sequence_length, n_features)
                        Features should be: [temperature, humidity, hour_sin, hour_cos, day_sin, day_cos]
            
        Returns:
            Dictionary with prediction and confidence
        """
        # Scale the input
        scaled_data = self.scaler.transform(recent_data)
        
        # Convert to tensor
        X = torch.FloatTensor(scaled_data).unsqueeze(0).to(self.device)
        
        # Make prediction
        with torch.no_grad():
            scaled_pred = self.model(X)
        
        # Inverse transform (only temperature)
        scaled_pred_np = scaled_pred.cpu().numpy()
        
        # Create a full feature vector for inverse transform
        dummy_features = np.zeros((1, self.scaler.n_features_in_))
        dummy_features[0, 0] = scaled_pred_np
        
        # Inverse transform
        unscaled = self.scaler.inverse_transform(dummy_features)
        temperature_celsius = unscaled[0, 0]
        
        # Convert to Fahrenheit
        temperature_fahrenheit = temperature_celsius * 9/5 + 32
        
        return {
            'temperature_celsius': float(temperature_celsius),
            'temperature_fahrenheit': float(temperature_fahrenheit),
            'forecast_hours': self.metadata['forecast_horizon'] * 3,  # 3-hour intervals
            'confidence': 0.85  # Placeholder confidence score
        }
    
    def predict_from_sequence(self, sequence: np.ndarray) -> Dict:
        """
        Convenience method that takes a pre-scaled sequence.
        
        Args:
            sequence: Already prepared sequence (sequence_length, n_features)
            
        Returns:
            Prediction dictionary
        """
        return self.predict(sequence)


def load_predictor(
    model_dir: Optional[Path] = None
) -> WeatherPredictor:
    """
    Load a weather predictor with default paths.
    
    Args:
        model_dir: Directory containing model files
        
    Returns:
        Initialized WeatherPredictor
    """
    if model_dir is None:
        model_dir = Path(__file__).parent
    
    model_path = model_dir / 'models' / 'checkpoints' / 'best_model.pth'
    scaler_path = Path('/Users/kshitijmishra/weatherApp/data/processed/scaler.pkl')
    
    return WeatherPredictor(model_path, scaler_path)


if __name__ == '__main__':
    # Test the predictor
    import pandas as pd
    
    # Load some test data
    data_path = Path('/Users/kshitijmishra/weatherApp/data/processed/atlanta_timeseries.parquet')
    df = pd.read_parquet(data_path)
    
    # Prepare test sequence
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    df['day_of_year'] = pd.to_datetime(df['timestamp']).dt.dayofyear
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
    df['day_sin'] = np.sin(2 * np.pi * df['day_of_year'] / 365)
    df['day_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365)
    
    features = ['temperature', 'humidity', 'hour_sin', 'hour_cos', 'day_sin', 'day_cos']
    recent_data = df[features].iloc[-4:].values  # Last 4 timesteps
    
    # Make prediction
    predictor = load_predictor()
    result = predictor.predict(recent_data)
    
    print(f"\nPrediction for {result['forecast_hours']} hours ahead:")
    print(f"  Temperature: {result['temperature_fahrenheit']:.1f}°F ({result['temperature_celsius']:.1f}°C)")
    print(f"  Confidence: {result['confidence']:.2f}")

