# Table sources for the BioMedical Engineering OnLine submission

Each `.tex` table in this directory is paired with a CSV that records the raw numbers reported in the manuscript. The CSVs are the artifacts uploaded to BMC for reader reanalysis and serve as the authoritative source for regenerating the `.tex` tables.

## Main manuscript tables
- `main_overall_metrics.tex` / `overall_metrics.csv`: aggregate accuracy, macro- and weighted-averaged precision/recall/F1.
- `main_per_class_metrics.tex` / `classification_report.csv`: per-class precision, recall, F1, and support for the held-out test cohort.

## Supplementary tables
- `supp_kfold_accuracy.tex` / `kfold_accuracy.csv`: five-fold cross-validation loss and accuracy for the Conformer (\autoref{tab:supp-kfold-acc}).
- `auc_by_class.tex` / `auc_by_class.csv`: per-class AUROC values referenced in the supplementary text (\autoref{tab:auc-by-class}).

To regenerate the `.tex` tables from the CSVs, a script such as the one used for the figures could be extended to read these files and emit LaTeX tabular blocks. The values here come directly from the logged run artifacts in `Research_Runs/final_run_Main_Model_20250824_154136/`.
