# Journal of Electrocardiology Editorial Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce `paper-joe-submission/` as an evidence-bounded, submission-oriented revision of `paper-journal-A/` with stronger narrative, clearer claims, publication-quality tables/figures, and reproducible QA.

**Architecture:** Start from an exact subtree copy of `paper-journal-A/`, then edit only the new folder. Keep a claim ledger tied to archived experiment outputs, regenerate visual diagnostics from the stored main-model predictions, and finish with build, visual, citation, numerical, and base-folder integrity checks.

**Tech Stack:** LaTeX (`elsarticle`, `latexmk`), BibTeX, Python 3, NumPy, scikit-learn, Matplotlib, Git/GitHub, existing repository experiment artifacts.

## Global Constraints

- Base manuscript `paper-journal-A/` must remain unchanged.
- Target working copy is exactly `paper-joe-submission/`.
- No invented experiments, metrics, cohorts, citations, or clinical claims.
- No `state of the art`, autonomous-diagnosis, clinical-readiness, or uncontrolled superiority claims.
- Strong claims must be scoped to `the baselines evaluated in this study` and/or `the subject-separated protocol used here`.
- Existing held-out evidence anchors are 15,573 beats from 7 test subjects; accuracy 0.60 [0.59, 0.60]; macro-F1 0.26 [0.26, 0.27]; weighted-F1 0.68 [0.67, 0.68].
- Main archived prediction source is `Research_Runs/final_run_Main_Model_20250824_154136/raw_predictions.npz`.
- Main archived class report is `Research_Runs/final_run_Main_Model_20250824_154136/classification_report.txt`.
- Controlled comparator runs are `Research_Runs/final_run_AttentionOnly_20250824_090531/`, `Research_Runs/final_run_CNNLSTM_Model_20250824_213453/`, and `Research_Runs/final_run_Baseline_Model_20250824_182728/`.
- Journal fit is demonstrated through computerized electrocardiology, arrhythmia discrimination, monitoring, morphology, patient heterogeneity, and decision-support implications, not repeated journal-name mentions.

---

### Task 1: Create the isolated manuscript copy and provenance record

**Files:**
- Create subtree: `paper-joe-submission/` from `paper-journal-A/`
- Create: `paper-joe-submission/REVISION_PROVENANCE.md`

**Interfaces:**
- Consumes: source tree `paper-journal-A/`
- Produces: an initially identical manuscript tree that all later tasks modify

- [ ] **Step 1: Copy the base manuscript exactly**

Local equivalent:
```bash
cp -a paper-journal-A paper-joe-submission
```

Git-data equivalent: add a top-level tree entry named `paper-joe-submission` pointing at the exact tree SHA currently used by `paper-journal-A`, then commit that tree.

- [ ] **Step 2: Verify initial identity**

Run:
```bash
diff -qr paper-journal-A paper-joe-submission
```
Expected: no output.

- [ ] **Step 3: Add provenance record**

Create `paper-joe-submission/REVISION_PROVENANCE.md` containing:
```markdown
# Revision provenance

Base: `paper-journal-A/`
Working copy: `paper-joe-submission/`
Created: 2026-08-10
Purpose: submission-oriented Journal of Electrocardiology editorial revision.
Evidence rule: all quantitative claims must remain traceable to existing repository outputs; no new experimental result is implied by editorial changes.
```

- [ ] **Step 4: Commit**

```bash
git add paper-joe-submission
git commit -m "chore: create isolated JoE submission copy"
```

### Task 2: Build the evidence and claim ledger

**Files:**
- Create: `paper-joe-submission/qa/claim-ledger.md`
- Read: `paper-joe-submission/tables/test_metrics.tex`
- Read: `Research_Runs/final_run_Main_Model_20250824_154136/classification_report.txt`
- Read: `Research_Runs/final_run_Main_Model_20250824_154136/temperature_scaling_results.txt`
- Read comparator classification reports/logs from the three controlled baseline run folders

**Interfaces:**
- Consumes: archived metrics and existing manuscript claims
- Produces: one authoritative textual ledger for later manuscript/table/caption checks

- [ ] **Step 1: Record cohort and overall metrics**

The ledger must include exactly:
```text
Held-out cohort: 7 subjects, 15,573 beats
Development cohort: 38 records
Proposed: accuracy 0.60 [0.59, 0.60]; macro-F1 0.26 [0.26, 0.27]; weighted-F1 0.68 [0.67, 0.68]
Attention-only: accuracy 0.27 [0.26, 0.28]; macro-F1 0.15 [0.14, 0.15]; weighted-F1 0.38 [0.37, 0.39]
CNN-LSTM: accuracy 0.18 [0.17, 0.18]; macro-F1 0.15 [0.15, 0.16]; weighted-F1 0.29 [0.28, 0.29]
Feature-engineered: accuracy 0.14 [0.13, 0.14]; macro-F1 0.07 [0.07, 0.07]; weighted-F1 0.23 [0.22, 0.23]
```

- [ ] **Step 2: Record proposed-model class metrics**

The ledger must include:
```text
Normal: precision 0.95; recall 0.60; F1 0.74; support 12,061; AUC 0.9009
SVEB: precision 0.00; recall 0.00; F1 0.00; support 214; AUC 0.6681
VEB: precision 0.48; recall 0.70; F1 0.57; support 2,913; AUC 0.8431
Fusion: precision 0.01; recall 0.01; F1 0.01; support 383; AUC 0.3140
Unknown: precision 0.00; recall 0.00; F1 0.00; support 2; AUC 0.5837
```

- [ ] **Step 3: Add allowed and disallowed claim formulations**

Allowed examples:
```text
outperformed all baselines evaluated in this study
under the subject-separated protocol used here
strong discrimination for normal and ventricular ectopic beats
rare-class failure persisted despite threshold adjustment
```

Disallowed examples:
```text
state of the art
clinically ready
cardiologist-level performance
generalizes to real-world populations
autonomous arrhythmia diagnosis
```

- [ ] **Step 4: Check ledger against source files**

Run a manual two-source reconciliation: every ledger number must be present in either `test_metrics.tex` or the archived main classification report, with calibration/threshold values linked to their archived analysis file.

- [ ] **Step 5: Commit**

```bash
git add paper-joe-submission/qa/claim-ledger.md
git commit -m "docs: add evidence-bounded claim ledger"
```

### Task 3: Rewrite Results and Discussion around the evidence hierarchy

**Files:**
- Modify: `paper-joe-submission/src/sections/results.tex`
- Modify: `paper-joe-submission/src/sections/discussion.tex`
- Read: `paper-joe-submission/qa/claim-ledger.md`

**Interfaces:**
- Consumes: claim ledger and existing literature citations
- Produces: the central scientific narrative used by all later sections

- [ ] **Step 1: Rewrite Results in this order**

Use these subsection responsibilities:
```latex
\subsection{Held-out cohort and class imbalance}
\subsection{Performance relative to evaluated baselines}
\subsection{Class-specific discrimination and error structure}
\subsection{Threshold and calibration findings}
```

The first two paragraphs must establish the subject-separated cohort, severe class imbalance, absolute metrics, and comparator results before interpretation.

- [ ] **Step 2: Scope every superiority statement**

Replace unbounded language such as `substantially outperforming` with formulations that identify the comparison set, for example:
```text
The proposed model produced the highest accuracy, macro-F1, and weighted-F1 among the four architectures evaluated under the same held-out split.
```

- [ ] **Step 3: Make the rare-class failure a result, not a footnote**

State explicitly that the strong Normal/VEB results coexist with near-zero SVEB/Fusion F1 and that threshold adjustment does not resolve this without extreme false-positive trade-offs.

- [ ] **Step 4: Rewrite Discussion in this order**

Use paragraph sequence:
```text
principal finding
importance of subject-separated evaluation
architectural interpretation limited to controlled baselines
clinical meaning of class-dependent performance
comparison with literature and protocol differences
reproducibility contribution
limitations
future validation
```

- [ ] **Step 5: Remove unsupported deployment positioning**

Describe the current system as a research benchmark and possible clinician-supervised prioritization component, not a deployed triage system.

- [ ] **Step 6: Run claim-ledger text audit**

Search the two files for the forbidden phrases from Task 2 and inspect every occurrence of `better`, `superior`, `robust`, `clinical`, `generaliz`, and `deploy` for explicit evidence scope.

- [ ] **Step 7: Commit**

```bash
git add paper-joe-submission/src/sections/results.tex paper-joe-submission/src/sections/discussion.tex
git commit -m "edit: reframe JoE results and discussion"
```

### Task 4: Redesign the three main evidence tables

**Files:**
- Create or replace: `paper-joe-submission/tables/cohort_distribution.tex`
- Replace: `paper-joe-submission/tables/test_metrics.tex`
- Create: `paper-joe-submission/tables/class_metrics.tex`
- Modify: `paper-joe-submission/src/sections/methods.tex`
- Modify: `paper-joe-submission/src/sections/results.tex`

**Interfaces:**
- Consumes: exact values from the claim ledger
- Produces: concise main-text tables with no new metrics

- [ ] **Step 1: Create cohort/class distribution table**

Columns:
```text
Split | Records/subjects | Total beats | N | S | V | F | Q
```
Only populate counts that are directly available from the repository; if development per-class counts are not directly archived, report the held-out row plus total development records without fabricating class counts.

- [ ] **Step 2: Simplify model comparison table**

Main columns:
```text
Model | Accuracy (95% CI) | Macro-F1 (95% CI) | Weighted-F1 (95% CI)
```
Move the five class-specific AUC columns to `class_metrics.tex` or supplementary material to reduce horizontal density.

- [ ] **Step 3: Create class-specific proposed-model table**

Columns:
```text
Class | Support | Precision | Recall | F1 | AUC (95% CI)
```
Use class supports and point metrics from the archived classification report and AUC CIs already present in the current `test_metrics.tex`.

- [ ] **Step 4: Update table callouts and captions**

Each caption must state why the table matters. Example direction: `Performance varies markedly by rhythm class despite the model-level gain over controlled baselines.`

- [ ] **Step 5: Compile table syntax**

Run:
```bash
cd paper-joe-submission/src && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```
Expected: LaTeX exits successfully with all three main tables rendered.

- [ ] **Step 6: Commit**

```bash
git add paper-joe-submission/tables paper-joe-submission/src/sections/methods.tex paper-joe-submission/src/sections/results.tex
git commit -m "edit: restructure JoE evidence tables"
```

### Task 5: Regenerate publication-oriented diagnostic figures from stored predictions

**Files:**
- Create: `paper-joe-submission/scripts/generate_submission_figures.py`
- Create outputs: `paper-joe-submission/figures/fig-confusion-matrix.pdf`
- Create outputs: `paper-joe-submission/figures/fig-confusion-matrix.png`
- Create outputs: `paper-joe-submission/figures/fig-roc-curves.pdf`
- Create outputs: `paper-joe-submission/figures/fig-roc-curves.png`
- Create outputs: `paper-joe-submission/figures/fig-precision-recall-curves.pdf`
- Create outputs: `paper-joe-submission/figures/fig-precision-recall-curves.png`
- Create outputs: `paper-joe-submission/figures/fig-model-comparison.pdf`
- Create outputs: `paper-joe-submission/figures/fig-model-comparison.png`
- Modify: `paper-joe-submission/src/sections/results.tex`

**Interfaces:**
- Consumes: `Research_Runs/final_run_Main_Model_20250824_154136/raw_predictions.npz` and fixed ledger metrics
- Produces: deterministic PDF/PNG figures referenced by Results

- [ ] **Step 1: Implement deterministic data loading**

The script must read:
```python
preds_path = repo_root / "Research_Runs" / "final_run_Main_Model_20250824_154136" / "raw_predictions.npz"
y_true = loaded["y_true"]
y_probs = loaded["y_pred_probs"]
y_pred = loaded["y_pred_classes"]
class_names = ["Normal", "SVEB", "VEB", "Fusion", "Unknown"]
```

- [ ] **Step 2: Implement confusion matrix with counts and row-normalized percentages**

Compute both:
```python
cm = confusion_matrix(y_true, y_pred, labels=range(5))
row_pct = cm / cm.sum(axis=1, keepdims=True)
```
Render each cell as `count\n(percent%)`; handle zero-row division safely with `np.divide(..., where=...)`.

- [ ] **Step 3: Implement ROC figure**

Use one-vs-rest `roc_curve` and `auc` for all classes present in `y_true`. Include AUC in legend and a chance diagonal. Save both PDF and 300-dpi PNG.

- [ ] **Step 4: Implement precision-recall figure**

Use `precision_recall_curve` and `average_precision_score`. Add each class prevalence as a light horizontal reference or include prevalence in legend text so minority-class difficulty is visually explicit.

- [ ] **Step 5: Implement model comparison figure**

Use the exact model-level triplets from Task 2 for four models. Plot grouped markers/bars for Accuracy, Macro-F1, and Weighted-F1 with a 0–1 y-axis and direct numeric labels. Do not add unreported uncertainty bars unless the plotted interval is taken directly from the ledger.

- [ ] **Step 6: Save reproducibly**

Use Matplotlib only, fixed figure dimensions, `bbox_inches="tight"`, vector PDF plus 300-dpi PNG, and no 3D effects.

- [ ] **Step 7: Run generator**

Run:
```bash
python paper-joe-submission/scripts/generate_submission_figures.py
```
Expected: eight output files exist and are non-empty.

- [ ] **Step 8: Update Results figure layout and captions**

Use separate or logically grouped figures rather than a crowded three-panel block. Captions must state the principal interpretation, especially the Normal/VEB versus SVEB/Fusion contrast.

- [ ] **Step 9: Commit**

```bash
git add paper-joe-submission/scripts paper-joe-submission/figures paper-joe-submission/src/sections/results.tex
git commit -m "fig: regenerate JoE diagnostic visuals"
```

### Task 6: Rewrite Introduction and tighten Methods for journal fit

**Files:**
- Modify: `paper-joe-submission/src/sections/introduction.tex`
- Modify: `paper-joe-submission/src/sections/methods.tex`

**Interfaces:**
- Consumes: final Results/Discussion thesis and existing bibliography
- Produces: a problem-driven opening and methods text that directly supports the claims

- [ ] **Step 1: Replace the current Introduction argument**

Use four paragraphs:
```text
clinical/computerized-ECG problem: patient heterogeneity + class imbalance
methodological comparability problem: evaluation protocol matters
representation rationale: local morphology + temporal/global context
study objective and three evidence-bounded contributions
```

- [ ] **Step 2: Remove journal-name targeting language**

Search:
```bash
grep -Rni "Journal of Electrocardiology" paper-joe-submission/src/sections/introduction.tex paper-joe-submission/src/sections/methods.tex
```
Expected: no promotional or self-conscious targeting phrases; journal-relevant citations may remain without naming the journal in the sentence.

- [ ] **Step 3: Tighten Methods to the reproducibility chain**

Ensure the section states, in order: database and exclusions; exact subject-separated split; beat/scalogram construction; three-beat context; CNN-Conformer and comparators; training protocol; evaluation metrics; calibration/threshold analyses.

- [ ] **Step 4: Audit any claim of `lightweight`**

Retain `lightweight` only if a parameter count or directly documented computational basis exists in the repository. Otherwise use `compact` only when the architecture description justifies it, or remove the adjective.

- [ ] **Step 5: Compile**

```bash
cd paper-joe-submission/src && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```
Expected: successful build.

- [ ] **Step 6: Commit**

```bash
git add paper-joe-submission/src/sections/introduction.tex paper-joe-submission/src/sections/methods.tex
git commit -m "edit: strengthen JoE introduction and methods"
```

### Task 7: Finish title, abstract, conclusion, highlights, and front matter

**Files:**
- Modify: `paper-joe-submission/src/sections/frontmatter.tex`
- Modify: `paper-joe-submission/src/sections/abstract.tex`
- Modify: `paper-joe-submission/src/sections/conclusion.tex`
- Modify: `paper-joe-submission/src/sections/highlights.tex`

**Interfaces:**
- Consumes: final body text and claim ledger
- Produces: first-page/editor-facing summary consistent with the manuscript

- [ ] **Step 1: Set evidence-led title**

Use as the starting title:
```text
Subject-Separated ECG Beat Classification with a Morlet–Conformer Network: Reproducible Benchmarking and Rare-Rhythm Failure Analysis
```
Shorten only if meaning is preserved.

- [ ] **Step 2: Rewrite structured abstract**

Background: patient heterogeneity and class imbalance.
Methods: MIT-BIH, 38 development records, 7 held-out subjects, Morlet three-beat sequences, controlled comparators.
Results: exact overall metrics, controlled baseline gain, Normal/VEB strength, SVEB/Fusion failure.
Conclusion: reproducible benchmark value plus need for rare-class and external validation.

- [ ] **Step 3: Rewrite Conclusion**

Use three moves: what was demonstrated; what remains unresolved; what the reproducible benchmark enables next. Do not introduce a new metric or application claim.

- [ ] **Step 4: Rewrite highlights**

Create 3–5 concise statements that each contain one evidence-backed point. Keep each line short enough for Elsevier highlights and avoid promotional adjectives.

- [ ] **Step 5: Numerical consistency scan**

Verify every number in the abstract against `qa/claim-ledger.md` and tables.

- [ ] **Step 6: Commit**

```bash
git add paper-joe-submission/src/sections/frontmatter.tex paper-joe-submission/src/sections/abstract.tex paper-joe-submission/src/sections/conclusion.tex paper-joe-submission/src/sections/highlights.tex
git commit -m "edit: finalize JoE title abstract and highlights"
```

### Task 8: Final build, visual inspection, integrity audit, and submission notes

**Files:**
- Modify as needed: `paper-joe-submission/src/**/*.tex`, `paper-joe-submission/tables/*.tex`
- Create: `paper-joe-submission/qa/submission-readiness.md`
- Create/update: `paper-joe-submission/CHANGELOG.md`

**Interfaces:**
- Consumes: complete revised manuscript
- Produces: compiled manuscript plus explicit QA record

- [ ] **Step 1: Clean build**

Run:
```bash
cd paper-joe-submission/src
latexmk -C
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```
Expected: successful PDF build.

- [ ] **Step 2: Check unresolved LaTeX references**

Run:
```bash
grep -E "undefined references|Citation .* undefined|Reference .* undefined" main.log
```
Expected: no matches.

- [ ] **Step 3: Check prohibited claim language**

Run:
```bash
grep -RniE "state[- ]of[- ]the[- ]art|clinically ready|cardiologist-level|autonomous diagnosis|generalizes to real-world" ../src/sections ../tables
```
Expected: no manuscript claim matches.

- [ ] **Step 4: Verify base manuscript integrity**

Compare `paper-journal-A/` against the branch point/main version. Expected: no modifications under `paper-journal-A/`.

- [ ] **Step 5: Inspect PDF visually**

Review every page for table width, clipped labels, figure legibility, caption separation, orphan headings, excessive whitespace, and broken references. Record each inspected element in `qa/submission-readiness.md`.

- [ ] **Step 6: Write change log**

Summarize narrative reframing, table redesign, figure regeneration, claim-scope changes, and QA results without implying new experiments.

- [ ] **Step 7: Run repository QA that applies to manuscript/bibliography**

Use existing repository QA scripts/workflows where locally runnable; record command and result in `qa/submission-readiness.md`.

- [ ] **Step 8: Final commit**

```bash
git add paper-joe-submission
git commit -m "qa: finalize JoE submission-oriented revision"
```
