# 1. AI System Risk Identification and Classification - Foundry Code Sample

## Automation status
This evaluation cannot be completed by Microsoft Foundry code alone.

Reason: AI Act risk classification (GPAI, GPAI with systemic risk, high-risk) requires legal and policy interpretation of intended use, deployment context, and sector-specific obligations.

## What code can do
Code can collect evidence used by reviewers and store the final human decision.

```python
import json
from datetime import datetime, UTC

# Replace with real metadata pulled from your model registry and app config.
evidence = {
    "model_name": "gpt-4o-mini",
    "provider": "Microsoft Foundry",
    "intended_use": "Customer support assistant for financial products",
    "deployment_regions": ["eu-west", "westeurope"],
    "uses_biometrics": False,
    "automated_decisions_with_legal_effect": False,
}

# Human assessor must set this after legal review.
classification_record = {
    "timestamp_utc": datetime.now(UTC).isoformat(),
    "ai_act_classification": "REQUIRES_HUMAN_ASSESSMENT",
    "assessor": "compliance.team@company.com",
    "evidence": evidence,
    "notes": "Pending legal interpretation and FRIA scope check.",
}

with open("outputs/01_risk_classification_record.json", "w", encoding="utf-8") as f:
    json.dump(classification_record, f, indent=2)
```

## Required non-code action
Compliance/legal owners must perform and sign off the classification decision.

## Additional automatable approach
### Rule-based risk trigger scan before legal review

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

