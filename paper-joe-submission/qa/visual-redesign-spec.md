# Visual redesign specification and evidence map

Date: 2026-08-10
Target: *Journal of Electrocardiology*
Status: implemented as editable TikZ figures in the working submission draft.

Current Elsevier journal policy permits AI-assisted explanatory images and reproducible data visualisations when the assistance is transparently disclosed and the scientific content is faithfully derived from underlying evidence. The working manuscript therefore includes four AI-assisted TikZ figures with tool disclosure in Methods and captions. A general-purpose generative-AI graphical abstract is not included.

## Figure 1 — Study design / evaluation workflow

Purpose: make the evaluation boundary visually explicit.

Implemented content:

1. MIT-BIH source and paced-record exclusions.
2. Fixed record-level split into 38 development records and 7 held-out records.
3. Development branch: beat extraction -> 32-scale Morlet scalograms -> three-beat sequences -> Hyperband -> five-fold CV -> final fitting.
4. Held-out branch: 15,573 beats -> final evaluation.
5. Separate post-hoc branch for threshold sweeps and calibration analysis.

Solid arrows represent model-development/evaluation flow and the post-hoc branch is visually differentiated. The figure does not describe threshold or temperature scaling as independent validation.

Source: `figures/pipeline_diagram.tex`.

## Figure 2 — Model-level comparison

Purpose: communicate the controlled baseline result in one glance.

The plotted values are:

| Model | Accuracy | Macro-F1 | Weighted-F1 |
|---|---:|---:|---:|
| CNN--Conformer | 0.60 | 0.26 | 0.68 |
| Attention-only | 0.27 | 0.15 | 0.38 |
| CNN--LSTM | 0.18 | 0.15 | 0.29 |
| Feature-engineered | 0.14 | 0.07 | 0.23 |

The figure deliberately excludes class-specific AUCs so that it does not imply uniform class-wise superiority. Confidence intervals remain in Table 2.

Source: `figures/model_comparison.tex`.

## Figure 3 — Class-specific performance

Purpose: expose the gap between aggregate performance and rare-rhythm recognition.

| Class | Support | F1 | AUC |
|---|---:|---:|---:|
| N | 12,061 | 0.74 | 0.90 |
| S | 214 | 0.00 | 0.67 |
| V | 2,913 | 0.57 | 0.84 |
| F | 383 | 0.01 | 0.31 |
| Q | 2 | 0.00 | 0.59 |

The central visual message is that SVEB can show moderate ranking AUC while realised F1 remains 0.00 under the current decision rule and prevalence.

Source: `figures/class_performance.tex`.

## Figure 4 — Rare-rhythm error structure

Purpose: make the clinically important failure mode concrete.

Displayed error paths:

- SVEB -> Normal: 151/214 (71%).
- SVEB -> VEB: 51/214 (24%).
- Fusion -> VEB: 343/383 (90%).

Displayed post-hoc threshold diagnostics:

- SVEB max F1 0.06 at threshold 0.09, precision 0.03, recall 0.90.
- Fusion max F1 0.05 at threshold 0.00, precision 0.02, recall 1.00.

The figure explicitly treats these as descriptive held-out diagnostics rather than independently validated operating points.

Source: `figures/error_structure.tex`.

## Archived-prediction diagnostic plots

The confusion matrix, ROC, and precision--recall plots are retained as Supplementary Figures S1--S3. For the production build they were regenerated deterministically from the archived held-out prediction arrays because the original Git LFS image objects were unavailable. The predictions, confusion counts, curve metrics, and scientific interpretation were not changed.

## Graphical abstract

No graphical abstract created with a general-purpose generative-AI tool is included. If the authors create one before submission, it should use a dedicated scientific/professional illustration workflow compatible with the journal's current policy.

## Visual style

- Editable vector TikZ for the new explanatory/data-summary figures.
- Consistent class names and typography.
- No 3D effects or decorative gradients.
- Captions state the scientific takeaway and disclose AI assistance.
- Exact numerical labels are traceable to `qa/claim-ledger.md`.
