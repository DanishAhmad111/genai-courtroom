# 🚀 GenAI Courtroom Deployment Guide

This guide covers deploying your GenAI Courtroom application with the fine-tuned judge model to various cloud platforms.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Upload Model to Hugging Face](#upload-model-to-hugging-face)
3. [Deployment Options](#deployment-options)
   - [Streamlit Cloud (Recommended)](#option-1-streamlit-cloud-recommended)
   - [Render](#option-2-render)
   - [Railway](#option-3-railway)
   - [Hugging Face Spaces](#option-4-hugging-face-spaces)
4. [Local Docker Testing](#local-docker-testing)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required

1. **Groq API Key**: Get one from [console.groq.com](https://console.groq.com)
2. **Git Repository**: Push your code to GitHub
3. **Hugging Face Account**: For hosting the fine-tuned model

### Optional

- **Hugging Face Token**: Only if making your model private
- **Docker**: For local testing

---

## Upload Model to Hugging Face

Before deploying, you need to upload your fine-tuned `judge-lora` model to Hugging Face Hub.

### Step 1: Install Hugging Face CLI

```bash
pip install huggingface-hub
```

### Step 2: Login to Hugging Face

```bash
huggingface-cli login
```

Enter your Hugging Face token when prompted.

### Step 3: Create a Model Repository

1. Go to [huggingface.co/new](https://huggingface.co/new)
2. Choose "Model" as the repository type
3. Name it something like `genai-courtroom-judge`
4. Choose public or private

### Step 4: Upload Your Model

```bash
python scripts/upload_model_to_hf.py --repo_name YOUR_USERNAME/genai-courtroom-judge
```

Replace `YOUR_USERNAME` with your Hugging Face username.

**Example:**
```bash
python scripts/upload_model_to_hf.py --repo_name johndoe/genai-courtroom-judge
```

For a private model, add `--private`:
```bash
python scripts/upload_model_to_hf.py --repo_name johndoe/genai-courtroom-judge --private
```

✅ **Success!** Your model is now at `https://huggingface.co/YOUR_USERNAME/genai-courtroom-judge`

---

## Deployment Options

### Option 1: Streamlit Cloud (Recommended)

**Best for:** Quick deployment, free hosting, automatic updates

#### Steps:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Go to Streamlit Cloud**
   - Visit [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"

3. **Configure Deployment**
   - **Repository**: Select your `genai-courtroom` repo
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`

4. **Set Environment Variables (Secrets)**
   Click "Advanced settings" → "Secrets" and add:
   
   ```toml
   CHATGROQ_API_KEY = "your_groq_api_key_here"
   USE_LOCAL_JUDGE = "true"
   JUDGE_LORA_PATH = "YOUR_USERNAME/genai-courtroom-judge"
   ```
   
   If your model is private, also add:
   ```toml
   HF_TOKEN = "your_huggingface_token_here"
   ```

5. **Deploy**
   - Click "Deploy!"
   - Wait 5-10 minutes for initial deployment (model download takes time)

6. **Access Your App**
   - You'll get a URL like `https://your-app.streamlit.app`

#### Notes:
- ⚠️ **First load will be slow** (downloading model from HuggingFace)
- ⚠️ **Free tier limitations**: 1GB RAM, may need to optimize for large models
- ✅ **Automatic updates**: Push to GitHub → auto-redeploy

---

### Option 2: Render

**Best for:** Docker deployments, more control, persistent storage

#### Steps:

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure Service**
   - **Name**: `genai-courtroom`
   - **Environment**: `Docker`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Plan**: Free (or paid for better performance)

4. **Set Environment Variables**
   Add these in the "Environment" section:
   ```
   CHATGROQ_API_KEY=your_groq_api_key_here
   USE_LOCAL_JUDGE=true
   JUDGE_LORA_PATH=YOUR_USERNAME/genai-courtroom-judge
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for build and deployment (~10-15 minutes)

6. **Access Your App**
   - You'll get a URL like `https://genai-courtroom.onrender.com`

#### Notes:
- ✅ **Better performance** than Streamlit Cloud free tier
- ⚠️ **Free tier sleeps after inactivity** (30 min to wake up)
- ✅ **Persistent storage** available

---

### Option 3: Railway

**Best for:** Easy deployment, good free tier, fast builds

#### Steps:

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign in with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `genai-courtroom` repository

3. **Configure Deployment**
   Railway will auto-detect the Dockerfile

4. **Set Environment Variables**
   In the project settings, add:
   ```
   CHATGROQ_API_KEY=your_groq_api_key_here
   USE_LOCAL_JUDGE=true
   JUDGE_LORA_PATH=YOUR_USERNAME/genai-courtroom-judge
   PORT=8501
   ```

5. **Deploy**
   - Railway will automatically build and deploy
   - Wait ~5-10 minutes

6. **Access Your App**
   - Click "Generate Domain" to get a public URL

#### Notes:
- ✅ **$5 free credit per month**
- ✅ **Fast deployments**
- ✅ **No sleep on free tier** (unlike Render)

---

### Option 4: Hugging Face Spaces

**Best for:** ML-focused deployments, GPU support (paid)

#### Steps:

1. **Create New Space**
   - Go to [huggingface.co/new-space](https://huggingface.co/new-space)
   - Choose "Streamlit" as the SDK
   - Name it `genai-courtroom`

2. **Clone and Push**
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/genai-courtroom
   cd genai-courtroom
   
   # Copy your project files
   cp -r /path/to/genai-courtroom/* .
   
   git add .
   git commit -m "Initial deployment"
   git push
   ```

3. **Configure Secrets**
   In Space settings → "Repository secrets":
   ```
   CHATGROQ_API_KEY=your_groq_api_key_here
   USE_LOCAL_JUDGE=true
   JUDGE_LORA_PATH=YOUR_USERNAME/genai-courtroom-judge
   ```

4. **Create `app.py`**
   Hugging Face Spaces expects `app.py` in the root:
   ```bash
   cp streamlit_app.py app.py
   ```

5. **Access Your App**
   - URL: `https://huggingface.co/spaces/YOUR_USERNAME/genai-courtroom`

#### Notes:
- ✅ **GPU support available** (paid)
- ✅ **Great for ML models**
- ⚠️ **Different file structure** than other platforms

---

## Local Docker Testing

Test your deployment locally before pushing to cloud:

### Build Docker Image

```bash
docker build -t genai-courtroom .
```

### Run Container

```bash
docker run -p 8501:8501 \
  -e CHATGROQ_API_KEY="your_api_key" \
  -e USE_LOCAL_JUDGE="true" \
  -e JUDGE_LORA_PATH="YOUR_USERNAME/genai-courtroom-judge" \
  genai-courtroom
```

### Access Locally

Open [http://localhost:8501](http://localhost:8501)

### Using docker-compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "8501:8501"
    env_file:
      - .env
    volumes:
      - ./rag/embeddings:/app/rag/embeddings
```

Then run:
```bash
docker-compose up
```

---

## Troubleshooting

### Model Download Issues

**Problem**: Model fails to download from Hugging Face

**Solutions**:
1. Verify model exists: `https://huggingface.co/YOUR_USERNAME/genai-courtroom-judge`
2. Check if model is private → add `HF_TOKEN` environment variable
3. Check logs for specific error messages

### Out of Memory Errors

**Problem**: App crashes with memory errors

**Solutions**:
1. Use a paid tier with more RAM
2. Disable fine-tuned model: Set `USE_LOCAL_JUDGE=false`
3. Optimize model loading (lazy loading is already implemented)

### Slow First Load

**Problem**: App takes 5-10 minutes to start

**Explanation**: This is normal! The app needs to:
1. Download the fine-tuned model from Hugging Face (~500MB)
2. Load the base model
3. Initialize FAISS embeddings

**Solutions**:
- Use a platform with persistent storage (Render, Railway)
- Consider pre-warming the cache
- Show a loading message to users

### API Rate Limits

**Problem**: Groq API returns 429 errors

**Solutions**:
1. The code already has retry logic with backoff
2. Check your Groq API quota
3. Consider upgrading Groq plan for higher limits

### PDF Upload Not Working

**Problem**: PDF upload fails or doesn't process

**Solutions**:
1. Check file size limits (Streamlit default: 200MB)
2. Verify PyMuPDF is installed correctly
3. Check logs for specific errors

### Constitution Index Missing

**Problem**: "FAISS index not found" error

**Solutions**:
1. Upload a PDF through the UI to create the index
2. Pre-build the index:
   ```bash
   python build_constitution_index.py
   ```
3. Include pre-built index in deployment

---

## Performance Optimization

### For Production Deployments:

1. **Pre-build Constitution Index**
   ```bash
   python build_constitution_index.py
   ```
   Commit the `rag/embeddings/` directory

2. **Use CPU-optimized Models**
   - The current setup uses `faiss-cpu` (good for free tiers)
   - For GPU deployments, switch to `faiss-gpu`

3. **Enable Caching**
   - Streamlit has built-in caching
   - Model loading is already cached globally

4. **Monitor Usage**
   - Track API calls to Groq
   - Monitor memory usage
   - Set up error logging (Sentry, LogRocket)

---

## Next Steps

1. ✅ Upload model to Hugging Face
2. ✅ Choose deployment platform
3. ✅ Set environment variables
4. ✅ Deploy and test
5. 📊 Monitor performance
6. 🎨 Customize UI (optional)
7. 📚 Add more legal documents (optional)

---

## Support

- **Groq API**: [console.groq.com](https://console.groq.com)
- **Hugging Face**: [huggingface.co/docs](https://huggingface.co/docs)
- **Streamlit**: [docs.streamlit.io](https://docs.streamlit.io)

---

**Good luck with your deployment! 🚀**
