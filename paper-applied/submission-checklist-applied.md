# Applied Sciences Submission Checklist (Internal)

- **Title**
  - Morlet–Conformer ECG Heartbeat Classification on MIT-BIH: A Reproducible Pipeline with Calibration and Robustness Analysis

- **Keywords**
  - Electrocardiogram (ECG)
  - Arrhythmia classification
  - MIT-BIH Arrhythmia Database
  - AAMI heartbeat classes
  - Conformer–CNN
  - Wavelet scalogram
  - Calibration
  - Reproducible pipeline

- **Manuscript Sections (mapped)**
  - Abstract: `paper-applied/src/sections/abstract.tex`
  - Introduction: `paper-applied/src/sections/introduction.tex`
  - Materials and Methods: `paper-applied/src/sections/methods.tex`
  - Results: `paper-applied/src/sections/results.tex`
  - Discussion: `paper-applied/src/sections/discussion.tex`
  - Conclusions: `paper-applied/src/sections/conclusion.tex`
  - References: generated from `paper-journal-A/bib/references.bib`

- **Tables used**
  - Test metrics + baselines: `paper-journal-A/tables/test_metrics.tex`
  - Per-class metrics: `paper/tables/table_stratified_perf.tex`
  - Calibration (ECE, Brier): `paper/tables/table_calibration.tex`
  - Robustness (noise sweeps): `paper/tables/table_robustness.tex`

- **Figures used**
  - ROC curves: `paper-journal-A/figures/roc_curves.png`
  - Confusion matrix: `paper-journal-A/figures/confusion_matrix.png`
  - Precision–recall curves: `paper-journal-A/figures/precision_recall_curves.png`

- **Declarations (to be filled from existing journal A/B sections)**
  - Funding: adapt from `paper-journal-A/src/sections/funding.tex`
  - Conflicts of Interest: adapt from `paper-journal-A/src/sections/competing-interest.tex`
  - Data Availability: adapt from `paper-journal-A/src/sections/data-availability.tex`
  - Ethics: adapt from `paper-journal-A/src/sections/ethics.tex`
  - Author Contributions: adapt from `paper-journal-B/src/sections/authors-contributions.tex`
  - Acknowledgements: adapt from `paper-journal-A/src/sections/acknowledgements.tex`

