# Journal of Electrocardiology Manuscript Workspace

This directory provides an author-ready LaTeX skeleton tailored to the Journal of Electrocardiology requirements documented in [`../journals.md`](../journals.md).

## Directory layout

- `main.tex` – compiles the manuscript using `biblatex` with the numeric style required by the journal.
- `preamble.tex` and `macros.tex` – shared packages and custom commands.
- `sections/` – structured content files (highlights, abstract, body sections, compliance statements).
- `bibliography/references.bib` – central BibTeX database for the manuscript.
- `figures/` – folder for final figures that meet Elsevier resolution standards.
- `supplementary/main.tex` – entry point for supplementary material submitted alongside the manuscript.

## Building locally

```bash
latexmk -pdf main.tex
```

The default preamble uses `biber`. Run `latexmk -pdf -bibtex main.tex` if you prefer BibTeX.

## Journal-specific checklist hooks

- Highlights block included before the abstract (3–5 bullets ≤85 characters).
- Numerical references generated with `biblatex` numeric style and `sorting=none`.
- Dedicated Data Availability section in accordance with Elsevier Option B expectations.

## Independent repository bootstrapping

Use `../scripts/bootstrap_journal_repos.sh` to clone this layout into a standalone Git repository, commit the initial version, and register remotes. Example:

```bash
../scripts/bootstrap_journal_repos.sh \
  --journal paper-journal-A \
  --target ../deploy \
  --primary git@github.com:example-org/paper-journal-A.git \
  --overleaf https://git.overleaf.com/your-overleaf-project-id
```

This creates `../deploy/paper-journal-A` as an independent Git repository with the provided GitHub `origin` and Overleaf remote.
