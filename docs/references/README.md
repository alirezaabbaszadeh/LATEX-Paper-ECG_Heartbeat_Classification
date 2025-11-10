# Reference Asset Layout

This directory documents how bibliography resources are organized for the ECG heartbeat classification manuscripts. Use it as the entry point when adding new reference entries or updating journal-specific styles.

## Directory Overview

- `references/journal-A/` – Elsevier resources for Journal~A submissions.
  - `references.bib` holds Journal~A references. Add new entries here when targeting the Elsevier manuscript template.
  - `elsarticle-num.bst` and `elsarticle.cls` are the accompanying BibTeX style and document class copied from the official template.
- `references/journal-B/` – Springer resources for Journal~B submissions.
  - `references.bib` stores Journal~B references.
  - `sn-basic.bst` and `sn-jnl.cls` are the BibTeX style and document class distributed with the Springer template.
- `tests/reference-smoke/main.tex` – A lightweight TeX file that exercises each bibliography/style pair to confirm Overleaf (or local LaTeX) builds can locate them.

## Adding or Updating References

1. Identify the journal target and open the matching `.bib` file above.
2. Follow the citation key conventions described in [`WORKFLOW.md`](WORKFLOW.md) when inserting new entries.
3. Keep journal-specific references scoped to their respective `.bib` files. Shared citations can be duplicated if both journals require them.

## Updating Journal Styles

- Replace the `.bst` or `.cls` file in the appropriate `references/journal-*` directory when journals publish a new template version.
- Commit updates together with a short summary of the journal change and include any relevant release notes in the PR description.
- Run the smoke test (`tests/reference-smoke/main.tex`) in Overleaf or your local LaTeX toolchain to ensure the new styles are resolved correctly.
