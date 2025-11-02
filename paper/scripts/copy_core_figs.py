#!/usr/bin/env python3
import argparse, os, shutil
from pathlib import Path

TARGETS = {
 'confusion_matrix.png': ['confusion','confmat','confusion_matrix'],
 'roc_curves.png': ['roc','auc','roc_curve'],
 'precision_recall.png': ['precision_recall','precision','pr','pr_curve'],
 'class_dist.png': ['class_dist','class_distribution','dataset_distribution']
}

def find_best(root, keys):
    best = None
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if name.lower().endswith('.png'):
                path = Path(dirpath)/name
                low = path.as_posix().lower()
                if any(k in low for k in keys):
                    if best is None or path.stat().st_size > best.stat().st_size:
                        best = path
    return best

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--repo', required=True)
    p.add_argument('--out', default='paper/figures')
    p.add_argument('--force', action='store_true')
    args = p.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    copied = []
    for tgt, keys in TARGETS.items():
        src = find_best(args.repo, keys)
        if src:
            dst = out/tgt
            if (not dst.exists()) or args.force:
                shutil.copy2(src, dst)
                copied.append((str(src), str(dst)))
    for s,d in copied:
        print(f'copied {s} -> {d}')
    if not copied:
        print('no figures found')
