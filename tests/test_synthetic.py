import numpy as np
from alveolar_pheno.synthetic import SyntheticConfig, generate_dataset


def test_synthetic_generator_is_deterministic(tmp_path):
    cfg = SyntheticConfig(n_batches=1, images_per_class_per_batch=1, height=64, width=64, seed=7)
    a = generate_dataset(tmp_path / "a", cfg)
    b = generate_dataset(tmp_path / "b", cfg)
    assert list(a["phenotype"]) == list(b["phenotype"])
    assert np.allclose(np.load(a.iloc[0]["path"]), np.load(b.iloc[0]["path"]))
