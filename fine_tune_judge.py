"""Fine-tune a PEFT LoRA adapter for the judge on Indian legal data prepared by
prepare_dataset.py.

Usage:
    python fine_tune_judge.py --data judge_dataset.jsonl \
        --base microsoft/DialoGPT-medium \
        --output judge-lora

For better results with instruction following, try:
    --base google/flan-t5-base
    --base distilgpt2
"""
import argparse
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import LoraConfig, get_peft_model
try:
    import bitsandbytes as bnb  # noqa: F401
except ImportError:
    print("Warning: bitsandbytes not available, using standard precision")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="judge_dataset.jsonl")
    parser.add_argument("--base", default="distilgpt2")
    parser.add_argument("--output", default="judge-lora")
    parser.add_argument("--epochs", type=int, default=3)
    args = parser.parse_args()

    dataset = load_dataset("json", data_files=args.data, split="train")

    try:
        tokenizer = AutoTokenizer.from_pretrained(args.base, padding_side="right")
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
    except OSError as e:
        if "gated repo" in str(e) or "restricted" in str(e):
            print(f"\nERROR: {args.base} requires authentication.")
            print("Please run: huggingface-cli login")
            print("Or use an open model like: --base microsoft/DialoGPT-medium")
            exit(1)
        raise

    def fmt(ex):
        try:
            # Try to use chat template if available
            return tokenizer.apply_chat_template(ex["messages"], tokenize=False)
        except:
            # Fallback: manually format the conversation
            formatted = ""
            for msg in ex["messages"]:
                if msg["role"] == "system":
                    formatted += f"System: {msg['content']}\n\n"
                elif msg["role"] == "user":
                    formatted += f"User: {msg['content']}\n\n"
                elif msg["role"] == "assistant":
                    formatted += f"Assistant: {msg['content']}"
            return formatted

    print("Formatting dataset...")
    dataset = dataset.map(lambda x: {"text": fmt(x)}, remove_columns=dataset.column_names)
    print(f"Dataset formatted. Sample count: {len(dataset)}")

    # Load model without quantization for better compatibility
    try:
        print(f"Loading base model: {args.base}")
        model = AutoModelForCausalLM.from_pretrained(
            args.base,
            torch_dtype="auto",
            device_map="auto" if torch.cuda.is_available() else None,
        )
        print(f"Model loaded successfully. Parameters: {model.num_parameters():,}")
    except OSError as e:
        if "gated repo" in str(e) or "restricted" in str(e):
            print(f"\nERROR: {args.base} requires authentication.")
            print("Please run: huggingface-cli login")
            print("Or use an open model like: --base distilgpt2")
            exit(1)
        raise

    # Configure LoRA for DistilGPT2 architecture
    peft_cfg = LoraConfig(
        r=16, 
        lora_alpha=32, 
        target_modules=["c_attn", "c_proj", "c_fc"],  # DistilGPT2 layer names
        lora_dropout=0.05, 
        bias="none", 
        task_type="CAUSAL_LM"
    )
    print(f"Applying LoRA to target modules: {peft_cfg.target_modules}")
    model = get_peft_model(model, peft_cfg)

    training_args = TrainingArguments(
        output_dir=args.output,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=8,
        learning_rate=2e-4,
        num_train_epochs=args.epochs,
        fp16=True,
        logging_steps=10,
        save_strategy="epoch",
    )

    # Tokenize the dataset
    def tokenize_function(examples):
        return tokenizer(examples["text"], truncation=True, padding=False, max_length=512)
    
    print("Tokenizing dataset...")
    tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=dataset.column_names)
    
    # Data collator for language modeling
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,  # We're doing causal language modeling, not masked
    )
    
    trainer = Trainer(
        model=model, 
        args=training_args, 
        train_dataset=tokenized_dataset,
        data_collator=data_collator
    )
    
    print("Starting training...")
    trainer.train()

    model.save_pretrained(args.output)
    tokenizer.save_pretrained(args.output)

    print(f"LoRA adapter saved to {args.output}")

if __name__ == "__main__":
    main()
