#!/usr/bin/env python3
"""
Post-hoc temperature scaling for the final Conformer Main_Model.

This script:
  - loads raw test-set predictions from
      Research_Runs/final_run_Main_Model_20250824_154136/raw_predictions.npz
  - computes baseline per-class ECE and Brier scores (15-bin reliability),
  - fits a single global temperature T by minimising negative log-likelihood,
    and
  - recomputes ECE/Brier after calibration.

Results are written to:
  Research_Runs/final_run_Main_Model_20250824_154136/temperature_scaling_results.txt

The implementation uses only NumPy; it does not retrain or modify the model.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Tuple, Dict

import numpy as np


RUN_DIR = Path("Research_Runs/final_run_Main_Model_20250824_154136")
NPZ_PATH = RUN_DIR / "raw_predictions.npz"
OUTPUT_PATH = RUN_DIR / "temperature_scaling_results.txt"

CLASS_NAMES = ["Normal", "SVEB", "VEB", "Fusion", "Unknown"]
NUM_BINS = 15


def softmax_temperature(probs: np.ndarray, temperature: float) -> np.ndarray:
    """
    Apply temperature scaling to probability vectors by working in log-space.

    Args:
        probs: Array of shape (N, K) with row-wise class probabilities.
        temperature: Positive scalar temperature T.

    Returns:
        Array of shape (N, K) with calibrated probabilities.
    """
    if temperature <= 0:
        raise ValueError("Temperature must be positive.")

    # Work in log space; an unknown additive log-constant cancels in softmax.
    log_p = np.log(np.clip(probs, 1e-12, 1.0))
    log_p_scaled = log_p / float(temperature)
    log_p_scaled -= log_p_scaled.max(axis=1, keepdims=True)
    exp_logits = np.exp(log_p_scaled)
    return exp_logits / exp_logits.sum(axis=1, keepdims=True)


def negative_log_likelihood(y_true: np.ndarray, probs: np.ndarray) -> float:
    """
    Compute mean negative log-likelihood for a multiclass classification problem.
    """
    probs_clipped = np.clip(probs[np.arange(len(y_true)), y_true], 1e-12, 1.0)
    return float(-np.mean(np.log(probs_clipped)))


def ece_and_brier_per_class(
    y_true: np.ndarray, probs: np.ndarray, num_bins: int
) -> Dict[str, Tuple[float, float]]:
    """
    Compute per-class ECE and Brier scores using 15-bin reliability estimates.
    """
    n_samples, n_classes = probs.shape
    bins = np.linspace(0.0, 1.0, num_bins + 1)

    metrics: Dict[str, Tuple[float, float]] = {}

    for class_index in range(n_classes):
        p = probs[:, class_index]
        y = (y_true == class_index).astype(float)

        brier = float(np.mean((p - y) ** 2))

        ece = 0.0
        for i in range(num_bins):
            lo, hi = bins[i], bins[i + 1]
            if i == 0:
                mask = (p >= lo) & (p <= hi)
            else:
                mask = (p > lo) & (p <= hi)
            if not np.any(mask):
                continue
            conf = float(p[mask].mean())
            acc = float(y[mask].mean())
            ece += (mask.sum() / n_samples) * abs(acc - conf)

        class_name = CLASS_NAMES[class_index] if class_index < len(CLASS_NAMES) else f"class_{class_index}"
        metrics[class_name] = (ece, brier)

    return metrics


def fit_global_temperature(
    y_true: np.ndarray, probs: np.ndarray, t_min: float = 0.5, t_max: float = 5.0, num_grid: int = 91
) -> float:
    """
    Fit a single global temperature T by grid search over [t_min, t_max].

    Returns:
        Best temperature (float) minimising the negative log-likelihood.
    """
    best_T = 1.0
    best_nll = math.inf

    for T in np.linspace(t_min, t_max, num_grid):
        calibrated = softmax_temperature(probs, float(T))
        nll = negative_log_likelihood(y_true, calibrated)
        if nll < best_nll:
            best_nll = nll
            best_T = float(T)

    return best_T


def main() -> None:
    if not NPZ_PATH.exists():
        raise FileNotFoundError(f"Could not find raw predictions at {NPZ_PATH}")

    data = np.load(NPZ_PATH)
    y_true = data["y_true"].astype(int)
    y_probs = data["y_pred_probs"].astype("float64")

    if y_probs.ndim != 2:
        raise ValueError(f"Expected 2D probs array, got shape {y_probs.shape}")

    # Baseline metrics (uncalibrated softmax).
    baseline_nll = negative_log_likelihood(y_true, y_probs)
    baseline_metrics = ece_and_brier_per_class(y_true, y_probs, NUM_BINS)

    # Fit temperature on the same test set (internal calibration).
    best_T = fit_global_temperature(y_true, y_probs)
    calibrated_probs = softmax_temperature(y_probs, best_T)

    calibrated_nll = negative_log_likelihood(y_true, calibrated_probs)
    calibrated_metrics = ece_and_brier_per_class(y_true, calibrated_probs, NUM_BINS)

    # Write summary to disk.
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        f.write("Temperature scaling for Main_Model (Conformer) on MIT-BIH test set\n")
        f.write("==================================================================\n\n")
        f.write(f"Number of test beats: {len(y_true)}\n")
        f.write(f"Number of classes: {y_probs.shape[1]}\n\n")

        f.write("Global temperature (single-parameter scaling):\n")
        f.write(f"  T* = {best_T:.3f}\n\n")

        f.write("Negative log-likelihood (mean over test beats):\n")
        f.write(f"  Baseline NLL   : {baseline_nll:.6f}\n")
        f.write(f"  Calibrated NLL : {calibrated_nll:.6f}\n\n")

        f.write(f"Per-class ECE and Brier scores (using {NUM_BINS} bins)\n")
        f.write("  Class           |  ECE_before  Brier_before  |  ECE_after   Brier_after\n")
        f.write("  -----------------------------------------------------------------------\n")
        for class_name in CLASS_NAMES:
            ece_b, brier_b = baseline_metrics[class_name]
            ece_a, brier_a = calibrated_metrics[class_name]
            f.write(
                f"  {class_name:<14}  {ece_b:10.3f}  {brier_b:12.3f}  |"
                f"  {ece_a:10.3f}  {brier_a:12.3f}\n"
            )

        f.write("\nNotes:\n")
        f.write(
            "- Temperature was fitted on the held-out MIT-BIH test cohort itself,\n"
            "  so these values quantify internal calibration rather than external\n"
            "  generalisation.\n"
        )
        f.write(
            "- The script operates entirely on stored probabilities from\n"
            "  raw_predictions.npz and does not retrain or modify the model.\n"
        )


if __name__ == "__main__":
    main()

