"""Placeholder evaluation runner. Implemented in Week 7."""
import json

with open("evaluation/test_set.jsonl", encoding="utf-8") as f:
    items = [json.loads(line) for line in f if line.strip()]
print(f"Loaded {len(items)} test questions.")
