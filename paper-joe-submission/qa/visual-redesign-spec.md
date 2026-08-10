# Manual visual redesign specification

Date: 2026-08-10
Target: *Journal of Electrocardiology*
Status: author-side redesign specification; **not submission artwork**.

The current Elsevier guidance for this journal does not permit generative-AI or AI-assisted tools to create or alter submitted artwork, including graphical abstracts. Accordingly, the present revision retains only the pre-existing study plots in the submission manuscript. The following specification records how an author can manually recreate improved artwork without relying on AI-assisted image generation or alteration.

## Figure 1 — Study design / evaluation workflow

Purpose: make the evaluation boundary visually undeniable.

Recommended manual layout:

1. MIT-BIH source and paced-record exclusions.
2. Fixed record-level split into 38 development records and 7 held-out records.
3. Development branch: beat extraction -> 32-scale Morlet scalograms -> three-beat sequences -> Hyperband -> five-fold CV -> final fitting.
4. Held-out branch: 15,573 beats -> one final evaluation.
5. A clearly separated post-hoc branch for threshold sweeps and calibration analysis.

Use solid arrows for model-development/evaluation flow and dashed arrows for post-hoc diagnostics. Do not describe threshold or temperature scaling as independent validation.

## Figure 2 — Model-level comparison

Purpose: communicate the controlled baseline result in one glance.

Manually plot the four evaluated models using three grouped metrics only:

| Model | Accuracy | Macro-F1 | Weighted-F1 |
|---|---:|---:|---:|
| CNN--Conformer | 0.60 | 0.26 | 0.68 |
| Attention-only | 0.27 | 0.15 | 0.38 |
| CNN--LSTM | 0.18 | 0.15 | 0.29 |
| Feature-engineered | 0.14 | 0.07 | 0.23 |

Do not imply that the proposed model is best on every class-specific AUC. Confidence intervals belong in Table 2 unless the author manually adds the exact archived intervals to the plot.

## Figure 3 — Class-specific performance

Purpose: expose the gap between aggregate performance and rare-rhythm recognition.

Recommended manual display: paired horizontal markers/bars for F1 and one-vs-rest AUC, with class support written beside each class.

| Class | Support | F1 | AUC |
|---|---:|---:|---:|
| N | 12,061 | 0.74 | 0.90 |
| S | 214 | 0.00 | 0.67 |
| V | 2,913 | 0.57 | 0.84 |
| F | 383 | 0.01 | 0.31 |
| Q | 2 | 0.00 | 0.59 |

The key visual message should be that SVEB can show moderate ranking AUC while still having realised F1=0.00 under the current decision rule and prevalence.

## Figure 4 — Rare-rhythm error structure

Purpose: make the clinically important failure mode concrete.

Show only the dominant error paths supported by archived counts:

- SVEB -> Normal: 151/214 (71%).
- SVEB -> VEB: 51/214 (24%).
- Fusion -> VEB: 343/383 (90%).

A small annotation can add the post-hoc threshold result:

- SVEB max F1 0.06 at threshold 0.09, precision 0.03, recall 0.90.
- Fusion max F1 0.05 at threshold 0.00, precision 0.02, recall 1.00.

The figure must state that these threshold sweeps are descriptive analyses of the held-out predictions, not independently validated operating points.

## Graphical abstract

A graphical abstract is optional. If the authors create one manually, use four blocks:

1. subject-separated benchmark;
2. Morlet + three-beat representation;
3. controlled architecture comparison;
4. two-sided result: stronger aggregate metrics **and** unresolved rare-rhythm failure.

Avoid phrases such as `triage-ready`, `clinically ready`, `state of the art`, or `lightweight` unless separately substantiated.

## Visual style

- Prefer vector PDF/EPS for diagrams and charts.
- Use consistent typography and class naming across all figures.
- Avoid 3D effects and decorative gradients.
- Use a colour-blind-safe palette chosen manually by the authors.
- Keep labels readable at the journal's final print/display size.
- Captions should state the interpretation, not merely identify the plot.
- Preserve exact values from `qa/claim-ledger.md`.
