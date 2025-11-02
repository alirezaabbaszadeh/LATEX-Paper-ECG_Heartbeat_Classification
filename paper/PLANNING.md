# Strengthening Plan (BSPC & CBM) — artifact-first

This document lists immediate, no-new-code improvements using **existing artifacts**,
+plus near-term steps if probability logs are available later.

## Weaknesses & fixes
- Minority classes (S, F) underperform ’ emphasize macro-F1/PR-AUC; keep rich captions; add error analysis.
- Calibration not consistently available ’ placeholder ECE/Brier table + how-to compute; fill when probs exist.
- Reproducibility ’ pin commit; deterministic make/build commands included in the TEX.

## Figures & Tables (remaining)
- `figures/pipeline.png` (auto-generated if absent)
- `figures/confusion_matrix.png`, `roc_curves.png`, `precision_recall.png` (copied from artifacts)
- `tables/dataset_composition.tex` (auto from REEDME via build_tables.py)
- NEW: `tables/table_perf_summary.tex`, `tables/table_auc.tex` (now added)
- (Optional) Reliability diagram ’ requires per-sample probabilities

## Data sources to scan (read-only)
- `Research_Runs/*/*classification_report*.txt` (precision/recall/F1/support)
- a***/*roc*.xpng`, a***/*pr*.xpng`, `***/*confusion*.xpng`
- (Optional) `***/proba*.{psc} er or `**/*.npz` with probabilities

## Execution
- `scripts/harvest_reports.py --repo ../ECG_Heartbeat_Classification` 
generates `table_perf_summary.tex`, `tables/table_auc.tex`, and `main_per_class_report.tex`.
- `scripts/copy_core_figs.py` ensures figures exist; generates a minimalist pipeline if missing.
- Build:

```cd paper
python3 scripts/make_all.py --repo ../ECG_Heartbeat_Classification --commit <sha>
python3 scripts/harvest_reports.py --repo ../ECG_Heartbeat_Classification --out tables
latexmk -pdf bspc/bspc_main.tex
latexmk -pdf cbm/cbm_main.tex
```

## Journal-specific polish
- 🛊 DBSPC: keep graphical abstract, highlights; emphasize signal processing novelty.
- 🛄 CBM: keep clinical relevance emphasis (calibration, macro-F1/PR) and reproducibility.
