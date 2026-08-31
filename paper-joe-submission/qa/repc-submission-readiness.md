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
- [ ] Add the final manuscript word count to the title page after the final texcount pass.
- [ ] Author/professional check of the Portuguese (Portugal) title, abstract and keywords.
- [ ] Confirm the AI-use statement accurately describes the authors' actual use and approve it.
- [ ] Complete the journal's official detailed Declaration of Interest form; the local PDF is a summary/supporting document, not a substitute for the journal form.

### Automated/preflight checks still required

- [ ] Compile the manuscript and every ancillary TeX file without errors.
- [ ] Verify the graphical abstract is horizontal and at least 1328 x 531 px (or proportional equivalent) and readable at the journal's stated display size.
- [ ] Verify all references cited in text are present in the bibliography and vice versa.
- [ ] Audit DOI/persistent identifiers and bibliographic completeness for the final reference list.
- [ ] Verify final PDF visually for figure/table placement, line breaks, hyperlinks and no clipping/overlap.

## Reproducibility link policy

The experimental outputs are unchanged from the verified software snapshot. Until a journal-neutral release alias is intentionally created, cite the existing immutable release rather than a moving branch. The public repository root is also linked for ongoing development.
