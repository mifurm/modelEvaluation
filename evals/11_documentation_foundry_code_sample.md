# 11. Documentation and Technical File Creation - Foundry Code Sample

## Automation status
Partially automatable.

Code can assemble evidence and draft technical documentation, but accountable owners must review and sign the final compliance file.

```python
import json
from pathlib import Path

artifacts = {
    "risk_classification": "outputs/01_risk_classification_record.json",
    "safety_results": "outputs/04_safety_results.json",
    "quality_results": "outputs/05_quality_results.json",
    "lineage": "outputs/08_lineage_record.json",
}

lines = [
    "# AI Technical File (Draft)",
    "",
    "## Included Artifacts",
]

for name, path in artifacts.items():
    exists = Path(path).exists()
    lines.append(f"- {name}: {path} ({'present' if exists else 'missing'})")

Path("outputs").mkdir(exist_ok=True)
Path("outputs/11_technical_file_draft.md").write_text("\n".join(lines), encoding="utf-8")

print("Draft written to outputs/11_technical_file_draft.md")
```

## Required non-code action
Compliance, legal, and product owners must validate completeness and approve the final package.

## Additional automatable approach
### Documentation completeness checker

```python
from pathlib import Path

required_sections = [
    "Risk classification",
    "Safety evaluation outcomes",
    "Quality and robustness outcomes",
    "Bias and FRIA summary",
    "Human oversight design",
    "Post-deployment monitoring plan",
]

doc_path = Path("outputs/11_technical_file_draft.md")
text = doc_path.read_text(encoding="utf-8")

missing = [section for section in required_sections if section not in text]
if missing:
    raise SystemExit(f"Documentation incomplete. Missing sections: {missing}")

print("Documentation completeness passed")
```

