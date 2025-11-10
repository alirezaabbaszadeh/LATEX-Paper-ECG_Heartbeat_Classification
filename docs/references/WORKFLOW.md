# Reference Management Workflow

This workflow explains how contributors should update the project's `.bib` files and request review for citation changes.

## Editing `.bib` Files via GitHub

You can update references directly from the GitHub web interface when making small edits.

1. Navigate to the `.bib` file that needs modification.
2. Click **Edit this file** (pencil icon) and apply your changes.
3. Ensure citation keys follow the `AuthorYearKeyword` pattern. Use the primary author's surname, publication year, and a short unique keyword, e.g., `Smith2021Arrhythmia` or `Garcia2019DeepLearning`.
4. At the bottom of the editor, add a concise commit message (see [Commit Message Guidelines](#commit-message-guidelines)).
5. Select **Create a new branch for this commit**, provide a descriptive branch name, and click **Propose changes**.
6. Open a pull request (PR) against the default branch and follow the review request instructions below.

## Editing `.bib` Files Locally

For larger edits or when working offline, update references locally.

1. Create a feature branch: `git checkout -b feature/update-references`.
2. Modify the required `.bib` files in your editor, following the `AuthorYearKeyword` citation key style (e.g., `Lee2020TransferLearning`).
3. Run any relevant checks or formatters.
4. Stage and commit your changes with an informative message (see [Commit Message Guidelines](#commit-message-guidelines)).
5. Push the branch to your fork: `git push origin feature/update-references`.
6. Open a PR on GitHub and complete the review request steps.

## Commit Message Guidelines

Clear commit messages make it easier to review reference updates:

- Start with a verb in the imperative mood (e.g., `Add`, `Update`, `Fix`).
- Mention the affected `.bib` file or the nature of the reference change (e.g., `Update citations in references/ecg.bib`).
- If multiple references are updated, summarize the scope succinctly.
- Avoid generic messages such as "misc updates".

## Opening Pull Requests and Requesting Review

When your branch is ready:

1. Draft the PR with a summary of the reference changes and highlight any new sources.
2. Add labels or link issues as appropriate.
3. Request reviewer assignment by tagging a maintainer in a PR comment (e.g., `@maintainer Please review the updated references.`) or using the GitHub "Request a review" feature if you have permissions.
4. Monitor the PR for feedback and apply follow-up commits using the same commit message principles.

Following this workflow keeps the bibliography consistent and ensures timely reviews for reference updates.

## Handling BibTeX Lint Workflow Failures

Every pull request automatically runs the **BibTeX Lint** GitHub Actions workflow against both bibliography files (`references/journal-A/references.bib` and `references/journal-B/references.bib`). If the workflow detects malformed entries, it will:

- Fail the `BibTeX Lint` check in the PR status list.
- Post a PR comment summarizing the validation output from `biber --tool` so you can see which entries need attention.

When the workflow fails:

1. Open the PR conversation tab and locate the comment labelled **BibTeX Lint Report**.
2. Review the error messages for each `.bib` file. Typical issues include missing required fields, unmatched braces, or invalid characters.
3. Fix the highlighted problems locally and re-run the validation command to confirm:

   ```bash
   biber --tool --validate-datamodel references/journal-A/references.bib
   biber --tool --validate-datamodel references/journal-B/references.bib
   ```

4. Commit and push your corrections. The workflow re-runs automatically and will clear once the bibliographies pass validation.

Reach out to the maintainers if the comment output is unclear or you need help interpreting a specific message.
