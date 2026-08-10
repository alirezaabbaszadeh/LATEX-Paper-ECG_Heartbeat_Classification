# Figures for Journal of Electrocardiology submission

The submission manuscript uses only the study figures that pre-date the present AI-assisted editorial rewrite. The current Journal of Electrocardiology / Elsevier guidance does not permit generative-AI or AI-assisted tools to create or alter submitted artwork; consequently, AI-assisted visual concepts developed during editorial revision are not retained as submission figures.

## Main retained assets

| Filename | Description | Archived source |
| --- | --- | --- |
| `confusion_matrix.png` | Held-out test confusion matrix for the CNN--Conformer main model. | `Research_Runs/final_run_Main_Model_20250824_154136/confusion_matrix.png` |
| `roc_curves.png` | One-vs-rest ROC curves for AAMI classes. | `Research_Runs/final_run_Main_Model_20250824_154136/roc_curves.png` |
| `precision_recall_curves.png` | Precision--recall curves for AAMI classes. | `Research_Runs/final_run_Main_Model_20250824_154136/precision_recall_curves.png` |

The captions and manuscript callouts have been rewritten to make class imbalance, class support, and rare-rhythm failure more prominent without altering the underlying artwork.

## Regeneration

If the authors regenerate these plots from the archived study predictions without generative-AI assistance, use the existing study scripts and preserve the exact underlying predictions and metrics. The repository's original export path should be changed to the independent revision folder:

```bash
python scripts/export_figures.py --run Research_Runs/final_run_Main_Model_20250824_154136 \
  --out paper-joe-submission/figures --dpi 300
```

Any newly created or altered artwork should be checked against the journal's current artwork and generative-AI policies before submission.
