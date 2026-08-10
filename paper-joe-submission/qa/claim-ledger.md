# Evidence-bounded claim ledger

This ledger is the authoritative editorial source for quantitative statements in `paper-joe-submission/`. Values are copied from existing repository outputs; editorial revision does not imply a new experiment.

## Evaluation protocol

- Source database: MIT-BIH Arrhythmia Database.
- AAMI-oriented model-development subset: 45 non-paced records.
- Development cohort: 38 records.
- Strictly held-out cohort: 7 records/subjects (106, 207, 208, 220, 228, 231, 233).
- Held-out test beats: 15,573.
- Five-fold development accuracy reported for the proposed model: 0.44 ± 0.16.
- The same subject-level partition is used across tuning, cross-validation, and final evaluation.

## Model-level held-out metrics

| Model | Accuracy (95% CI) | Macro-F1 (95% CI) | Weighted-F1 (95% CI) |
|---|---:|---:|---:|
| Proposed Conformer | 0.60 [0.59, 0.60] | 0.26 [0.26, 0.27] | 0.68 [0.67, 0.68] |
| Attention-only baseline | 0.27 [0.26, 0.28] | 0.15 [0.14, 0.15] | 0.38 [0.37, 0.39] |
| CNN-LSTM baseline | 0.18 [0.17, 0.18] | 0.15 [0.15, 0.16] | 0.29 [0.28, 0.29] |
| Feature-engineered baseline | 0.14 [0.13, 0.14] | 0.07 [0.07, 0.07] | 0.23 [0.22, 0.23] |

Safe comparison wording: the proposed model produced the highest accuracy, macro-F1, and weighted-F1 **among the four architectures evaluated under the same held-out split**.

Absolute differences versus the best competing neural baseline (attention-only): +0.33 accuracy, +0.11 macro-F1, +0.30 weighted-F1. These are percentage-point/absolute metric differences, not relative-percentage improvements.

## Proposed-model class metrics

| AAMI class | Support | Precision | Recall | F1 | AUC | AUC 95% CI |
|---|---:|---:|---:|---:|---:|---:|
| Normal (N) | 12,061 | 0.95 | 0.60 | 0.74 | 0.9009 | [0.89, 0.91] |
| SVEB (S) | 214 | 0.00 | 0.00 | 0.00 | 0.6681 | [0.65, 0.68] |
| VEB (V) | 2,913 | 0.48 | 0.70 | 0.57 | 0.8431 | [0.84, 0.85] |
| Fusion (F) | 383 | 0.01 | 0.01 | 0.01 | 0.3140 | [0.29, 0.34] |
| Unknown (Q) | 2 | 0.00 | 0.00 | 0.00 | 0.5837 | [0.46, 0.71] |

Interpretation boundary: Normal and VEB are the only classes with meaningful F1 in the held-out report. The Q class has only two test examples and must not support substantive class-level inference.

## Error structure and threshold sweeps

Existing supplementary analysis reports:

- 151/214 SVEB beats (71%) predicted as Normal.
- 51/214 SVEB beats (24%) predicted as VEB.
- 343/383 Fusion beats (90%) predicted as VEB.
- Best post-hoc one-vs-rest SVEB F1: 0.06 at threshold 0.09 (precision 0.03, recall 0.90).
- Best post-hoc one-vs-rest Fusion F1: 0.05 at threshold 0.00 (precision 0.02, recall 1.00).

Safe interpretation: threshold adjustment alone did not recover balanced minority-class performance; large recall gains were accompanied by very low precision.

Do not call the threshold sweep a validation-set threshold optimization: it was performed on stored held-out test probabilities as a post-hoc diagnostic.

## Calibration analysis

Archived temperature-scaling analysis uses 15 bins and stored test probabilities.

Before scaling:

| Class | ECE | Brier |
|---|---:|---:|
| Normal | 0.417 | 0.289 |
| SVEB | 0.098 | 0.039 |
| VEB | 0.089 | 0.121 |
| Fusion | 0.103 | 0.049 |
| Unknown | 0.153 | 0.051 |

Global temperature T* = 1.050. Baseline NLL = 1.047989; calibrated NLL = 1.047731.

Critical scope note: the temperature parameter was fitted on the held-out test cohort itself. These numbers are **internal post-hoc calibration diagnostics**, not independent calibration validation and not evidence of external generalisation.

## Comparator AUCs

These values may be used only when a class-specific architecture comparison is genuinely necessary.

| Model | N | S | V | F | Q |
|---|---:|---:|---:|---:|---:|
| Proposed Conformer | 0.90 | 0.67 | 0.84 | 0.31 | 0.59 |
| Attention-only | 0.76 | 0.76 | 0.69 | 0.40 | 0.80 |
| CNN-LSTM | 0.73 | 0.73 | 0.86 | 0.47 | 0.03 |
| Feature-engineered | 0.69 | 0.65 | 0.72 | 0.41 | 0.85 |

Important: the proposed model is **not** uniformly best in class-specific AUC. For example, CNN-LSTM has higher VEB AUC (0.86 vs 0.84), and several baselines have higher Fusion/Q AUC. Therefore claims of across-the-board superiority are prohibited.

## Allowed claim formulations

- `outperformed all baselines evaluated in this study on accuracy, macro-F1, and weighted-F1`
- `under the subject-separated protocol used here`
- `showed strong discrimination for normal and ventricular ectopic beats relative to the minority classes`
- `exposed a persistent rare-class failure mode that post-hoc threshold adjustment did not resolve`
- `provides a reproducible benchmark and failure-analysis framework`
- `supports further research on clinician-supervised prioritization or decision support`
- `the observed gain is consistent with a benefit from combining local convolutional processing and global/temporal attention within the controlled comparisons used here`

## Claims requiring qualification

- `robust`: qualify with the exact evaluation dimension; do not use as a general property.
- `generalizable`: current data do not establish external generalisability; use `requires external validation`.
- `lightweight`: retain only if parameter count/compute evidence is explicitly documented and verified. Otherwise omit or use a neutral architecture description.
- `clinical utility`: current retrospective benchmark does not establish clinical utility. Use `clinical relevance`, `decision-support implications`, or `future clinician-in-the-loop evaluation` as appropriate.
- `calibrated`: temperature scaling was fit on the test set, so call it an `internal post-hoc calibration analysis`.

## Prohibited claim formulations

- `state of the art` / `state-of-the-art`
- `clinically ready`
- `cardiologist-level performance`
- `superior to existing methods` without limiting the claim to the evaluated baselines
- `generalizes to real-world populations`
- `suitable for autonomous diagnosis`
- `safe for deployment`
- `clinically acceptable minority-class performance`

## Source map

- Model-level metrics and bootstrap intervals: `paper-journal-A/tables/test_metrics.tex`.
- Proposed class report and point AUCs: `Research_Runs/final_run_Main_Model_20250824_154136/classification_report.txt`.
- Threshold sweeps and confusion-count interpretation: `paper-journal-A/supplementary/main.tex`.
- Internal calibration diagnostics: `Research_Runs/final_run_Main_Model_20250824_154136/temperature_scaling_results.txt`.
- Evaluation protocol and split: `paper-journal-A/src/sections/methods.tex` and supplementary methods.

Any manuscript number not represented here must be re-verified against an archived source before publication.