# 08. Artifact Integrity Hashing

## Description
Generates SHA-256 hashes for critical evaluation artifacts to strengthen traceability and detect tampering between runs.

## Code Sample
```python
import hashlib
import json
from pathlib import Path

artifacts = [
    "data/05_quality_eval.jsonl",
    "outputs/04_safety_results.json",
    "outputs/05_quality_results.json",
]

def sha256(path: str) -> str:
    data = Path(path).read_bytes()
    return hashlib.sha256(data).hexdigest()

manifest = {path: sha256(path) for path in artifacts if Path(path).exists()}
Path("outputs/08_artifact_hash_manifest.json").write_text(
    json.dumps(manifest, indent=2),
    encoding="utf-8",
)

print("Wrote outputs/08_artifact_hash_manifest.json")
```
