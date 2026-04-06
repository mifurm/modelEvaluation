# 01. Rule-Based Risk Trigger Scan

## Description
Scans the use-case description for high-risk keywords and phrases before legal classification. This is a triage step that flags possible regulatory risk signals early.

## Code Sample
```python
import json
import re
from pathlib import Path

use_case_text = Path("configs/01_use_case_description.txt").read_text(encoding="utf-8")

triggers = {
    "biometric_identification": [r"\\bbiometric\\b", r"facial recognition"],
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
    "detected_count": sum(1 for v in scan.values() if v),
    "next_step": "human_legal_classification_required",
}

Path("outputs").mkdir(exist_ok=True)
Path("outputs/01_risk_trigger_scan.json").write_text(json.dumps(record, indent=2), encoding="utf-8")
```
