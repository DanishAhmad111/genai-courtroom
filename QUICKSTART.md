# 🚀 Quick Deployment Guide

## TL;DR - Deploy in 3 Steps

### 1️⃣ Upload Model to HuggingFace

```bash
pip install huggingface-hub
huggingface-cli login
python scripts/upload_model_to_hf.py --repo_name YOUR_USERNAME/genai-courtroom-judge
```

### 2️⃣ Push to GitHub

```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 3️⃣ Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app" → Select your repo
3. Add secrets:
   ```toml
   CHATGROQ_API_KEY = "your_groq_api_key"
   USE_LOCAL_JUDGE = "true"
   JUDGE_LORA_PATH = "YOUR_USERNAME/genai-courtroom-judge"
   ```
4. Click "Deploy!"

---

## 📋 Pre-Deployment Checklist

- [ ] Have Groq API key ([Get one](https://console.groq.com))
- [ ] Have HuggingFace account ([Sign up](https://huggingface.co/join))
- [ ] Code pushed to GitHub
- [ ] Model uploaded to HuggingFace
- [ ] `.env.example` copied to `.env` locally for testing

---

## 🔑 Required Secrets/Environment Variables

```toml
CHATGROQ_API_KEY = "gsk_..."           # From console.groq.com
USE_LOCAL_JUDGE = "true"                # Enable fine-tuned model
JUDGE_LORA_PATH = "username/model-name" # Your HF model path
```

---

## 🧪 Test Locally First (Optional)

```bash
# Using Docker Compose
docker-compose up

# Or using Streamlit directly
streamlit run streamlit_app.py
```

Visit [http://localhost:8501](http://localhost:8501)

---

## 🌐 Platform Comparison

| Platform | Difficulty | Free Tier | Best For |
|----------|-----------|-----------|----------|
| **Streamlit Cloud** | ⭐ Easy | 1GB RAM | Quick demos |
| **Railway** | ⭐⭐ Medium | $5 credit | Production |
| **Render** | ⭐⭐ Medium | 512MB RAM | Docker apps |
| **HF Spaces** | ⭐⭐⭐ Hard | 16GB RAM | ML models |

**Recommendation**: Start with Streamlit Cloud, upgrade to Railway for production.

---

## ⚡ Common Issues & Fixes

### "Model not found"
→ Check HuggingFace model URL is correct  
→ Make model public or add `HF_TOKEN`

### "Out of memory"
→ Upgrade to paid tier  
→ Or set `USE_LOCAL_JUDGE=false` (use only Groq API)

### "Slow first load"
→ Normal! Model downloading takes 5-10 minutes  
→ Subsequent loads will be faster

---

## 📖 Full Documentation

- **Detailed Guide**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Project Info**: [README.md](README.md)
- **Complete Walkthrough**: See artifacts

---

**Need help?** Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.
