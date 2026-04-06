"""11 - Documentation completeness checker.

Validates that the required technical-file sections are present.
"""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DOC_PATH = ROOT / "outputs/11_technical_file_draft.md"

required_sections = [
    "Risk classification",
    "Safety evaluation outcomes",
    "Quality and robustness outcomes",
    "Bias and FRIA summary",
    "Human oversight design",
    "Post-deployment monitoring plan",
]

text = DOC_PATH.read_text(encoding="utf-8")
missing = [section for section in required_sections if section not in text]
if missing:
    raise SystemExit(f"Documentation incomplete. Missing sections: {missing}")

print("Documentation completeness passed")
