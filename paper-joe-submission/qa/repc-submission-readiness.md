# Revista Portuguesa de Cardiologia (REPC) submission readiness

Status date: 2026-08-29

## Canonical lineage

- Scientific baseline: final Journal of Electrocardiology manuscript branch `joe-editorial-rewrite-2026-08-10`, commit `1d79b7012085fdce66474f1c688ec7833f323aeb`.
- REPC adaptation: `repc-submission`, currently 11 commits ahead of the JoE baseline and 0 commits behind it.
- Active finalization branch: `repc-finalization-2026-08-29`, created from the current `repc-submission` head.
- Do not restart from `main`; it diverged from the final JoE/REPC manuscript lineage.

## Manual-file reconciliation

- The later manually supplied manuscript PDF is the copy that includes the Vahid Torkzadeh CRediT contribution; the older copy without that contribution must not be used as the canonical manuscript.
- The standalone title-page PDF supplied manually predates the REPC-specific title-page source and is reference-only.
- The generic `graphical_abstract.pdf` copies are legacy assets; the numbered REPC `04_Graphical_Abstract` source/output is canonical for this submission.
- The author-declarations DOCX is the source of truth for the informed-consent/ethics wording and must remain consistent with the manuscript and separate ethics statement.

## REPC-required gates

### Implemented on this branch

- [x] Target journal set to Revista Portuguesa de Cardiologia.
- [x] Structured English abstract heading changed from `Background` to `Introduction and Objectives`.
- [x] Portuguese title/abstract/keywords submission file added.
- [x] Exact no-conflict summary wording added: `Declarations of interest: none.`
- [x] Generative-AI disclosure heading and statement aligned to the journal's current author guide.
- [x] Data Availability exposes both the public GitHub repository and an immutable versioned release.
- [x] Workflow builds manuscript and ancillary files from source.
- [x] Workflow includes the Declaration of Interest PDF and Portuguese metadata PDF.

### Author-supplied blockers before final upload

- [x] Publication-style postal affiliation added: Department of Computer Engineering, Mashhad Branch, Islamic Azad University, Mashhad 9187147578, Iran; final author confirmation remains recommended at portal entry.
- [ ] Confirm the exact wording/name of affiliation 2 (`Ma.C., Islamic Azad University`) as it should appear in publication metadata.
- [ ] Add the final manuscript word count to the title page after the final automated count.
- [ ] Author/professional check of the Portuguese (Portugal) title, abstract and keywords.
- [ ] Confirm the AI-use statement accurately describes the authors' actual use and approve it.
- [ ] Complete the journal's official detailed Declaration of Interest form; the local PDF is a summary/supporting document, not a substitute for the journal form.

### Automated/preflight checks still required

- [x] Compile the manuscript and every ancillary TeX file without errors (local TinyTeX preflight).
- [x] Draft graphical abstract is horizontal and 4200 x 1860 px at 300 dpi, exceeding the journal minimum; final policy-compliant human/non-generative recreation remains a separate provenance gate.
- [x] All 24 active in-text citation keys are present in the bibliography; uncited library entries are not emitted by BibTeX.
- [x] All 24 active references carry DOI/persistent identifiers and were resolver/bibliographic-audited.
- [ ] Verify final PDF visually for figure/table placement, line breaks, hyperlinks and no clipping/overlap.

## Reproducibility link policy

The experimental outputs are unchanged from the verified software snapshot. Until a journal-neutral release alias is intentionally created, cite the existing immutable release rather than a moving branch. The public repository root is also linked for ongoing development.


### Non-automatable author confirmations

- [ ] Authors confirm the publication spelling and postal affiliation used in the submission metadata.
- [ ] Authors confirm the Portuguese (Portugal) translation or obtain a human language review.
- [ ] Authors confirm the AI-use statement accurately describes the writing assistance.
- [ ] The mandatory graphical abstract is recreated or independently approved using a journal-permitted non-generative scientific/professional illustration workflow; the current AI-assisted TikZ draft is retained only as a layout/data specification and must not be uploaded as the final graphical abstract.
- [ ] Complete the journal's official detailed Declaration of Interest form in the submission system.


### Automated manuscript-size audit

- [x] Main text word count: 2,338 words (Introduction through Conclusions; excludes abstract, references, tables/figure content, declarations, and supplementary material), below the current 5,000-word Original Investigation limit.
- [x] Structured English abstract: 208 whitespace-delimited source words, below the current 250-word limit.
- [x] Keywords: 6, within the current 3--10 keyword range.
- [x] Active bibliography citations: 24 unique references, below the current limit of 75.

- [x] Supplementary material separated from the primary manuscript into its own upload-ready PDF source.
