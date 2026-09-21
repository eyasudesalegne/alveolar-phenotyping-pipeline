from __future__ import annotations

import numpy as np
from scipy.spatial import distance_matrix
from skimage.measure import regionprops


def spatial_features(labels: np.ndarray) -> dict[str, float]:
    props = regionprops(labels)
    centroids = np.asarray([p.centroid for p in props], dtype=float)
    if len(centroids) < 2:
        return {"nn_distance_mean": float("nan"), "nn_distance_cv": float("nan")}
    d = distance_matrix(centroids, centroids)
    np.fill_diagonal(d, np.inf)
    nn = d.min(axis=1)
    return {
        "nn_distance_mean": float(np.mean(nn)),
        "nn_distance_cv": float(np.std(nn) / max(np.mean(nn), 1e-8)),
    }
