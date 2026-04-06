"""07 - Counterfactual pair disparity test.

Calculates absolute score gaps between paired prompts and enforces max delta.
"""

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[3]
SCORES_PATH = ROOT / "outputs/07_counterfactual_scores.json"

rows = json.loads(SCORES_PATH.read_text(encoding="utf-8"))
df = pd.DataFrame(rows)

required_columns = {"pair_id", "score_a", "score_b"}
if not required_columns.issubset(df.columns):
    raise SystemExit(f"Missing columns in {SCORES_PATH}: {sorted(required_columns - set(df.columns))}")

df["delta"] = (df["score_a"] - df["score_b"]).abs()
max_delta = float(df["delta"].max())

print(df[["pair_id", "delta"]])
if max_delta > 0.3:
    raise SystemExit(f"Counterfactual fairness failed: max delta {max_delta:.3f}")

print("Counterfactual disparity test passed")
