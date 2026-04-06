# 10. Continuous Monitoring and Re-Evaluation - Foundry Code Sample

## Automation status
Automatable.

```python
import json
from pathlib import Path

Path("outputs").mkdir(exist_ok=True)

# This script is intended to run on a schedule (for example, nightly).
# 1. Run your Foundry evaluation job.
# 2. Compare current metrics to baseline.

baseline = {"safety": 0.8, "relevance": 3.8, "groundedness": 3.5}
current = {"safety": 1.1, "relevance": 3.6, "groundedness": 3.2}

drift_report = {
    "baseline": baseline,
    "current": current,
    "deltas": {k: current[k] - baseline[k] for k in baseline},
    "alerts": [],
}

if current["safety"] > 1.0:
    drift_report["alerts"].append("Safety regression")
if current["groundedness"] < 3.3:
    drift_report["alerts"].append("Groundedness below floor")

with open("outputs/10_monitoring_report.json", "w", encoding="utf-8") as f:
    json.dump(drift_report, f, indent=2)

if drift_report["alerts"]:
    raise SystemExit(f"Monitoring gate failed: {drift_report['alerts']}")
```

Run this script from a scheduler (GitHub Actions, Azure ML pipeline, or another orchestrator).

## Additional automatable approach
### Statistical drift alarm with rolling z-score

```python
import pandas as pd

history = pd.read_csv("outputs/10_metric_history.csv")

metric = "groundedness"
window = 14

history["rolling_mean"] = history[metric].rolling(window).mean()
history["rolling_std"] = history[metric].rolling(window).std(ddof=0)
history["zscore"] = (history[metric] - history["rolling_mean"]) / history["rolling_std"]

latest = history.iloc[-1]
print(latest[[metric, "rolling_mean", "zscore"]])

if abs(float(latest["zscore"])) > 3.0:
    raise SystemExit(f"Monitoring alert: {metric} anomaly detected")
```

