# Journal of Electrocardiology Manuscript Workspace

This directory provides an author-ready LaTeX skeleton tailored to the Journal of Electrocardiology requirements documented in [`../journals.md`](../journals.md). It now builds directly on Elsevier's official `elsarticle` class and numeric bibliography style.

## Directory layout

```
paper-journal-A/
├── bib/                 # BibTeX database(s)
├── figures/             # Submission-ready figures
├── src/
│   ├── main.tex         # Entry point compiled with latexmk
│   ├── macros.tex       # Custom commands
│   ├── preamble.tex     # Package and formatting configuration
│   └── sections/        # Modular manuscript content
├── supplementary/       # Appendix and supplementary text
├── templates/           # Bundled elsarticle class and BST files
└── tables/              # Table source files (CSV/TeX)
```

## Building locally

```bash
cd paper-journal-A
latexmk -pdf -cd src/main.tex
```

`latexmk` automatically invokes `bibtex` (via the `elsarticle-num` style) to respect the journal's numeric reference format. Clean artifacts with `latexmk -c -cd src/main.tex`.

## Journal-specific checklist hooks

- Highlights provided with the official `highlights` environment within the `frontmatter` block.
- Numerical references generated with `bibtex` and the `elsarticle-num` style to respect order of appearance.
- Data availability statement sectioned explicitly after the discussion, following Elsevier Option B guidance.

## Overleaf usage

1. Create a new Overleaf project using the "Upload Project" option.
2. Zip the contents of `paper-journal-A/` (excluding the `latexmk` build directory if present) and upload the archive.
3. Set the main file to `src/main.tex` in Overleaf's project settings.
4. Enable the `latexmk` compiler in Overleaf (Menu → Settings → Compiler → `Latexmk`), which matches the local workflow.

Overleaf automatically provides Elsevier's `elsarticle` class, but this repository also ships the exact class and bibliography style under `templates/` for reproducible offline builds.
