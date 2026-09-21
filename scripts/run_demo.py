from pathlib import Path
from alveolar_pheno.pipeline import run_synthetic_demo

if __name__ == "__main__":
    root = Path("work/synthetic_demo")
    metrics = run_synthetic_demo("configs/default.yaml", root)
    print(metrics)
