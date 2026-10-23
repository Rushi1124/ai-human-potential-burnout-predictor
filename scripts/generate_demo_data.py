"""Generate a synthetic dataset for demonstration only; not real burnout data."""
from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "data" / "synthetic_demo_data.csv"
rng = np.random.default_rng(42)
n = 3500
df = pd.DataFrame({
    "sleep_hours": rng.uniform(3, 10, n),
    "workload_hours": rng.uniform(1, 14, n),
    "stress": rng.integers(1, 11, n),
    "motivation": rng.integers(1, 11, n),
    "focus": rng.integers(1, 11, n),
    "work_life_balance": rng.integers(1, 11, n),
    "exercise_days": rng.integers(0, 8, n),
})
score = (
    (8 - df["sleep_hours"]).clip(lower=0) * 8
    + df["workload_hours"] * 3
    + df["stress"] * 5
    - df["motivation"] * 2
    - df["focus"] * 1.5
    - df["work_life_balance"] * 3
    - df["exercise_days"] * 1.5
    + rng.normal(0, 8, n)
)
df["synthetic_demo_label"] = (score > 55).astype(int)
OUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUT, index=False)
print(f"Wrote {len(df)} synthetic rows to {OUT}")
print("Warning: these labels are artificial and are not real burnout outcomes.")
