# Paper scripts

This PR adds scripts for syncing figures from your artifacts repo and stubs for leaderboard/calibration/appendix.

## Copy core figures (confusion, ROC, PR, class distribution)

```bash
python3 paper/scripts/copy_core_figs.py --repo ../ECG_Heartbeat_Classification --out paper/figures
```

This will populate: `paper/figures/confusion_matrix.png`, `roc_curves.png`, `precision_recall.png`, `class_dist.png` (if found).

## Next (optional, you can run locally)
- Leaderboard (from saved classification_report*.txt) — stub file included.
- Calibration ECE/Brier — placeholder writer included.
- Appendix pack — stub file included.

If you prefer, I can open a follow-up PR that generates LaTeX tables automatically.
