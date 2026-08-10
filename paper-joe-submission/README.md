# Journal of Electrocardiology — submission-oriented revision

This directory is the independent editorial revision of `paper-journal-A/`. It was created from an exact copy of the base manuscript and is the only manuscript folder edited on branch `joe-editorial-rewrite-2026-08-10`.

## Revision purpose

The manuscript has been reframed around a subject-separated ECG benchmark, controlled architecture comparisons, and transparent rare-rhythm failure analysis. Quantitative wording and figure labels are constrained by `qa/claim-ledger.md`; editorial strengthening must not introduce new experiments, metrics, cohorts, or clinical-readiness claims.

## Directory layout

```text
paper-joe-submission/
├── bib/                 # BibTeX database
├── figures/             # Editable TikZ summaries + archived-prediction diagnostic plots
├── qa/                  # Claim ledger, compliance notes, visual evidence map
├── submission/          # Standalone highlights/captions and upload notes
├── src/
│   ├── main.tex         # Manuscript entry point
│   ├── preamble.tex
│   └── sections/        # Modular manuscript sections
├── supplementary/       # Extended methods and diagnostic figures
├── templates/           # Elsevier class/BST files
└── tables/              # Editable table sources
```

## Building locally

Git LFS must be materialized because the original confusion-matrix, ROC, and precision--recall PNG files are tracked as LFS objects.

```bash
cd paper-joe-submission
latexmk -pdf -cd src/main.tex
```

Generated files under `src/` are ignored and should not be committed. The branch also contains `.github/workflows/joe-submission-build.yml`, which checks base-folder integrity, prohibited claim language, LFS figure materialization, unresolved references, and overfull boxes before uploading a manuscript preview.

## AI-assisted preparation disclosure

OpenAI ChatGPT (GPT-5.6 Sol) assisted with language/editorial revision, identification and formatting of ten topical *Journal of Electrocardiology* references, and LaTeX/TikZ code for explanatory/data-summary figures. The research data, stored predictions, and experimental results were not generated or altered by the tool. Bibliographic metadata and DOIs for the added references were checked against publisher and DOI records. The manuscript includes a working AI declaration before the references and figure-specific disclosure for AI-assisted visualisations. The author must review and approve the final wording, visual content, and bibliographic additions before submission.

No graphical abstract made with a general-purpose generative-AI tool is included.

## Submission-facing files

See `submission/README.md` for final author-side checks. The most important remaining items are author approval of the AI-assisted revision, full affiliation/contact verification, creation of an immutable repository release for citation, and a final check of the journal's current Guide for Authors on the actual submission date.
