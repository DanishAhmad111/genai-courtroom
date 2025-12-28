"""
Upload the fine-tuned judge LoRA adapter to Hugging Face Hub.

This script helps you upload your local judge-lora model to Hugging Face Hub
so it can be downloaded during deployment.

Usage:
    python scripts/upload_model_to_hf.py --model_path judge-lora --repo_name your-username/genai-courtroom-judge

Prerequisites:
    1. Install huggingface-hub: pip install huggingface-hub
    2. Login to HuggingFace: huggingface-cli login
    3. Create a model repository on https://huggingface.co/new
"""

import argparse
import os
from huggingface_hub import HfApi, create_repo
from pathlib import Path


def upload_model_to_hub(model_path: str, repo_name: str, private: bool = False):
    """
    Upload a local model directory to Hugging Face Hub.
    
    Args:
        model_path: Local path to the model directory (e.g., 'judge-lora')
        repo_name: HuggingFace repository name (e.g., 'username/model-name')
        private: Whether to make the repository private
    """
    api = HfApi()
    
    # Verify model path exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model path '{model_path}' does not exist")
    
    print(f"📦 Preparing to upload model from: {model_path}")
    print(f"🎯 Target repository: {repo_name}")
    print(f"🔒 Private: {private}")
    
    # Create repository if it doesn't exist
    try:
        print("\n🔨 Creating repository...")
        create_repo(
            repo_id=repo_name,
            repo_type="model",
            private=private,
            exist_ok=True
        )
        print("✅ Repository created/verified")
    except Exception as e:
        print(f"⚠️  Repository creation warning: {e}")
        print("Continuing with upload...")
    
    # Upload all files in the model directory
    print(f"\n📤 Uploading files from {model_path}...")
    
    try:
        api.upload_folder(
            folder_path=model_path,
            repo_id=repo_name,
            repo_type="model",
        )
        print("\n✅ Upload complete!")
        print(f"\n🎉 Your model is now available at: https://huggingface.co/{repo_name}")
        print(f"\n📝 To use in deployment, set environment variable:")
        print(f"   JUDGE_LORA_PATH={repo_name}")
        
    except Exception as e:
        print(f"\n❌ Upload failed: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you're logged in: huggingface-cli login")
        print("2. Check your internet connection")
        print("3. Verify the repository name format: username/model-name")
        raise


def main():
    parser = argparse.ArgumentParser(
        description="Upload fine-tuned judge model to Hugging Face Hub"
    )
    parser.add_argument(
        "--model_path",
        type=str,
        default="judge-lora",
        help="Local path to the model directory"
    )
    parser.add_argument(
        "--repo_name",
        type=str,
        required=True,
        help="HuggingFace repository name (format: username/model-name)"
    )
    parser.add_argument(
        "--private",
        action="store_true",
        help="Make the repository private"
    )
    
    args = parser.parse_args()
    
    # Validate repo_name format
    if "/" not in args.repo_name:
        print("❌ Error: repo_name must be in format 'username/model-name'")
        print("Example: myusername/genai-courtroom-judge")
        return
    
    upload_model_to_hub(
        model_path=args.model_path,
        repo_name=args.repo_name,
        private=args.private
    )


if __name__ == "__main__":
    main()
