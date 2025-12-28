#!/bin/bash
# Step-by-step deployment script for GenAI Courtroom (Linux/Mac)

echo "========================================"
echo "GenAI Courtroom Deployment Helper"
echo "========================================"
echo ""

# Step 1: Check if huggingface-hub is installed
echo "[Step 1/5] Checking HuggingFace Hub installation..."
python -c "import huggingface_hub" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "HuggingFace Hub not found. Installing..."
    pip install huggingface-hub
else
    echo "HuggingFace Hub already installed."
fi
echo ""

# Step 2: Check login status
echo "[Step 2/5] Checking HuggingFace login status..."
huggingface-cli whoami 2>/dev/null
if [ $? -ne 0 ]; then
    echo "You are not logged in to HuggingFace."
    echo "Please run: huggingface-cli login"
    echo "Then run this script again."
    exit 1
fi
echo ""

# Step 3: Prompt for model repository name
echo "[Step 3/5] Model Upload Configuration"
read -p "Enter your HuggingFace username: " HF_USERNAME
MODEL_REPO="$HF_USERNAME/genai-courtroom-judge"
echo ""
echo "Model will be uploaded to: $MODEL_REPO"
echo ""
read -p "Is this correct? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "Upload cancelled."
    exit 1
fi
echo ""

# Step 4: Upload model
echo "[Step 4/5] Uploading model to HuggingFace Hub..."
echo "This may take several minutes..."
python scripts/upload_model_to_hf.py --repo_name "$MODEL_REPO"
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Model upload failed!"
    echo "Please check the error messages above."
    exit 1
fi
echo ""

# Step 5: Update .env file
echo "[Step 5/5] Updating .env file..."
if [ ! -f .env ]; then
    cp .env.example .env
fi

cat > .env << EOF
CHATGROQ_API_KEY=your_groq_api_key_here
USE_LOCAL_JUDGE=true
JUDGE_LORA_PATH=$MODEL_REPO
GROQ_MODEL=llama-3.3-70b-versatile
EOF

echo ""
echo "========================================"
echo "SUCCESS! Model uploaded successfully!"
echo "========================================"
echo ""
echo "Model URL: https://huggingface.co/$MODEL_REPO"
echo ""
echo "NEXT STEPS:"
echo "1. Update your .env file with your Groq API key"
echo "2. Test locally: docker-compose up"
echo "3. Push to GitHub: git add . && git commit -m 'Ready for deployment' && git push"
echo "4. Deploy to Streamlit Cloud (see DEPLOYMENT.md)"
echo ""
echo "Your .env has been updated with:"
echo "  JUDGE_LORA_PATH=$MODEL_REPO"
echo ""
