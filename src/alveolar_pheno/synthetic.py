from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter
from skimage.draw import ellipse
from skimage.util import random_noise


PHENOTYPES = ("control", "injury", "senescent", "recovery")


@dataclass(frozen=True)
class SyntheticConfig:
    n_batches: int = 4
    images_per_class_per_batch: int = 6
    height: int = 192
    width: int = 192
    seed: int = 20260921


def _cell_params(phenotype: str) -> dict[str, float]:
    # Deliberately separated but overlapping synthetic phenotypes.
    params = {
        "control": dict(n_cells=24, r_mean=7.6, elong=1.18, marker=0.45, texture=0.12),
        "injury": dict(n_cells=21, r_mean=8.2, elong=1.30, marker=0.54, texture=0.16),
        "senescent": dict(n_cells=18, r_mean=9.1, elong=1.24, marker=0.62, texture=0.18),
        "recovery": dict(n_cells=22, r_mean=7.9, elong=1.21, marker=0.49, texture=0.13),
    }
    return params[phenotype]


def _render_image(rng: np.random.Generator, phenotype: str, batch: int, shape: tuple[int, int]) -> np.ndarray:
    h, w = shape
    p = _cell_params(phenotype)
    # Three channels: nuclei, cytoplasm-like signal, phenotype marker.
    img = np.zeros((3, h, w), dtype=np.float32)
    n_cells = max(5, int(rng.normal(p["n_cells"], 2.5)))
    batch_gain = 1.0 + 0.05 * (batch - 1.5)
    batch_bias = 0.015 * batch

    for _ in range(n_cells):
        cy = int(rng.integers(16, h - 16))
        cx = int(rng.integers(16, w - 16))
        r0 = max(4.0, rng.normal(p["r_mean"], 1.2))
        elong = max(1.0, rng.normal(p["elong"], 0.12))
        rr_n, cc_n = ellipse(cy, cx, r0, max(3.0, r0 / elong), shape=(h, w))
        rr_c, cc_c = ellipse(cy, cx, r0 * 1.65, max(5.0, r0 * 1.65 / elong), shape=(h, w))

        nuc_int = np.clip(rng.normal(0.74, 0.08), 0.35, 1.0)
        cyto_int = np.clip(rng.normal(0.32 + 0.04 * (p["r_mean"] - 7), 0.05), 0.1, 0.8)
        marker_int = np.clip(rng.normal(p["marker"], 0.08), 0.05, 1.0)
        img[0, rr_n, cc_n] += nuc_int
        img[1, rr_c, cc_c] += cyto_int
        img[2, rr_c, cc_c] += marker_int

    # Smooth optics + low frequency illumination field + phenotype-dependent texture.
    yy, xx = np.mgrid[:h, :w]
    field = 1 + 0.06 * np.sin(2 * np.pi * xx / w + batch * 0.4) + 0.04 * np.cos(2 * np.pi * yy / h)
    img = gaussian_filter(img, sigma=(0, 1.0, 1.0))
    texture = gaussian_filter(rng.normal(0, p["texture"], size=(h, w)), sigma=2.2)
    img[2] += 0.06 * texture
    img = img * field[None, :, :] * batch_gain + batch_bias
    img = random_noise(img, mode="gaussian", var=0.0018, rng=rng, clip=True)
    return np.asarray(img, dtype=np.float32)


def generate_dataset(output_dir: str | Path, cfg: SyntheticConfig = SyntheticConfig()) -> pd.DataFrame:
    """Generate deterministic synthetic high-content-like microscopy data and metadata.

    Returns image-level metadata. Data are synthetic technical validation only.
    """
    output_dir = Path(output_dir)
    image_dir = output_dir / "images"
    image_dir.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(cfg.seed)
    records: list[dict[str, object]] = []
    image_id = 0
    for batch in range(cfg.n_batches):
        for phenotype in PHENOTYPES:
            for rep in range(cfg.images_per_class_per_batch):
                img = _render_image(rng, phenotype, batch, (cfg.height, cfg.width))
                # Deterministic minority of synthetic acquisition defects for QC testing.
                qc_injected = "none"
                if rep == 0 and batch == 1 and phenotype == "injury":
                    img = gaussian_filter(img, sigma=(0, 3.2, 3.2)); qc_injected = "blur"
                elif rep == 1 and batch == 2 and phenotype == "senescent":
                    img = np.clip(img * 1.8, 0, 1); qc_injected = "saturation"
                path = image_dir / f"img_{image_id:04d}.npy"
                np.save(path, img)
                records.append({
                    "image_id": f"img_{image_id:04d}",
                    "path": str(path),
                    "phenotype": phenotype,
                    "batch": f"batch_{batch+1}",
                    "plate": f"plate_{batch+1}",
                    "well": f"{chr(65 + (image_id % 8))}{1 + (image_id % 12):02d}",
                    "replicate": rep,
                    "qc_injected": qc_injected,
                    "synthetic": True,
                })
                image_id += 1
    df = pd.DataFrame.from_records(records)
    df.to_csv(output_dir / "metadata.csv", index=False)
    return df
