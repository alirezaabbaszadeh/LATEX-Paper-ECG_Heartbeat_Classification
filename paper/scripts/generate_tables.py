#!/usr/bin/env python3
"""Generate LaTeX tables and metrics from stored Research_Runs artifacts."""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RESEARCH_DIR = ROOT / "Research_Runs"
TABLE_DIR = ROOT / "paper" / "tables"

CLASS_ORDER = ["Normal", "SVEB", "VEB", "Fusion", "Unknown"]
CLASS_TO_INDEX = {name: idx for idx, name in enumerate(CLASS_ORDER)}
NUM_CLASSES = len(CLASS_ORDER)

TIME_FORMAT = "%Y-%m-%d %H:%M:%S,%f"


def parse_classification_report(path: Path) -> Dict[str, Dict[str, float]]:
    pattern = re.compile(
        r"^(?P<label>[A-Za-z ]+?)\s+"
        r"(?P<precision>\d+\.\d+)\s+"
        r"(?P<recall>\d+\.\d+)\s+"
        r"(?P<f1>\d+\.\d+)\s+"
        r"(?P<support>\d+)"
    )
    metrics: Dict[str, Dict[str, float]] = {}
    accuracy = None
    macro_f1 = None
    with path.open() as f:
        for raw_line in f:
            line = raw_line.rstrip()
            match = pattern.match(line.strip())
            if match:
                label = match.group("label").strip()
                metrics[label] = {
                    "precision": float(match.group("precision")),
                    "recall": float(match.group("recall")),
                    "f1": float(match.group("f1")),
                    "support": int(match.group("support")),
                }
                if label.lower().startswith("macro avg"):
                    macro_f1 = metrics[label]["f1"]
            if "accuracy" in line and accuracy is None:
                parts = line.split()
                try:
                    accuracy = float(parts[-2])
                except (IndexError, ValueError):
                    continue
            if line.strip().startswith("macro avg"):
                parts = line.split()
                try:
                    macro_f1 = float(parts[-2])
                except (IndexError, ValueError):
                    continue
    if accuracy is None or macro_f1 is None:
        raise ValueError(f"Failed to parse overall metrics from {path}")
    metrics["accuracy"] = {"value": accuracy}
    metrics["macro_f1"] = {"value": macro_f1}
    return metrics


def macro_f1_from_preds(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    scores: List[float] = []
    for cls in range(NUM_CLASSES):
        tp = int(np.sum((y_true == cls) & (y_pred == cls)))
        fp = int(np.sum((y_true != cls) & (y_pred == cls)))
        fn = int(np.sum((y_true == cls) & (y_pred != cls)))
        if tp == 0 and fp == 0 and fn == 0:
            scores.append(0.0)
            continue
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        if precision + recall == 0.0:
            scores.append(0.0)
        else:
            scores.append(2 * precision * recall / (precision + recall))
    return float(np.mean(scores))


def compute_calibration(y_true: np.ndarray, probs: np.ndarray, num_bins: int = 15) -> Dict[str, Tuple[float, float]]:
    results: Dict[str, Tuple[float, float]] = {}
    bins = np.linspace(0.0, 1.0, num_bins + 1)
    for cls_name, cls_idx in CLASS_TO_INDEX.items():
        cls_probs = probs[:, cls_idx]
        cls_true = (y_true == cls_idx).astype(float)
        bin_ids = np.digitize(cls_probs, bins) - 1
        total = len(cls_probs)
        ece = 0.0
        for b in range(num_bins):
            mask = bin_ids == b
            count = int(np.sum(mask))
            if count == 0:
                continue
            conf = float(np.mean(cls_probs[mask]))
            acc = float(np.mean(cls_true[mask]))
            ece += abs(acc - conf) * (count / total)
        brier = float(np.mean((cls_probs - cls_true) ** 2))
        results[cls_name] = (ece, brier)
    return results


def evaluate_probs(y_true: np.ndarray, probs: np.ndarray) -> Tuple[float, float]:
    preds = np.argmax(probs, axis=1)
    accuracy = float(np.mean(preds == y_true))
    macro = macro_f1_from_preds(y_true, preds)
    return accuracy, macro


def load_predictions(run_dir: Path) -> Tuple[np.ndarray, np.ndarray]:
    npz_path = run_dir / "raw_predictions.npz"
    with np.load(npz_path) as data:
        y_true = data["y_true"].astype(int)
        probs = data["y_pred_probs"].astype(float)
    return y_true, probs


def write_leaderboard(run_metrics: Dict[str, Dict[str, float]]) -> None:
    lines = [
        "% Leaderboard across runs (auto-generated)",
        "\\begin{table}[H]\\centering",
        "\\caption{Leaderboard across final evaluation runs (sorted by macro-F1).}",
        "\\label{tab:leaderboard}",
        "\\begin{tabular}{lrr}",
        "\\toprule",
        "Run & Acc & Macro-F1 " + r"\\",
        "\\midrule",
    ]
    for run_name, metrics in sorted(run_metrics.items(), key=lambda kv: kv[1]["macro_f1"], reverse=True):
        lines.append(f"{run_name} & {metrics['accuracy']:.2f} & {metrics['macro_f1']:.2f} " + r"\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}"])
    (TABLE_DIR / "leaderboard_all_runs.tex").write_text("\n".join(lines) + "\n")


def write_per_class_table(class_metrics: Dict[str, Dict[str, float]]) -> None:
    lines = [
        "% Per-class metrics for the main model",
        "\\begin{table}[H]\\centering",
        "\\caption{Per-class precision, recall, and F1 for the main Conformer-CNN on the hold-out test split.}",
        "\\label{tab:perclass}",
        "\\begin{tabular}{lrrrr}",
        "\\toprule",
        "Class & Precision & Recall & F1 & Support " + r"\\",
        "\\midrule",
    ]
    for cls in CLASS_ORDER:
        metrics = class_metrics[cls]
        lines.append(
            f"{cls} & {metrics['precision']:.2f} & {metrics['recall']:.2f} & {metrics['f1']:.2f} & {metrics['support']} " + r"\\"
        )
    total_support = sum(class_metrics[cls]["support"] for cls in CLASS_ORDER)
    lines.append(f"Total & -- & -- & -- & {total_support} " + r"\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}"])
    (TABLE_DIR / "table_stratified_perf.tex").write_text("\n".join(lines) + "\n")


def write_calibration_table(calibration: Dict[str, Tuple[float, float]]) -> None:
    lines = [
        "% Calibration metrics (ECE, Brier) per class",
        "\\begin{table}[H]\\centering",
        "\\caption{Expected calibration error (ECE) and Brier scores for the main model using 15-bin reliability estimates.}",
        "\\label{tab:calibration}",
        "\\begin{tabular}{lrr}",
        "\\toprule",
        "Class & ECE $\\downarrow$ & Brier $\\downarrow$ " + r"\\",
        "\\midrule",
    ]
    for cls in CLASS_ORDER:
        ece, brier = calibration[cls]
        lines.append(f"{cls} & {ece:.3f} & {brier:.3f} " + r"\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}"])
    (TABLE_DIR / "table_calibration.tex").write_text("\n".join(lines) + "\n")


def write_robustness_table(y_true: np.ndarray, probs: np.ndarray) -> None:
    np.random.seed(42)
    noise_levels = [0.0, 0.05, 0.10, 0.15]
    lines = [
        "% Robustness to additive probability noise",
        "\\begin{table}[H]\\centering",
        "\\caption{Accuracy and macro-F1 of the main model after injecting Gaussian noise ($\\sigma$) into logits and renormalising probabilities.}",
        "\\label{tab:robustness}",
        "\\begin{tabular}{lrr}",
        "\\toprule",
        "$\\sigma$ & Accuracy & Macro-F1 " + r"\\",
        "\\midrule",
    ]
    for sigma in noise_levels:
        if sigma == 0.0:
            perturbed = probs.copy()
        else:
            noise = np.random.normal(loc=0.0, scale=sigma, size=probs.shape)
            perturbed = probs + noise
            perturbed = np.clip(perturbed, 1e-8, None)
            perturbed = perturbed / perturbed.sum(axis=1, keepdims=True)
        acc, macro = evaluate_probs(y_true, perturbed)
        lines.append(f"{sigma:.2f} & {acc:.2f} & {macro:.2f} " + r"\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}"])
    (TABLE_DIR / "table_robustness.tex").write_text("\n".join(lines) + "\n")


def parse_log_times(log_path: Path) -> Tuple[float, float, int, int]:
    start_train = end_train = start_eval = end_eval = None
    epochs = None
    batch_size = None
    with log_path.open() as f:
        for line in f:
            if "Starting final training for" in line and epochs is None:
                match = re.search(r"for (\d+) epochs", line)
                if match:
                    epochs = int(match.group(1))
            if "Starting final training" in line and start_train is None:
                start_train = datetime.strptime(line[:23], TIME_FORMAT)
            if "Final model training completed" in line and end_train is None:
                end_train = datetime.strptime(line[:23], TIME_FORMAT)
            elif "Starting evaluation" in line:
                start_eval = datetime.strptime(line[:23], TIME_FORMAT)
            if "Precision-Recall curves" in line and end_eval is None:
                end_eval = datetime.strptime(line[:23], TIME_FORMAT)
            if "Using batch size" in line and batch_size is None:
                match = re.search(r"batch size: (\d+)", line)
                if match:
                    batch_size = int(match.group(1))
    if None in (start_train, end_train, start_eval, end_eval):
        raise ValueError(f"Missing timestamps in {log_path}")
    train_minutes = (end_train - start_train).total_seconds() / 60.0
    eval_seconds = (end_eval - start_eval).total_seconds()
    return train_minutes, eval_seconds, epochs or 0, batch_size or 0


def write_compute_table(run_metrics: Dict[str, Dict[str, float]]) -> None:
    lines = [
        "% Training and inference efficiency",
        "\\begin{table}[H]\\centering",
        "\\caption{Training duration and evaluation latency measured from final run logs (minutes and seconds).}",
        "\\label{tab:compute}",
        "\\begin{tabular}{lrrrr}",
        "\\toprule",
        "Run & Train (min) & Eval (s) & Epochs & Batch " + r"\\",
        "\\midrule",
    ]
    for run_name, stats in run_metrics.items():
        lines.append(
            f"{run_name} & {stats['train_min']:.1f} & {stats['eval_s']:.1f} & {int(stats['epochs'])} & {int(stats['batch'])} " + r"\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}"])
    (TABLE_DIR / "table_compute.tex").write_text("\n".join(lines) + "\n")


def write_dataset_table(test_support: Dict[str, int]) -> None:
    lines = [
        "% Dataset composition (test support available)",
        "\\begin{table}[H]\\centering",
        "\\caption{Beat counts per class on the hold-out test split (train/validation managed via inter-patient K-fold across 38 records).}",
        "\\label{tab:dataset}",
        "\\begin{tabular}{lrrr}",
        "\\toprule",
        "Class & Train & Val & Test " + r"\\",
        "\\midrule",
    ]
    total_test = 0
    for cls in CLASS_ORDER:
        support = test_support.get(cls, 0)
        total_test += support
        lines.append(f"{cls} & -- & -- & {support} " + r"\\")
    lines.append(f"Total & -- & -- & {total_test} " + r"\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}"])
    (TABLE_DIR / "table_dataset_composition.tex").write_text("\n".join(lines) + "\n")


def write_subject_ids_table(split_info: Dict[str, List[str]]) -> None:
    lines = [
        "% Subject IDs per split",
        "\\begin{table}[H]\\centering",
        "\\caption{Record identifiers allocated to training (K-fold) and final testing.}",
        "\\label{tab:subjects}",
        "\\begin{tabular}{lpr}",
        "\\toprule",
        "Split & IDs & Count " + r"\\",
        "\\midrule",
    ]
    kfold_ids = split_info.get("kfold_records", [])
    test_ids = split_info.get("final_test_records", [])
    lines.append(f"K-fold train/val & {', '.join(kfold_ids)} & {len(kfold_ids)} " + r"\\")
    lines.append(f"Hold-out test & {', '.join(test_ids)} & {len(test_ids)} " + r"\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}"])
    (TABLE_DIR / "table_subject_ids.tex").write_text("\n".join(lines) + "\n")


def main() -> None:
    leaderboard_metrics: Dict[str, Dict[str, float]] = {}
    compute_stats: Dict[str, Dict[str, float]] = {}
    main_class_metrics: Dict[str, Dict[str, float]] | None = None
    calibration: Dict[str, Tuple[float, float]] | None = None
    y_true_main: np.ndarray | None = None
    probs_main: np.ndarray | None = None
    test_support: Dict[str, int] = {}

    for run_dir in sorted(RESEARCH_DIR.glob("final_run_*")):
        report = parse_classification_report(run_dir / "classification_report.txt")
        run_name = run_dir.name.replace("final_run_", "")
        leaderboard_metrics[run_name] = {
            "accuracy": report["accuracy"]["value"],
            "macro_f1": report["macro_f1"]["value"],
        }
        train_min, eval_s, epochs, batch = parse_log_times(run_dir / "final_run_log.txt")
        compute_stats[run_name] = {
            "train_min": train_min,
            "eval_s": eval_s,
            "epochs": epochs,
            "batch": batch,
        }
        if run_dir.name.endswith("Main_Model_20250824_154136"):
            main_class_metrics = {cls: report[cls] for cls in CLASS_ORDER}
            test_support = {cls: report[cls]["support"] for cls in CLASS_ORDER}
            y_true_main, probs_main = load_predictions(run_dir)
            calibration = compute_calibration(y_true_main, probs_main)

    if main_class_metrics is None or calibration is None or y_true_main is None or probs_main is None:
        raise RuntimeError("Failed to locate main model artifacts.")

    write_leaderboard(leaderboard_metrics)
    write_per_class_table(main_class_metrics)
    write_calibration_table(calibration)
    write_robustness_table(y_true_main, probs_main)
    write_compute_table(compute_stats)
    write_dataset_table(test_support)

    split_path = RESEARCH_DIR / "tuning_Main_Model_20250823_145919" / "data_splits.json"
    with split_path.open() as f:
        split_info = json.load(f)
    write_subject_ids_table(split_info)


if __name__ == "__main__":
    main()
