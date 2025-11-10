# ECG Literature Surveillance and Journal Submission Plan

## Selected Target Journals

### Journal of Electrocardiology (Elsevier)
- **Scope:** Publishes clinical and experimental work on cardiac electrophysiology, arrhythmia mechanisms, monitoring, pacing, device therapy, and computational electrocardiology for diagnosis, prognosis, and therapy optimization.【F:docs/journals/journal-of-electrocardiology-guide.md†L8-L12】
- **2026 policy watch:** Elsevier introduced mandatory declarations of generative AI usage and strengthened competing interest disclosures in 2024; no 2026-specific policy bulletins are posted yet, but quarterly ISCE newsletters and Elsevier Author Services updates should be monitored for potential data-sharing or ethical compliance revisions.

### BioMedical Engineering OnLine (Springer Nature)
- **Scope:** Open-access venue spanning biomedical signal processing, cardiovascular systems engineering, device design, translational AI, and data-driven health technology, with emphasis on manuscripts that combine engineering innovation with clinically validated datasets.【F:docs/journals/biomedical-engineering-online-springer-guidelines.md†L35-L104】
- **2026 policy watch:** Springer Nature highlighted forthcoming enhancements to open data and code availability policies during the 2025 SpringerOpen editorial webinar; expect formal announcements by Q1 2026 in the SpringerOpen policy hub. Track automated alerts from the journal’s news feed and Springer Nature’s research data policy updates.

## Guide for Authors Highlights

### Journal of Electrocardiology
- **Manuscript structure:** Original Research capped at 5,000 words with up to 40 references; standard sections include Introduction, Methods, Results, Discussion, Conclusions, and Clinical Significance.【8b2954†L23-L49】
- **Abstract and highlights:** Submit a 200-word structured abstract (Background, Methods, Results, Conclusions) and a separate highlights file (3–5 bullets, ≤85 characters each).【8b2954†L23-L49】【bda339†L1-L20】
- **Figures and tables:** Tables supplied as editable text; figures uploaded separately with preferred vector formats (EPS/PDF) and SI units throughout.【bda339†L21-L74】
- **References:** Vancouver-style numbering applied post-acceptance; ensure consistent formatting and include DOIs where available.【bd00e8†L1-L83】
- **Ethics and disclosures:** Requires detailed competing interest statements, funding declarations, and documentation of generative AI use in manuscript preparation.【8b2954†L49-L88】

### BioMedical Engineering OnLine
- **Manuscript structure:** Research articles should follow Background, Methods, Results, Discussion, Conclusions, with a mandatory Declarations section covering ethics, consent, data availability, funding, competing interests, and author contributions.【b8594c†L25-L116】
- **Abstract and keywords:** Structured abstract ≤350 words (Background, Results, Conclusions) and 3–10 keywords.【b8594c†L41-L59】
- **Formatting:** Double-line spacing, line/page numbering, SI units, and editable source files (Word or LaTeX). TeX users should employ the Springer Nature LaTeX template (`sn-jnl.cls`, `sn-basic.bst`).【d33bd4†L37-L104】
- **Figures and tables:** Multi-panel figures submitted as composite files, legends within manuscript, high-resolution graphics (≤10 MB each).【d33bd4†L104-L168】
- **References:** Vancouver numeric style with URLs cited in the reference list; BMC data policies encourage dataset deposition and explicit availability statements.【d33bd4†L104-L168】【b8594c†L116-L162】
- **Ethics and data:** Strongly encourages open data and source code release, aligning with Springer Nature research data policy requirements.【b8594c†L25-L116】

## Submission Checklists

### Journal of Electrocardiology
Refer to the shared checklist at `docs/journals/journal-A-checklist.md` for detailed required and recommended items compiled from the latest Guide for Authors.【F:docs/journals/journal-A-checklist.md†L1-L34】【F:docs/journals/journal-A-checklist.md†L35-L58】

### BioMedical Engineering OnLine
Refer to the shared checklist at `docs/journals/journal-B-checklist.md` for detailed required and recommended items aligned with Springer Nature’s research article instructions.【F:docs/journals/journal-B-checklist.md†L1-L39】【F:docs/journals/journal-B-checklist.md†L40-L69】

### Circulation log (2025-11-06)
- Checklists posted under `docs/journals/` and flagged for team review via repository update; no outstanding questions remain after reconciling policy pages on Elsevier and Springer Link.【F:docs/journals/journal-A-checklist.md†L1-L34】【F:docs/journals/journal-B-checklist.md†L1-L39】【F:docs/journals/journal-of-electrocardiology-2026-policy-check.md†L1-L5】【F:docs/journals/biomedical-engineering-online-2026-policy-check.md†L1-L5】

## Literature Database Coverage

| Database | Coverage Focus | Strengths | Update Frequency | Access Notes |
| --- | --- | --- | --- | --- |
| **PubMed** | Peer-reviewed biomedical and clinical ECG studies | MeSH indexing, advanced clinical filters, NIHMS compliance tracking | Daily | Free API (E-utilities) for automated alerts |
| **IEEE Xplore** | Engineering and signal-processing conference/journal articles | Full-text IEEE/IES publications, controlled vocabulary for ECG signal processing | Daily | Subscription for PDFs; metadata accessible via Institutional API |
| **arXiv (eess.SP, cs.LG, q-bio.QM)** | Preprints on novel algorithms and theoretical advances | Rapid dissemination, version history, LaTeX source availability | Twice daily batches | Free; set up RSS per category + query for “ECG” keywords |
| **bioRxiv/medRxiv** | Translational biomedical AI, regulatory updates | Preprints on clinical validation, living reviews | Daily | CC-BY licensing; requires screening for clinical trial registration |
| **Embase** | International clinical trials, device registries, conference abstracts | Emtree terms capture device/diagnostic nuance, includes grey literature | Daily | Subscription; schedule librarian export quarterly |
| **ClinicalTrials.gov / WHO ICTRP** | Ongoing interventional studies involving ECG endpoints | Regulatory compliance data, recruitment status | Continuous | Free; export XML/CSV for tracking upcoming standards |

## Section-Specific Citations for Manuscript Drafting

### Methods (algorithm design and preprocessing)
1. J. Liu *et al.*, “Frequency-Enhanced Hybrid Multimodal CNN-Transformer Network for Electrocardiogram Classification,” *Proc. 14th Int. Conf. Information Science and Technology (ICIST)*, 2024, doi:10.1109/ICIST63249.2024.10805383.
2. R. Aulia *et al.*, “Study of Arrhythmia Classification Algorithms on Electrocardiogram Using Deep Learning,” *Sinkron*, vol. 8, no. 3, 2023, doi:10.33395/sinkron.v8i3.12687.
3. N. A. M. Isa *et al.*, “Transformer-based Neural Network for Electrocardiogram Classification,” *Int. J. Adv. Comput. Sci. Appl.*, vol. 13, no. 11, 2022, doi:10.14569/IJACSA.2022.0131139.

### Results (benchmarking and clinical validation)
1. M. Bahoura, “Deep Learning-Based Sleep Apnea Detection Using Single-Lead ECG Signals from the PhysioNet Apnea-ECG Database,” *Commun. Math. Biol. Neurosci.*, 2024, doi:10.28919/cmbn/8840.
2. Y. Nugroho *et al.*, “Arrhythmia Classification Using the Deep Learning Visual Geometry Group (VGG) Model,” *Nusantara Sci. Technol. Proc.*, 2023, doi:10.11594/nstp.2023.3702.
3. X. Zhao *et al.*, “Classification of Arrhythmia by Using Deep Learning With 2-D ECG Spectral Image Representation,” *J. Popul. Ther. Clin. Pharmacol.*, vol. 30, no. 7, 2023, doi:10.47750/jptcp.2023.30.07.003.

### Discussion (clinical context, standards, and future work)
1. J. Wang *et al.*, “Self-Supervised Learning for Biomedical Signal Processing: A Systematic Review on ECG and PPG Signals,” *bioRxiv*, 2024, doi:10.1101/2024.09.30.24314588.
2. D. Pathinarupothi *et al.*, “ECG Synthesis for Cardiac Arrhythmias: Integrating Self-Supervised Learning and Generative Adversarial Networks,” SSRN preprint, 2024, doi:10.2139/ssrn.4884218.
3. J. L. Anderson *et al.*, “2023 ACC/AHA/ACCP/HRS Guideline for the Management of Patients with Atrial Fibrillation,” *J. Am. Coll. Cardiol.*, 2023, doi:10.1016/j.jacc.2023.07.002.

## Bibliography and Template Configuration

- **Journal of Electrocardiology:** Use Elsevier’s `elsarticle.cls` with `elsarticle-num.bst` (bundled in `docs/journal-styles/journal-of-electrocardiology/`). Enable numeric Vancouver references and ensure `\bibliographystyle{elsarticle-num}` in the manuscript preamble.
- **BioMedical Engineering OnLine:** Apply Springer Nature `sn-jnl.cls` and `sn-basic.bst` located under `docs/journal-styles/biomedical-engineering-online/`. Activate author-year suppression (`\bibliographystyle{sn-basic}` produces numbered Vancouver format when paired with `\bibliography{}`) and include `\jyear{2025}` metadata as required by the template.
- **Shared BibTeX practices:** Maintain separate `.bib` files per manuscript section for modular revisions, annotate entries with database source tags (e.g., `keywords = {PubMed}`), and validate with `bibtex` during CI builds (`latexmk` or `arara`). Document repository-specific citation keys to ease cross-submission conversion.

## Literature Surveillance Schedule (2024–2026)

| Quarter | Actions | Responsible Tools |
| --- | --- | --- |
| 2024 Q4 | Establish RSS/API alerts for PubMed (search: “electrocardiogram AND deep learning”), IEEE Xplore (subject: “ECG signal processing”), arXiv (daily email digest). Generate Zotero group library with automated import. | PubMed E-utilities, IEEE Alerts, arXiv API, Zotero + Better BibTeX |
| 2025 Q1–Q2 | Biannual manual review of BioMedical Engineering OnLine and Journal of Electrocardiology editorials for policy updates; refresh institutional Embase export; archive references in Git LFS snapshot for traceability. | Publisher newsletters, Embase export scheduler, GitHub Actions cron |
| 2025 Q3–Q4 | Run citation gap analysis comparing new studies vs. existing bibliography; update BibTeX keys; prepare interim memo on emerging evaluation standards (e.g., multi-lead transformer benchmarks). | OpenAlex analytics, Pandoc citeproc reports |
| 2026 Q1 | Verify compliance with any newly announced data/code mandates; adjust checklists and templates accordingly; coordinate with institutional library on APC budget updates. | SpringerOpen policy RSS, Elsevier Author Services bulletins, Notion tracker |
| 2026 Q2–Q4 | Quarterly sweep of clinical trial registries and regulatory guidance (FDA, EMA) for ECG-related AI requirements; integrate new references and annotate repository readme. | ClinicalTrials.gov API, WHO ICTRP, FDA Digital Health Center updates |

