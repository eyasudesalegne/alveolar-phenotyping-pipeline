from __future__ import annotations

import numpy as np
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
from skimage.filters import threshold_otsu
from skimage.measure import label
from skimage.segmentation import watershed


def _remove_small_binary_objects(mask: np.ndarray, min_size: int) -> np.ndarray:
    lab = label(mask)
    counts = np.bincount(lab.ravel())
    keep = counts >= min_size
    keep[0] = False
    return keep[lab]


def segment_nuclei(channel: np.ndarray, min_size: int = 25) -> np.ndarray:
    x = np.asarray(channel, dtype=float)
    if not np.isfinite(x).all():
        raise ValueError("Segmentation input contains non-finite values")
    if float(x.max() - x.min()) < 1e-8:
        return np.zeros_like(x, dtype=np.int32)
    thr = threshold_otsu(x)
    mask = x > max(thr, 0.12)
    mask = _remove_small_binary_objects(mask, min_size=min_size)
    mask = ndi.binary_fill_holes(mask)
    distance = ndi.distance_transform_edt(mask)
    coords = peak_local_max(distance, min_distance=5, labels=mask, exclude_border=False)
    markers = np.zeros_like(mask, dtype=np.int32)
    for i, (r, c) in enumerate(coords, start=1):
        markers[r, c] = i
    if markers.max() == 0:
        return label(mask).astype(np.int32)
    labels = watershed(-distance, markers=markers, mask=mask)
    return labels.astype(np.int32)


def expand_cells(nuclei_labels: np.ndarray, distance: int = 7) -> np.ndarray:
    """Approximate cell regions by nearest-label expansion around segmented nuclei."""
    if nuclei_labels.max() == 0:
        return nuclei_labels.copy()
    bg = nuclei_labels == 0
    dist, indices = ndi.distance_transform_edt(bg, return_indices=True)
    nearest = nuclei_labels[tuple(indices)]
    cells = nearest.copy()
    cells[dist > distance] = 0
    return cells.astype(np.int32)
