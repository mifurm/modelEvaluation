"""08 - Artifact integrity hashing.

Produces a SHA-256 manifest for key artifacts.
"""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = ROOT / "outputs/08_artifact_hash_manifest.json"
artifacts = [
    ROOT / "data/05_quality_eval.jsonl",
    ROOT / "outputs/04_safety_results.json",
    ROOT / "outputs/05_quality_results.json",
]

missing = [str(path.relative_to(ROOT)) for path in artifacts if not path.exists()]
if missing:
    raise SystemExit(f"Cannot compute hash manifest. Missing artifacts: {missing}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


manifest = {str(path.relative_to(ROOT)): sha256(path) for path in artifacts}
OUTPUT_PATH.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
print(f"Wrote {OUTPUT_PATH}")
