"""02 - Control-to-metric coverage gate.

Verifies that mandatory compliance controls are represented in objective
configuration files.
"""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OBJECTIVES_PATH = ROOT / "configs/02_eval_objectives.json"
OVERSIGHT_PATH = ROOT / "configs/09_human_oversight_policy.json"

required_controls = {
    "harmful_content_detection",
    "hallucination_control",
    "fairness_disparity_tracking",
    "human_review_escalation",
}

objectives = json.loads(OBJECTIVES_PATH.read_text(encoding="utf-8"))
oversight_policy = json.loads(OVERSIGHT_PATH.read_text(encoding="utf-8"))

implemented = set()
if "safety" in objectives:
    implemented.add("harmful_content_detection")

if "quality" in objectives and "groundedness.min_score" in objectives["quality"].get("thresholds", {}):
    implemented.add("hallucination_control")

if "fairness" in objectives:
    implemented.add("fairness_disparity_tracking")

if oversight_policy.get("escalation_sla_hours"):
    implemented.add("human_review_escalation")

missing = sorted(required_controls - implemented)
if missing:
    raise SystemExit(f"Objective coverage failed. Missing controls: {missing}")

print("Objective coverage passed")
