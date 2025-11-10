# Paper workspace (BSPC / CBM)

This folder contains a journal-ready LaTeX kit targeting two Elsevier journals in parallel:
- Biomedical Signal Processing and Control (BSPC) — `paper/bspc/` (elsarticle).
- Computers in Biology and Medicine (CBM) — `paper/cbm/` (elsarticle).

## Build
```bash
cd paper
make bspc   # builds paper/bspc/bspc_main.pdf
make cbm    # builds paper/cbm/cbm_main.pdf
```

## Figures
Run:
```bash
python3 scripts/copy_core_figs.py --repo .. --out figures
```
This searches for confusion matrix / ROC / PR curves and a pipeline diagram and copies them into `paper/figures/` with clean names.

## Tables
`scripts/build_tables.py` can auto-populate: dataset composition, run leaderboard, calibration (ECE/Brier) if probabilities exist.

## Reproducibility
Use the macro `\commit{<SHA>}` to pin the code version.

## Version Control Policy
- **Keep journal assets tracked.** The repository intentionally stores camera-ready friendly artifacts such as `templates/heartbeat-template.cls`, `templates/heartbeat-style.bst`, and curated PDFs in `figures/` so Overleaf mirrors and collaborators have consistent inputs.
- **Ignore only transient LaTeX noise.** Auxiliary build files (`*.aux`, `*.log`, `*.out`, etc.), the latexmk `_build/` directory, and scratch artifacts that match `figures/*-scratch.*` remain excluded through `paper/.gitignore`.
- **Regenerate, then commit.** When figures are regenerated or templates change, rerun the producing script and commit the updated PDFs/TEX assets instead of relying on local copies that may drift.
