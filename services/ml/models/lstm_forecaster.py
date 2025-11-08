"""
LSTM-based Weather Forecasting Model

A simple LSTM architecture for predicting temperature from time-series weather data.
"""
import torch
import torch.nn as nn


class WeatherLSTM(nn.Module):
    """LSTM model for weather forecasting."""
    
    def __init__(
        self,
        input_size: int,
        hidden_size: int = 64,
        num_layers: int = 2,
        dropout: float = 0.2
    ):
        """
        Initialize the LSTM model.
        
        Args:
            input_size: Number of input features
            hidden_size: Number of hidden units in LSTM layers
            num_layers: Number of LSTM layers
            dropout: Dropout rate
        """
        super(WeatherLSTM, self).__init__()
        
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        # LSTM layers
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout if num_layers > 1 else 0,
            batch_first=True
        )
        
        # Fully connected layers
        self.fc1 = nn.Linear(hidden_size, hidden_size // 2)
        self.fc2 = nn.Linear(hidden_size // 2, 1)
        
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x):
        """
        Forward pass.
        
        Args:
            x: Input tensor of shape (batch_size, sequence_length, input_size)
            
        Returns:
            Output tensor of shape (batch_size, 1)
        """
        # LSTM forward pass
        lstm_out, (hidden, cell) = self.lstm(x)
        
        # Use the last hidden state
        last_hidden = lstm_out[:, -1, :]
        
        # Fully connected layers
        out = self.fc1(last_hidden)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.fc2(out)
        
        return out.squeeze()
    
    def predict(self, x):
        """
        Make predictions (convenience method).
        
        Args:
            x: Input tensor
            
        Returns:
            Predictions
        """
        self.eval()
        with torch.no_grad():
            return self.forward(x)


def create_model(input_size: int, **kwargs) -> WeatherLSTM:
    """
    Factory function to create a Weather LSTM model.
    
    Args:
        input_size: Number of input features
        **kwargs: Additional arguments for WeatherLSTM
        
    Returns:
        Initialized WeatherLSTM model
    """
    return WeatherLSTM(input_size, **kwargs)


if __name__ == '__main__':
    # Test the model
    model = create_model(input_size=6, hidden_size=64, num_layers=2)
    print(model)
    
    # Test forward pass
    batch_size = 4
    sequence_length = 8
    input_size = 6
    
    x = torch.randn(batch_size, sequence_length, input_size)
    y = model(x)
    
    print(f"\nInput shape: {x.shape}")
    print(f"Output shape: {y.shape}")
    print(f"Parameters: {sum(p.numel() for p in model.parameters()):,}")

