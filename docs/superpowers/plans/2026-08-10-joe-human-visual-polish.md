# JoE Human Narrative & Visual Clarity Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the Journal of Electrocardiology revision more natural, persuasive, and visually readable without changing any experimental evidence.

**Architecture:** Work only inside `paper-joe-submission/` on branch `joe-editorial-rewrite-2026-08-10`. First rewrite the narrative-bearing sections, then simplify the four deterministic TikZ figures and their captions, then run evidence/claim and LaTeX quality gates. The base `paper-journal-A/` folder remains untouched.

**Tech Stack:** LaTeX (`elsarticle`), TikZ, BibTeX, GitHub branch workflow, local `pdflatex`/`bibtex` QA harness.

## Global Constraints

- No new experiments, model runs, metrics, or inferred numerical results.
- Every quantitative statement must remain traceable to `paper-joe-submission/qa/claim-ledger.md`.
- Comparative claims remain limited to the four architectures evaluated on the common held-out split.
- No SOTA, clinical-readiness, autonomous-diagnosis, deployment, or external-generalisation claims.
- Post-hoc threshold/calibration analyses remain explicitly descriptive rather than independently validated.
- Abstract must remain below 250 words.
- `paper-journal-A/` must remain unchanged.

---

### Task 1: Rewrite the narrative spine

**Files:**
- Modify: `paper-joe-submission/src/sections/abstract.tex`
- Modify: `paper-joe-submission/src/sections/introduction.tex`
- Modify: `paper-joe-submission/src/sections/discussion.tex`
- Modify: `paper-joe-submission/src/sections/conclusion.tex`

**Interfaces:**
- Consumes: exact evidence in `paper-joe-submission/qa/claim-ledger.md`.
- Produces: authorial prose that later Results/captions can echo without adding claims.

- [ ] **Step 1:** Rewrite the Abstract as problem -> protocol -> two-sided result -> implication, retaining the current key metrics and held-out counts.
- [ ] **Step 2:** Count the Abstract conservatively after stripping LaTeX commands; require fewer than 250 words.
- [ ] **Step 3:** Rewrite the Introduction into four connected paragraphs: clinical/technical problem, evaluation protocol, representation hypothesis, study purpose/contribution.
- [ ] **Step 4:** Rewrite the Discussion so each paragraph answers one reasoning question and headline metrics are not redundantly repeated.
- [ ] **Step 5:** Rewrite the Conclusion into three compact ideas: controlled-benchmark gain, rare-rhythm bottleneck, next validation step.
- [ ] **Step 6:** Scan the four files for prohibited claim phrases and compare all retained numbers against the claim ledger.
- [ ] **Step 7:** Commit the narrative pass.

### Task 2: Redesign Figure 1 and Figure 2 for journal-scale readability

**Files:**
- Modify: `paper-joe-submission/figures/pipeline_diagram.tex`
- Modify: `paper-joe-submission/figures/model_comparison.tex`
- Modify: `paper-joe-submission/src/sections/methods.tex`
- Modify: `paper-joe-submission/src/sections/results.tex`

**Interfaces:**
- Consumes: split counts and model-level metrics from the claim ledger.
- Produces: compact deterministic TikZ graphics embedded by Methods/Results.

- [ ] **Step 1:** Convert the workflow to a two-lane diagram with development and held-out lanes, large cohort counts, and a dashed post-hoc branch.
- [ ] **Step 2:** Rebuild the model comparison with larger text, reduced legend density, exact bar-end values, and clear emphasis on the proposed model.
- [ ] **Step 3:** Shorten Methods/Results captions so scientific interpretation comes first and disclosure text is concise.
- [ ] **Step 4:** Compile a standalone/harness preview of both figures; reject overlap, clipping, or text too small at normal PDF zoom.
- [ ] **Step 5:** Commit Figure 1/2 changes.

### Task 3: Redesign Figure 3 and Figure 4 around the rare-rhythm finding

**Files:**
- Modify: `paper-joe-submission/figures/class_performance.tex`
- Modify: `paper-joe-submission/figures/error_structure.tex`
- Modify: `paper-joe-submission/src/sections/results.tex`

**Interfaces:**
- Consumes: class support, F1/AUC, confusion counts, and threshold diagnostics from the claim ledger.
- Produces: two primary figures that make the class-specific bottleneck visible without a dense text block.

- [ ] **Step 1:** Increase row spacing and label size in the class-performance figure; show support as a separate label and visually de-emphasise Q (`n=2`).
- [ ] **Step 2:** Make the SVEB contrast (AUC 0.67 vs F1 0.00) immediately legible.
- [ ] **Step 3:** Simplify the error-structure figure to three dominant confusion pathways plus two compact threshold callouts.
- [ ] **Step 4:** Rewrite corresponding captions to state the take-home result and preserve the post-hoc qualification.
- [ ] **Step 5:** Compile and visually inspect both figures for clipping/readability.
- [ ] **Step 6:** Commit Figure 3/4 changes.

### Task 4: Improve Results transitions and table presentation

**Files:**
- Modify: `paper-joe-submission/src/sections/results.tex`
- Modify only if needed: `paper-joe-submission/tables/cohort_distribution.tex`
- Modify only if needed: `paper-joe-submission/tables/test_metrics.tex`
- Modify only if needed: `paper-joe-submission/tables/class_metrics.tex`

**Interfaces:**
- Consumes: completed figures and narrative spine.
- Produces: a Results section where every subsection has one question, one evidence block, and one interpretation.

- [ ] **Step 1:** Add short transitions that connect cohort imbalance to aggregate comparison and aggregate comparison to class-specific failure.
- [ ] **Step 2:** Remove duplicated interpretive sentences now carried by figures/captions.
- [ ] **Step 3:** Keep tables numerically complete but shorten captions and unnecessary prose if visual hierarchy can do the work.
- [ ] **Step 4:** Run a numeric consistency scan between Results, Tables, Abstract, and TikZ source values.
- [ ] **Step 5:** Commit Results/table polish.

### Task 5: Full manuscript QA and review PDF

**Files:**
- Verify: `paper-joe-submission/src/main.tex` and all included sections.
- Update: `paper-joe-submission/qa/submission-readiness.md`
- Update: `paper-joe-submission/CHANGELOG.md`

**Interfaces:**
- Consumes: all completed editorial/visual changes.
- Produces: a verified manuscript source and a review PDF for the author.

- [ ] **Step 1:** Build the full manuscript with three LaTeX passes and BibTeX using the current sources; materialise real study PNGs when available or clearly label any review-build limitation.
- [ ] **Step 2:** Require zero fatal LaTeX errors, zero unresolved citations/references, and zero overfull/underfull boxes attributable to manuscript content.
- [ ] **Step 3:** Render and visually inspect pages containing all four primary figures and all three main tables.
- [ ] **Step 4:** Re-run prohibited-claim and number consistency scans.
- [ ] **Step 5:** Compare the branch against `main` and verify no `paper-journal-A/` path changed.
- [ ] **Step 6:** Update readiness/changelog with the second-pass changes and exact QA result.
- [ ] **Step 7:** Produce a clean review PDF and provide it to the author.
