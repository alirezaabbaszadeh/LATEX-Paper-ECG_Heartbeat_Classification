import argparse, re
from pathlib import Path
import pandas as pd

REPORT_NAME = "classification_report.txt"
RUN_LOG = "final_run_log.txt"

def clean_name(run_dir: Path) -> str:
    n = run_dir.name
    n = n.replace("final_run_", "")
    n = n.replace("_Model", "")
    n = re.sub(r"_\d{8}_\d{6}", "", n)  # strip timestamps
    n = n.replace("_", " ")
    n = n.replace("Main", "Main (CNN+Conformer)")
    n = n.replace("Baseline", "Baseline (CNN)")
    n = n.replace("CNNLSTM", "CNN+LSTM")
    n = n.replace("AttentionOnly", "Attention-only")
    return n.strip()

def parse_classification_report(text: str):
    data = {}
    lines = [l.rstrip() for l in text.splitlines() if l.strip()]
    for l in lines:
        if l.lower().startswith("accuracy"):
            parts = l.split()
            try:
                data["accuracy"] = float(parts[-2])
                data["support_total"] = int(parts[-1])
            except:
                pass
        if l.lower().startswith("macro avg"):
            parts = l.split()
            if len(parts) >= 4:
                data["macro_precision"] = float(parts[-3]); data["macro_recall"] = float(parts[-2]); data["macro_f1"] = float(parts[-1])
        if l.lower().startswith("weighted avg"):
            parts = l.split()
            if len(parts) >= 4:
                data["weighted_precision"] = float(parts[-3]); data["weighted_recall"] = float(parts[-2]); data["weighted_f1"] = float(parts[-1])
    per = []
    header_seen = False
    for l in lines:
        if re.search(r'precision\s+recall\s+f1-score\s+support', l):
            header_seen = True
            continue
        if header_seen:
            if l.lower().startswith(("accuracy", "macro avg", "weighted avg")):
                continue
            parts = l.split()
            if len(parts) >= 5:
                cls = parts[0]
                try:
                    prec, rec, f1, sup = float(parts[1]), float(parts[2]), float(parts[3]), int(parts[4])
                    per.append({"class": cls, "precision": prec, "recall": rec, "f1": f1, "support": sup})
                except:
                    pass
    data["per_class"] = per
    return data

def read_report_from_run(run_dir: Path) -> str:
    cr = run_dir / REPORT_NAME
    if cr.exists():
        return cr.read_text(encoding="utf-8", errors="ignore")
    logp = run_dir / RUN_LOG
    if logp.exists():
        txt = logp.read_text(encoding="utf-8", errors="ignore")
        import re
        m = re.search(r"""Classification Report\s*=+\s*(.*?)\Z""", txt, flags=re.S|re.I)
        if m:
            return m.group(1)
    return ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="Path to local clone of repo")
    ap.add_argument("--out_csv_runs", default="tables/all_runs_summary.csv")
    ap.add_argument("--out_csv_perclass", default="tables/all_runs_perclass.csv")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    rr = repo / "Research_Runs"
    if not rr.exists():
        raise SystemExit(f"[ERROR] {rr} not found.")

    rows = []; per_rows = []
    for run_dir in rr.glob("final_run_*"):
        rep = read_report_from_run(run_dir)
        if not rep:
            continue
        metrics = parse_classification_report(rep)
        name = clean_name(run_dir)
        rows.append({
            "run_dir": str(run_dir.relative_to(repo)),
            "name": name,
            "accuracy": metrics.get("accuracy"),
            "macro_f1": metrics.get("macro_f1"),
            "weighted_f1": metrics.get("weighted_f1"),
            "support_total": metrics.get("support_total"),
        })
        for pr in metrics.get("per_class", []):
            per_rows.append({"name": name, **pr})

    if not rows:
        raise SystemExit("[ERROR] No runs with classification_report found.")

    Path("tables").mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(args.out_csv_runs, index=False)
    pd.DataFrame(per_rows).to_csv(args.out_csv_perclass, index=False)
    print(f"[OK] Wrote {args.out_csv_runs} and {args.out_csv_perclass}")

if __name__ == "__main__":
    main()
