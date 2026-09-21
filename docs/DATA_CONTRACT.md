# Data contract

The pipeline is designed around image-level metadata plus one multichannel image per field of view.

## Minimum metadata columns

| Column | Meaning |
|---|---|
| `image_id` | Unique image/FOV identifier |
| `path` | Path to image array/file |
| `phenotype` | Experimental state/label when available |
| `batch` | Experimental batch identifier |
| `plate` | Plate identifier |
| `well` | Well identifier |
| `replicate` | Technical/biological replicate index |

The synthetic generator writes three-channel NumPy arrays `(C,H,W)` for deterministic validation. In a real deployment, an adapter should map microscopy formats (e.g. TIFF/OME-TIFF) to the same internal channel-first representation while preserving acquisition metadata.

## Experimental hierarchy

Image-level random splits are intentionally avoided as a default because they can leak plate/batch structure. The demonstration holds out an entire batch. For real screening data, the split unit should be chosen from the experimental design: donor, biological replicate, plate, batch, or treatment series.
