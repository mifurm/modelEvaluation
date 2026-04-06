# 9. Human Oversight Design and Validation - Foundry Code Sample

## Automation status
Not fully automatable.

Reason: Oversight design is an organizational control (roles, authority, escalation, auditability). Code can enforce routing rules, but humans must perform reviews.

```python
import csv
from pathlib import Path

Path("outputs").mkdir(exist_ok=True)

def requires_human_review(safety_score: float, groundedness_score: float) -> bool:
    return safety_score > 1.0 or groundedness_score < 3.0

sample_outputs = [
    {"id": "r1", "safety_score": 0.2, "groundedness_score": 4.2},
    {"id": "r2", "safety_score": 1.4, "groundedness_score": 2.8},
]

with open("outputs/09_human_review_queue.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "review_required", "reason"])
    writer.writeheader()
    for row in sample_outputs:
        flagged = requires_human_review(row["safety_score"], row["groundedness_score"])
        writer.writerow(
            {
                "id": row["id"],
                "review_required": flagged,
                "reason": "policy_gate" if flagged else "none",
            }
        )
```

## Required non-code action
Define reviewer SLA, escalation path, override authority, and training requirements.

## Additional automatable approach
### Reviewer-policy consistency audit

```python
import csv

def policy_should_escalate(safety_score: float, groundedness_score: float) -> bool:
    return safety_score > 1.0 or groundedness_score < 3.0

violations = []
with open("outputs/09_human_review_decisions.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        expected = policy_should_escalate(
            float(row["safety_score"]),
            float(row["groundedness_score"]),
        )
        actual = row["review_required"].lower() == "true"
        if expected != actual and not row.get("override_reason"):
            violations.append(row["id"])

if violations:
    raise SystemExit(f"Oversight audit failed. Missing override reason for: {violations}")

print("Oversight audit passed")
```

