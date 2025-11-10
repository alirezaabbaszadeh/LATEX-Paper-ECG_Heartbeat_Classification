# BioMedical Engineering OnLine Manuscript Outline

## Abstract → Conclusion Narrative Flow
1. **Background (Abstract & Introduction).** Emphasize unmet need for interpretable ECG heartbeat classifiers in biomedical engineering, referencing MIT-BIH Arrhythmia dataset limitations and regulatory push for reproducible AI in cardiology.
2. **Methods summary (Abstract & Methods).** Describe structured background/methods/results/conclusions abstract ≤350 words with 3–10 keywords. Highlight dataset acquisition, scalogram preprocessing, Conformer-CNN training (k-fold + champion model), statistical evaluations (macro-F1, calibration, robustness), and compute footprint.
3. **Results headline (Abstract & Results).** Present primary metrics (accuracy 0.60, macro-F1 0.26), per-class disparities, calibration metrics, and robustness noise sweep. Mention availability of supplementary reliability curves and dataset composition.
4. **Discussion emphasis.** Address clinical engineering implications, comparison with baseline architectures, generalizability to wearable devices, and constraints due to minority class performance. Tie to translational engineering focus.
5. **Conclusions & Declarations.** Reinforce reproducibility package (code, TFRecords, Research_Runs), planned open data release, and ensure structured Declarations (ethics, consent, data availability, competing interests, funding, authors’ contributions, acknowledgements, author information).

## Section Plan & Content Mapping
| Section | Primary Content | Dataset Coverage | Experiments & Analyses | Figures/Tables | Checklist Hooks |
| --- | --- | --- | --- | --- | --- |
| Title Page | Manuscript title, author affiliations, corresponding author details, ORCID iDs, suggested reviewers. | Cite MIT-BIH source, licensing. | — | — | Submission logistics (Springer guidelines §414–424). |
| Abstract & Keywords | Structured (Background/Methods/Results/Conclusions), ≤350 words, 3–10 keywords. | Mention dataset size, splits. | Summaries of main experiment, calibration, robustness. | — | Checklist: Article type & length. |
| Introduction | Engineering motivation, literature review, contribution summary. | Dataset provenance, patient demographics via Table~\ref{tab:subjects}. | Outline research questions driving experiments. | Fig.~1 pipeline. | Scope alignment & SI units. |
| Methods | Subsections per BMC template: Dataset, Preprocessing, Model, Training/tuning, Evaluation metrics, Statistical analysis. Include reproducibility subsection (code/data availability). | Provide dataset access instructions, consent/IRB details, repository plan. | Document k-fold tuning, final training, robustness (noise injection), planned ablations, compute profiling. | Table~\ref{tab:dataset}, Table~\ref{tab:subjects}, Fig.~1 pipeline. | Double spacing, numbering, data policy compliance. |
| Results | Baseline comparison (Table~\ref{tab:leaderboard}), per-class metrics (Table~\ref{tab:perclass}), calibration (Table~\ref{tab:calibration}, PR/ROC figures), robustness (Table~\ref{tab:robustness}), compute (Table~\ref{tab:compute}). | Relate class imbalance to outcomes, reference dataset splits. | Provide narrative for champion vs baselines, calibration bins, robustness sigma sweep, runtime summary, placeholder for ablations. | Figures: confusion matrix, PR curves, ROC curves; optional reliability diagrams. | Figures/tables formatting & numbering. |
| Discussion | Interpretation vs prior art, limitations (data imbalance, generalizability, ablation gaps), engineering implications, future work. | Note need for external datasets, plan for open repository deposit. | Reference experiments requiring expansion (ablation). | Possibly include synthetic ECG illustration if adds clarity. | Ethical policy reinforcement. |
| Conclusions | Concise restatement of contributions, reproducibility resources, potential for deployment, pointer to forthcoming data/code release. | Provide repository DOI (pending). | — | — | Link to Declarations. |
| Declarations | Structured subheadings: Ethics approval & consent, Consent for publication, Availability of data and materials, Competing interests, Funding, Authors’ contributions (CRediT), Acknowledgements, Authors’ information, AI usage disclosure. | Provide IRB reference, dataset licensing, repository details. | Mention code availability, supplementary files. | — | Mandatory per BMC template. |
| Supplementary Information | List additional tables/figures (extended confusion matrix, calibration curves, hyperparameter sweeps), dataset archives, video or interactive components ≤20 MB each. | Provide metadata for supplementary datasets/logs, referencing Research_Runs. | Extended analyses, ablation completion. | Additional figures/CSV zipped files. | Supplementary guidelines (≤20 MB, metadata). |

## Content Gaps & Owner Assignments
- **Ethics approval & consent statement (structured Declarations).** _Owner:_ Dr. Emily Chen. Deadline: 2025-10-11.
- **Data & materials availability paragraph (FORCE11-compliant wording).** _Owner:_ Priya Singh. Deadline: 2025-10-15.
- **Competing interests & funding disclosure updates.** _Owner:_ Alireza Abbaszadeh. Deadline: 2025-10-10.
- **Authors’ contributions (CRediT) + Authors’ information section.** _Owner:_ Marco Ruiz collating team inputs. Deadline: 2025-10-18.
- **Ablation results narrative and populated Table~\ref{tab:ablation}.** _Owner:_ Priya Singh with ML subteam. Deadline: 2025-10-20.
- **Supplementary files packaging (calibration curves, Research_Runs metadata ≤20 MB).** _Owner:_ Marco Ruiz. Deadline: 2025-10-22.
- **Cover letter draft addressing scope fit and policy compliance.** _Owner:_ Alireza Abbaszadeh. Deadline: 2025-10-25.

## Co-author Review & Revisions
- **Feedback workshop (2025-09-18).** Priya emphasized mapping each figure/table to Results narrative and ensuring Declarations align with BMC structure → added dedicated Declarations row and supplementary packaging actions. Dr. Chen requested ethics/consent gap be flagged with owner → added top of gap list. Marco suggested referencing cover letter requirements and reviewer suggestions → captured under Title Page and Content Gaps.
- **Next steps (2025-09-25).** Circulate outline to co-authors via shared doc; schedule async comments. Track revisions in issue `#outline-bmeo` and update upon receipt.
