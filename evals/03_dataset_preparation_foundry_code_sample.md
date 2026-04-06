# 3. Dataset Preparation (Ground Truth and Synthetic Data) - Foundry Code Sample

## Automation status
Mostly automatable.

```python
import json
import random
from pathlib import Path

random.seed(42)

records = [
    {
        "query": "Can I transfer money internationally?",
        "context": "International transfer is available for verified users.",
        "ground_truth": "Yes, verified users can transfer money internationally.",
        "sensitive_group": "group_a",
    },
    {
        "query": "How do I close my account?",
        "context": "Account closure requires identity verification.",
        "ground_truth": "You can close your account after identity verification.",
        "sensitive_group": "group_b",
    },
]

# Simple synthetic augmentation example.
synthetic = []
for row in records:
    synthetic.append({
        **row,
        "query": row["query"].replace("I", "a customer"),
    })

dataset = records + synthetic
random.shuffle(dataset)

Path("data").mkdir(exist_ok=True)
with open("data/03_eval_dataset.jsonl", "w", encoding="utf-8") as f:
    for row in dataset:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

print(f"Wrote {len(dataset)} records to data/03_eval_dataset.jsonl")
```

## Notes
Add representativeness checks (language, geography, protected groups, edge cases) before using the dataset for compliance evidence.

## Additional automatable approach
### Representativeness floor checks by segment

```python
import json
from collections import Counter

records = []
with open("data/03_eval_dataset.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        records.append(json.loads(line))

group_counts = Counter(r["sensitive_group"] for r in records)
min_required = 50

violations = {group: count for group, count in group_counts.items() if count < min_required}

print("Group counts:", dict(group_counts))
if violations:
    raise SystemExit(f"Dataset representativeness failed: {violations}")
```

