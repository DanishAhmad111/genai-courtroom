# 🎯 Create GitHub Repository - Step by Step

## The Issue
The repository `https://github.com/DanishAhmad111/genai-courtroom` doesn't exist yet. You need to create it first!

---

## ✅ Step-by-Step: Create GitHub Repository

### Step 1: Go to GitHub
Open your browser and visit: **https://github.com/new**

(Or go to https://github.com and click the "+" icon → "New repository")

### Step 2: Fill in Repository Details

**Repository name:**
```
genai-courtroom
```

**Description (optional):**
```
AI-powered courtroom simulation with RAG and fine-tuned LLM for legal verdicts
```

**Visibility:**
- ✅ Select **Public** (so Streamlit Cloud can access it)

**Initialize repository:**
- ❌ **DO NOT** check "Add a README file"
- ❌ **DO NOT** check "Add .gitignore"
- ❌ **DO NOT** select a license

**Why?** Because you already have these files locally!

### Step 3: Create Repository
Click the green **"Create repository"** button

### Step 4: You'll See Instructions
GitHub will show you commands. **IGNORE THEM** - we'll use our own commands.

---

## 🚀 Step 5: Push Your Code

Now that the repository exists, run these commands in your terminal:

```cmd
cd c:\Users\Asus\OneDrive\Desktop\projects\genai-courtroom

REM Verify remote is set correctly
git remote -v

REM Push to GitHub
git push -u origin main
```

**If you get an error about branch name**, try:
```cmd
git branch -M main
git push -u origin main
```

---

## 🔐 Authentication

When you push, GitHub may ask for authentication:

### Option 1: Personal Access Token (Recommended)

1. **Create Token:**
   - Go to: https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Name: `genai-courtroom-deploy`
   - Expiration: 90 days (or your preference)
   - Select scopes: ✅ **repo** (check all repo boxes)
   - Click "Generate token"
   - **COPY THE TOKEN** (you won't see it again!)

2. **Use Token:**
   - When prompted for username: enter `DanishAhmad111`
   - When prompted for password: **paste your token** (not your GitHub password!)

### Option 2: GitHub CLI (Easier)

```cmd
gh auth login
```
Follow the prompts to authenticate through your browser.

---

## ✅ Verify Success

After pushing:

1. Go to: **https://github.com/DanishAhmad111/genai-courtroom**
2. Refresh the page
3. You should see all your files!

---

## 📋 Quick Checklist

- [ ] Go to https://github.com/new
- [ ] Repository name: `genai-courtroom`
- [ ] Visibility: Public
- [ ] **DO NOT** initialize with README/gitignore/license
- [ ] Click "Create repository"
- [ ] Run: `git push -u origin main`
- [ ] Authenticate with Personal Access Token
- [ ] Verify files appear on GitHub

---

## 🚀 After GitHub Push Succeeds

Follow **STREAMLIT_DEPLOY.md** to deploy your app!

---

**Let me know once you've created the repository and I'll help you push!** 🎯
