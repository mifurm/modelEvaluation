# 8. Model Traceability and Logging - Foundry Code Sample

## Automation status
Automatable.

```python
import json
from datetime import datetime, UTC
from pathlib import Path

import mlflow

Path("outputs").mkdir(exist_ok=True)

run_metadata = {
    "timestamp_utc": datetime.now(UTC).isoformat(),
    "model_deployment": "gpt-4o-mini-prod",
    "dataset_path": "data/05_quality_eval.jsonl",
    "evaluation_output": "outputs/05_quality_results.json",
    "code_version": "git:REPLACE_WITH_COMMIT_SHA",
}

with mlflow.start_run(run_name="eval-traceability") as run:
    mlflow.log_params(run_metadata)
    mlflow.log_artifact("outputs/05_quality_results.json")

    lineage = {
        "mlflow_run_id": run.info.run_id,
        **run_metadata,
    }

    with open("outputs/08_lineage_record.json", "w", encoding="utf-8") as f:
        json.dump(lineage, f, indent=2)

print("Traceability record written to outputs/08_lineage_record.json")
```

## Additional automatable approach
### Artifact integrity hashing

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

