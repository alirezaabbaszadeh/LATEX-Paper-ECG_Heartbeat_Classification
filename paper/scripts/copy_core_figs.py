#!/usr/bin/env python3
import argparse, shutil, re, sys
from pathlib import Path

CANDIDATES = [
    ('confusion_matrix.png', ['confusion','confmat']),
    ('roc_curves.png', ['roc','auc']),
    ('precision_recall.png', ['precision.*recall','pr','pr_curve']),
    ('pipeline.png', ['pipeline','diagram','graphical_abstract']),
]

def find_best(repo_root: Path, patterns):
    files = []
    for pat in patterns:
        rx = re.compile(pat, re.IGNORECASE)
        for p in repo_root.rglob('*.png'):
            if rx.search(p.as_posix()):
                files.append(p)
    files = sorted(set(files), key=lambda p: (len(p.as_posix()), p.stat().st_mtime), reverse=True)
    return files[0] if files else None

def fallback_generate_pipeline(dst: Path):
    try:
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        from matplotlib.patches import Rectangle, FancyArrow
        fig, ax = plt.subplots(figsize=(4.8,2.4))
        ax.axis('off')
        def box(x,y,w,h,label,fs=8):
            ax.add_patch(Rectangle((x,y), w, h, fill=False, linewidth=1))
            ax.text(x+w/2, y+h/2, label, ha='center', va='center', fontsize=fs)
        box(0.03,0.4,0.18,0.25,'ECG')
        box(0.27,0.4,0.18,0.25,'CWT')
        box(0.51,0.50,0.12,0.12,'CNN',fs=7)
        box(0.51,0.33,0.12,0.12,'Conformer',fs=7)
        box(0.73,0.4,0.24,0.25,'AAMI N/S/V/F/Q',fs=7)
        def arrow(x1,y1,x2,y2):
            ax.add_patch(FancyArrow(x1,y1,x2-x1,y2-y1,width=0.0015,head_width=0.02,length_includes_head=True))
        arrow(0.21,0.525,0.27,0.525); arrow(0.45,0.525,0.51,0.56); arrow(0.45,0.525,0.51,0.39)
        arrow(0.63,0.56,0.73,0.525); arrow(0.63,0.39,0.73,0.525)
        fig.tight_layout(); fig.savefig(dst, dpi=100)
        return True
    except Exception as e:
        print('WARN: could not auto-generate pipeline.png:', e, file=sys.stderr)
        return False

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--out', default='figures')
    args = ap.parse_args()

    repo = Path(args.repo)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    copied = []
    for target, pats in CANDIDATES:
        src = find_best(repo, pats)
        if src:
            dst = out / target
            shutil.copy2(src, dst)
            copied.append((src, dst))
    # Ensure a pipeline.png exists (copy or generate)
    pipeline_dst = out / 'pipeline.png'
    if not pipeline_dst.exists():
        ok = fallback_generate_pipeline(pipeline_dst)
        if ok:
            print('Generated', pipeline_dst)
    for s,d in copied:
        print(f'Copied {s} -> {d}')
    if not copied and not pipeline_dst.exists():
        print('No figures found to copy; pipeline.png not generated.', file=sys.stderr)
