import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

FEATURES = [
    "sleep_hours",
    "workload_hours",
    "stress",
    "motivation",
    "focus",
    "work_life_balance",
    "exercise_days",
]

def _train_demo_model():
    """Train a model on artificial examples. Not validated for real burnout prediction."""
    rng = np.random.default_rng(42)
    n = 3500
    data = pd.DataFrame({
        "sleep_hours": rng.uniform(3, 10, n),
        "workload_hours": rng.uniform(1, 14, n),
        "stress": rng.integers(1, 11, n),
        "motivation": rng.integers(1, 11, n),
        "focus": rng.integers(1, 11, n),
        "work_life_balance": rng.integers(1, 11, n),
        "exercise_days": rng.integers(0, 8, n),
    })
    score = (
        (8 - data["sleep_hours"]).clip(lower=0) * 8
        + data["workload_hours"] * 3
        + data["stress"] * 5
        - data["motivation"] * 2
        - data["focus"] * 1.5
        - data["work_life_balance"] * 3
        - data["exercise_days"] * 1.5
        + rng.normal(0, 8, n)
    )
    data["target"] = (score > 55).astype(int)
    model = RandomForestClassifier(
        n_estimators=120,
        min_samples_leaf=3,
        class_weight="balanced",
        random_state=42,
    )
    model.fit(data[FEATURES], data["target"])
    return model

_MODEL = None

def get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = _train_demo_model()
    return _MODEL

def get_demo_model_info():
    return {
        "type": "RandomForestClassifier",
        "training_data": "synthetic/artificial",
        "validated_for_burnout": False,
    }

def predict_risk(answers):
    model = get_model()
    row = pd.DataFrame([{key: answers[key] for key in FEATURES}])
    probabilities = model.predict_proba(row[FEATURES])[0]
    positive_index = list(model.classes_).index(1)
    probability = float(probabilities[positive_index])
    percent = round(probability * 100)

    if probability >= 0.65:
        category = "Higher demo score"
    elif probability >= 0.35:
        category = "Moderate demo score"
    else:
        category = "Lower demo score"

    # Transparent response indicators, not explanations of causal risk.
    indicators = {
        "Sleep shortfall": round(max(0, 8 - answers["sleep_hours"]), 1),
        "Workload": round(answers["workload_hours"], 1),
        "Stress": answers["stress"],
        "Motivation difficulty": 11 - answers["motivation"],
        "Focus difficulty": 11 - answers["focus"],
        "Balance difficulty": 11 - answers["work_life_balance"],
    }
    return {
        "risk_probability": probability,
        "risk_percent": percent,
        "category": category,
        "pattern_indicators": indicators,
    }
