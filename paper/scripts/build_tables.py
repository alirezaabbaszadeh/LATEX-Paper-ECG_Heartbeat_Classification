import argparse
from pathlib import Path
import pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary_csv", default="tables/all_runs_summary.csv")
    ap.add_argument("--perclass_csv", default="tables/all_runs_perclass.csv")
    ap.add_argument("--readme", help="Path to README.md in repo", required=False)
    args = ap.parse_args()

    Path("tables").mkdir(parents=True, exist_ok=True)
    summ = pd.read_csv(args.summary_csv)

    cols = ["name","accuracy","macro_f1","weighted_f1","support_total"]
    t = summ[cols].sort_values("macro_f1", ascending=False).copy()
    t.columns = ["Model", "Accuracy", "Macro-F1", "Weighted-F1", "Support"]
    with open("tables/leaderboard_all_runs.tex","w") as f:
        f.write("\\begin{tabular}{lcccc}\\toprule Model & Acc & Macro-F1 & Weighted-F1 & Support\\\\midrule\n")
        for _,r in t.iterrows():
            f.write(f"{r['Model']} & {r['Accuracy']:.2f} & {r['Macro-F1']:.2f} & {r['Weighted-F1']:.2f} & {int(r['Support'])}\\\n")
        f.write("\\bottomrule\\end{tabular}
")

    per = pd.read_csv(args.perclass_csv)
    main_name = None
    for nm in t["Model"]:
        if "Main" in nm:
            main_name = nm; break
    if main_name:
        m = per[per["name"]==main_name]
        with open("tables/main_per_class_report.tex","w") as f:
            f.write("\\begin{tabular}{lcccc}\\toprule Class & Precision & Recall & F1 & Support\\\\midrule\n")
            for _,r in m.iterrows():
                f.write(f"{r['class']} & {r['precision']:.2f} & {r['recall']:.2f} & {r['f1']:.2f} & {int(r['support'])}\\\n")
            f.write("\\bottomrule\\end{tabular}
")

    with open("tables/dataset_composition.tex","w") as f:
        f.write("\\begin{tabular}{lrr}\\toprule Class & Count & Percent\\\\midrule\n")
        f.write("\\textit{(fill from README table if available)} & -- & --\\\n")
        f.write("\\bottomrule\\end{tabular}
")

    print("[OK] Generated tables in tables/")

if __name__ == "__main__":
    main()
