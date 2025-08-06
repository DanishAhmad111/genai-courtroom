"""Download Indian legal dataset from HuggingFace and convert to JSONL format that the
fine_tune_judge.py training script expects.

Each record in the output JSONL will look like:
{
  "messages": [
    {"role": "system", "content": "You are an Indian High-Court judge..."},
    {"role": "user", "content": "<CASE FACTS>"},
    {"role": "assistant", "content": "<GROUND-TRUTH JUDGMENT SUMMARY>"}
  ]
}

Run:
    python prepare_dataset.py --out judge_dataset.jsonl --limit 2000
"""
import argparse
import json
from datasets import load_dataset

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="judge_dataset.jsonl", help="Output JSONL path")
    parser.add_argument("--limit", type=int, default=None, help="Max records to export")
    args = parser.parse_args()

    ds = load_dataset("ninadn/indian-legal", split="train")  # open dataset

    system_prompt = "You are an Indian High-Court judge specialising in constitutional and criminal law. Provide well-reasoned, concise verdicts citing precedents where possible."

    count = 0
    skipped = 0
    with open(args.out, "w", encoding="utf-8") as fout:
        for ex in ds:
            # Heuristic: try several possible column names for facts/judgment
            # dynamic search
            lower_map = {k.lower(): k for k in ex.keys()}
            facts_key = next((k for l,k in lower_map.items() if any(tok in l for tok in ["fact", "case", "text", "content"])), None)
            judge_key = next((k for l,k in lower_map.items() if any(tok in l for tok in ["judgement", "judgment", "decision", "verdict", "summary", "result", "label"])), None)
            facts = ex.get(facts_key) if facts_key else None
            judgment = ex.get(judge_key) if judge_key else None
            if not facts or not judgment:
                skipped += 1
                continue
            record = {
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": facts.strip()},
                    {"role": "assistant", "content": judgment.strip()}
                ]
            }
            fout.write(json.dumps(record, ensure_ascii=False) + "\n")
            count += 1
            if args.limit and count >= args.limit:
                break
    print(f"Wrote {count} records to {args.out}. Skipped {skipped} records without both fields.")

if __name__ == "__main__":
    main()
