# WeatherAI - LSTM-Based Weather Forecasting System

## Executive Summary

WeatherAI is an advanced weather forecasting application that generates its own predictions using machine learning instead of relying on traditional third-party weather APIs. The system downloads raw meteorological data from NOAA, processes it through a custom data pipeline, trains an LSTM (Long Short-Term Memory) neural network, and serves predictions through a modern REST API to a beautiful Progressive Web App interface.

**Current Status**: Phase 1 (Proof-of-Concept) - Fully Functional MVP for Atlanta, GA

---

## Table of Contents

1. [What This Project Does](#what-this-project-does)
2. [Architecture Overview](#architecture-overview)
3. [Key Features](#key-features)
4. [Technology Stack](#technology-stack)
5. [System Components](#system-components)
6. [How It Works](#how-it-works)
7. [Installation & Setup](#installation--setup)
8. [Usage](#usage)
9. [API Documentation](#api-documentation)
10. [Project Structure](#project-structure)
11. [Performance Metrics](#performance-metrics)
12. [Limitations](#limitations)
13. [Future Roadmap](#future-roadmap)
14. [Contributing](#contributing)
15. [License](#license)

---

## What This Project Does

### Core Functionality

WeatherAI replaces traditional weather API services with a custom machine learning pipeline that:

1. **Acquires Raw Data**: Downloads GFS (Global Forecast System) weather data in GRIB2 format from NOAA
2. **Processes Data**: Extracts and transforms binary meteorological data into structured time-series
3. **Trains Models**: Uses LSTM neural networks to learn weather patterns and make predictions
4. **Serves Predictions**: Provides REST API endpoints for real-time weather forecasts
5. **Displays Results**: Shows predictions in a modern, responsive web interface

### What Makes It Unique

Unlike traditional weather apps that simply fetch data from weather APIs:

- ✅ **No API Dependencies**: Generates predictions independently
- ✅ **Custom ML Models**: Trained specifically on local data patterns
- ✅ **Full Control**: Complete ownership of the prediction pipeline
- ✅ **Transparent**: Understand exactly how predictions are made
- ✅ **Extensible**: Add features without API limitations

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        WeatherAI System                          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   NOAA GFS  │─────▶│ Data Pipeline│─────▶│  Training   │
│  (GRIB2)    │      │  Processor   │      │  Pipeline   │
└─────────────┘      └──────────────┘      └─────────────┘
                            │                      │
                            ▼                      ▼
                     ┌──────────────┐      ┌─────────────┐
                     │  Processed   │      │   Trained   │
                     │    Data      │      │ LSTM Model  │
                     └──────────────┘      └─────────────┘
                                                   │
                                                   ▼
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Browser   │◀─────│  FastAPI     │◀─────│ Inference   │
│  (PWA UI)   │      │   Server     │      │   Engine    │
└─────────────┘      └──────────────┘      └─────────────┘
```

### Data Flow

```
Raw GRIB2 → Parse → Time Series → Feature Engineering → 
LSTM Sequences → Training → Model Checkpoint → 
Inference → API Response → UI Display
```

---

## Key Features

### 🌐 Data Acquisition
- Automated downloads from NOAA servers
- Customizable geographic regions and time ranges
- Support for multiple weather variables
- Efficient filtered downloads (only required data)

### 🔄 Data Processing
- GRIB2 binary format parsing
- Geospatial data extraction
- Time-series generation
- Feature engineering with temporal encoding
- Data normalization and scaling

### 🧠 Machine Learning
- LSTM neural network architecture
- PyTorch implementation
- GPU acceleration (Apple Silicon MPS)
- Early stopping to prevent overfitting
- Model checkpointing and versioning

### 🚀 API Backend
- RESTful API with FastAPI
- CORS-enabled for frontend access
- Model loaded at startup (fast predictions)
- JSON responses
- Error handling and validation

### 💻 Progressive Web App
- Modern, responsive design
- Offline capability
- Service worker for caching
- Dark/light theme toggle
- Beautiful gradient animations
- Mobile-friendly interface

---

## Technology Stack

### Backend Technologies

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Data Acquisition** | Python 3.13, requests | Download GRIB2 files |
| **Data Processing** | cfgrib, xarray, pandas | Parse and transform data |
| **Feature Engineering** | numpy, scikit-learn | Create ML-ready features |
| **Machine Learning** | PyTorch 2.7.1 | Train LSTM models |
| **API Framework** | FastAPI 0.115.2 | REST API server |
| **Server** | Uvicorn | ASGI web server |

### Frontend Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **UI Framework** | Vanilla JavaScript | No dependencies, fast |
| **Styling** | CSS3 (Grid, Flexbox) | Modern layouts |
| **PWA Features** | Service Workers | Offline capability |
| **Fonts** | Google Fonts (Inter) | Beautiful typography |

### Infrastructure

| Tool | Purpose |
|------|---------|
| **Package Manager** | Homebrew (eccodes) |
| **Python Env** | venv (isolated environments) |
| **Version Control** | Git |

---

## System Components

### 1. Data Ingestion (`data/ingestion/`)

**Purpose**: Download weather data from NOAA

**Key File**: `gfs_download.py`

**Capabilities**:
- Filtered GFS data downloads
- Customizable date ranges
- Geographic bounding box selection
- Multiple forecast hours
- Resume capability (skips existing files)

**Configuration**:
```python
DEFAULT_LEFTLON = -85.0    # Atlanta region
DEFAULT_RIGHTLON = -83.0
DEFAULT_TOPLAT = 34.2
DEFAULT_BOTTOMLAT = 32.8
```

### 2. Data Processing (`data/processing/`)

#### GRIB Parser (`grib_parser.py`)

**Purpose**: Extract weather variables from GRIB2 files

**Capabilities**:
- Multi-variable extraction
- Geospatial point selection
- Unit conversions (K→°C, Pa→hPa, m→mm)
- Parquet output for efficiency

**Variables Supported**:
- Temperature (2m)
- Relative Humidity (2m)
- Wind U/V components (10m)
- Mean Sea-Level Pressure
- Total Cloud Cover
- Precipitation

#### Feature Engineer (`feature_engineering.py`)

**Purpose**: Create ML-ready sequences

**Capabilities**:
- Temporal feature encoding (sine/cosine)
- Sliding window sequence generation
- Feature scaling (StandardScaler)
- Train/validation splitting

**Output Format**:
- X: (n_samples, sequence_length, n_features)
- y: (n_samples,) - temperature target

### 3. ML Service (`services/ml/`)

#### LSTM Model (`models/lstm_forecaster.py`)

**Architecture**:
```
Input: (batch, 4 timesteps, 6 features)
  ↓
LSTM Layer 1: 64 hidden units
  ↓
LSTM Layer 2: 64 hidden units (dropout=0.2)
  ↓
Dense Layer: 64 → 32 (ReLU)
  ↓
Dropout: 0.2
  ↓
Output: 32 → 1 (temperature)
```

**Parameters**: 14,113 trainable weights

#### Training (`train.py`)

**Features**:
- Adam optimizer
- MSE loss function
- Early stopping (patience=20)
- Model checkpointing
- GPU acceleration

#### Inference (`inference.py`)

**Capabilities**:
- Model loading from checkpoint
- Scaler loading for normalization
- Batch prediction support
- Celsius/Fahrenheit conversion

### 4. API Backend (`services/api/`)

#### FastAPI Server (`app/main.py`)

**Endpoints**:

1. **GET /health**
   - Returns: `{"status": "ok", "model_loaded": bool}`
   - Purpose: System health check

2. **GET /forecast**
   - Parameters: `lat`, `lon`, `hours`
   - Returns: Current weather + forecast
   - Purpose: Get predictions

**Features**:
- CORS middleware
- Model preloading
- Error handling
- JSON responses

### 5. Frontend (`frontend/`)

#### Progressive Web App

**Files**:
- `index.html` - Main interface
- `script.js` - Application logic
- `styles.css` - Styling and animations
- `sw.js` - Service worker
- `manifest.json` - PWA configuration

**Features**:
- Responsive design
- Theme toggle
- Search functionality
- Weather display cards
- 7-day forecast grid
- Connection status indicator

---

## How It Works

### Step-by-Step Process

#### 1. Data Acquisition
```bash
# Download GRIB2 files from NOAA
python data/ingestion/gfs_download.py \
  --start-date 2025-10-29 \
  --end-date 2025-10-30 \
  --cycles 00 12
```

Output: GRIB2 files in `data/raw/gfs/YYYYMMDD/HH/`

#### 2. Data Parsing
```bash
# Extract weather variables
python data/processing/grib_parser.py \
  data/raw/gfs \
  --output data/processed/atlanta_timeseries.parquet
```

Output: Structured time-series data

#### 3. Feature Engineering
```bash
# Create ML sequences
python data/processing/feature_engineering.py \
  data/processed/atlanta_timeseries.parquet \
  --sequence-length 4 \
  --forecast-horizon 4
```

Output: Training/validation arrays (.npy files)

#### 4. Model Training
```bash
# Train LSTM
python services/ml/train.py \
  --epochs 200 \
  --batch-size 2 \
  --lr 0.01
```

Output: Trained model checkpoint

#### 5. Start API Server
```bash
# Launch API
cd services/api
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Server loads model and serves predictions

#### 6. Access Frontend
```bash
# Start frontend server
cd frontend
python3 -m http.server 3000
```

Browser: http://localhost:3000

### Prediction Flow

```
User Request (lat, lon)
    ↓
API receives request
    ↓
Load recent weather data (4 timesteps)
    ↓
Prepare features (add temporal encoding)
    ↓
Normalize with StandardScaler
    ↓
Pass through LSTM model
    ↓
Inverse transform prediction
    ↓
Convert to Fahrenheit
    ↓
Return JSON response
    ↓
Frontend displays prediction
```

---

## Installation & Setup

### Prerequisites

- macOS (for MPS GPU acceleration) or Linux
- Python 3.13+
- Homebrew (macOS)
- 2GB+ free disk space
- Internet connection

### Quick Start

```bash
# 1. Clone repository
git clone <repository-url>
cd weatherApp

# 2. Install system dependencies (macOS)
brew install eccodes

# 3. Set up data processing
cd data/processing
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Set up ML service
cd ../../services/ml
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Set up API
cd ../api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Download Data

```bash
cd data/ingestion
source venv/bin/activate
python gfs_download.py --start-date 2025-10-29 --end-date 2025-10-29
```

### Process Data

```bash
cd ../processing
source venv/bin/activate
python grib_parser.py ../raw/gfs --output ../processed/atlanta_timeseries.parquet
python feature_engineering.py ../processed/atlanta_timeseries.parquet
```

### Train Model

```bash
cd ../../services/ml
source venv/bin/activate
python train.py --epochs 200 --batch-size 2
```

### Run Application

```bash
# Terminal 1: API
cd services/api
source venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000

# Terminal 2: Frontend
cd frontend
python3 -m http.server 3000

# Browser: http://localhost:3000
```

---

## Usage

### API Usage

#### Health Check
```bash
curl http://127.0.0.1:8000/health
```

Response:
```json
{
  "status": "ok",
  "model_loaded": true
}
```

#### Get Forecast
```bash
curl "http://127.0.0.1:8000/forecast?lat=33.749&lon=-84.388&hours=24"
```

Response:
```json
{
  "location": {
    "name": "Atlanta, GA",
    "lat": 33.749,
    "lon": -84.388
  },
  "current": {
    "temperature": 43.0,
    "humidity": 96.1,
    "timestamp": "2025-10-30 12:00:00"
  },
  "forecast": {
    "temperature": 46.6,
    "forecast_hours": 12,
    "timestamp": "2025-10-31 00:00:00"
  },
  "confidence": 0.85,
  "note": "MVP version - predictions based on limited training data"
}
```

### Frontend Usage

1. Open http://localhost:3000 in browser
2. Search for "Atlanta" (or any location - defaults to Atlanta for MVP)
3. View current weather and forecast
4. See LSTM-generated predictions

---

## API Documentation

### Base URL
```
http://127.0.0.1:8000
```

### Endpoints

#### GET /health

Check API and model status.

**Response**:
```json
{
  "status": "ok",
  "model_loaded": true
}
```

#### GET /forecast

Get weather forecast for a location.

**Query Parameters**:
- `lat` (float, optional): Latitude (default: 33.749)
- `lon` (float, optional): Longitude (default: -84.388)
- `hours` (int, optional): Forecast hours ahead (default: 24)

**Response**:
```json
{
  "location": {
    "name": "Atlanta, GA",
    "lat": 33.749,
    "lon": -84.388
  },
  "current": {
    "temperature": 43.0,
    "humidity": 96.1,
    "timestamp": "2025-10-30 12:00:00"
  },
  "forecast": {
    "temperature": 46.6,
    "forecast_hours": 12,
    "timestamp": "2025-10-31 00:00:00"
  },
  "confidence": 0.85,
  "note": "MVP version - predictions based on limited training data"
}
```

**Error Response**:
```json
{
  "error": "Location not supported",
  "message": "Currently only Atlanta, GA area is supported in this MVP"
}
```

---

## Project Structure

```
weatherApp/
├── README.md                           # Main documentation
├── PROJECT_OVERVIEW.md                 # This file
├── PROJECT_JOURNEY.md                  # Development journey
├── PHASE1_COMPLETE.md                  # Phase 1 completion notes
├── Project_outline.md                  # Original project plan
│
├── data/
│   ├── ingestion/                      # Data download scripts
│   │   ├── gfs_download.py
│   │   ├── requirements.txt
│   │   ├── README.md
│   │   └── venv/
│   ├── processing/                     # Data processing pipeline
│   │   ├── grib_parser.py
│   │   ├── feature_engineering.py
│   │   ├── requirements.txt
│   │   └── venv/
│   ├── raw/                            # Downloaded GRIB2 files
│   │   └── gfs/
│   │       └── 20251029/
│   │           ├── 00/
│   │           └── 12/
│   └── processed/                      # Processed data
│       ├── atlanta_timeseries.parquet
│       ├── X_train.npy
│       ├── y_train.npy
│       ├── X_val.npy
│       ├── y_val.npy
│       ├── scaler.pkl
│       └── metadata.json
│
├── services/
│   ├── ml/                             # Machine learning service
│   │   ├── models/
│   │   │   ├── lstm_forecaster.py
│   │   │   └── checkpoints/
│   │   │       └── best_model.pth
│   │   ├── train.py
│   │   ├── inference.py
│   │   ├── requirements.txt
│   │   ├── README.md
│   │   └── venv/
│   └── api/                            # API backend
│       ├── app/
│       │   └── main.py
│       ├── requirements.txt
│       └── venv/
│
├── frontend/                           # Progressive Web App
│   ├── index.html
│   ├── script.js
│   ├── styles.css
│   ├── sw.js
│   ├── manifest.json
│   └── README.md
│
└── infrastructure/                     # Future: K8s, Docker, etc.
    └── README.md
```

---

## Performance Metrics

### Model Performance

| Metric | Value |
|--------|-------|
| Training Samples | 4 |
| Validation Samples | 2 |
| Best Validation Loss | 0.1398 |
| Training Time | ~30 seconds |
| Model Parameters | 14,113 |
| Inference Time | <50ms |

### API Performance

| Metric | Value |
|--------|-------|
| Startup Time | ~3 seconds |
| Model Load Time | ~1 second |
| Response Time | <100ms |
| Concurrent Requests | 10+ |

### Data Metrics

| Metric | Value |
|--------|-------|
| GRIB2 Files | 18 |
| Time Range | 36 hours |
| Geographic Area | Atlanta region |
| Variables | 2 (temperature, humidity) |
| Time Resolution | 3 hours |

---

## Limitations

### Current Constraints (MVP)

#### Data Limitations
- **Limited Historical Data**: Only 18 records from 1 day
- **Single Location**: Atlanta, GA only
- **Few Variables**: Only temperature and humidity
- **Recent Data Only**: NOAA archives older data

#### Model Limitations
- **Simple Architecture**: Basic 2-layer LSTM
- **Small Training Set**: Not enough for production accuracy
- **No Ensemble**: Single model (no redundancy)
- **Fixed Horizon**: 12-hour forecast only

#### System Limitations
- **No Real-Time Updates**: Manual data refresh required
- **No Caching**: Loads data on every request
- **Single Region**: Not scalable to multiple locations
- **No Database**: File-based storage only

---

## Future Roadmap

### Phase 2: Core Improvements (3-6 months)

#### Data Expansion
- [ ] Download 1+ year of historical data
- [ ] Support multiple geographic regions
- [ ] Add all weather variables (wind, pressure, precip)
- [ ] Set up automated daily downloads

#### Model Enhancement
- [ ] Deeper LSTM architecture
- [ ] Attention mechanisms
- [ ] Ensemble models
- [ ] Confidence intervals

#### Infrastructure
- [ ] PostgreSQL for data storage
- [ ] Redis for caching
- [ ] Docker containers
- [ ] CI/CD pipeline

### Phase 3: Advanced Features (6-12 months)

#### ML Improvements
- [ ] Transformer models
- [ ] Multi-task learning
- [ ] Transfer learning
- [ ] Hyperparameter optimization

#### Real-Time Features
- [ ] Server-Sent Events (SSE)
- [ ] Live data updates
- [ ] Background sync
- [ ] Push notifications

#### User Features
- [ ] User accounts
- [ ] Favorite locations
- [ ] Custom alerts
- [ ] Historical comparison

### Phase 4: Production Scale (12+ months)

#### Infrastructure
- [ ] Kubernetes deployment
- [ ] Load balancing
- [ ] CDN integration
- [ ] Multi-region servers

#### Advanced NLP
- [ ] Fuzzy location search
- [ ] Typo correction
- [ ] Semantic understanding
- [ ] Natural language queries

#### Data Sources
- [ ] Satellite imagery
- [ ] Local sensor networks
- [ ] Weather balloons
- [ ] Multiple data providers

---

## Contributing

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Areas for Contribution

- 🔧 Bug fixes and improvements
- 📊 More weather variables
- 🌍 Multi-location support
- 🧠 Model architecture experiments
- 📱 Mobile app development
- 📚 Documentation improvements

---

## License

[Add your license here]

---

## Acknowledgments

- **NOAA** - For providing free GFS data
- **PyTorch Team** - For excellent deep learning framework
- **FastAPI** - For modern Python web framework
- **eccodes** - For GRIB2 file support

---

## Contact & Support

- **GitHub Issues**: [repository-url]/issues
- **Documentation**: [repository-url]/wiki
- **Email**: [your-email]

---

## Project Status

**Current Phase**: ✅ Phase 1 Complete (Proof-of-Concept)

**Next Phase**: 🚀 Phase 2 (Core Improvements) - Ready to begin

**Production Status**: 📊 MVP - Functional but not production-ready

---

**Built with ❤️ using Python, PyTorch, and modern web technologies**

Last Updated: November 7, 2025

