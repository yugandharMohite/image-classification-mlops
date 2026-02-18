# CI/CD Pipeline - Quick Setup

## 🚀 Quick Start (5 Minutes)

### 1. Create GitHub Repository
```bash
cd "e:/LP 2/Experiment 1 Image classification"
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Configure GitHub Secrets
1. Go to: `Settings` → `Secrets and variables` → `Actions`
2. Add secrets:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub password/token

### 3. Trigger Pipeline
```bash
git push origin main
```

✅ **Done!** Check the Actions tab on GitHub.

---

## 📊 Pipeline Stages

```
Code Push → Lint (flake8) → Test (pytest) → Build (Docker) → Deploy (Docker Hub)
```

**On Every Push:**
- ✅ Code linting
- ✅ API tests

**On Main Branch:**
- ✅ Docker build
- ✅ Push to Docker Hub

---

## 🧪 Test Locally First

```bash
# Run tests
python app.py &
sleep 5
pytest tests/ -v

# Run linting
flake8 .

# Build Docker
docker build -t test-image .
```

---

## 🐳 Deploy from Docker Hub

```bash
# Pull image
docker pull YOUR_USERNAME/image-classifier:latest

# Run container
docker run -d -p 8000:8000 --name classifier YOUR_USERNAME/image-classifier:latest

# Test
curl http://localhost:8000/
```

---

## 🔍 Monitor Pipeline

1. Go to GitHub repository
2. Click **Actions** tab
3. View workflow runs and logs

---

## ⚠️ Common Issues

| Issue | Solution |
|-------|----------|
| Tests fail | Increase sleep time in workflow (line 31) |
| Docker auth fails | Check GitHub Secrets are correct |
| Workflow not running | Ensure file is in `.github/workflows/` |

---

## 📚 Full Documentation

See [CI_CD_GUIDE.md](file:///C:/Users/ASUS/.gemini/antigravity/brain/30d93d1d-5df4-4f38-96e2-3a0ddf5c1cdf/CI_CD_GUIDE.md) for detailed instructions.
