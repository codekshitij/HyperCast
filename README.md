# HyperCast 🌦️

### AI-Driven Hyper-Local Weather Forecasting System

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.7.1-red.svg)](https://pytorch.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> A machine learning-powered weather forecasting application that generates predictions without relying on traditional weather APIs. Built with LSTM neural networks, real NOAA data, and a stunning PWA interface.

![HyperCast Demo](https://img.shields.io/badge/Status-Phase%201%20Complete-success)

---

## ✨ Features

- 🧠 **LSTM Neural Network** - Custom-trained model for temperature prediction
- 🌐 **NOAA GFS Data** - Downloads and processes real meteorological data
- ⚡ **FastAPI Backend** - High-performance REST API
- 🎨 **Premium UI** - Glassmorphism design with animations
- 📱 **Progressive Web App** - Offline-capable, mobile-friendly
- 🔮 **No API Dependencies** - Generates own predictions

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- Homebrew (macOS) or equivalent
- 2GB+ free disk space

### Installation

```bash
# 1. Clone repository
git clone https://github.com/codekshitij/HyperCast.git
cd HyperCast

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

### Running the Application

```bash
# Terminal 1: Start API
cd services/api
source venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000

# Terminal 2: Start Frontend
cd frontend
python3 -m http.server 3000

# Open: http://localhost:3000
```

---

## 📊 Architecture

```
NOAA GFS Data → GRIB Parser → Feature Engineering → LSTM Model
                                                         ↓
Browser (PWA) ← FastAPI ← Inference Engine ← Trained Model
```

---

## 🧠 Machine Learning

### Model Architecture
- **Type**: LSTM (Long Short-Term Memory)
- **Layers**: 2 LSTM layers (64 hidden units each)
- **Parameters**: 14,113 trainable weights
- **Framework**: PyTorch 2.7.1
- **Training**: Early stopping, GPU acceleration (MPS)
- **Validation Loss**: 0.1398

### Training Data
- **Source**: NOAA GFS (Global Forecast System)
- **Format**: GRIB2
- **Location**: Atlanta, GA (MVP)
- **Variables**: Temperature, Humidity
- **Resolution**: 3-hour intervals

---

## 📁 Project Structure

```
HyperCast/
├── data/
│   ├── ingestion/           # Download GRIB2 files
│   ├── processing/          # Parse and prepare data
│   ├── raw/                 # Downloaded GRIB2 files
│   └── processed/           # ML-ready datasets
├── services/
│   ├── ml/                  # LSTM model & training
│   │   ├── models/          # Model architecture
│   │   ├── train.py         # Training script
│   │   └── inference.py     # Prediction module
│   └── api/                 # FastAPI backend
│       └── app/main.py      # REST endpoints
├── frontend/                # PWA interface
│   ├── index.html
│   ├── script.js
│   └── styles-enhanced.css  # Premium UI
└── docs/                    # Documentation
```

---

## 🎨 UI Features

### Premium Design
- ✨ **Glassmorphism** - Frosted glass effects
- 🌈 **Animated Background** - 3 floating gradient orbs
- ❄️ **Particle Effects** - 50 animated particles
- 💫 **Smooth Animations** - Entrance, hover, continuous
- 🎨 **Gradient Text** - Shimmer effects
- 📱 **Responsive** - Mobile-optimized

![UI Preview](https://via.placeholder.com/800x400/667eea/ffffff?text=Premium+Weather+UI)

---

## 🔌 API Endpoints

### `GET /health`
Check API and model status
```json
{
  "status": "ok",
  "model_loaded": true
}
```

### `GET /forecast`
Get weather forecast
```json
{
  "location": {
    "name": "Atlanta, GA",
    "lat": 33.749,
    "lon": -84.388
  },
  "current": {
    "temperature": 43.0,
    "humidity": 96.1
  },
  "forecast": {
    "temperature": 46.6,
    "forecast_hours": 12
  }
}
```

---

## 📚 Documentation

- 📖 [Project Overview](PROJECT_OVERVIEW.md) - Complete technical documentation
- 📝 [Project Journey](PROJECT_JOURNEY.md) - Development process & learnings
- 🎯 [Phase 1 Complete](PHASE1_COMPLETE.md) - MVP completion notes
- 🎨 [UI Enhancements](UI_ENHANCEMENTS.md) - Design system details
- 📋 [Project Outline](Project_outline.md) - Original plan & roadmap

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **ML** | PyTorch, NumPy, scikit-learn |
| **Data** | cfgrib, xarray, pandas |
| **API** | FastAPI, Uvicorn |
| **Frontend** | Vanilla JS, CSS3, PWA |
| **System** | Python 3.13, eccodes |

---

## 📈 Performance

| Metric | Value |
|--------|-------|
| Inference Time | <50ms |
| Model Size | 14K parameters |
| API Response | <100ms |
| Validation Loss | 0.1398 |

---

## 🚧 Current Limitations (MVP)

- ⚠️ Single location: Atlanta, GA only
- ⚠️ Limited training data: 18 records
- ⚠️ Few variables: Temperature & humidity only
- ⚠️ Simple model: 2-layer LSTM

---

## 🗺️ Roadmap

### Phase 2: Core Improvements
- [ ] Download 1+ year historical data
- [ ] Multi-location support
- [ ] Add all weather variables
- [ ] Deeper LSTM architecture

### Phase 3: Advanced Features
- [ ] Transformer models
- [ ] Real-time updates (SSE)
- [ ] User accounts & favorites
- [ ] Mobile app

### Phase 4: Production
- [ ] Kubernetes deployment
- [ ] Multi-region servers
- [ ] Satellite imagery
- [ ] Advanced NLP search

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **NOAA** - Free GFS weather data
- **PyTorch Team** - Deep learning framework
- **FastAPI** - Modern Python web framework
- **eccodes** - GRIB2 file support

---

## 📧 Contact

**Project Link**: [https://github.com/codekshitij/HyperCast](https://github.com/codekshitij/HyperCast)

---

<div align="center">

### Built with ❤️ using Python, PyTorch, and modern web technologies

**⭐ Star this repo if you find it helpful!**

</div>
