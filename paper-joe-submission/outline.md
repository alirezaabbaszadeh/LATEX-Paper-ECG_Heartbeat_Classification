# Journal of Electrocardiology Manuscript Outline

## Abstract → Conclusion Narrative Flow
1. **Clinical motivation (Abstract & Introduction).** Highlight arrhythmia monitoring gaps in ambulatory settings, emphasizing unreliable minority class detection in the MIT-BIH Arrhythmia Database. State objective: reproducible Conformer-CNN pipeline delivering calibrated beat-level predictions under AAMI EC57 protocol.
2. **Methods overview (Abstract & Methods).** Summarize dataset splits (38-train/7-test records), Morlet scalogram preprocessing, Conformer-CNN architecture, hyperparameter tuning, and evaluation metrics (accuracy, macro-F1, calibration). Reference adherence to Elsevier Option B data expectations.
3. **Key quantitative findings (Abstract & Results).** Report hold-out accuracy 0.60/macro-F1 0.26 (Table~\ref{tab:leaderboard}), per-class disparities (Table~\ref{tab:perclass}), calibration metrics (Table~\ref{tab:calibration}), and robustness probe outcomes (Table~\ref{tab:robustness}). Note pipeline figure and reliability plots.
4. **Clinical interpretation (Discussion).** Discuss implications of low recall for supraventricular/fusion beats, necessity for decision support thresholds, and calibration-informed triage. Compare against prior CNN/LSTM baselines.
5. **Limitations and future work (Discussion).** Address dataset imbalance, limited demographics, synthetic augmentation gaps, and need for external validation. Outline planned ablation studies and potential for wearable deployment.
6. **Conclusion.** Reiterate reproducibility assets (public code, TFRecords, Research_Runs), emphasize contribution to arrhythmia monitoring, and mention compliance with highlights/graphical abstract deliverables.

## Section Plan & Content Mapping
| Section | Primary Content | Dataset Coverage | Experiments & Analyses | Figures/Tables | Checklist Hooks |
| --- | --- | --- | --- | --- | --- |
| Title Page & Highlights | Final title, authors/affiliations, corresponding author contact, 3–5 bullet highlights, optional graphical abstract. | MIT-BIH attribution on title page. | — | Graphical abstract (new). | Highlights + structured front matter (Elsevier Guide §290–342). |
| Abstract | 3-paragraph structured summary (Background/Methods/Findings), ≤250 words, include 3 key metrics. | State dataset name, size (15,573 test beats), split strategy. | Mention main experiment and calibration analysis. | — | ≤250 words, keywords (Checklist: Manuscript structure). |
| Introduction | Clinical context, prior work gap analysis, contributions. | Explain patient cohort composition (Table~\ref{tab:subjects}). | Summarize baseline comparisons and research questions. | Fig.~1 pipeline (existing). | Scope alignment + SI units. |
| Methods | Subsections: Dataset acquisition (MIT-BIH), preprocessing (scalograms), Model architecture, Training/tuning (run scripts), Evaluation (metrics, calibration, robustness). | Detail repository location, licensing, consent provenance. | Reference k-fold workflow, champion selection, robustness noise injection, planned ablations (Table~\ref{tab:ablation}). | Fig.~1 pipeline; Table~\ref{tab:dataset}; Table~\ref{tab:subjects}. | Editable source, reproducibility, numbered footnotes. |
| Results | Present leaderboard, per-class metrics, calibration, robustness, compute profile. | Include dataset imbalance effect on results. | Main run vs baselines (leaderboard), calibration, robustness noise sweep, compute efficiency, placeholder for ablations once populated. | Table~\ref{tab:leaderboard}, Table~\ref{tab:perclass}, Table~\ref{tab:calibration}, Fig.~2 confusion matrix, Fig.~3 PR curves, Fig.~4 ROC, Table~\ref{tab:robustness}, Table~\ref{tab:compute}. | Figure resolution, numbering, captions (Checklist Tables/Figures). |
| Discussion | Interpret findings, clinical relevance, limitations, comparison to literature, generalization prospects. | Address dataset representativeness, external datasets for future validation. | Reference planned ablations and robustness expansions. | Possibly Fig.~5 synthetic ECG (if used as illustration). | Data sharing encouragement, co-submission note. |
| Conclusion | Summarize contributions, reiterate reproducibility resources, highlight Option B data-sharing compliance, mention future prospective studies. | Provide link to repository release and dataset DOI (pending). | — | — | Data availability statement tie-in. |
| Declarations (pre-References) | Funding, competing interests, generative AI usage, CRediT roles, acknowledgements, data availability statement. | Cite dataset repository, licensing, consent. | Mention code availability (GitHub). | — | Compliance statements (Checklist). |
| Supplementary Materials | Enumerate additional analyses (extended metrics, hyperparameter sweeps) with cross-references. | Provide metadata for supplementary datasets/logs. | Extended robustness or calibration curves. | Additional figures or CSVs. | Supplementary material management. |

## Content Gaps & Owner Assignments
- **Data availability statement (Option B wording + repository DOI).** _Owner:_ Priya Singh (Data curator). Deadline: 2025-10-15.
- **Generative AI usage disclosure (affirm none used in writing or figures).** _Owner:_ Alireza Abbaszadeh (Lead author). Deadline: 2025-10-10.
- **Highlights (3–5 bullets, ≤85 characters) & graphical abstract draft.** _Owner:_ Marco Ruiz (Visualization lead). Deadline: 2025-10-12.
- **CRediT contribution table and acknowledgements specifics (funding IDs).** _Owner:_ Dr. Emily Chen (Clinical PI). Deadline: 2025-10-18.
- **Ablation grid completion with experiment IDs.** _Owner:_ Priya Singh coordinating with ML team. Deadline: 2025-10-20.
- **Supplementary dataset packaging (Research_Runs metadata).** _Owner:_ Marco Ruiz. Deadline: 2025-10-22.

## Co-author Review & Revisions
- **Feedback session (2025-09-18).** Priya requested explicit mention of TFRecord release path and Option B compliance → added to Methods mapping and Conclusion bullet. Marco asked for figure callouts per checklist → enumerated figures in Results row. Dr. Chen sought clearer clinical framing of supraventricular recall gaps → strengthened Discussion flow and Abstract note.
- **Pending follow-up (2025-09-25).** Circulate updated outline for sign-off; capture additional comments in repository issue `#outline-jecg`.
