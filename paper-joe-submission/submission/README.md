# Journal of Electrocardiology submission package notes

This directory contains submission-facing files kept separate from the main LaTeX source.

## Included files

- `ECG_JoE_Manuscript_Final.pdf` — built manuscript with the current author metadata.
- `Highlights.txt` — five editable highlights; every bullet is below 85 characters.
- `Figure_Captions.txt` — captions/disclosures for the four main figures in manuscript order.

## Main manuscript

Build from `paper-joe-submission/src/`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The manuscript is double-spaced and uses editable LaTeX tables and TikZ vector figures.

## Figure policy and disclosure

Current Elsevier policy permits AI-assisted explanatory images and reproducible data visualisations when their use is transparent and the underlying scientific content is not fabricated or altered. The four main TikZ figures therefore include explicit caption disclosure, and the Methods section identifies OpenAI ChatGPT (GPT-5.6 Sol), the purpose of its use, and the evidence source. The supplementary confusion matrix, ROC curves, and precision--recall curves were regenerated deterministically from the unchanged archived prediction arrays.

A graphical abstract generated with a general-purpose generative-AI tool is not included. If one is added, it should use a journal-compatible dedicated scientific/professional illustration workflow and be checked against the current policy at submission time.

## Editorial evidence boundary

The source of truth for quantitative wording and figure labels is `qa/claim-ledger.md`. Do not strengthen a claim or change a plotted value beyond that ledger without adding and verifying new experimental evidence.

## Required author-side checks before upload

- Confirm full postal affiliation/contact details required by the submission system.
- Review and approve every AI-assisted textual and visual revision.
- Convert the working AI declaration to final author-approved wording before upload.
- Create a versioned/immutable repository release and cite it in the Data Availability statement.
- Confirm the regenerated diagnostic PNGs and final 23-page production PDF.
- Re-check the journal's current AI/artwork instructions on the actual submission date.
