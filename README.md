# Alveolar Phenotyping Pipeline

**Reproducible technical framework for high-content image QC, segmentation, quantitative morphology, spatial profiling and interpretable phenotyping of alveolar epithelial screening data.**

> **Status:** engineering-grade proof-of-concept under active development. The repository currently ships a deterministic **synthetic technical-validation dataset only**. It contains no ICGEB, patient, donor or biological experimental data, and synthetic model performance is **not** presented as an IPF biological result.

## Why this repository exists

High-content microscopy can quantify cellular responses at scale, but useful phenotypic screening requires more than a classifier. A defensible workflow needs acquisition QC, traceable metadata, segmentation review, single-cell measurements, population-level summaries, batch-aware validation, uncertainty estimates and interpretable outputs.

This repository implements that end-to-end computational skeleton in advance of access to the proposed host-lab data. It is designed to be adapted to alveolar epithelial injury, senescence, regeneration and treatment-response experiments once the exact assay, channels, controls and biological readouts are defined with the host laboratory.

## Pipeline architecture

```text
multichannel microscopy + metadata
              |
              v
    acquisition / image QC
              |
              v
 nuclear segmentation -> approximate cell regions
              |
              v
 single-cell morphology + intensity + ratios
              |
              +----> spatial organization
              |
              v
 image / well-level phenotype profiles
              |
              v
 batch-aware train/test separation
              |
              v
 interpretable multinomial model
              |
              v
 metrics + bootstrap CI + ranked features + audit tables
```

## What is implemented

- deterministic multi-batch synthetic high-content-like data generator with control, injury, senescent and recovery states;
- explicit synthetic blur and saturation defects to test QC behavior;
- quantitative focus, saturation, illumination-uniformity and foreground QC;
- nuclear watershed segmentation and approximate cell expansion;
- single-cell morphology and intensity features;
- phenotype-marker/cytoplasm and nucleus/cell ratios;
- nearest-neighbour spatial organization features;
- per-image robust population summaries (mean, SD, median, IQR);
- QC-gated analysis while retaining failed images in the audit record;
- whole-batch holdout rather than random image splitting;
- transparent multinomial logistic regression with standardized coefficients;
- accuracy, balanced accuracy, macro-F1, log loss and multiclass Brier score;
- bootstrap 95% interval for macro-F1;
- ranked feature table with coefficient sign-consistency diagnostic;
- machine-readable CSV/JSON outputs and serialized model artifact;
- unit + integration tests and GitHub Actions CI on Python 3.10–3.12.

## Quick start

```bash
git clone https://github.com/eyasudesalegne/alveolar-phenotyping-pipeline.git
cd alveolar-phenotyping-pipeline
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
alveolar-pheno synthetic-demo --config configs/default.yaml --output work/synthetic_demo
```

The demo writes:

```text
work/synthetic_demo/
├── data/
│   ├── metadata.csv
│   └── images/*.npy
└── results/
    ├── image_features.csv
    ├── batch_summary.csv
    ├── feature_ranking.csv
    ├── metrics.json
    └── model.joblib
```

## Synthetic demonstration design

The current generator creates four deliberately overlapping technical phenotypes across four synthetic batches. It varies cell count, nuclear size, elongation, marker intensity, texture and acquisition gain/bias. The objective is **not** to simulate IPF biology faithfully. It is to stress the software contracts and make failures visible before the pipeline is connected to laboratory data.

The default validation holds out `batch_4` entirely. This prevents the easiest form of batch leakage and reflects the intended principle for real screening data: split at the level of the independent experimental unit, not at the image level.

## Scientific interpretation policy

The repository separates three levels of evidence:

1. **Software correctness** — tested functions, deterministic runs, configuration, CI.
2. **Technical image-analysis validity** — QC behavior, segmentation plausibility, feature extraction and batch-aware evaluation.
3. **Biological validity** — requires real experiments, host-lab controls, replicate-aware statistics and biological confirmation; **not established by this repository**.

Any preliminary-results document generated from this repository should therefore use wording such as **“synthetic technical validation”** rather than “preliminary IPF results.”

## Adapting to real host-lab data

The pipeline is intentionally modular. The synthetic `.npy` loader can be replaced by an OME-TIFF/TIFF adapter; watershed segmentation can be replaced by Cellpose/StarDist; assay-specific markers can be added to the feature table; and learned image embeddings can be compared against morphology profiles while retaining transparent baselines and batch-aware validation.

See [`docs/ROADMAP.md`](docs/ROADMAP.md), [`docs/DATA_CONTRACT.md`](docs/DATA_CONTRACT.md), [`docs/METHODS.md`](docs/METHODS.md) and [`docs/VALIDATION.md`](docs/VALIDATION.md).

## Reproducibility

The synthetic generator uses an explicit seed. Experimental parameters and QC thresholds live in `configs/default.yaml`. Outputs are written as plain CSV/JSON in addition to the model binary. Tests cover the main components and the full synthetic execution path.

## Scope and limitations

This is research software, not a clinical decision-support system. It does not diagnose IPF, predict treatment response in patients, or establish biological biomarkers. See [`docs/ETHICS_AND_LIMITATIONS.md`](docs/ETHICS_AND_LIMITATIONS.md).

## Author

**Eyasu Desalegne Beyene**  
PhD Researcher, Biomedical Engineering  
Istanbul University-Cerrahpaşa

## License

MIT License.

## Current deterministic synthetic benchmark

The checked-in benchmark is intentionally **not perfectly separable**. Four synthetic phenotypes overlap and one entire batch is held out. With the default configuration, the current deterministic run generates 96 fields of view; 90 pass the predefined QC gate and 24 held-out `batch_4` images are evaluated. The baseline obtains balanced accuracy **0.792** and macro-F1 **0.787** with bootstrap 95% interval **0.617–0.922**. These numbers exist to regression-test the analytical workflow, not to estimate performance on real IPF data.

Top model coefficients in this run include nuclear eccentricity summaries, marker-to-cytoplasm intensity ratios, marker-intensity summaries and solidity/perimeter descriptors. This is expected from how the synthetic generator is parameterized and must not be interpreted as a biological discovery.

Machine-readable benchmark outputs are committed under [`results/synthetic_demo/`](results/synthetic_demo/).
