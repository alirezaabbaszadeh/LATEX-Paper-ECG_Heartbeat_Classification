# Figures for BioMedical Engineering OnLine Submission

Run `./paper-journal-B/scripts/generate_figures.py` with the bundled virtual environment (`.venv/bin/python`) to reproduce every plot from `Research_Runs/final_run_Main_Model_20250824_154136/raw_predictions.npz`. Each figure is exported as both a publication-ready 300 dpi PNG and a vector PDF.

- `fig-roc-curves.{png,pdf}` — ROC curves per AAMI class on the held-out test set; caption uses `fig:roc-curves`.
- `fig-precision-recall-curves.{png,pdf}` — Precision–recall curves per class, highlighting imbalance effects; caption uses `fig:pr-curves`.
- `fig-confusion-matrix.{png,pdf}` — Confusion matrix on the held-out test set; caption uses `fig:confusion-matrix`.
