# Image Classification Platform - CI/CD Pipeline

## 🎯 Complete CI/CD Implementation

This project now includes a **fully automated CI/CD pipeline** using GitHub Actions, Docker, and pytest.

---

## 📚 Documentation

### Quick Start
- **[CI_CD_QUICKSTART.md](CI_CD_QUICKSTART.md)** - 5-minute setup guide
- **[CI_CD_STEP_BY_STEP.md](CI_CD_STEP_BY_STEP.md)** - Detailed walkthrough

### Reference
- **[CI/CD Guide](https://github.com/YOUR_USERNAME/YOUR_REPO/blob/main/CI_CD_GUIDE.md)** - Complete documentation

---

## 🚀 Quick Setup (3 Steps)

### 1. Push to GitHub
```bash
git init
git add .
git commit -m "Add CI/CD pipeline"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Configure Secrets
- Go to: Settings → Secrets → Actions
- Add: `DOCKER_USERNAME` and `DOCKER_PASSWORD`

### 3. Done!
- Check the **Actions** tab to see your pipeline run

---

## 🔄 Pipeline Workflow

```
Push Code → Lint → Test → Build Docker → Push to Hub
```

**Triggers:**
- ✅ Every push to `main` or `develop`
- ✅ Every pull request to `main`

**Actions:**
- ✅ Code linting (flake8)
- ✅ API tests (pytest)
- ✅ Docker build & push (main branch only)

---

## 📊 Power BI Dashboard

### Export Metrics
```bash
python export_metrics_for_powerbi.py
```

This creates CSV files in `output/` directory:
- `confusion_matrix.csv` - Confusion matrix
- `per_class_metrics.csv` - Per-class accuracy
- `overall_metrics.csv` - Overall performance
- `classification_report.csv` - Detailed metrics

### Import to Power BI
1. Open Power BI Desktop
2. Get Data → Text/CSV
3. Select files from `output/` folder
4. Create visualizations

---

## 🧪 Testing

### Run Tests Locally
```bash
# Start API
python app.py

# Run tests
pytest tests/ -v
```

### Run in Docker
```bash
docker build -t image-classifier .
docker run -p 8000:8000 image-classifier
```

---

## 📁 Project Structure

```
├── .github/workflows/
│   └── ci_cd.yaml           # CI/CD pipeline
├── tests/
│   └── test_api.py          # API tests
├── model/
│   └── image_classifier_clean.keras
├── app.py                   # FastAPI application
├── Dockerfile               # Docker configuration
├── requirements.txt         # Dependencies
└── export_metrics_for_powerbi.py  # Metrics export
```

---

## ✅ Features

- ✅ Automated testing on every push
- ✅ Code quality checks (flake8)
- ✅ Docker containerization
- ✅ Automated deployment to Docker Hub
- ✅ API integration tests
- ✅ Power BI metrics export

---

## 🆘 Troubleshooting

See [CI_CD_STEP_BY_STEP.md](CI_CD_STEP_BY_STEP.md#troubleshooting-guide) for common issues and solutions.

---

## 📞 Quick Commands

```bash
# Git
git push origin main         # Trigger pipeline

# Testing
pytest tests/ -v             # Run tests
flake8 .                     # Run linting

# Docker
docker build -t test .       # Build image
docker run -p 8000:8000 test # Run container

# Metrics
python export_metrics_for_powerbi.py  # Export for Power BI
```

---

**Status:** ✅ CI/CD Pipeline Active

![CI/CD Pipeline](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/CI/CD%20Pipeline/badge.svg)
