# BioMedical Engineering OnLine Manuscript Workspace

This directory prepares an author-ready LaTeX skeleton aligned with BioMedical Engineering OnLine policies summarized in [`../journals.md`](../journals.md).

## Directory layout

- `main.tex` – orchestrates the manuscript and mandatory declarations.
- `preamble.tex` and `macros.tex` – packages, spacing, line numbers, and helper commands.
- `sections/` – modular content files mirroring the journal's required headings.
- `bibliography/references.bib` – BibTeX database compiled with `natbib` (unsorted numeric style).
- `figures/` – destination for final submission-ready figures (≤10 MB each).
- `supplementary/main.tex` – entry point for additional files uploaded to BMC's system.

## Building locally

```bash
latexmk -pdf main.tex
```

Line numbers are enabled by default through `lineno`. Disable by removing `\linenumbers` in `preamble.tex` if not needed.

## Journal-specific checklist hooks

- Explicit sections for data availability, ethics, competing interests, funding, and author contributions.
- Double-line spacing and line numbers for peer review, as requested by BMC.
- Numerical citations produced via `natbib` using `unsrtnat` to preserve order of appearance.

## Independent repository bootstrapping

Run `../scripts/bootstrap_journal_repos.sh` to materialize this directory as its own Git repository with distinct remotes. Example:

```bash
../scripts/bootstrap_journal_repos.sh \
  --journal paper-journal-B \
  --target ../deploy \
  --primary git@gitlab.com:example-group/paper-journal-B.git \
  --overleaf https://git.overleaf.com/your-overleaf-project-id
```

The script creates `../deploy/paper-journal-B`, initializes Git history, and adds a GitLab `origin` plus an Overleaf remote for collaborative editing.
