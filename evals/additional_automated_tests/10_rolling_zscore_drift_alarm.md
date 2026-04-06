# 10. Rolling Z-Score Drift Alarm

## Description
Uses rolling mean and standard deviation to detect anomalous metric shifts over time. Suitable for scheduled post-deployment monitoring.

## Code Sample
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
