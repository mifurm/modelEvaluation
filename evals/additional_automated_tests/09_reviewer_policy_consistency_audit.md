# 09. Reviewer-Policy Consistency Audit

## Description
Checks whether human escalation decisions match policy rules, and requires an override reason when reviewers diverge from automated routing logic.

## Code Sample
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
