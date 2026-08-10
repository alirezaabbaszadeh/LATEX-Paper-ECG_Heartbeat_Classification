# Figures for Journal of Electrocardiology submission

The revised manuscript separates two kinds of visual evidence.

## AI-assisted explanatory/data-summary figures

The following editable TikZ figures were prepared with assistance from OpenAI ChatGPT (GPT-5.6 Sol). They contain no AI-generated research data: scientific content and plotted values are direct transcriptions of the archived study protocol and outputs recorded in `qa/claim-ledger.md`. Their use is disclosed in the Methods section, individual captions, and the manuscript AI declaration.

| Filename | Purpose |
| --- | --- |
| `pipeline_diagram.tex` | Subject-separated study workflow and post-hoc analysis boundary. |
| `model_comparison.tex` | Accuracy, macro-F1, and weighted-F1 across the four controlled models. |
| `class_performance.tex` | Class support, F1, and one-vs-rest AUC for the proposed model. |
| `error_structure.tex` | Dominant SVEB/Fusion error paths and threshold trade-offs. |

## Original study-generated diagnostic plots

These image files were generated from the archived study predictions before the present editorial rewrite and their image content has not been altered:

| Filename | Description | Archived source |
| --- | --- | --- |
| `confusion_matrix.png` | Held-out test confusion matrix for the CNN--Conformer main model. | `Research_Runs/final_run_Main_Model_20250824_154136/confusion_matrix.png` |
| `roc_curves.png` | One-vs-rest ROC curves for AAMI classes. | `Research_Runs/final_run_Main_Model_20250824_154136/roc_curves.png` |
| `precision_recall_curves.png` | Precision--recall curves for AAMI classes. | `Research_Runs/final_run_Main_Model_20250824_154136/precision_recall_curves.png` |

The original plots are retained as Supplementary Figures S1--S3, while the editable data-summary figures carry the main narrative in the article.

## Graphical abstract

No graphical abstract created with a general-purpose generative-AI tool is included. If a graphical abstract is added before submission, it should be produced with a journal-compatible dedicated scientific/professional illustration workflow and checked against the current Elsevier policy.

## Regeneration

The original diagnostic plots can be regenerated from the archived study predictions with the existing study scripts. Preserve the exact predictions and metrics and export into the independent revision folder:

```bash
python scripts/export_figures.py --run Research_Runs/final_run_Main_Model_20250824_154136 \
  --out paper-joe-submission/figures --dpi 300
```

All newly submitted artwork should be rechecked against the journal's current artwork and generative-AI policies at the time of submission.
