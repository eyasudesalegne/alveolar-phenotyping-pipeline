from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


NON_FEATURES = {
    "image_id", "path", "phenotype", "batch", "plate", "well", "replicate",
    "qc_pass", "qc_failure_reasons", "qc_injected", "synthetic",
}


@dataclass
class ModelBundle:
    pipeline: Pipeline
    features: list[str]
    classes: list[str]


def select_features(df: pd.DataFrame) -> list[str]:
    features = []
    for c in df.columns:
        if c in NON_FEATURES or c.startswith("qc_"):
            continue
        if pd.api.types.is_numeric_dtype(df[c]):
            features.append(c)
    if not features:
        raise ValueError("No numeric phenotype features available")
    return features


def fit_interpretable_model(train: pd.DataFrame) -> ModelBundle:
    features = select_features(train)
    model = Pipeline([
        ("impute", SimpleImputer(strategy="median")),
        ("scale", StandardScaler()),
        ("clf", LogisticRegression(max_iter=2500, C=0.8, random_state=17)),
    ])
    model.fit(train[features], train["phenotype"])
    return ModelBundle(model, features, list(model.named_steps["clf"].classes_))


def rank_features(bundle: ModelBundle) -> pd.DataFrame:
    coef = np.asarray(bundle.pipeline.named_steps["clf"].coef_, dtype=float)
    importance = np.mean(np.abs(coef), axis=0)
    signs = np.sign(coef)
    sign_consistency = np.abs(np.mean(signs, axis=0))
    return pd.DataFrame({
        "feature": bundle.features,
        "mean_abs_standardized_coefficient": importance,
        "coefficient_sign_consistency": sign_consistency,
    }).sort_values("mean_abs_standardized_coefficient", ascending=False, ignore_index=True)
