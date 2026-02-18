# Image Classification Platform - Quick Start Guide

## Running the Dashboard

```bash
streamlit run dashboard.py
```

Access at: http://localhost:8501

## Running Tests

```bash
# Terminal 1: Start API
python app.py

# Terminal 2: Run tests
pytest tests/ -v
```

## Dashboard Features

1. **Model Info**: View architecture and training details
2. **Image Prediction**: Upload and classify images
3. **Performance Metrics**: View confusion matrix and accuracy

## CI/CD Setup

Push to GitHub to trigger automated:
- Linting (flake8)
- Testing (pytest)
- Docker build & push (on main branch)

Required GitHub Secrets:
- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`
