# Validation strategy

This repository distinguishes **software validation**, **technical image-analysis validation**, and **biological validation**.

## Implemented now

- deterministic synthetic dataset generation;
- explicit injected acquisition defects for QC checks;
- unit tests for QC, segmentation, feature extraction and modelling;
- end-to-end integration test;
- held-out-batch evaluation;
- bootstrap uncertainty interval for macro-F1;
- versioned configuration and machine-readable results;
- CI across Python 3.10, 3.11 and 3.12.

## Required before biological claims

Real screening data would require at minimum: marker-specific assay definition, segmentation review by domain experts, predefined experimental controls, replicate-aware statistical analysis, batch-effect assessment, biological validation of candidate signatures, and evaluation on independent experiments. If patient/donor material is involved, donor-level separation and appropriate ethics/data-governance procedures are required.

Synthetic accuracy must never be interpreted as expected performance on real alveolar epithelial images.
