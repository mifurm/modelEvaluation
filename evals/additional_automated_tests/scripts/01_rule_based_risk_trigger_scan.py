"""01 - Rule-based risk trigger scan.

This script scans the use-case description for pre-defined risk signals and
writes a machine-readable summary used for human legal review.
"""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
INPUT_PATH = ROOT / "configs/01_use_case_description.txt"
OUTPUT_PATH = ROOT / "outputs/01_risk_trigger_scan.json"

use_case_text = INPUT_PATH.read_text(encoding="utf-8")

triggers = {
    "biometric_identification": [r"\bbiometric\b", r"facial recognition"],
    "critical_infrastructure": [r"energy grid", r"transport control"],
    "employment_or_hr_decisions": [r"hiring", r"employee scoring"],
    "law_enforcement_context": [r"law enforcement", r"police investigation"],
}

scan = {
    key: any(re.search(pattern, use_case_text, flags=re.IGNORECASE) for pattern in patterns)
    for key, patterns in triggers.items()
}

record = {
    "risk_signals_detected": scan,
    "detected_count": sum(1 for value in scan.values() if value),
    "next_step": "human_legal_classification_required",
}

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.write_text(json.dumps(record, indent=2), encoding="utf-8")
print(f"Wrote {OUTPUT_PATH}")
