# 🚀 Final Step: Deploy to Streamlit Cloud

## ✅ What You've Completed So Far:
- [x] Model uploaded to HuggingFace: **XDanish/genai-courtroom-judge**
- [x] Code pushed to GitHub
- [ ] Deploy to Streamlit Cloud ← **YOU ARE HERE**

---

## 📝 Step-by-Step Streamlit Cloud Deployment

### Step 1: Go to Streamlit Cloud
Open your browser and visit: **https://share.streamlit.io**

### Step 2: Sign In
- Click **"Sign in with GitHub"**
- Authorize Streamlit to access your GitHub account

### Step 3: Create New App
- Click the **"New app"** button (top right)

### Step 4: Configure Your App

Fill in the deployment form:

**Repository:**
- Select your GitHub repository: `genai-courtroom`

**Branch:**
- Select: `main` (or `master` if that's your default branch)

**Main file path:**
- Enter: `streamlit_app.py`

### Step 5: Advanced Settings (IMPORTANT!)

Click **"Advanced settings"** at the bottom

#### Add Secrets

Click on the **"Secrets"** tab and paste this EXACTLY:

```toml
CHATGROQ_API_KEY = "your_actual_groq_api_key_here"
USE_LOCAL_JUDGE = "true"
JUDGE_LORA_PATH = "XDanish/genai-courtroom-judge"
```

**⚠️ IMPORTANT:**
- Replace `your_actual_groq_api_key_here` with your real Groq API key
- Get your Groq API key from: https://console.groq.com
- Keep the quotes around the values
- Make sure there are NO extra spaces

**Example with real key:**
```toml
CHATGROQ_API_KEY = "gsk_abc123xyz456..."
USE_LOCAL_JUDGE = "true"
JUDGE_LORA_PATH = "XDanish/genai-courtroom-judge"
```

### Step 6: Deploy!

- Click **"Deploy!"** button
- Wait for deployment (this will take 10-15 minutes on first deploy)

---

## ⏳ What Happens During Deployment:

1. **Building** (2-3 minutes)
   - Installing dependencies
   - Setting up environment

2. **Downloading Model** (5-10 minutes)
   - Downloading your fine-tuned model from HuggingFace
   - This is the longest part - be patient!

3. **Starting App** (1-2 minutes)
   - Initializing Streamlit
   - Loading models

4. **Ready!** 🎉
   - Your app will be live!

---

## 🎯 Your App URL

Once deployed, you'll get a URL like:
```
https://YOUR-APP-NAME.streamlit.app
```

You can customize the app name in the deployment settings.

---

## ✅ Test Your Deployed App

1. **Open your app URL**

2. **Enter a test case:**
   ```
   A person is accused of theft of a mobile phone worth Rs. 15,000 
   from a shop. The defense claims mistaken identity and provides 
   an alibi. The prosecution has CCTV footage.
   ```

3. **Click "Simulate Trial"**

4. **Wait for results** (30-60 seconds)

5. **Verify you see:**
   - ✅ Prosecution argument
   - ✅ Defense response
   - ✅ Judge verdict (using your fine-tuned model!)

6. **Test PDF upload:**
   - Upload any legal PDF
   - Wait for "Document processed" message
   - Submit another case to test RAG

---

## 🎉 Success Criteria

Your deployment is successful when:
- ✅ App loads without errors
- ✅ Can submit cases and get all three outputs
- ✅ Fine-tuned model is working (check logs for "Model loaded successfully")
- ✅ PDF upload works
- ✅ No errors in Streamlit Cloud logs

---

## 🔧 If You See Errors

### "Module not found" error
→ Check that `requirements.txt` was pushed to GitHub
→ Redeploy the app

### "Out of memory" error
→ Streamlit Cloud free tier has 1GB RAM
→ Try setting `USE_LOCAL_JUDGE = "false"` in secrets
→ Or upgrade to paid tier

### "Model not found" error
→ Verify `JUDGE_LORA_PATH = "XDanish/genai-courtroom-judge"` in secrets
→ Check that model is public on HuggingFace
→ Visit: https://huggingface.co/XDanish/genai-courtroom-judge

### "API key invalid" error
→ Check your `CHATGROQ_API_KEY` in secrets
→ Make sure it's a valid key from console.groq.com
→ No extra spaces or quotes issues

---

## 📊 Monitor Your App

### View Logs
- In Streamlit Cloud dashboard, click on your app
- Click "Manage app" → "Logs"
- Watch for errors or model loading messages

### Check Usage
- Monitor your Groq API usage at console.groq.com
- Free tier has rate limits

---

## 🔄 Making Updates

To update your deployed app:

1. Make changes locally
2. Test locally: `streamlit run streamlit_app.py`
3. Commit and push:
   ```bash
   git add .
   git commit -m "Your update message"
   git push origin main
   ```
4. Streamlit Cloud will **automatically redeploy**!

---

## 🎊 Congratulations!

Your GenAI Courtroom is now:
- ✅ **Live on the internet**
- ✅ **Using your fine-tuned judge model**
- ✅ **Accessible to anyone with the URL**
- ✅ **Automatically updated from GitHub**

---

## 📱 Share Your App

Share your app URL with:
- Friends and colleagues
- Legal professionals
- On social media
- In your portfolio

---

## 🆘 Need Help?

- **Streamlit Docs**: https://docs.streamlit.io/streamlit-community-cloud
- **Community Forum**: https://discuss.streamlit.io
- **Check logs** in Streamlit Cloud dashboard

---

**You're all done! Enjoy your deployed GenAI Courtroom!** 🎉🧑‍⚖️
