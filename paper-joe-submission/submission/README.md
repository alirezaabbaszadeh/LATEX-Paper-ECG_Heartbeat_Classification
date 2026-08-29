# Revista Portuguesa de Cardiologia submission package

This directory contains the submission-facing files for the **Revista Portuguesa de Cardiologia (REPC)** adaptation of the final Journal of Electrocardiology scientific manuscript.

The historical parent directory name `paper-joe-submission` is intentionally retained so the manuscript lineage remains traceable. The active finalization branch is `repc-finalization-2026-08-29`.

## Canonical submission files

- `01_Cover_Letter_Revista_Portuguesa_de_Cardiologia.pdf` — journal-specific cover letter.
- `02_Manuscript_Record_Level_ECG_Classification.pdf` — current manuscript built from `../src/main.tex`.
- `03_Ethical_Statement.pdf` — separate ethics statement.
- `04_Graphical_Abstract.pdf` and `04_Graphical_Abstract.png` — journal-facing graphical abstract.
- `05_Title_Page_with_Author_Details.pdf` — separate title page and author metadata.
- `06_Declaration_of_Interest_Statement.pdf` — concise no-interest statement; the journal's official disclosure form must still be completed if requested by the submission system.
- `07_Portuguese_Title_Abstract_Keywords.pdf` — Portuguese title, structured abstract and keywords for submission metadata.
- `Highlights.txt` — legacy Elsevier highlights retained as an editable auxiliary file.
- `Figure_Captions.txt` — editable figure captions/disclosures.

Legacy JoE PDFs remain only for provenance and must not be uploaded in place of the numbered REPC files.

## Manuscript source

Build from `paper-joe-submission/src/`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The paper uses editable LaTeX tables and vector TikZ figures where applicable. Quantitative claims must remain consistent with `../qa/claim-ledger.md` and the archived prediction artifacts.

## Reproducibility links

The manuscript links to:

1. the public development repository:
   `https://github.com/alirezaabbaszadeh/ECG_Heartbeat_Classification`
2. the immutable experimental snapshot:
   `v1.0-joe-submission`

The release name retains the original JoE provenance because the experimental results have not changed. A moving branch must not replace the immutable snapshot as the reproducibility citation.

## Quality gate

See `../qa/repc-submission-readiness.md` for the final submission blockers and verification checklist. In particular, full postal affiliations, manuscript word count, Portuguese-language author review, and final author approval of the AI disclosure are still required before upload.

The GitHub Actions workflow `.github/workflows/repc-finalize-submission.yml` compiles the manuscript and all numbered ancillary TeX files, creates a 300-dpi graphical-abstract PNG, checks key manuscript statements, checks minimum graphical-abstract pixel dimensions, and publishes the current build artifacts back to the active branch.
