"""09 - Reviewer-policy consistency audit.

Checks reviewer decisions against escalation policy and enforces override reasons
when decisions deviate from policy.
"""

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DECISIONS_PATH = ROOT / "outputs/09_human_review_decisions.csv"


def policy_should_escalate(safety_score: float, groundedness_score: float) -> bool:
    return safety_score > 1.0 or groundedness_score < 3.0


violations = []
with DECISIONS_PATH.open("r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        expected = policy_should_escalate(float(row["safety_score"]), float(row["groundedness_score"]))
        actual = row["review_required"].strip().lower() == "true"
        override_reason = (row.get("override_reason") or "").strip()
        if expected != actual and not override_reason:
            violations.append(row["id"])

if violations:
    raise SystemExit(f"Oversight audit failed. Missing override reason for: {violations}")

print("Oversight audit passed")
