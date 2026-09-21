from __future__ import annotations

import numpy as np
import pandas as pd
from skimage.measure import regionprops_table


def extract_single_cell_features(image: np.ndarray, nuclei: np.ndarray, cells: np.ndarray) -> pd.DataFrame:
    if nuclei.shape != image.shape[1:] or cells.shape != nuclei.shape:
        raise ValueError("Image and label dimensions are inconsistent")
    if nuclei.max() == 0:
        return pd.DataFrame()

    nuc = regionprops_table(
        nuclei,
        intensity_image=image[0],
        properties=("label", "area", "eccentricity", "solidity", "perimeter", "mean_intensity"),
    )
    df = pd.DataFrame(nuc).rename(columns={
        "area": "nucleus_area",
        "eccentricity": "nucleus_eccentricity",
        "solidity": "nucleus_solidity",
        "perimeter": "nucleus_perimeter",
        "mean_intensity": "nucleus_mean_intensity",
    })

    # Cells share labels with nuclei after expansion. Extract cytoplasm and marker intensity.
    cyto = pd.DataFrame(regionprops_table(cells, intensity_image=image[1], properties=("label", "area", "mean_intensity")))
    cyto = cyto.rename(columns={"area":"cell_area", "mean_intensity":"cytoplasm_mean_intensity"})
    marker = pd.DataFrame(regionprops_table(cells, intensity_image=image[2], properties=("label", "mean_intensity")))
    marker = marker.rename(columns={"mean_intensity":"marker_mean_intensity"})
    df = df.merge(cyto, on="label", how="left").merge(marker, on="label", how="left")
    df["nucleus_to_cell_area_ratio"] = df["nucleus_area"] / df["cell_area"].clip(lower=1)
    df["marker_to_cytoplasm_ratio"] = df["marker_mean_intensity"] / df["cytoplasm_mean_intensity"].clip(lower=1e-6)
    return df


def aggregate_image_features(cells: pd.DataFrame) -> dict[str, float]:
    if cells.empty:
        return {"cell_count": 0.0}
    out: dict[str, float] = {"cell_count": float(len(cells))}
    numeric = [c for c in cells.columns if c != "label" and pd.api.types.is_numeric_dtype(cells[c])]
    for col in numeric:
        values = cells[col].replace([np.inf, -np.inf], np.nan).dropna().to_numpy(dtype=float)
        if values.size == 0:
            continue
        out[f"{col}_mean"] = float(np.mean(values))
        out[f"{col}_std"] = float(np.std(values, ddof=0))
        out[f"{col}_median"] = float(np.median(values))
        out[f"{col}_iqr"] = float(np.percentile(values, 75) - np.percentile(values, 25))
    return out
