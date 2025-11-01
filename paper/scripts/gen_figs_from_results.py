import argparse, pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary_csv", default="tables/all_runs_summary.csv")
    ap.add_argument("--perclass_csv", default="tables/all_runs_perclass.csv")
    args = ap.parse_args()

    summ = pd.read_csv(args.summary_csv)
    perc = pd.read_csv(args.perclass_csv)

    Path("figures").mkdir(parents=True, exist_ok=True)

    # Leaderboard Macro-F1
    plt.figure()
    summ.sort_values("macro_f1", ascending=False).plot(x="name", y="macro_f1", kind="bar")
    plt.ylabel("Macro-F1")
    plt.title("Leaderboard (Macro-F1 across runs)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("figures/leaderboard_macro_f1.png", dpi=300)

    # Class-wise F1 grid
    classes = sorted(perc["class"].unique())
    pivot = perc.pivot_table(index="name", columns="class", values="f1", aggfunc="mean")
    plt.figure()
    pivot.plot(kind="bar")
    plt.ylabel("F1")
    plt.title("Class-wise F1 across runs")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("figures/classwise_f1_grid.png", dpi=300)

    # Delta vs Main
    main_rows = summ[summ["name"].str.contains("Main", case=False, na=False)]
    if not main_rows.empty:
        main_name = main_rows.iloc[0]["name"]
        main_per = perc[perc["name"] == main_name][["class","f1"]].set_index("class")["f1"]
        deltas = []
        for nm, g in perc.groupby("name"):
            g2 = g.set_index("class")["f1"].reindex(main_per.index)
            d = (g2 - main_per).rename(nm)
            deltas.append(d)
        import pandas as pd
        deltas_df = pd.concat(deltas, axis=1).T  # runs x classes
        plt.figure()
        deltas_df.plot(kind="bar")
        plt.ylabel("ΔF1 vs Main")
        plt.title("Per-class ΔF1 relative to Main model")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig("figures/delta_f1_vs_main.png", dpi=300)

    print("[OK] Generated figures in figures/")

if __name__ == "__main__":
    main()
