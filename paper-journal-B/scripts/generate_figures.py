#!/usr/bin/env python3
"""
Generate the publication-quality ROC, precision--recall, and confusion matrix figures
that feed directly into paper-journal-B. The script reads the stored predictions from
the final Conformer run so that the published figures match the text and tables.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import (auc, average_precision_score, confusion_matrix,
                             precision_recall_curve, roc_curve)
from sklearn.preprocessing import label_binarize

CLASS_NAMES = ["Normal", "SVEB", "VEB", "Fusion", "Unknown"]


def _base_paths():
    repo_root = Path(__file__).resolve().parents[2]
    fig_dir = repo_root / "paper-journal-B" / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    preds_path = repo_root / "Research_Runs" / "final_run_Main_Model_20250824_154136" / "raw_predictions.npz"
    return repo_root, fig_dir, preds_path


def _load_predictions(preds_path: Path):
    if not preds_path.exists():
        raise FileNotFoundError(f"Raw predictions not found at {preds_path}")

    loaded = np.load(preds_path)
    return loaded["y_true"], loaded["y_pred_probs"], loaded["y_pred_classes"]


def _save_figure(fig: plt.Figure, basepath: Path, name: str):
    for ext in ("png", "pdf"):
        output_path = basepath / f"{name}.{ext}"
        fig.savefig(output_path, dpi=300, bbox_inches="tight")


def plot_confusion(y_true: np.ndarray, y_pred: np.ndarray, fig_dir: Path):
    fig, ax = plt.subplots(figsize=(6, 5))
    cm = confusion_matrix(y_true, y_pred)
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap=sns.color_palette("Blues", as_cmap=True),
        cbar=False,
        linewidths=0.8,
        linecolor="white",
        ax=ax,
    )
    ax.set_xlabel("Predicted class")
    ax.set_ylabel("True class")
    ax.set_xticklabels(CLASS_NAMES, rotation=45, ha="right")
    ax.set_yticklabels(CLASS_NAMES, rotation=0)
    ax.set_title("Confusion matrix on the held-out test set")
    fig.tight_layout(pad=0.5)
    _save_figure(fig, fig_dir, "fig-confusion-matrix")
    plt.close(fig)


def plot_roc(y_true: np.ndarray, y_probs: np.ndarray, fig_dir: Path):
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    binarized = label_binarize(y_true, classes=list(range(len(CLASS_NAMES))))

    for idx, name in enumerate(CLASS_NAMES):
        if np.sum(binarized[:, idx]) == 0:
            continue
        fpr, tpr, _ = roc_curve(binarized[:, idx], y_probs[:, idx])
        ax.plot(fpr, tpr, lw=2, label=f"{name} (AUC = {auc(fpr, tpr):.2f})")

    ax.plot([0, 1], [0, 1], "k--", lw=1)
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel("False positive rate")
    ax.set_ylabel("True positive rate")
    ax.set_title("Receiver operating characteristic curves (test set)")
    ax.legend(loc="lower right", fontsize="small")
    ax.grid(True, linestyle=":", linewidth=0.5)
    fig.tight_layout(pad=0.5)
    _save_figure(fig, fig_dir, "fig-roc-curves")
    plt.close(fig)


def plot_precision_recall(y_true: np.ndarray, y_probs: np.ndarray, fig_dir: Path):
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    binarized = label_binarize(y_true, classes=list(range(len(CLASS_NAMES))))

    for idx, name in enumerate(CLASS_NAMES):
        positives = np.sum(binarized[:, idx])
        if positives == 0:
            continue
        precision, recall, _ = precision_recall_curve(binarized[:, idx], y_probs[:, idx])
        avg_pr = average_precision_score(binarized[:, idx], y_probs[:, idx])
        ax.plot(recall, precision, lw=2, label=f"{name} (AP = {avg_pr:.2f})")

    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.02])
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Precision–recall curves (test set imbalances)")
    ax.legend(loc="lower left", fontsize="small")
    ax.grid(True, linestyle=":", linewidth=0.5)
    fig.tight_layout(pad=0.5)
    _save_figure(fig, fig_dir, "fig-precision-recall-curves")
    plt.close(fig)


def main():
    sns.set_theme(style="whitegrid")
    _, fig_dir, preds_path = _base_paths()
    y_true, y_probs, y_pred = _load_predictions(preds_path)

    if y_probs.shape[1] != len(CLASS_NAMES):
        raise ValueError("Mismatch between predicted probabilities and expected classes.")

    plot_confusion(y_true, y_pred, fig_dir)
    plot_roc(y_true, y_probs, fig_dir)
    plot_precision_recall(y_true, y_probs, fig_dir)


if __name__ == "__main__":
    main()
