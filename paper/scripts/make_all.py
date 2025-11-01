import argparse, subprocess, sys
from pathlib import Path

def run(cmd):
    print('+', ' '.join(cmd))
    r = subprocess.run(cmd, check=False)
    if r.returncode != 0:
        print('[WARN] command failed:', ' '.join(cmd))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', required=True, help='Path to local repo clone')
    ap.add_argument('--commit', required=True, help='Commit SHA to pin in LaTeX')
    args = ap.parse_args()

    run([sys.executable, 'scripts/collect_runs.py', '--repo', args.repo])
    run([sys.executable, 'scripts/copy_core_figs.py', '--repo', args.repo])
    run([sys.executable, 'scripts/gen_figs_from_results.py'])
    readme = str(Path(args.repo)/'README.md')
    run([sys.executable, 'scripts/build_tables.py', '--readme', readme])

    tex = Path('main_unlimited.tex').read_text(encoding='utf-8')
    tex = tex.replace('<<COMMIT_SHA>>', args.commit)
    Path('main_unlimited.tex').write_text(tex, encoding='utf-8')
    print('[OK] Updated commit SHA in main_unlimited.tex')

if __name__ == '__main__':
    main()
