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
