from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import sys
from pathlib import Path
import numpy as np
import pandas as pd

# Add ML service to path
ml_service_path = Path(__file__).parent.parent.parent / 'ml'
sys.path.insert(0, str(ml_service_path))

from inference import load_predictor

app = FastAPI(title="Weather API", version="0.1.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load predictor at startup
predictor = None

@app.on_event("startup")
async def startup_event():
    global predictor
    try:
        predictor = load_predictor()
        print("✓ Weather predictor loaded successfully")
    except Exception as e:
        print(f"⚠ Warning: Could not load predictor: {e}")
        predictor = None

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": predictor is not None
    }

@app.get("/forecast")
async def get_forecast(
    lat: float = Query(33.749, description="Latitude"),
    lon: float = Query(-84.388, description="Longitude"),
    hours: int = Query(24, description="Forecast hours ahead")
):
    """
    Get weather forecast for a location.
    
    Currently supports Atlanta area only (MVP).
    """
    # For MVP, we only support Atlanta
    if not (33.0 < lat < 34.5 and -85.0 < lon < -83.5):
        return {
            "error": "Location not supported",
            "message": "Currently only Atlanta, GA area is supported in this MVP",
            "supported_area": {
                "lat_range": [33.0, 34.5],
                "lon_range": [-85.0, -83.5]
            }
        }
    
    if predictor is None:
        return {
            "error": "Model not loaded",
            "message": "The weather prediction model is not available"
        }
    
    try:
        # Load recent data
        data_path = Path('/Users/kshitijmishra/weatherApp/data/processed/atlanta_timeseries.parquet')
        df = pd.read_parquet(data_path)
        
        # Prepare features
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        df['day_of_year'] = pd.to_datetime(df['timestamp']).dt.dayofyear
        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
        df['day_sin'] = np.sin(2 * np.pi * df['day_of_year'] / 365)
        df['day_cos'] = np.cos(2 * np.pi * df['day_of_year'] / 365)
        
        features = ['temperature', 'humidity', 'hour_sin', 'hour_cos', 'day_sin', 'day_cos']
        recent_data = df[features].iloc[-4:].values  # Last 4 timesteps
        
        # Make prediction
        result = predictor.predict(recent_data)
        
        # Get current conditions (last observation)
        current = df.iloc[-1]
        current_temp_f = current['temperature'] * 9/5 + 32
        
        return {
            "location": {
                "name": "Atlanta, GA",
                "lat": lat,
                "lon": lon
            },
            "current": {
                "temperature": float(current_temp_f),
                "humidity": float(current['humidity']),
                "timestamp": str(current['timestamp'])
            },
            "forecast": {
                "temperature": result['temperature_fahrenheit'],
                "forecast_hours": result['forecast_hours'],
                "timestamp": str(pd.to_datetime(current['timestamp']) + pd.Timedelta(hours=result['forecast_hours']))
            },
            "confidence": result['confidence'],
            "note": "MVP version - predictions based on limited training data"
        }
    
    except Exception as e:
        return {
            "error": "Prediction failed",
            "message": str(e)
        }
