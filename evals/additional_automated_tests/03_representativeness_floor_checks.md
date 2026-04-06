# 03. Representativeness Floor Checks

## Description
Validates that protected or important segments have enough samples in the evaluation dataset. Prevents weak statistical conclusions from underrepresented groups.

## Code Sample
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
