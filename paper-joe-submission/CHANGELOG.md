# Changelog — Journal of Electrocardiology revision

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
