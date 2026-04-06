# 11. Documentation Completeness Checker

## Description
Scans the generated technical file draft for mandatory compliance sections and fails if required sections are missing.

## Code Sample
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
