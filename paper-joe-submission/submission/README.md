# Journal of Electrocardiology submission package notes

This directory contains submission-facing text files kept separate from the main LaTeX source.

## Included files

- `Highlights.txt` — five editable highlights; every bullet is below the journal's 85-character maximum.
- `Figure_Captions.txt` — captions for the three retained study figures in manuscript order.

## Main manuscript

Build from `paper-joe-submission/src/`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The manuscript is double-spaced and uses editable LaTeX tables.

## Artwork policy decision

The current Journal of Electrocardiology / Elsevier guide does not permit generative-AI or AI-assisted tools to create or alter submitted artwork, including graphical abstracts. For that reason, visual concepts created during the present AI-assisted editorial session are not included as submission figures or a graphical abstract.

The manuscript retains the pre-existing author/study-generated confusion matrix, ROC curves, and precision--recall curves. Their captions and narrative placement have been improved without changing the image content. A text-only redesign specification is stored under `qa/visual-redesign-spec.md` if the authors wish to recreate additional artwork manually and independently before submission.

## Editorial evidence boundary

The source of truth for quantitative wording is `qa/claim-ledger.md`. Do not strengthen a claim beyond that ledger without adding and verifying new experimental evidence.

## Required author-side checks before upload

- Confirm the full postal affiliation/contact details required by the submission system.
- Review and approve every AI-assisted textual change.
- Keep the generative-AI declaration immediately before the references.
- If new artwork or a graphical abstract is added, create it without generative-AI assistance and re-check the current journal policy.
