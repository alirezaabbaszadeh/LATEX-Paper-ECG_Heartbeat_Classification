#!/usr/bin/env python3
import argparse, shutil, re
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
    for s,d in copied:
        print(f'Copied {s} -> {d}')
    if not copied:
        print('No figures found to copy.')
