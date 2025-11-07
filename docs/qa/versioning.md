# Manuscript Versioning Guide

This document outlines how we name tags and when to create them for the manuscript repositories (`paper`, `paper-journal-A`, and `paper-journal-B`).

## Tag Naming Convention
- Tags follow the pattern `v<major>.<minor>-<stage>`.
- `major` increments for major publication phases (e.g., acceptance-level rewrites or journal switches).
- `minor` increments for intermediate milestones inside the current phase (e.g., outline, draft, submission candidate).
- `stage` describes the deliverable state using short descriptors such as `outline`, `draft`, `submission`, or `revision`.
- Examples: `v0.1-outline` for the first outline handoff, `v0.2-draft` for the first full draft, `v1.0-submission` for the version sent to a journal.

## Criteria for Cutting a Tag
- Capture each milestone that is ready for broader review or handoff (e.g., internal QA sign-off, stakeholder review, or journal submission).
- Tag after integrating all feedback for the milestone and updating the relevant `CHANGELOG.md` with the user-facing summary.
- Ensure that supporting assets (figures, tables, supplementary files) referenced in the milestone are committed and cross-checked.
- When backporting fixes to an older milestone, use an incremented minor version with a `-hotfix` stage (e.g., `v0.1-hotfix`).

## Release Notes Expectations
- Every tagged release should have a corresponding entry in the appropriate `CHANGELOG.md` that mirrors the `Added/Changed/Fixed` structure.
- Highlight concrete manuscript changes (new sections, reordered figures, resolved reviewer concerns) rather than implementation details.
- Link to the tag or commit hash within the release notes when publishing summaries in progress trackers or status updates.
