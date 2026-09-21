# Preliminary technical results — synthetic validation only

## Purpose

This document records an executable technical proof-of-concept for the proposed high-content alveolar epithelial image-phenotyping workflow. It is intended to demonstrate computational preparedness before access to host-laboratory experiments. **No result in this document is derived from ICGEB, patient, donor or biological IPF data.**

## Dataset generated for software validation

The deterministic default configuration creates 96 multichannel synthetic microscopy-like fields of view across four batches and four deliberately overlapping technical states (`control`, `injury`, `senescent`, `recovery`). The generator varies cell number, nuclear size/elongation, phenotype-marker intensity, texture and batch-level gain/bias. It additionally injects selected blur and saturation defects so that QC rejection can be tested.

## Pipeline exercised

1. image-level focus, saturation, illumination and foreground QC;
2. nuclear thresholding, morphological cleanup and watershed separation;
3. approximate cell-region expansion;
4. single-cell morphology and intensity measurement;
5. image-level robust aggregation and nearest-neighbour spatial profiling;
6. exclusion of QC failures from model fitting while retaining them in the audit table;
7. whole-batch holdout validation;
8. interpretable multinomial logistic regression;
9. balanced accuracy, macro-F1, log loss and multiclass Brier score;
10. bootstrap uncertainty interval and coefficient-based feature ranking.

## Current deterministic benchmark

| Quantity | Result |
|---|---:|
| Total synthetic fields of view | 96 |
| QC pass | 90 |
| QC fail | 6 |
| Held-out test batch | `batch_4` |
| Held-out test fields | 24 |
| Accuracy | 0.792 |
| Balanced accuracy | 0.792 |
| Macro-F1 | 0.787 |
| Bootstrap macro-F1 mean | 0.777 |
| Bootstrap 95% CI | 0.617–0.922 |
| Multiclass log loss | 0.435 |
| Multiclass Brier score | 0.269 |

The benchmark is intentionally not tuned for perfect classification. Its role is to verify that the pipeline can process images, preserve metadata, gate technical failures, extract phenotypes and evaluate a model on a batch that was not used for training.

## Ranked technical features

The highest standardized model coefficients in the current synthetic run include nuclear eccentricity summaries, marker-to-cytoplasm ratios, marker-intensity summaries, nuclear solidity and perimeter descriptors. These rankings follow the synthetic generation rules and are **not biological candidate biomarkers**.

## What this establishes

The repository demonstrates a reproducible computational architecture that can be adapted to real high-content experiments once the host laboratory defines the exact channels, controls, markers and biological replicate structure.

## What this does not establish

It does not validate IPF biology, alveolar epithelial regeneration, treatment response, a biomarker, or any clinical endpoint. Biological interpretation requires real experimental data, host-lab assay controls, replicate-aware statistics and independent confirmation.
