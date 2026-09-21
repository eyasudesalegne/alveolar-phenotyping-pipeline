from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, log_loss


def multiclass_brier(y_true: np.ndarray, prob: np.ndarray, classes: list[str]) -> float:
    mapping = {c: i for i, c in enumerate(classes)}
    onehot = np.zeros_like(prob, dtype=float)
    for r, y in enumerate(y_true):
        onehot[r, mapping[y]] = 1.0
    return float(np.mean(np.sum((prob - onehot) ** 2, axis=1)))


def evaluate(bundle, df: pd.DataFrame) -> dict[str, float]:
    y = df["phenotype"].to_numpy()
    pred = bundle.pipeline.predict(df[bundle.features])
    prob = bundle.pipeline.predict_proba(df[bundle.features])
    return {
        "n": float(len(df)),
        "accuracy": float(accuracy_score(y, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(y, pred)),
        "macro_f1": float(f1_score(y, pred, average="macro")),
        "log_loss": float(log_loss(y, prob, labels=bundle.classes)),
        "multiclass_brier": multiclass_brier(y, prob, bundle.classes),
    }


def bootstrap_macro_f1(bundle, df: pd.DataFrame, n_boot: int = 300, seed: int = 41) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    y = df["phenotype"].to_numpy()
    pred = bundle.pipeline.predict(df[bundle.features])
    vals = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(df), size=len(df))
        # Some resamples can omit a class; macro F1 remains defined with zero_division=0.
        vals.append(f1_score(y[idx], pred[idx], average="macro", zero_division=0))
    lo, hi = np.percentile(vals, [2.5, 97.5])
    return {"macro_f1_bootstrap_mean": float(np.mean(vals)), "macro_f1_ci95_low": float(lo), "macro_f1_ci95_high": float(hi)}
