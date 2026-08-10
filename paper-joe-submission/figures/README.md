# Figures for Journal of Electrocardiology Submission

This folder stores the production-ready figures referenced throughout the manuscript and supplementary appendix. Each raster export is tagged with Elsevier-compliant metadata (\(\geq 300\)~dpi) and mirrored in the LaTeX sources via relative paths.

## Current assets

| Filename | Description | Source notebook/log |
| --- | --- | --- |
| `confusion_matrix.png` | Held-out test confusion matrix for the Conformer main model. | `Research_Runs/final_run_Main_Model_20250824_154136/confusion_matrix.png` |
| `roc_curves.png` | One-vs-rest ROC curves for AAMI classes (Conformer main model). | `Research_Runs/final_run_Main_Model_20250824_154136/roc_curves.png` |
| `precision_recall_curves.png` | Precision-recall curves for AAMI classes (Conformer main model). | `Research_Runs/final_run_Main_Model_20250824_154136/precision_recall_curves.png` |
| `pipeline_diagram.tex` | TikZ schematic of the end-to-end data and modelling pipeline. | Derived from `docs/figures/pipeline.mmd` | 

To regenerate the PNG diagnostics with updated DPI metadata, run:

```bash
python scripts/export_figures.py --run Research_Runs/final_run_Main_Model_20250824_154136 \
  --out paper-journal-A/figures --dpi 300
```

Ensure each figure has a paired caption in the manuscript or supplementary text and avoid mixing colourmaps between related plots.
