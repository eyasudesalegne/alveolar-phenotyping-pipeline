import numpy as np
from alveolar_pheno.segmentation import segment_nuclei, expand_cells


def test_segmentation_returns_labeled_objects():
    x = np.zeros((96, 96), dtype=float)
    x[20:31, 20:31] = 1
    x[60:73, 58:70] = 0.9
    labels = segment_nuclei(x, min_size=10)
    cells = expand_cells(labels, distance=5)
    assert labels.max() >= 2
    assert cells.shape == labels.shape
    assert cells.max() == labels.max()
