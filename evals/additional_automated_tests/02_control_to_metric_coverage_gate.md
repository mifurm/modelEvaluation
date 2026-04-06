# 02. Control-to-Metric Coverage Gate

## Description
Checks whether required compliance controls are actually mapped to measurable objectives and thresholds. Fails if any required control is missing.

## Code Sample
```python
import json

required_controls = [
    "harmful_content_detection",
    "hallucination_control",
    "fairness_disparity_tracking",
    "human_review_escalation",
]

with open("configs/02_eval_objectives.json", "r", encoding="utf-8") as f:
    objectives = json.load(f)

implemented = set()
if "safety" in objectives:
    implemented.add("harmful_content_detection")
if "quality" in objectives and "groundedness.min_score" in objectives["quality"]["thresholds"]:
    implemented.add("hallucination_control")
if "fairness" in objectives:
    implemented.add("fairness_disparity_tracking")

with open("configs/09_human_oversight_policy.json", "r", encoding="utf-8") as f:
    oversight_policy = json.load(f)
if oversight_policy.get("escalation_sla_hours"):
    implemented.add("human_review_escalation")

missing = [c for c in required_controls if c not in implemented]
if missing:
    raise SystemExit(f"Objective coverage failed. Missing controls: {missing}")

print("Objective coverage passed")
```
