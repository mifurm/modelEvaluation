"""12 - Conformity checklist validator.

Ensures all required pre-deployment conformity controls are set to true.
"""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CHECKLIST_PATH = ROOT / "configs/12_conformity_checklist.json"

checklist = json.loads(CHECKLIST_PATH.read_text(encoding="utf-8"))
required_true = [
    "risk_classification_signed",
    "safety_gate_passed",
    "quality_gate_passed",
    "fairness_review_completed",
    "human_oversight_operational",
    "monitoring_pipeline_enabled",
]

missing_or_false = [key for key in required_true if not checklist.get(key, False)]
if missing_or_false:
    raise SystemExit(f"Conformity gate failed: {missing_or_false}")

print("Checklist validation passed. Ready for formal human sign-off.")
