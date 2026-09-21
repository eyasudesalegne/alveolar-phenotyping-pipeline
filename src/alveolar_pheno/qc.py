from __future__ import annotations

import numpy as np
from scipy.ndimage import gaussian_filter


def focus_score(channel: np.ndarray) -> float:
    """Variance of high-frequency residual; larger usually means sharper."""
    residual = channel.astype(float) - gaussian_filter(channel.astype(float), sigma=1.5)
    return float(np.var(residual))


def illumination_cv(channel: np.ndarray) -> float:
    low = gaussian_filter(channel.astype(float), sigma=14)
    mean = float(np.mean(low))
    return float(np.std(low) / max(mean, 1e-8))


def saturation_fraction(image: np.ndarray, threshold: float = 0.985) -> float:
    return float(np.mean(image >= threshold))


def foreground_fraction(nuclear_channel: np.ndarray, threshold: float = 0.18) -> float:
    return float(np.mean(nuclear_channel > threshold))


def compute_qc(image: np.ndarray, thresholds: dict[str, float] | None = None) -> dict[str, float | bool | str]:
    if image.ndim != 3 or image.shape[0] < 3:
        raise ValueError("Expected image shaped (channels, height, width) with >=3 channels")
    t = {
        "min_focus": 0.00055,
        "max_saturation": 0.035,
        "max_illumination_cv": 0.38,
        "min_foreground_fraction": 0.01,
        "max_foreground_fraction": 0.45,
    }
    if thresholds:
        t.update(thresholds)
    focus = focus_score(image[0])
    saturation = saturation_fraction(image)
    illum = illumination_cv(image[1])
    fg = foreground_fraction(image[0])
    failures = []
    if focus < t["min_focus"]: failures.append("low_focus")
    if saturation > t["max_saturation"]: failures.append("saturation")
    if illum > t["max_illumination_cv"]: failures.append("illumination_nonuniformity")
    if fg < t["min_foreground_fraction"]: failures.append("low_foreground")
    if fg > t["max_foreground_fraction"]: failures.append("high_foreground")
    return {
        "qc_focus": focus,
        "qc_saturation_fraction": saturation,
        "qc_illumination_cv": illum,
        "qc_foreground_fraction": fg,
        "qc_pass": len(failures) == 0,
        "qc_failure_reasons": ";".join(failures),
    }
