# Journal of Electrocardiology — Human Narrative & Visual Clarity Pass

Date: 2026-08-10
Branch: `joe-editorial-rewrite-2026-08-10`
Target workspace: `paper-joe-submission/`

## Goal

Improve the revised Journal of Electrocardiology manuscript without changing the experimental evidence. The pass should make the prose sound more natural and authorial, make the scientific argument easier to follow, and make the four primary figures readable at journal scale.

## Non-negotiable evidence boundary

- No new experiments, model runs, metrics, or inferred numerical results.
- Every quantitative statement must remain traceable to `paper-joe-submission/qa/claim-ledger.md`.
- Comparative claims remain limited to the four architectures evaluated on the common held-out split.
- No SOTA, clinical-readiness, autonomous-diagnosis, deployment, or external-generalisation claims.
- Post-hoc threshold/calibration analyses remain explicitly descriptive rather than independently validated.

## Narrative design

### Abstract

Use a compact four-part arc: problem -> protocol -> two-sided result -> implication. Reduce report-like phrasing, avoid stacking multiple qualifiers in one sentence, and preserve the key numbers. The closing sentence should frame the work as a reproducible benchmark that identifies a rare-rhythm bottleneck.

### Introduction

Use a human scientific progression rather than a checklist of concepts:

1. Why patient-to-patient ECG variation and class imbalance make automated heartbeat classification difficult.
2. Why subject-separated evaluation changes the question being asked.
3. Why Morlet time-frequency structure plus local/global modelling is a reasonable hypothesis.
4. What this study tests and what it deliberately does not claim.

The final paragraph should state the contributions in prose rather than sounding like a grant-style enumerated list.

### Results

Retain the current hierarchy but improve transitions. Each subsection should open with its scientific question and end with the interpretation supported by the data. Aggregate performance and class-specific limitations should be presented as complementary findings, not competing narratives.

### Discussion

Adopt a more human reasoning voice: what was learned, why it matters, where the evidence stops, and what the failures imply. Keep causal language conservative because the comparator models are not a complete one-factor ablation. Avoid repeating all headline metrics after they have been established once.

### Conclusion

End with three ideas only: strongest aggregate result within the controlled benchmark; unresolved rare-rhythm limitation; value of the auditable evaluation framework and what validation is still needed.

## Visual design

All visualisations remain deterministic TikZ/data figures with values transcribed from the claim ledger. No generative-image artwork or graphical abstract is added.

### Figure 1 — Study workflow

- Replace the long left-to-right chain with a compact two-lane layout.
- Make the development lane and held-out lane visually distinct.
- Put the key counts (45, 38, 7, 15,573) in large/readable text.
- Keep post-hoc analyses in a clearly dashed diagnostic branch.
- Remove explanatory sentences that can live in the caption.

Primary message: the held-out records are separated before model development and are used for one fixed final evaluation.

### Figure 2 — Model-level comparison

- Keep only Accuracy, Macro-F1, and Weighted-F1.
- Increase label and value size.
- Reduce legend density.
- Use consistent spacing and stronger visual emphasis on the proposed model without hiding baseline values.
- Keep exact values printed on the bars.

Primary message: the CNN--Conformer has the strongest aggregate score profile among the evaluated baselines.

### Figure 3 — Class-specific performance

- Keep F1 and one-vs-rest AUC, with class support shown separately.
- Increase row spacing and label size.
- De-emphasise Q because n=2.
- Make the SVEB AUC-vs-F1 contrast visually obvious.

Primary message: aggregate gains are concentrated in Normal/VEB and do not translate to rare-rhythm F1.

### Figure 4 — Rare-rhythm error structure

- Show only the three dominant error pathways supported by archived counts.
- Convert the threshold details into two concise callouts rather than one dense paragraph.
- Keep the post-hoc qualification in the caption.

Primary message: minority-class failure is systematic and is not repaired by a simple threshold shift.

## Captions and tables

- Captions should state the finding/interpretation rather than merely naming plot contents.
- Disclosure language remains present but should be concise enough not to overwhelm the scientific caption.
- Tables keep exact values but use short captions and visible hierarchy; no duplicate metric blocks are added.

## Quality gates

1. Abstract remains under 250 words.
2. Main manuscript remains comfortably below the journal word ceiling.
3. No numeric mismatch with the claim ledger.
4. No prohibited overclaim language.
5. LaTeX builds without fatal errors, unresolved references, or layout overflow.
6. Figure labels remain readable in a full-page PDF review at normal zoom.
7. `paper-journal-A/` remains unchanged.
