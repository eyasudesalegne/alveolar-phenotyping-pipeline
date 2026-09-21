# Roadmap toward real high-content screening data

1. **Microscope/assay adapter** — ingest OME-TIFF/TIFF exports and map channels using acquisition metadata.
2. **Host-lab QC calibration** — define focus, saturation, illumination and cell-count thresholds from control wells.
3. **Segmentation benchmarking** — compare baseline watershed against Cellpose/StarDist or host-lab preferred models with manual review.
4. **Assay-specific phenotypes** — add proliferation, viability, senescence-associated and lineage-marker features according to the final experimental panel.
5. **Plate normalization** — robust control-based normalization and explicit plate/batch-effect diagnostics.
6. **Biological replicate validation** — predefine held-out replicate/batch testing and bootstrap confidence intervals.
7. **Learned representations** — compare transparent morphology profiles with pretrained/task-specific embeddings without replacing interpretability checks.
8. **Signature stability** — quantify cross-batch feature-direction stability and replicate consistency.
9. **Reporting** — generate per-plate QC reports, phenotype maps, model cards and provenance manifests.
10. **External/independent experiment** — validate prioritized signatures in a separately acquired experiment before biological generalization.
