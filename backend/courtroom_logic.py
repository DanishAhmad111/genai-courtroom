import os
import requests
from dotenv import load_dotenv
from rag.rag_utils import search_top_chunks
import time 

load_dotenv()  # Load CHATGROQ_API_KEY from .env

# --- Local PEFT model configuration ---
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel, PeftConfig
USE_LOCAL_MODEL = os.getenv("USE_LOCAL_JUDGE", "false").lower() in ("1","true","yes")
_local_model = None
_local_tok = None

def _ensure_local():
    """Lazily load the base model plus LoRA adapter once and cache globally.
    Supports both local paths and HuggingFace Hub model IDs."""
    global _local_model, _local_tok
    if _local_model is None:
        adapter_path = os.getenv("JUDGE_LORA_PATH", "judge-lora")
        
        # Check if it's a HuggingFace Hub model ID (contains /)
        if "/" in adapter_path:
            print(f"🌐 Downloading model from HuggingFace Hub: {adapter_path}")
            # HuggingFace Hub will automatically cache the model
            from huggingface_hub import snapshot_download
            try:
                # Download model if not cached
                local_path = snapshot_download(
                    repo_id=adapter_path,
                    token=os.getenv("HF_TOKEN")  # Optional: for private models
                )
                adapter_path = local_path
                print(f"✅ Model downloaded to: {adapter_path}")
            except Exception as e:
                print(f"❌ Failed to download model from HuggingFace: {e}")
                print("💡 Tip: Make sure the model exists and you have access")
                raise
        else:
            print(f"📁 Loading local model from: {adapter_path}")
        
        try:
            cfg = PeftConfig.from_pretrained(adapter_path)
            base = AutoModelForCausalLM.from_pretrained(
                cfg.base_model_name_or_path,
                torch_dtype="auto",
                device_map="auto" if torch.cuda.is_available() else None,
            )
            _local_model = PeftModel.from_pretrained(base, adapter_path)
            _local_tok = AutoTokenizer.from_pretrained(cfg.base_model_name_or_path)
            print("✅ Model loaded successfully")
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise


# Load a prompt from file
def load_prompt(path):
    with open(path, 'r') as file:
        return file.read()

# Replace {placeholders} with actual content
def fill_prompt(template, **kwargs):
    for key, value in kwargs.items():
        template = template.replace(f"{{{key}}}", value)
    return template

# Call LLM (local LoRA if enabled, otherwise Groq API)
import time

def call_llm(prompt: str, model: str = "llama-3.3-70b-versatile", retries: int = 3):
    """Generate a response using either the local LoRA-fine-tuned model or the remote Groq endpoint."""
    if USE_LOCAL_MODEL:
        _ensure_local()
        inputs = _local_tok(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=_local_tok.model_max_length
        ).to(_local_model.device)
        out = _local_model.generate(**inputs, max_new_tokens=512, temperature=0.7)
        return _local_tok.decode(out[0], skip_special_tokens=True)

    # --- Remote fallback (Groq) ---
    api_key = os.getenv("CHATGROQ_API_KEY")
    endpoint = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Allow override via env var
    model_override = os.getenv("GROQ_MODEL")
    if model_override:
        model = model_override
    print(f"[call_llm] Using Groq model: {model}")

    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 500,  # Limit response length
        "stop": ["\n\n\n", "---", "CASE:", "You are"]  # Stop on repetitive patterns
    }

    for attempt in range(retries):
        response = requests.post(endpoint, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        elif response.status_code == 429:
            # Rate limited — wait and retry
            print("⏳ Rate limited. Waiting before retrying...")
            time.sleep(12)  # Add buffer
        else:
            return f"❌ Error {response.status_code}: {response.text}"

    return "❌ Failed after retries."

def call_hybrid_judge(prompt: str, model: str = "llama-3.3-70b-versatile", retries: int = 3):
    """Hybrid judge function that uses both fine-tuned and original models for enhanced judgment."""
    
    # Get response from fine-tuned model if available
    finetuned_response = None
    if USE_LOCAL_MODEL:
        try:
            _ensure_local()
            inputs = _local_tok(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=_local_tok.model_max_length
        ).to(_local_model.device)
            out = _local_model.generate(**inputs, max_new_tokens=512, temperature=0.7)
            finetuned_response = _local_tok.decode(out[0], skip_special_tokens=True)
            print("🔧 Fine-tuned model response obtained")
        except Exception as e:
            print(f"⚠️ Fine-tuned model failed: {e}")
    
    # Get response from original model via Groq API
    original_response = None
    api_key = os.getenv("CHATGROQ_API_KEY")
    if api_key:
        endpoint = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        # Allow override via env var
        model_override = os.getenv("GROQ_MODEL")
        if model_override:
            model = model_override
        print(f"[call_hybrid_judge] Using Groq model: {model}")
        data = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 500,
            "stop": ["\n\n\n", "---", "CASE:", "You are"]
        }
        
        for attempt in range(retries):
            response = requests.post(endpoint, headers=headers, json=data)
            if response.status_code == 200:
                original_response = response.json()['choices'][0]['message']['content']
                print("🌐 Original model response obtained")
                break
            elif response.status_code == 429:
                print("⏳ Rate limited. Waiting before retrying...")
                time.sleep(12)
    
    # Combine responses intelligently
    if finetuned_response and original_response:
        # Create a synthesis prompt for final judgment
        synthesis_prompt = f"""As a senior Indian High Court judge, synthesize these two legal analyses into a final, authoritative verdict:

FINE-TUNED LEGAL ANALYSIS:
{finetuned_response}

BROAD LEGAL ANALYSIS:
{original_response}

Provide a final, well-reasoned verdict that incorporates the best insights from both analyses, citing relevant precedents and legal principles:"""
        
        # Use original model for synthesis to ensure coherent final output
        if api_key:
            # Apply same override to synthesis call
            model_override = os.getenv("GROQ_MODEL")
            if model_override:
                model = model_override
            print(f"[call_hybrid_judge:synthesis] Using Groq model: {model}")
            synthesis_data = {
                "model": model,
                "messages": [{"role": "user", "content": synthesis_prompt}],
                "temperature": 0.6,
                "max_tokens": 600,
                "stop": ["\n\n\n", "---", "CASE:", "You are"]
            }
            synthesis_response = requests.post(endpoint, headers=headers, json=synthesis_data)
            if synthesis_response.status_code == 200:
                final_verdict = synthesis_response.json()['choices'][0]['message']['content']
                print("⚖️ Hybrid judgment synthesized successfully")
        
        # Fallback: return fine-tuned response if synthesis fails
        return f"**HYBRID JUDGMENT**\n\n**Fine-tuned Analysis:**\n{finetuned_response}\n\n**Broad Analysis:**\n{original_response}"
    
    elif finetuned_response:
        print("🔧 Using fine-tuned model response only")
        return finetuned_response
    elif original_response:
        print("🌐 Using original model response only")
        return original_response
    else:
        return "❌ Both models failed to generate a response."

# Orchestrate the courtroom process
def run_courtroom(case):
    # Load all prompt templates with absolute paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prosecution_template = load_prompt(os.path.join(base_dir, "prompts", "prosecution.txt"))
    defense_template = load_prompt(os.path.join(base_dir, "prompts", "defense.txt"))
    judge_template = load_prompt(os.path.join(base_dir, "prompts", "judge.txt"))

    # Step 1: RAG – search for relevant context (optional)
    try:
        top_chunks = search_top_chunks(case, k=2)
        evidence = "\n".join(top_chunks)
    except (FileNotFoundError, ValueError, Exception) as e:
        # No PDF uploaded or index missing - that's okay, proceed without RAG
        evidence = ""

    # Step 2: Add evidence into the case
    enriched_case = f"CASE:\n{case}\n\nLEGAL REFERENCES (if any):\n{evidence}"

    # Step 3: Generate prosecution and defense arguments
    prosecution_prompt = fill_prompt(prosecution_template, case=enriched_case)
    defense_prompt = fill_prompt(defense_template, case=enriched_case)

    prosecution = call_llm(prosecution_prompt)
    defense = call_llm(defense_prompt)

    # Step 4: Generate verdict from judge using hybrid logic
    judge_prompt = fill_prompt(judge_template, prosecution=prosecution, defense=defense, context=evidence)
    verdict = call_hybrid_judge(judge_prompt)

    return prosecution, defense, verdict