"""10 - Rolling z-score drift alarm.

Computes anomaly score for the latest metric point using rolling stats.
"""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
HISTORY_PATH = ROOT / "outputs/10_metric_history.csv"

metric = "groundedness"
window = 14

history = pd.read_csv(HISTORY_PATH)
if len(history) < window:
    raise SystemExit(f"Need at least {window} rows in {HISTORY_PATH}, found {len(history)}")

history["rolling_mean"] = history[metric].rolling(window).mean()
history["rolling_std"] = history[metric].rolling(window).std(ddof=0)
history["zscore"] = (history[metric] - history["rolling_mean"]) / history["rolling_std"]

latest = history.iloc[-1]
zscore = float(latest["zscore"])
if pd.isna(zscore):
    raise SystemExit("Latest z-score is NaN. Check metric history variability and window size.")

print(latest[[metric, "rolling_mean", "zscore"]])
if abs(zscore) > 3.0:
    raise SystemExit(f"Monitoring alert: {metric} anomaly detected")

print("Rolling z-score drift alarm passed")
