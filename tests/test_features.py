import numpy as np
from alveolar_pheno.features import extract_single_cell_features, aggregate_image_features
from alveolar_pheno.segmentation import expand_cells


def test_feature_extraction_has_expected_fields():
    labels = np.zeros((64, 64), dtype=int)
    labels[10:20, 10:20] = 1
    labels[35:48, 35:48] = 2
    cells = expand_cells(labels, distance=4)
    image = np.zeros((3, 64, 64), dtype=float)
    image[0][labels > 0] = 0.8
    image[1][cells > 0] = 0.4
    image[2][cells > 0] = 0.6
    f = extract_single_cell_features(image, labels, cells)
    agg = aggregate_image_features(f)
    assert len(f) == 2
    assert "marker_to_cytoplasm_ratio" in f.columns
    assert agg["cell_count"] == 2
    assert "nucleus_area_mean" in agg
