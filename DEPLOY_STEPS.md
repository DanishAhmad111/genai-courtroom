# 🚀 Manual Deployment Steps

Follow these steps in order to deploy your GenAI Courtroom application.

## ✅ Prerequisites Checklist

Before starting, make sure you have:
- [ ] Groq API Key from [console.groq.com](https://console.groq.com)
- [ ] HuggingFace account from [huggingface.co/join](https://huggingface.co/join)
- [ ] GitHub account and repository created
- [ ] Git installed on your computer

---

## 📦 Step 1: Upload Model to HuggingFace

### Option A: Use Automated Script (Recommended)

**Windows:**
```cmd
deploy.bat
```

**Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh
```

The script will:
1. Install HuggingFace Hub if needed
2. Check if you're logged in
3. Prompt for your username
4. Upload the model
5. Update your .env file

### Option B: Manual Upload

1. **Install HuggingFace Hub**
   ```bash
   pip install huggingface-hub
   ```

2. **Login to HuggingFace**
   ```bash
   huggingface-cli login
   ```
   - Paste your HuggingFace token when prompted
   - Get token from: https://huggingface.co/settings/tokens

3. **Create Repository on HuggingFace**
   - Go to: https://huggingface.co/new
   - Repository type: Model
   - Name: `genai-courtroom-judge`
   - Visibility: Public (or Private if you prefer)
   - Click "Create repository"

4. **Upload Model**
   ```bash
   python scripts/upload_model_to_hf.py --repo_name YOUR_USERNAME/genai-courtroom-judge
   ```
   Replace `YOUR_USERNAME` with your actual HuggingFace username.

5. **Verify Upload**
   - Visit: `https://huggingface.co/YOUR_USERNAME/genai-courtroom-judge`
   - You should see your model files

---

## 🔧 Step 2: Update Environment Variables

1. **Copy the example file**
   ```bash
   copy .env.example .env    # Windows
   cp .env.example .env      # Linux/Mac
   ```

2. **Edit .env file** with your values:
   ```env
   CHATGROQ_API_KEY=gsk_your_actual_groq_api_key_here
   USE_LOCAL_JUDGE=true
   JUDGE_LORA_PATH=YOUR_USERNAME/genai-courtroom-judge
   GROQ_MODEL=llama-3.3-70b-versatile
   ```

   **Important**: Replace:
   - `YOUR_USERNAME` with your HuggingFace username
   - `gsk_...` with your actual Groq API key from console.groq.com

---

## 🧪 Step 3: Test Locally (Optional but Recommended)

### Option A: Using Docker Compose

```bash
docker-compose up
```

Then visit: http://localhost:8501

### Option B: Using Streamlit Directly

```bash
streamlit run streamlit_app.py
```

Then visit: http://localhost:8501

**Test the following:**
- [ ] App loads without errors
- [ ] Can enter a case description
- [ ] Can click "Simulate Trial"
- [ ] Prosecution, Defense, and Verdict all generate
- [ ] Can upload a PDF document
- [ ] No errors in terminal/console

**Stop the app:** Press `Ctrl+C` in terminal

---

## 📤 Step 4: Push to GitHub

1. **Check Git status**
   ```bash
   git status
   ```

2. **Add all new files**
   ```bash
   git add .
   ```

3. **Commit changes**
   ```bash
   git commit -m "Add deployment configuration with fine-tuned model support"
   ```

4. **Push to GitHub**
   ```bash
   git push origin main
   ```
   
   Or if your branch is named `master`:
   ```bash
   git push origin master
   ```

5. **Verify on GitHub**
   - Go to your repository on GitHub
   - Refresh the page
   - You should see all the new files

---

## ☁️ Step 5: Deploy to Streamlit Cloud

### 5.1 Create Streamlit Cloud Account

1. Go to: https://share.streamlit.io
2. Click "Sign in with GitHub"
3. Authorize Streamlit to access your GitHub

### 5.2 Deploy Your App

1. Click "New app" button

2. **Configure deployment:**
   - **Repository**: Select `genai-courtroom` (or your repo name)
   - **Branch**: `main` (or `master`)
   - **Main file path**: `streamlit_app.py`

3. **Click "Advanced settings"**

4. **Add Secrets** (very important!):
   Click on "Secrets" tab and paste:
   
   ```toml
   CHATGROQ_API_KEY = "gsk_your_actual_groq_api_key_here"
   USE_LOCAL_JUDGE = "true"
   JUDGE_LORA_PATH = "YOUR_USERNAME/genai-courtroom-judge"
   ```
   
   Replace with your actual values!
   
   If your HuggingFace model is private, also add:
   ```toml
   HF_TOKEN = "hf_your_huggingface_token_here"
   ```

5. **Click "Deploy!"**

### 5.3 Wait for Deployment

- Initial deployment takes **10-15 minutes** (downloading model)
- You'll see build logs in real-time
- Don't worry if it seems slow - this is normal!

### 5.4 Access Your App

Once deployed, you'll get a URL like:
```
https://YOUR-APP-NAME.streamlit.app
```

Share this URL with anyone!

---

## ✅ Step 6: Verify Deployment

Test your deployed app:

1. **Open the app URL**
2. **Enter a test case:**
   ```
   A person is accused of theft of a mobile phone worth Rs. 15,000 
   from a shop. The defense claims mistaken identity and provides 
   an alibi. The prosecution has CCTV footage.
   ```
3. **Click "Simulate Trial"**
4. **Wait for results** (may take 30-60 seconds)
5. **Verify all three sections appear:**
   - ✅ Prosecution argument
   - ✅ Defense response
   - ✅ Judge verdict

6. **Test PDF upload:**
   - Upload any legal PDF
   - Wait for "Document processed" message
   - Submit another case
   - Verify RAG is working

---

## 🎉 Success!

If everything works, congratulations! Your GenAI Courtroom is now live!

**Your app is now:**
- ✅ Deployed to the cloud
- ✅ Using the fine-tuned judge model
- ✅ Accessible via public URL
- ✅ Automatically updates when you push to GitHub

---

## 🔄 Making Updates

To update your deployed app:

1. Make changes to your code locally
2. Test locally
3. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Description of changes"
   git push origin main
   ```
4. Streamlit Cloud will automatically redeploy!

---

## 🆘 Troubleshooting

### "Model not found" error
- Check HuggingFace model URL is correct
- Make sure model is public, or add HF_TOKEN to secrets
- Verify JUDGE_LORA_PATH in secrets matches your HF repo

### "Out of memory" error
- Streamlit Cloud free tier has 1GB RAM limit
- Try setting `USE_LOCAL_JUDGE = "false"` to use only Groq API
- Or upgrade to Streamlit Cloud paid tier

### "API rate limit" error
- Check your Groq API quota at console.groq.com
- The app has retry logic, so wait a moment and try again
- Consider upgrading your Groq plan

### App is very slow
- First load is always slow (downloading model)
- Subsequent loads should be faster (cached)
- If consistently slow, consider upgrading to paid tier

### Changes not appearing
- Make sure you pushed to GitHub: `git push origin main`
- Check Streamlit Cloud logs for errors
- Try manually redeploying from Streamlit Cloud dashboard

---

## 📞 Need Help?

- **Streamlit Docs**: https://docs.streamlit.io
- **HuggingFace Docs**: https://huggingface.co/docs
- **Groq Docs**: https://console.groq.com/docs

---

## 🎯 Alternative Platforms

If Streamlit Cloud doesn't work for you, see **DEPLOYMENT.md** for:
- Render (Docker-based)
- Railway (easy deployment)
- Hugging Face Spaces (ML-focused)
- Self-hosting options

---

**Good luck with your deployment!** 🚀
