# CI/CD Pipeline - Step-by-Step Execution Guide

## 📋 Prerequisites Checklist

Before starting, ensure you have:
- [ ] GitHub account
- [ ] Docker Hub account  
- [ ] Git installed locally
- [ ] Docker installed locally
- [ ] Python 3.10+ installed

---

## 🎯 Step 1: Prepare Your Repository

### 1.1 Initialize Git Repository

```bash
# Navigate to your project
cd "e:/LP 2/Experiment 1 Image classification"

# Initialize git (if not done)
git init

# Check current status
git status
```

### 1.2 Create .gitignore (if needed)

```bash
# Create .gitignore
echo "__pycache__/" > .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore
echo "mlflow.db" >> .gitignore
```

### 1.3 Stage All Files

```bash
# Add all files
git add .

# Verify what will be committed
git status

# Commit
git commit -m "Initial commit with CI/CD pipeline"
```

---

## 🎯 Step 2: Create GitHub Repository

### 2.1 On GitHub Website

1. Go to [github.com](https://github.com)
2. Click **"+"** → **"New repository"**
3. Fill in:
   - **Repository name**: `image-classification-mlops`
   - **Description**: `Image Classification with MLOps Pipeline`
   - **Visibility**: Public or Private
4. **DO NOT** initialize with README (you already have files)
5. Click **"Create repository"**

### 2.2 Link Local to Remote

```bash
# Add remote (replace YOUR_USERNAME and YOUR_REPO)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Verify remote
git remote -v

# Push to GitHub
git push -u origin main
```

**If you get an error about 'main' branch:**
```bash
# Rename master to main
git branch -M main
git push -u origin main
```

---

## 🎯 Step 3: Set Up Docker Hub

### 3.1 Create Docker Hub Repository

1. Go to [hub.docker.com](https://hub.docker.com)
2. Click **"Create Repository"**
3. Fill in:
   - **Name**: `image-classifier`
   - **Visibility**: Public
4. Click **"Create"**

### 3.2 Generate Access Token (Recommended)

1. Go to **Account Settings** → **Security**
2. Click **"New Access Token"**
3. Description: `GitHub Actions CI/CD`
4. **Copy the token** (you won't see it again!)

---

## 🎯 Step 4: Configure GitHub Secrets

### 4.1 Add Docker Credentials

1. Go to your GitHub repository
2. Click **Settings** (top menu)
3. In left sidebar: **Secrets and variables** → **Actions**
4. Click **"New repository secret"**

**Add First Secret:**
- Name: `DOCKER_USERNAME`
- Value: `your-dockerhub-username`
- Click **"Add secret"**

**Add Second Secret:**
- Name: `DOCKER_PASSWORD`  
- Value: `your-access-token` (or password)
- Click **"Add secret"**

### 4.2 Verify Secrets

You should see:
- ✅ DOCKER_USERNAME
- ✅ DOCKER_PASSWORD

---

## 🎯 Step 5: Test Locally Before Pushing

### 5.1 Run Linting

```bash
# Install flake8 if needed
pip install flake8

# Run linting
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

**Expected:** No critical errors

### 5.2 Run Tests

```bash
# Terminal 1: Start API
python app.py

# Terminal 2: Run tests
pip install pytest requests
pytest tests/ -v
```

**Expected Output:**
```
tests/test_api.py::test_api_health PASSED
tests/test_api.py::test_predict_endpoint PASSED  
tests/test_api.py::test_predict_invalid_file PASSED

====== 3 passed in X.XXs ======
```

### 5.3 Test Docker Build

```bash
# Build Docker image
docker build -t image-classifier:test .

# Run container
docker run -d -p 8000:8000 --name test-classifier image-classifier:test

# Test API
curl http://localhost:8000/

# Clean up
docker stop test-classifier
docker rm test-classifier
```

**Expected:** API responds with JSON

---

## 🎯 Step 6: Trigger CI/CD Pipeline

### 6.1 Push to GitHub

```bash
# Ensure you're on main branch
git branch

# Push to trigger pipeline
git push origin main
```

### 6.2 Monitor Pipeline Execution

1. Go to your GitHub repository
2. Click **"Actions"** tab (top menu)
3. You should see a workflow running

**Pipeline Stages:**

```
┌─────────────┐
│  Push Code  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Checkout   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Setup Python│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Install Deps │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Linting   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Run Tests  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Build Docker │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Push to Hub  │
└─────────────┘
```

### 6.3 View Logs

1. Click on the workflow run
2. Click on **"test"** job
3. Expand each step to see logs
4. Check for ✅ green checkmarks

---

## 🎯 Step 7: Verify Deployment

### 7.1 Check Docker Hub

1. Go to [hub.docker.com](https://hub.docker.com)
2. Navigate to your repository
3. You should see a new image with tag `latest`
4. Check the **"Tags"** tab

### 7.2 Pull and Run Image

```bash
# Pull the image
docker pull YOUR_USERNAME/image-classifier:latest

# Run the container
docker run -d -p 8000:8000 --name classifier YOUR_USERNAME/image-classifier:latest

# Test the API
curl http://localhost:8000/

# Test prediction (with a sample image)
curl -X POST -F "file=@path/to/test/image.png" http://localhost:8000/predict
```

### 7.3 View Container Logs

```bash
# View logs
docker logs classifier

# Follow logs in real-time
docker logs -f classifier
```

---

## 🎯 Step 8: Make Changes and Re-deploy

### 8.1 Make Code Changes

```bash
# Edit a file (e.g., app.py)
# Make your changes...

# Stage changes
git add .

# Commit
git commit -m "Update: description of changes"

# Push (triggers pipeline again)
git push origin main
```

### 8.2 Monitor New Pipeline Run

1. Go to **Actions** tab
2. See new workflow run
3. Wait for completion
4. New Docker image will be pushed

---

## 🔧 Troubleshooting Guide

### Issue 1: "Tests Failed - Connection Refused"

**Cause:** API not ready when tests run

**Fix:** Increase wait time in workflow

```yaml
# In .github/workflows/ci_cd.yaml
- name: Run tests
  run: |
    python app.py &
    sleep 15  # Increase from 10 to 15
    pytest tests/ -v
```

### Issue 2: "Docker Build Failed - Model Not Found"

**Cause:** Model file too large or missing

**Fix Option 1:** Ensure model is committed
```bash
git add model/image_classifier_clean.keras
git commit -m "Add model file"
git push
```

**Fix Option 2:** Download model in Dockerfile
```dockerfile
# Add to Dockerfile
RUN wget https://your-storage.com/model.keras -O model/image_classifier_clean.keras
```

### Issue 3: "Authentication Failed - Docker Hub"

**Cause:** Wrong credentials in GitHub Secrets

**Fix:**
1. Go to GitHub → Settings → Secrets
2. Update `DOCKER_PASSWORD` with correct token
3. Re-run workflow

### Issue 4: "Workflow Not Triggering"

**Cause:** Workflow file in wrong location

**Fix:**
```bash
# Check file location
ls -la .github/workflows/ci_cd.yaml

# If missing, ensure directory exists
mkdir -p .github/workflows
# Move file to correct location
```

### Issue 5: "Permission Denied - Docker"

**Cause:** Docker daemon not running

**Fix:**
```bash
# Start Docker Desktop (Windows/Mac)
# Or start Docker service (Linux)
sudo systemctl start docker
```

---

## 📊 Pipeline Status Monitoring

### Add Status Badge to README

Add this to your `README.md`:

```markdown
# Image Classification MLOps Platform

![CI/CD Pipeline](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/CI/CD%20Pipeline/badge.svg)

## Status
- **Build**: ![Build Status](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/CI/CD%20Pipeline/badge.svg)
- **Tests**: Passing ✅
- **Docker**: Available on Docker Hub
```

### View Pipeline History

1. Go to **Actions** tab
2. See all workflow runs
3. Filter by:
   - Branch
   - Status (success/failure)
   - Date

---

## 🎓 Best Practices

### 1. Branch Strategy

```bash
# Create feature branch
git checkout -b feature/new-model

# Make changes
git add .
git commit -m "Add new model architecture"

# Push feature branch (tests run, but no deploy)
git push origin feature/new-model

# Create Pull Request on GitHub
# After review, merge to main (triggers full pipeline)
```

### 2. Version Tagging

```bash
# Tag releases
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

Update workflow to use version tags:

```yaml
tags: |
  ${{ secrets.DOCKER_USERNAME }}/image-classifier:latest
  ${{ secrets.DOCKER_USERNAME }}/image-classifier:v1.0.0
```

### 3. Environment Variables

Create `.env` file (don't commit!):

```env
MODEL_PATH=model/image_classifier_clean.keras
API_HOST=0.0.0.0
API_PORT=8000
```

Add to `.gitignore`:
```bash
echo ".env" >> .gitignore
```

---

## ✅ Success Checklist

After completing all steps, verify:

- [ ] Code pushed to GitHub
- [ ] GitHub Actions workflow exists
- [ ] GitHub Secrets configured
- [ ] Workflow runs successfully
- [ ] All tests pass
- [ ] Docker image on Docker Hub
- [ ] Can pull and run Docker image
- [ ] API responds correctly
- [ ] Status badge in README

---

## 🚀 Next Steps

1. **Set up branch protection:**
   - GitHub → Settings → Branches
   - Add rule for `main`
   - Require status checks

2. **Add more tests:**
   - Model accuracy tests
   - Performance tests
   - Integration tests

3. **Set up monitoring:**
   - Application logs
   - Performance metrics
   - Error tracking

4. **Deploy to cloud:**
   - AWS ECS/Fargate
   - Google Cloud Run
   - Azure Container Instances

---

## 📚 Additional Resources

- **GitHub Actions**: [docs.github.com/actions](https://docs.github.com/en/actions)
- **Docker**: [docs.docker.com](https://docs.docker.com/)
- **pytest**: [docs.pytest.org](https://docs.pytest.org/)
- **FastAPI**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com/)

---

## 🆘 Getting Help

If you encounter issues:

1. **Check workflow logs** in GitHub Actions
2. **Review error messages** carefully
3. **Test locally first** before pushing
4. **Verify secrets** are correct
5. **Check Docker Hub** for image

**Common Commands for Debugging:**

```bash
# Check Git status
git status
git log --oneline

# Check Docker
docker ps
docker images
docker logs CONTAINER_NAME

# Check Python environment
python --version
pip list

# Re-run tests
pytest tests/ -v --tb=short
```

---

**You're all set! 🎉**

Your CI/CD pipeline is now configured and ready to automate your deployment workflow.
