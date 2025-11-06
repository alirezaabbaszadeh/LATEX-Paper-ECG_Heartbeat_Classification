# BioMedical Engineering OnLine Manuscript Workspace

This directory prepares an author-ready LaTeX skeleton aligned with BioMedical Engineering OnLine policies summarized in [`../journals.md`](../journals.md). The template now relies on Springer Nature's official `sn-jnl` class with the numbered citation style expected by BMC.

## Directory layout

```
paper-journal-B/
├── bib/                 # BibTeX database(s)
├── figures/             # Submission-ready figures
├── src/
│   ├── main.tex         # Entry point compiled with latexmk
│   ├── macros.tex       # Custom commands
│   ├── preamble.tex     # Package and formatting configuration
│   └── sections/        # Modular manuscript content
├── supplementary/       # Appendix and supplementary text
├── templates/           # Bundled sn-jnl class and BST files
└── tables/              # Table source files (CSV/TeX)
```

## Building locally

```bash
cd paper-journal-B
latexmk -pdf -cd src/main.tex
```

`latexmk` uses `bibtex` under the hood to satisfy the `sn-basic` bibliography style included with the Springer template. Clean build artifacts with `latexmk -c -cd src/main.tex` so the command runs from the `src/` directory and removes intermediate files.

## Journal-specific checklist hooks

- Double-line spacing and line numbers activated automatically at the start of the document.
- Mandatory editorial statements (data availability, ethics, competing interests, funding, contributions) broken into dedicated sections.
- Numerical references rendered with the `sn-basic` style to preserve order of appearance.

## Overleaf usage

1. Create a new Overleaf project and choose "Upload Project".
2. Zip the contents of `paper-journal-B/` (excluding any previous `_latexmk/` build directory) and upload the archive.
3. Set the main document to `src/main.tex` in the Overleaf settings so the compiler runs from the new source tree.
4. Keep the compiler set to `Latexmk`. Overleaf provides the official `sn-jnl` class; the identical files from its public template mirror are stored locally under `templates/` for reproducibility.
