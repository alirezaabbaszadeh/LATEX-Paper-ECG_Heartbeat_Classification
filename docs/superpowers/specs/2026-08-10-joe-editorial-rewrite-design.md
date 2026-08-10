# Journal of Electrocardiology editorial rewrite design

Date: 2026-08-10
Branch: `joe-editorial-rewrite-2026-08-10`
Base manuscript: `paper-journal-A/`
Target working copy: `paper-joe-submission/`
Target journal: *Journal of Electrocardiology*

## Objective

Create a submission-oriented revision of the existing Journal of Electrocardiology manuscript by copying `paper-journal-A/` rather than rebuilding from zero. Preserve the original manuscript unchanged. Improve scientific narrative, editorial positioning, figures, tables, captions, and journal fit without inventing experiments, metrics, cohorts, citations, or clinical claims.

## Evidence boundary

All quantitative claims must be traceable to existing manuscript files or archived experiment outputs. No new training run or synthetic result will be presented as completed evidence. Language may become stronger only when the underlying evidence supports the stronger formulation.

Hard prohibitions:
- no state-of-the-art claim unless directly demonstrated against an appropriate literature benchmark;
- no autonomous-diagnosis or clinical-readiness claim;
- no superiority claim beyond the baselines actually evaluated;
- no fabricated external validation, ablation, calibration, robustness, demographic, or compute results;
- no hiding of weak SVEB/fusion performance.

## Current evidence that should drive the story

The held-out test set contains 15,573 beats from 7 subjects, separated from 38 development records. The proposed model reports 0.60 accuracy, 0.26 macro-F1, and 0.68 weighted-F1, with substantially higher performance than the attention-only, CNN-LSTM, and handcrafted baselines used in this study. Normal and ventricular ectopic beats are the strongest classes; SVEB and fusion beats remain weak. Cross-validation accuracy is reported as 0.44 ± 0.16, highlighting patient-level variability.

The revision should therefore avoid making raw accuracy the hero. The central value proposition is the combination of:
1. strict subject-separated evaluation;
2. reproducible Morlet + CNN-Conformer pipeline;
3. clear gains over the study's controlled baselines;
4. clinically relevant error analysis showing where rare-rhythm detection fails;
5. transparent interpretation that supports decision-support research rather than autonomous diagnosis.

## Central thesis

A lightweight Morlet–Conformer ECG pipeline can improve discrimination over the evaluated attention-only, recurrent, and handcrafted alternatives under subject-separated testing, but the clinically important lesson is that performance remains strongly rhythm-dependent. This combination of architectural gain and transparent rare-class failure analysis makes the study useful as a reproducible benchmark for computerized electrocardiology and clinician-supervised arrhythmia triage research.

## Journal fit

The journal's current Elsevier description states that it is devoted to clinical and experimental studies of the electrical activity of the heart and explicitly includes arrhythmias, monitoring, instrumentation, and computer applications. The manuscript should demonstrate fit through computerized electrocardiology, arrhythmia discrimination, patient heterogeneity, morphology-aware signal representation, monitoring, and decision-support implications—not through repeated mentions of the journal's name in the prose.

Source checked 2026-08-10: Elsevier Journal of Electrocardiology journal page / description.

## Editorial strategy

### Title and framing
Use a title that foregrounds the evaluation setting and scientific contribution rather than implying clinical deployment. Candidate direction:

`Subject-Separated ECG Beat Classification with a Morlet–Conformer Network: Reproducible Benchmarking and Rare-Rhythm Failure Analysis`

Final title may be shortened after the full rewrite.

### Introduction
Rewrite around a four-step argument:
1. clinically meaningful automated ECG analysis requires robustness to patient heterogeneity and class imbalance;
2. reported heartbeat-classification performance can be inflated or difficult to compare when evaluation protocols differ;
3. hybrid local/global representations are promising, but their value should be judged under subject-separated testing and class-specific analysis;
4. this study evaluates a Morlet–Conformer pipeline under that stricter framing and explicitly quantifies its failure modes.

Remove artificial phrases such as repeated `Journal of Electrocardiology studies...` references. Keep journal-relevant citations when they genuinely support the scientific point.

### Results
Reorder the Results so the reader sees the study's actual value quickly:
1. cohort/split and class imbalance;
2. overall model-versus-baseline comparison;
3. class-specific discrimination;
4. error structure and rare-class failure;
5. calibration/threshold findings where already supported by archived outputs.

Use relative improvements carefully and always pair them with absolute values.

### Discussion
Structure as:
1. principal finding;
2. why subject-separated testing matters;
3. what the hybrid representation appears to add relative to the controlled baselines;
4. clinical meaning of strong N/V and weak S/F performance;
5. comparison with literature without invalid apples-to-oranges claims;
6. reproducibility value;
7. limitations;
8. concrete next validation steps.

The Discussion should explicitly distinguish `discrimination`, `triage support`, and `clinical diagnosis`.

### Abstract and conclusion
Write these last so they match the final body exactly. Abstract should lead with the problem of patient heterogeneity and class imbalance rather than specialist shortage hype. Conclusion should state what was demonstrated, what was not demonstrated, and why the benchmark remains useful.

## Figure redesign

Reuse existing data and source plots. Do not manufacture new experimental results.

Planned main figures:
1. **Study design and pipeline** — records → subject-separated split → beat extraction → Morlet scalogram → three-beat sequence → CNN-Conformer → evaluation.
2. **Performance overview** — compact baseline comparison emphasizing accuracy, macro-F1, weighted-F1 with uncertainty/labels where available.
3. **Class-wise diagnostic performance** — redesigned confusion matrix plus class support, using a layout that makes imbalance and error direction obvious.
4. **ROC/PR diagnostic figure** — prioritize PR interpretation for minority classes and avoid visually overemphasizing ROC alone.
5. Optional **graphical abstract** — one-panel summary of study design, main gain, and rare-class limitation if it can be built entirely from existing evidence.

Visual requirements:
- consistent typography and dimensions;
- publication-safe vector output when possible;
- no decorative 3D effects;
- captions that state the takeaway, not just identify the plot;
- abbreviations expanded in captions;
- distinguish sample counts from model performance.

## Table redesign

Main-text target:
1. **Table 1 — Cohort and class distribution**: development/test records, beat counts, class support, split logic.
2. **Table 2 — Model comparison**: proposed model and evaluated baselines with accuracy, macro-F1, weighted-F1 and any directly supported uncertainty.
3. **Table 3 — Class-specific performance**: support, precision, recall, F1, AUC/CI where available.

Move highly granular threshold sweeps and secondary diagnostics to supplementary material unless needed for a central claim.

## File architecture

Create `paper-joe-submission/` as an exact starting copy of the `paper-journal-A/` subtree, including figures, bibliography, tables, supplementary material, templates, QA files, and build configuration. Subsequent edits happen only in the new folder.

Primary edit targets:
- `paper-joe-submission/src/sections/frontmatter.tex`
- `paper-joe-submission/src/sections/abstract.tex`
- `paper-joe-submission/src/sections/introduction.tex`
- `paper-joe-submission/src/sections/methods.tex`
- `paper-joe-submission/src/sections/results.tex`
- `paper-joe-submission/src/sections/discussion.tex`
- `paper-joe-submission/src/sections/conclusion.tex`
- `paper-joe-submission/src/sections/highlights.tex`
- `paper-joe-submission/tables/*`
- `paper-joe-submission/figures/*` or new figure-source files that reproduce publication-ready versions from existing data.

## Claim-strengthening rules

Prefer formulations such as:
- `outperformed all baselines evaluated in this study`;
- `under the subject-separated protocol used here`;
- `showed strong discrimination for normal and ventricular ectopic beats`;
- `exposed a persistent rare-class failure mode that threshold adjustment alone did not resolve`;
- `provides a reproducible benchmark and failure-analysis framework`.

Avoid formulations such as:
- `clinically ready`;
- `cardiologist-level`;
- `state of the art`;
- `generalizes to real-world populations`;
- `suitable for autonomous diagnosis`.

## Validation and QA

Before calling the revision submission-ready:
1. every number in Abstract, Results, Discussion, tables, and captions must reconcile;
2. every new comparative claim must identify the comparison set;
3. each literature statement must be supported by an appropriate citation;
4. no current-journal formatting requirement should be asserted without checking the current official guide;
5. build the LaTeX manuscript and resolve missing references/figures;
6. inspect the generated PDF visually, especially tables, multi-panel figures, captions, page breaks, and equation overflow;
7. verify that `paper-journal-A/` is unchanged;
8. compare the new folder against the base to produce a concise change log;
9. run any existing repository QA relevant to bibliography/manuscript consistency.

## Implementation order

1. duplicate base subtree into `paper-joe-submission/`;
2. establish claim ledger from existing results/tables/artifacts;
3. rewrite Results and Discussion;
4. redesign tables and main diagnostic figures using existing data;
5. rewrite Introduction and Methods for tighter logic and journal fit;
6. rewrite Conclusion, Abstract, Highlights, and title/front matter;
7. update captions and supplementary cross-references;
8. build and visually inspect PDF;
9. run numerical/citation consistency audit;
10. produce final submission-readiness notes.

## Acceptance criteria

The revision is successful when an editor can understand within the title, abstract, first page, and primary results figure that the paper contributes a reproducible subject-separated ECG classification benchmark with a clear architectural comparison and an unusually transparent rare-rhythm failure analysis—and when every strong statement remains traceable to existing evidence.