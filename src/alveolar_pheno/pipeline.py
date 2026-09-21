from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import yaml

from .evaluation import bootstrap_macro_f1, evaluate
from .features import aggregate_image_features, extract_single_cell_features
from .modeling import fit_interpretable_model, rank_features
from .qc import compute_qc
from .segmentation import expand_cells, segment_nuclei
from .spatial import spatial_features
from .synthetic import SyntheticConfig, generate_dataset


def load_config(path: str | Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def phenotype_metadata(metadata: pd.DataFrame, qc_thresholds: dict | None = None) -> pd.DataFrame:
    records = []
    for row in metadata.to_dict(orient="records"):
        image = np.load(row["path"])
        qc = compute_qc(image, qc_thresholds)
        nuclei = segment_nuclei(image[0])
        cells = expand_cells(nuclei)
        cell_df = extract_single_cell_features(image, nuclei, cells)
        agg = aggregate_image_features(cell_df)
        spatial = spatial_features(nuclei)
        records.append({**row, **qc, **agg, **spatial})
    return pd.DataFrame.from_records(records)


def run_synthetic_demo(config_path: str | Path, output_root: str | Path) -> dict:
    config = load_config(config_path)
    output_root = Path(output_root)
    data_dir = output_root / "data"
    result_dir = output_root / "results"
    data_dir.mkdir(parents=True, exist_ok=True)
    result_dir.mkdir(parents=True, exist_ok=True)

    scfg = SyntheticConfig(**config["synthetic"])
    metadata = generate_dataset(data_dir, scfg)
    features = phenotype_metadata(metadata, config.get("qc_thresholds"))
    features.to_csv(result_dir / "image_features.csv", index=False)

    # QC failures remain in the audit table, but are excluded from model fitting.
    analysis = features[features["qc_pass"]].copy()
    test_batch = config["validation"]["held_out_batch"]
    train = analysis[analysis["batch"] != test_batch].copy()
    test = analysis[analysis["batch"] == test_batch].copy()
    if train.empty or test.empty:
        raise ValueError("Held-out batch split produced empty train or test partition")

    bundle = fit_interpretable_model(train)
    joblib.dump(bundle, result_dir / "model.joblib")
    metrics = evaluate(bundle, test)
    metrics.update(bootstrap_macro_f1(bundle, test, n_boot=int(config["validation"]["bootstrap_replicates"])))
    metrics.update({
        "held_out_batch": test_batch,
        "n_total": int(len(features)),
        "n_qc_pass": int(features["qc_pass"].sum()),
        "n_qc_fail": int((~features["qc_pass"]).sum()),
        "synthetic_only": True,
    })
    ranking = rank_features(bundle)
    ranking.to_csv(result_dir / "feature_ranking.csv", index=False)
    with open(result_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    # Simple batch summary for auditability.
    batch_summary = features.groupby(["batch", "phenotype"], as_index=False).agg(
        n_images=("image_id", "count"),
        qc_pass_rate=("qc_pass", "mean"),
        median_cell_count=("cell_count", "median"),
    )
    batch_summary.to_csv(result_dir / "batch_summary.csv", index=False)
    return metrics
