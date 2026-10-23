"""Illustrative evaluation only. Metrics measure reproduction of artificial labels."""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

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
y = (score > 55).astype(int)
X_train, X_test, y_train, y_test = train_test_split(
    df, y, test_size=0.2, random_state=42, stratify=y
)
model = RandomForestClassifier(
    n_estimators=120, min_samples_leaf=3,
    class_weight="balanced", random_state=42
)
model.fit(X_train, y_train)
pred = model.predict(X_test)
proba = model.predict_proba(X_test)[:, 1]
print("DEMO ONLY: metrics reflect artificial labels, not real burnout prediction.")
print(classification_report(y_test, pred, zero_division=0))
print("Confusion matrix:\n", confusion_matrix(y_test, pred))
print("ROC-AUC:", round(roc_auc_score(y_test, proba), 3))
