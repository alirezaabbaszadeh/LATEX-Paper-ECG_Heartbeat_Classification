"""Regenerate supplementary diagnostics from the archived final-run predictions."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import (
    auc,
    average_precision_score,
    confusion_matrix,
    precision_recall_curve,
    roc_curve,
)
from sklearn.preprocessing import label_binarize


ROOT = Path(__file__).resolve().parents[2]
PREDICTIONS = (
    ROOT
    / "Research_Runs"
    / "final_run_Main_Model_20250824_154136"
    / "raw_predictions.npz"
)
OUTPUT = ROOT / "paper-joe-submission" / "figures"
CLASS_NAMES = ["Normal", "SVEB", "VEB", "Fusion", "Unknown"]


def save_figure(path: Path) -> None:
    """Save one publication-scale PNG and close its Matplotlib figure."""
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()


def main() -> None:
    """Load archived arrays and regenerate the three diagnostic plots."""
    arrays = np.load(PREDICTIONS)
    y_true = arrays["y_true"]
    y_pred_probs = arrays["y_pred_probs"].astype(np.float64)
    y_pred_classes = arrays["y_pred_classes"]
    y_true_binary = label_binarize(y_true, classes=range(len(CLASS_NAMES)))

    cm = confusion_matrix(y_true, y_pred_classes, labels=range(len(CLASS_NAMES)))
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=CLASS_NAMES,
        yticklabels=CLASS_NAMES,
    )
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    save_figure(OUTPUT / "confusion_matrix.png")

    plt.figure(figsize=(10, 8))
    for index, class_name in enumerate(CLASS_NAMES):
        fpr, tpr, _ = roc_curve(y_true_binary[:, index], y_pred_probs[:, index])
        score = auc(fpr, tpr)
        plt.plot(fpr, tpr, linewidth=2, label=f"{class_name} (AUC = {score:.2f})")
    plt.plot([0, 1], [0, 1], "k--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("Multi-Class ROC Curves (One-vs-Rest)")
    plt.legend(loc="lower right")
    plt.grid(alpha=0.35)
    save_figure(OUTPUT / "roc_curves.png")

    plt.figure(figsize=(10, 8))
    for index, class_name in enumerate(CLASS_NAMES):
        precision, recall, _ = precision_recall_curve(
            y_true_binary[:, index], y_pred_probs[:, index]
        )
        score = average_precision_score(y_true_binary[:, index], y_pred_probs[:, index])
        plt.plot(recall, precision, linewidth=2, label=f"{class_name} (AP = {score:.2f})")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Multi-Class Precision-Recall Curves")
    plt.legend(loc="best")
    plt.grid(alpha=0.35)
    save_figure(OUTPUT / "precision_recall_curves.png")

    print(f"Regenerated diagnostics from {PREDICTIONS}")
    print(f"Confusion-matrix total: {cm.sum()}")
    print(f"Output directory: {OUTPUT}")


if __name__ == "__main__":
    main()
