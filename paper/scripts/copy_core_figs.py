import argparse, shutil
from pathlib import Path

CANDIDATE_NAMES = [
    "confusion", "roc", "precision_recall", "precision-recall", "pr"
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    args = ap.parse_args()
    repo = Path(args.repo).resolve()
    out = Path("figures")
    out.mkdir(parents=True, exist_ok=True)

    candidates = list(repo.glob("**/*.png"))
    copied = 0
    for p in candidates:
        name = p.name.lower()
        if any(k in name for k in CANDIDATE_NAMES):
            dst = out / p.name  # COPY (user's preference)
            try:
                shutil.copy2(p, dst)
                copied += 1
            except Exception:
                pass
    print(f"[OK] Copied {copied} figure(s) into figures/")

if __name__ == "__main__":
    main()
