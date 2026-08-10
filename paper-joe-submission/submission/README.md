# Journal of Electrocardiology submission package notes

This directory contains submission-facing text files that are kept separate from the main LaTeX source.

## Included files

- `Highlights.txt` — five editable highlights; every bullet is below the journal's 85-character maximum.
- `Figure_Captions.txt` — captions for the four main figures in manuscript order.

## Main manuscript

Build from `paper-joe-submission/src/`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The manuscript is double-spaced and uses editable LaTeX tables and TikZ text graphics.

## Graphical abstract

The editable source is `paper-joe-submission/figures/graphical_abstract.tex`, which reuses `graphical_abstract_panel.tex`. Build it as a separate PDF with:

```bash
cd paper-joe-submission/figures
latexmk -pdf -interaction=nonstopmode -halt-on-error graphical_abstract.tex
```

The inherited Git-LFS PDF pointer from the base manuscript was intentionally removed so that the submission asset is regenerated from the revised vector source rather than mistaken for the old artwork.

## Main figures

The manuscript embeds the following vector TikZ sources:

1. `figures/pipeline_diagram.tex`
2. `figures/model_comparison.tex`
3. `figures/class_performance.tex`
4. `figures/error_structure.tex`

These sources can be wrapped in the LaTeX `standalone` class to export one-page vector PDFs for upload as individual artwork files. During QA, all four were exported successfully and inspected visually.

## Editorial evidence boundary

The source of truth for quantitative wording is `qa/claim-ledger.md`. Do not strengthen a claim beyond that ledger without adding and verifying new experimental evidence.
