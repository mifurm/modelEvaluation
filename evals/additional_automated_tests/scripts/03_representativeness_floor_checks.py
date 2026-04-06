"""03 - Representativeness floor checks.

Counts samples by sensitive_group and enforces a minimum per-group floor.
Override the floor with MIN_SAMPLES_PER_GROUP if needed.
"""

import json
import os
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DATASET_PATH = ROOT / "data/03_eval_dataset.jsonl"
MIN_REQUIRED = int(os.getenv("MIN_SAMPLES_PER_GROUP", "2"))

records = []
for line in DATASET_PATH.read_text(encoding="utf-8").splitlines():
    if line.strip():
        records.append(json.loads(line))

if not records:
    raise SystemExit(f"Dataset is empty: {DATASET_PATH}")

group_counts = Counter(row["sensitive_group"] for row in records)
violations = {group: count for group, count in group_counts.items() if count < MIN_REQUIRED}

print(f"Group counts: {dict(group_counts)}")
print(f"Minimum required per group: {MIN_REQUIRED}")

if violations:
    raise SystemExit(f"Dataset representativeness failed: {violations}")

print("Representativeness check passed")
