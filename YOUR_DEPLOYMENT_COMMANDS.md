# 🎯 Your Personalized Deployment Commands

## Your Configuration
- **HuggingFace Username**: XDanish
- **Model Repository**: XDanish/genai-courtroom-judge
- **Model URL**: https://huggingface.co/XDanish/genai-courtroom-judge

---

## 📋 Run These Commands in Order

### Step 1: Install HuggingFace Hub
```cmd
pip install huggingface-hub
```

### Step 2: Login to HuggingFace
```cmd
huggingface-cli login
```
**When prompted:**
- Paste your HuggingFace token (get from: https://huggingface.co/settings/tokens)
- Press Enter
- Choose "Y" to add token as git credential

### Step 3: Upload Model to HuggingFace
```cmd
python scripts/upload_model_to_hf.py --repo_name XDanish/genai-courtroom-judge
```

**This will:**
- Create repository on HuggingFace
- Upload all files from judge-lora directory
- Take 5-10 minutes depending on internet speed

### Step 4: Update .env File
```cmd
copy .env.example .env
```

Then edit `.env` file and add:
```env
CHATGROQ_API_KEY=your_groq_api_key_here
USE_LOCAL_JUDGE=true
JUDGE_LORA_PATH=XDanish/genai-courtroom-judge
GROQ_MODEL=llama-3.3-70b-versatile
```

**Replace `your_groq_api_key_here` with your actual Groq API key!**

### Step 5: Test Locally (Optional)
```cmd
streamlit run streamlit_app.py
```
Visit: http://localhost:8501

Press Ctrl+C to stop when done testing.

### Step 6: Prepare for GitHub
```cmd
git add .
git commit -m "Add deployment configuration with fine-tuned model"
git push origin main
```

If your branch is `master` instead of `main`:
```cmd
git push origin master
```

---

## 🌐 Step 7: Deploy to Streamlit Cloud

1. Go to: https://share.streamlit.io
2. Click "Sign in with GitHub"
3. Click "New app"
4. Configure:
   - **Repository**: genai-courtroom
   - **Branch**: main
   - **Main file**: streamlit_app.py

5. Click "Advanced settings" → "Secrets" and add:
```toml
CHATGROQ_API_KEY = "your_groq_api_key_here"
USE_LOCAL_JUDGE = "true"
JUDGE_LORA_PATH = "XDanish/genai-courtroom-judge"
```

6. Click "Deploy!"

---

## ✅ Verification

After deployment, test your app:
1. Visit your Streamlit Cloud URL
2. Enter a test case
3. Click "Simulate Trial"
4. Verify all three outputs appear

---

## 🆘 If You Get Errors

### "Not logged in to HuggingFace"
→ Run: `huggingface-cli login`

### "Repository already exists"
→ That's OK! The upload will still work.

### "Model upload failed"
→ Check your internet connection
→ Make sure you're logged in to HuggingFace
→ Try again

### "Git push rejected"
→ Run: `git pull origin main` first
→ Then: `git push origin main`

---

## 📞 Need Your Groq API Key?

Get it from: https://console.groq.com

---

**Start with Step 1 and work your way down!** 🚀
