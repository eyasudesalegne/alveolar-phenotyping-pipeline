# Methods implemented in the proof-of-concept

## 1. Quality control

Each field of view receives quantitative QC measurements before modelling: focus score from the variance of a high-frequency residual, saturated-pixel fraction, low-frequency illumination coefficient of variation, and foreground fraction. QC failures remain in the audit table and are excluded from model fitting rather than silently discarded.

## 2. Nuclear and approximate cell segmentation

The baseline segmentation uses Otsu thresholding, morphological cleanup, distance transform, peak detection, and watershed separation. Approximate cell masks are obtained by constrained nearest-label expansion around nuclei. This is intentionally modular: Cellpose, StarDist, SAM-derived models, or laboratory-specific segmentation can replace the baseline without changing downstream contracts.

## 3. Single-cell measurements

The implementation extracts nuclear area, eccentricity, solidity, perimeter and nuclear intensity, plus approximate cell area, cytoplasmic intensity, phenotype-marker intensity, nucleus-to-cell area ratio and marker-to-cytoplasm ratio.

## 4. Population and spatial phenotypes

Single-cell features are summarized per image with mean, standard deviation, median and interquartile range. Cell count and nearest-neighbour spacing statistics capture population density and spatial organization.

## 5. Interpretable modelling

The baseline model is multinomial logistic regression after median imputation and z-score scaling. It is deliberately chosen for transparent standardized coefficients. Feature rankings use mean absolute standardized coefficient magnitude with a sign-consistency diagnostic.

## 6. Validation

The synthetic demonstration uses a batch-held-out split. Metrics include accuracy, balanced accuracy, macro-F1, multiclass log loss, multiclass Brier score, and a nonparametric bootstrap interval for macro-F1.

These choices are engineering defaults for technical validation, not a claim that they are optimal for a future ICGEB dataset.
