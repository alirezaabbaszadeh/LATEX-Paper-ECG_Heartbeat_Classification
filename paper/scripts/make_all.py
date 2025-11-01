#!/usr/bin/env python3
import argparse, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

def run(cmd):
    print('+', ' '.join(cmd))
    return subprocess.run(cmd, check=False).returncode

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True)
    ap.add_argument('--commit')
    args = ap.parse_args()

    # dataset composition
    run([sys.executable, str(HERE/'build_tables.py'), '--repo', args.repo, '--out', 'tables/dataset_composition.tex'])

    # copy core figs if exist
    run([sys.executable, str(HERE/'copy_core_figs.py'), '--repo', args.repo, '--out', 'figures'])

    print('All done')
