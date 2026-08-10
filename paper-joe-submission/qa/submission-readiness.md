# Journal of Electrocardiology submission-readiness report

Date: 2026-08-10
Branch: `joe-editorial-rewrite-2026-08-10`
Working manuscript: `paper-joe-submission/`
Base manuscript: `paper-journal-A/`

## Status

**Second editorial/visual pass completed; working draft remains conditional on author sign-off and one Git-LFS-materialized production build before upload.**

The manuscript has now undergone two evidence-bounded revision passes. The first reorganized the paper around subject-separated benchmarking and rare-rhythm failure analysis. The second focused on a more natural authorial voice, clearer transitions, and journal-scale readability of the four primary figures. No experimental run, prediction, metric, or bibliographic source was added or altered during either pass.

## Base-folder integrity

A fresh Git comparison of `main` against the revision branch on 2026-08-10 shows changes only under:

- `.github/workflows/joe-submission-build.yml`
- `docs/superpowers/...`
- `paper-joe-submission/...`

No path under `paper-journal-A/` is modified. The independent working folder was originally created from the exact Git tree used by the base manuscript.

## Evidence boundary and primary results

Authoritative source: `qa/claim-ledger.md`.

Verified evidence retained in the second pass:

- 45 non-paced MIT-BIH records.
- 38 development records and 7 held-out records / subjects.
- 15,573 held-out beats.
- CNN--Conformer: accuracy 0.60 [0.59, 0.60], macro-F1 0.26 [0.26, 0.27], weighted-F1 0.68 [0.67, 0.68].
- Attention-only: 0.27 / 0.15 / 0.38.
- CNN--LSTM: 0.18 / 0.15 / 0.29.
- Feature-engineered: 0.14 / 0.07 / 0.23.
- Normal F1 0.74; VEB F1 0.57; SVEB F1 0.00; Fusion F1 0.01.
- SVEB AUC 0.67 despite realised F1 0.00.
- SVEB dominant errors: 151/214 to Normal and 51/214 to VEB.
- Fusion dominant error: 343/383 to VEB.
- Post-hoc SVEB max F1 0.06 at threshold 0.09 (precision 0.03, recall 0.90).
- Post-hoc Fusion max F1 0.05 at threshold 0.00 (precision 0.02, recall 1.00).
- Threshold and calibration analyses remain explicitly post-hoc and are not presented as independently validated operating points.

No headline number was strengthened or replaced in the human/visual polish pass.

## Second-pass narrative changes

The title now reads:

`Subject-Separated ECG Beat Classification With a Morlet CNN--Conformer: Performance Gains and Rare-Rhythm Limitations`

The Abstract was rewritten as a four-step argument: clinical/technical problem, subject-separated protocol, two-sided result, and implication. A conservative LaTeX-stripped count gives approximately **225 words**, below the 250-word target used for this revision.

The Introduction now moves from the real ECG problem to the evaluation boundary, then to the representation hypothesis, and finally to the study question. The previous grant-style numbered contribution paragraph was replaced with continuous scientific prose.

The Results section now uses question-driven transitions. Aggregate improvement is presented first, followed immediately by the class-specific evidence showing where that improvement does not translate into useful rare-rhythm F1.

The Discussion now uses a reasoning voice rather than repeating the metric table. It distinguishes what was learned, why subject separation matters, where architectural inference stops, why rare-rhythm errors matter, and what evidence is still needed. The comparators remain explicitly described as controlled alternatives rather than a complete one-factor ablation.

The Conclusion has been shortened to three points: strongest aggregate profile within the controlled benchmark, unresolved rare-rhythm limitation, and the value of the auditable framework for future validation.

## Second-pass visual changes

The four editable TikZ figures were redrawn for normal PDF viewing rather than dense source-level completeness:

1. **Study workflow:** converted to two visible lanes (development vs held-out), with the counts 45, 38, 7, and 15,573 given stronger hierarchy and the post-hoc branch shown separately.
2. **Model comparison:** larger labels and values, a compact legend, and a visually distinct proposed-model row while retaining every baseline value.
3. **Class performance:** increased row spacing, separate support labels, explicit emphasis on the SVEB AUC/F1 discrepancy, and visual de-emphasis of Q because `n=2`.
4. **Rare-rhythm error structure:** reduced to the three dominant confusion pathways plus two compact threshold callouts; the previous dense paragraph inside the figure was removed.

Captions are now interpretation-first rather than plot-description-only. The Methods and captions retain concise disclosure that ChatGPT assisted with deterministic LaTeX/TikZ layout while values come directly from archived study outputs.

The original study-generated confusion matrix, ROC, and precision--recall curves remain unaltered as Supplementary Figures S1--S3.

## Second-pass QA evidence

A dedicated four-page figure harness was compiled locally with `pdflatex` and rendered to images. All four redesigned figures were visually inspected: labels and numeric values were readable at normal review zoom, and no figure showed clipping or overlapping elements.

A ten-page editorial review PDF containing the updated title, Abstract, Introduction, core Methods/Results, the three principal tables, all four redesigned figures, Discussion, and Conclusion was compiled and visually inspected page-by-page.

Review-PDF checks:

- PDF generated successfully: 10 pages, US Letter.
- Abstract: approximately 225 words.
- Prohibited broad-claim scan: 0 matches for `state of the art`, `state-of-the-art`, `clinically ready`, `cardiologist-level`, `autonomous diagnosis`, `generalizes to real-world`, `triage-ready`, or `deployable arrhythmia`.
- No fatal LaTeX errors or unresolved references in the review harness.
- One 3.36-pt `Overfull \\hbox` warning is produced by `elsarticle` front-matter/author metadata in the review harness; visual inspection confirms no clipped author/title text. No scientific text, table, or primary figure is affected.
- Figure-specific compilation: 0 fatal errors; no visual clipping/overlap found.

This ten-page file is a review preview, not the final production submission PDF: it deliberately omits the bibliography, declarations, and Git-LFS-backed supplementary diagnostic PNG pages. The repository source remains the authoritative submission workspace.

## Previous full-source QA and remaining production build

Before the second visual/narrative pass, a full 20-page source QA build completed with zero undefined citations/references, zero manuscript-content overfull/underfull boxes, and zero fatal LaTeX errors. The second pass changed only editorial prose, title/captions, and deterministic TikZ layout; a final production build with the Git-LFS image objects materialized is still required before upload.

The branch workflow `.github/workflows/joe-submission-build.yml` is configured to check out Git LFS and build the production manuscript. The GitHub connector currently reports no workflow run for this branch, so no remote CI success is claimed here.

## AI-use disclosure

The manuscript contains a dedicated declaration immediately before the references. It states that OpenAI ChatGPT (GPT-5.6 Sol) assisted with language/editorial revision and deterministic TikZ layout code, while research data, stored predictions, experimental results, and bibliographic sources were not generated or altered by the tool. The author must review and approve the final wording and every AI-assisted textual/visual change before submission.

## Remaining author-side actions

Before upload:

1. Read and approve the complete manuscript and the four redesigned TikZ figures.
2. Confirm the exact affiliation, postal address, and corresponding-author details required by the Elsevier submission form.
3. Run a Git-LFS-materialized production build and inspect the PDF containing the real supplementary diagnostic PNGs.
4. Create an immutable/versioned repository release or archive and update Data Availability with the final citation/URL.
5. Re-check the live Journal of Electrocardiology Guide for Authors and Elsevier AI/artwork policy on the submission date.
6. If a graphical abstract is desired, prepare it through a policy-compatible workflow and review it independently before upload.

## Editorial assessment

After the second pass, the paper reads less like a model-performance report and more like an ECG study with a clear scientific tension: the hybrid representation improves the aggregate score profile under a subject-separated protocol, yet clinically relevant minority rhythms remain the decisive bottleneck. The figures now reinforce that argument at a glance rather than requiring the reader to extract it from dense labels or tables.
