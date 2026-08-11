# Changelog — Journal of Electrocardiology revision

## 2026-08-11 — Evidence-led human editorial reconstruction

### Narrative and argument
- Rebuilt the Discussion around the tension between aggregate performance and near-zero SVEB/Fusion F1 instead of retaining the previous repeated claim--qualification--implication paragraph pattern.
- Added an explicitly bounded interpretation of the dominant SVEB-to-Normal and Fusion-to-VEB error pathways; these mechanisms are identified as testable hypotheses rather than causal findings.
- Replaced the generic future-work list with a ranked sequence: error-linked representation experiments, minority-class learning under development-only selection, and then external and clinician-in-the-loop validation.
- Reworked the Introduction so the cited literature is compared by endpoint and validation boundary, including all ten verified *Journal of Electrocardiology* additions.
- Applied a light Results edit for sentence rhythm and authorial reasoning while leaving Materials and Methods technically unchanged.
- Rewrote the Abstract and Conclusion to preserve the aggregate gain/rare-rhythm boundary without repeating Discussion language.

### Evidence and production QA
- Confirmed that the set of numerical tokens across the revised narrative sections is unchanged from the preceding production version.
- Confirmed that the manuscript-wide citation-key set is unchanged: 34 rendered references, including all ten journal-specific additions.
- LaTeX-stripped Abstract count: 212 words.
- Production build: 23 pages; 0 undefined citations/references, 0 fatal LaTeX errors, 0 overfull boxes, and 0 underfull boxes.
- Embedded fonts are vector Type 1; no Type 3 fonts remain.
- Rendered and visually inspected all 23 pages, including the main figures and Supplementary Figures S1--S3; no clipping, overlap, or blank-page defect was found.

## 2026-08-10 — Verified JOE references and production PDF

### Journal-specific literature
- Added ten topical articles from the *Journal of Electrocardiology* (2024--2026) and cited them in the Introduction, Methods, and Discussion.
- Checked titles, author lists, publication details, and DOI identifiers against publisher and DOI records.
- Normalised DOI fields across the BibTeX database so the Elsevier bibliography style produces valid DOI links without duplicated URL prefixes.

### Reproducible supplementary diagnostics
- Regenerated the confusion matrix, ROC curves, and precision--recall curves from the unchanged archived `raw_predictions.npz` arrays after the original Git LFS image objects proved unavailable.
- Confirmed that the confusion-matrix total is 15,573 and that displayed AUC/AP values agree with the archived predictions.
- Added `scripts/regenerate_diagnostics.py` and updated figure provenance notes and the AI-use disclosure.
- Corrected Supplementary Figure numbering and captions to render cleanly as S1--S3 under the Elsevier class.

### Production QA
- Built the complete Elsevier manuscript successfully: 23 pages including declarations, bibliography, supplementary methods, and all diagnostic figures.
- Confirmed all ten new bibliography entries and DOI identifiers in the generated BibTeX output.
- Final log scan: 0 undefined citations/references, 0 fatal LaTeX errors, 0 overfull boxes, and 0 underfull boxes.
- Rendered and visually inspected all 23 pages; no clipping, overlap, broken figures, or malformed DOI links remained.

## 2026-08-10 — Human narrative and visual clarity pass

### Narrative
- Retitled the manuscript as `Subject-Separated ECG Beat Classification With a Morlet CNN--Conformer: Performance Gains and Rare-Rhythm Limitations`.
- Rewrote the Abstract into a problem → protocol → two-sided result → implication arc while retaining the existing evidence; conservative count is approximately 225 words.
- Reworked the Introduction into connected scientific prose focused on patient heterogeneity, subject-separated evaluation, the representation hypothesis, and the study question.
- Made Results transitions question-driven so aggregate improvement leads directly into the class-specific limitation.
- Rewrote Discussion in a more natural reasoning voice and reduced repetitive metric recitation.
- Shortened Conclusion to the controlled-benchmark gain, rare-rhythm bottleneck, and next validation steps.

### Visual clarity
- Rebuilt Figure 1 as a two-lane development/held-out workflow with more prominent cohort counts.
- Increased label/value size and visual hierarchy in Figure 2 while preserving all evaluated baseline values.
- Increased class-row spacing in Figure 3, highlighted the SVEB AUC/F1 discrepancy, and de-emphasised Q because only two test beats were available.
- Simplified Figure 4 to the three dominant rare-rhythm error pathways plus two compact post-hoc threshold callouts.
- Rewrote all four main captions to lead with the scientific interpretation rather than a generic plot description.
- Kept the original confusion matrix, ROC curves, and precision--recall curves unaltered in Supplementary Figures S1--S3.

### Second-pass QA
- Compiled and visually inspected a four-page TikZ figure harness; no clipping or overlap was observed.
- Compiled and visually inspected a ten-page editorial review PDF containing the revised narrative, three main tables, and all four primary figures.
- Abstract count: approximately 225 words.
- Prohibited broad-claim scan: 0 matches in the review source.
- Review harness: 0 fatal LaTeX errors; one minor 3.36-pt front-matter overfull warning with no visible clipping.
- Fresh `main` vs branch comparison confirms no changes under `paper-journal-A/`.

## 2026-08-10 — Submission-oriented editorial rewrite

### Isolation and provenance
- Created `paper-joe-submission/` from the exact `paper-journal-A/` Git tree rather than rebuilding from zero.
- Kept `paper-journal-A/` unchanged throughout the revision.
- Added `REVISION_PROVENANCE.md`, design notes, implementation plan, and branch-specific CI workflow.

### Scientific narrative
- Retitled the manuscript around subject-separated benchmarking and rare-rhythm failure analysis.
- Rewrote the Abstract, Introduction, Results, Discussion, Conclusion, Highlights, and Keywords.
- Replaced promotional/deployment language with evidence-bounded claims scoped to the evaluated baselines and held-out protocol.
- Made class imbalance, patient/record separation, cross-validation variability, and rare-class failure part of the central scientific story.
- Explicitly qualified class-specific AUC results so aggregate-model superiority is not misrepresented as uniform class-wise superiority.

### Methods and reproducibility
- Clarified the 38-record development / 7-record held-out protocol.
- Tightened beat/scalogram/three-beat-sequence and CNN--Conformer descriptions.
- Distinguished definitive evaluation from post-hoc threshold and calibration analyses.
- Added a dedicated subsection describing preparation and disclosure of AI-assisted explanatory/data visualisations.
- Updated Data Availability to point to the public repository and require an immutable release at final submission.

### Tables
- Added a cohort/class-distribution table.
- Simplified the main model-comparison table to accuracy, macro-F1, and weighted-F1 with confidence intervals.
- Added a dedicated class-specific performance table with support, precision, recall, F1, and AUC.
- Corrected the cross-validation table wording to refer to record-level development folds.

### Figures
- Added editable TikZ Figure 1: subject-separated study workflow.
- Added editable TikZ Figure 2: controlled model-level comparison.
- Added editable TikZ Figure 3: class-specific F1/AUC with class support.
- Added editable TikZ Figure 4: dominant rare-rhythm error paths and threshold trade-off.
- Moved the original study-generated confusion matrix, ROC curves, and precision--recall curves to Supplementary Figures S1--S3 without altering their image content.
- Added tool/use disclosure to Methods and captions for the AI-assisted TikZ layout code.
- Did not include a graphical abstract made with a general-purpose generative-AI image tool.

### Submission package
- Added standalone `submission/Highlights.txt` and `submission/Figure_Captions.txt`.
- Added `submission/README.md` with author-side pre-upload checks.
- Added a dedicated generative-AI declaration before the references and removed the inherited acknowledgement text that understated the extent of AI editorial assistance.

### QA and build hygiene
- Added `qa/claim-ledger.md` as the source of truth for quantitative claims and figure labels.
- Added `qa/visual-redesign-spec.md` as the visual evidence map.
- Added `qa/submission-readiness.md` with final build/compliance evidence and remaining author actions.
- Removed stale inherited compiled manuscript artifacts from the revision folder and added `src/.gitignore` for generated LaTeX files.
- Fresh QA build: 20 pages; 0 undefined citations/references; 0 overfull boxes; 0 underfull boxes; 0 fatal LaTeX errors.
- Automated checks: 0 primary numeric inconsistencies and 0 prohibited over-broad claim phrases.
