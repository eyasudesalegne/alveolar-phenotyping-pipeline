import yaml
from alveolar_pheno.pipeline import run_synthetic_demo


def test_end_to_end_demo(tmp_path):
    cfg={
        "synthetic":{"n_batches":2,"images_per_class_per_batch":2,"height":96,"width":96,"seed":11},
        "qc_thresholds":{"min_focus":0.00005,"max_saturation":0.2,"max_illumination_cv":1.0,"min_foreground_fraction":0.001,"max_foreground_fraction":0.8},
        "validation":{"held_out_batch":"batch_2","bootstrap_replicates":20},
    }
    p=tmp_path/"config.yaml"
    p.write_text(yaml.safe_dump(cfg), encoding="utf-8")
    metrics=run_synthetic_demo(p,tmp_path/"run")
    assert metrics["synthetic_only"] is True
    assert (tmp_path/"run/results/metrics.json").exists()
    assert (tmp_path/"run/results/feature_ranking.csv").exists()
