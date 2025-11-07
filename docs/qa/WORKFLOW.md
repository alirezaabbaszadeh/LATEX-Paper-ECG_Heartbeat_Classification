# QA Workflow

This document outlines how we coordinate quality assurance (QA) reviews for the manuscript and supporting assets. Use it alongside the issue template in `.github/ISSUE_TEMPLATE/review.yml` to keep findings consistent and traceable.

## Process Overview

1. **Scope the review.** Identify the manuscript sections, figures, or supplementary files relevant to your assignment.
2. **Capture precise references.** Link directly to LaTeX source files (and line ranges when possible) so authors can locate the context instantly.
3. **Assess severity.** Apply the severity labels defined below to communicate urgency and impact.
4. **File an issue.** Use the QA Review issue template to document findings, attach checklist links, and summarize remediation steps.
5. **Follow through.** Track fixes, update checklists, and close the issue when the problem is resolved or deferred.

## Label Conventions

| Label | Purpose |
| --- | --- |
| `qa-review` | Automatically applied by the issue template to flag QA review threads. |
| `qa-methods` | Findings affecting the Methods section or methodological descriptions. |
| `qa-results` | Issues involving Results narratives, statistics, or tables. |
| `qa-figures` | Problems with figures, captions, or visual assets. |
| `qa-data` | Concerns about datasets, preprocessing, or availability statements. |
| `qa-ethics` | Ethics approvals, consent statements, or compliance documentation. |
| `qa-style` | Stylistic or formatting deviations from journal requirements. |
| `qa-severity:critical` | Blocking issues that jeopardize publication (e.g., methodological flaws, missing approvals). |
| `qa-severity:major` | High-impact issues that require significant revisions before submission. |
| `qa-severity:minor` | Low-impact issues that should be fixed but are unlikely to block submission. |
| `qa-severity:info` | Informational notes or suggestions that do not require immediate action. |

> **Tip:** Apply topical labels (e.g., `qa-methods`, `qa-figures`) alongside a single severity label to keep triage queues meaningful.

## Review Checklist

Use this checklist when completing QA reviews. Link to the relevant item(s) from the issue template under **Checklist Links**.

- Methods describe sampling, preprocessing, and model training steps.
- Results include correct metric definitions, confidence intervals, and cohort counts.
- Figures follow journal resolution, caption, and legend requirements.
- Data availability statements match repository contents and licensing terms.
- Ethics and consent statements meet institutional and journal policies.
- Terminology, abbreviations, and references follow the target journal style guide.

## Example Issues with File References

When reporting issues, link to the exact file and line range. The examples below show preferred formatting using GitHub line anchors.

### Example 1 — Missing cross-validation details

```
paper/sections/methods.tex#L38-L72 — Cross-validation folds are not described; need to reference `scripts/train_kfold.py` outputs for clarity.
```

### Example 2 — Figure caption mismatch

```
paper/figures/roc_curve.tex#L12-L34 — Caption lists ``N=220`` while figure source `docs/figures/roc-summary.csv` shows 215 records.
```

### Example 3 — Data availability statement

```
paper/sections/discussion.tex#L120-L150 — Data availability mentions Zenodo DOI `10.5281/zenodo.1234567`, but repository README cites `10.5281/zenodo.7654321`.
```

Include similar line-anchored references in the **Section References** field of the QA Review issue template so authors can jump straight to the relevant source.

## Rerunning Failed QA Workflows

- Navigate to the **Actions** tab and open the failed `QA` workflow run.
- Click **Re-run jobs** > **Re-run all jobs** to execute every stage (LaTeX lint, figure validation, references) with the latest commits.
- For permission-restricted reruns (e.g., community contributors), ask a maintainer to trigger the rerun or push a no-op commit to retrigger the workflow automatically.

## Troubleshooting Workflow Logs

- Open the failed job (e.g., *LaTeX lint (chktex)* or *Figure format validation*) to inspect step-by-step logs.
- Expand the step showing a red ❌ icon to read the full error output. Pay attention to GitHub log annotations such as `::error file=...` emitted by the automation scripts.
- Download logs via **Download log archive** when you need to share them asynchronously or annotate them offline.
- After addressing the reported issues locally (e.g., running `chktex` or `python paper/scripts/check_figure_formats.py`), push the fixes and rerun the workflow to confirm the resolution.
