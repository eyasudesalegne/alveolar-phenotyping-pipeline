import numpy as np
from scipy.ndimage import gaussian_filter
from alveolar_pheno.qc import compute_qc


def test_qc_detects_blur_relative_to_sharp_image():
    img = np.zeros((3, 96, 96), dtype=float)
    img[0, 30:65, 30:65] = 1.0
    img[1:, 25:70, 25:70] = 0.4
    sharp = compute_qc(img, {"min_focus": 1e-4})
    blurred = compute_qc(gaussian_filter(img, sigma=(0, 5, 5)), {"min_focus": 1e-4})
    assert sharp["qc_focus"] > blurred["qc_focus"]
