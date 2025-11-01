# ======================================================================================
# Evaluator.py (Rewritten, Clean & Efficient Version)
#
# Author: [Your Name/Organization] - Refactored by AI Assistant
# Date: 2025-08-22
#
# Description:
# This rewritten version fixes a critical "out of data" bug and significantly
# improves performance by processing the test dataset only once. It now correctly
# and efficiently calculates all evaluation metrics and generates plots.
# ======================================================================================

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc, precision_recall_curve, average_precision_score
from sklearn.preprocessing import label_binarize
import logging
import os
from typing import List
from tqdm import tqdm

logger = logging.getLogger(__name__)

class Evaluator:
    """
    Handles advanced, efficient evaluation of a multi-class classification model.
    """
    def __init__(self,
                 model: tf.keras.Model,
                 test_dataset: tf.data.Dataset,
                 test_steps: int, # <-- KEY FIX 1: Added test_steps parameter
                 class_names: List[str]):
        """
        Initializes the Evaluator.

        Args:
            model (tf.keras.Model): The trained Keras model to be evaluated.
            test_dataset (tf.data.Dataset): The tf.data.Dataset for the test set.
            test_steps (int): The total number of batches in the test dataset.
            class_names (List[str]): A list of names for the target classes.
        """
        self.model = model
        self.test_dataset = test_dataset
        self.test_steps = test_steps
        self.class_names = class_names
        self.num_classes = len(class_names)
        self.y_true = None
        self.y_pred_probs = None
        self.y_pred_classes = None
        self.report = None
        self.roc_auc = None

    def evaluate(self):
        """
        Performs the full evaluation pipeline: prediction, metric calculation, and AUC computation.
        """
        logger.info("Starting evaluation on the test set...")

        # --- KEY FIX 2: Efficiently get all predictions and true labels in a single pass ---
        # This is much faster as it avoids iterating through the dataset twice.
        y_true_list = []
        y_pred_probs_list = []

        logger.info(f"Generating predictions and collecting true labels ({self.test_steps} steps)...")
        # Iterate through the dataset, predicting on each batch and collecting labels.
        # Using .take() ensures we don't loop forever if the dataset was accidentally repeated.
        for x, y in tqdm(self.test_dataset.take(self.test_steps), total=self.test_steps, desc="Evaluating Test Set"):
            y_true_list.append(y.numpy())
            y_pred_probs_list.append(self.model.predict_on_batch(x))

        self.y_true = np.concatenate(y_true_list)
        self.y_pred_probs = np.concatenate(y_pred_probs_list)

        # Ensure the number of labels matches predictions, trimming if necessary.
        # This handles the case where the last batch might not be full.
        num_predictions = self.y_pred_probs.shape[0]
        self.y_true = self.y_true[:num_predictions]
        self.y_pred_classes = np.argmax(self.y_pred_probs, axis=1)

        if self.y_true is None or self.y_pred_classes is None:
            logger.error("Could not generate predictions or true labels. Evaluation aborted.")
            return

        logger.info("Calculating classification report...")
        self.report = classification_report(self.y_true, self.y_pred_classes, target_names=self.class_names, zero_division=0)
        logger.info("Classification Report:\n" + self.report)

        logger.info("Calculating ROC curve and AUC for each class...")
        self._calculate_roc_auc()

    def _calculate_roc_auc(self):
        """Calculates ROC and AUC for each class using the One-vs-Rest (OvR) strategy."""
        y_true_binarized = label_binarize(self.y_true, classes=range(self.num_classes))

        self.roc_auc = {"fpr": {}, "tpr": {}, "auc": {}}

        for i in range(self.num_classes):
            # Handle cases where a class might not be present in the true labels
            if np.sum(y_true_binarized[:, i]) > 0:
                self.roc_auc["fpr"][i], self.roc_auc["tpr"][i], _ = roc_curve(y_true_binarized[:, i], self.y_pred_probs[:, i])
                self.roc_auc["auc"][i] = auc(self.roc_auc["fpr"][i], self.roc_auc["tpr"][i])
                logger.info(f"AUC for class '{self.class_names[i]}': {self.roc_auc['auc'][i]:.4f}")
            else:
                self.roc_auc["fpr"][i], self.roc_auc["tpr"][i], self.roc_auc["auc"][i] = [], [], float('nan')
                logger.warning(f"Class '{self.class_names[i]}' not found in true labels. AUC cannot be calculated.")

    def _plot_precision_recall_curves(self, run_dir: str):
        """Plots and saves Precision-Recall curves for each class."""
        prc_path = os.path.join(run_dir, "precision_recall_curves.png")
        plt.figure(figsize=(10, 8))

        y_true_binarized = label_binarize(self.y_true, classes=range(self.num_classes))

        for i in range(self.num_classes):
             if self.roc_auc["fpr"][i].size > 0:
                precision, recall, _ = precision_recall_curve(y_true_binarized[:, i], self.y_pred_probs[:, i])
                avg_precision = average_precision_score(y_true_binarized[:, i], self.y_pred_probs[:, i])
                plt.plot(recall, precision, lw=2,
                         label=f'PR curve for {self.class_names[i]} (AP = {avg_precision:.2f})')

        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('Multi-Class Precision-Recall Curves')
        plt.legend(loc="best")
        plt.grid()
        plt.savefig(prc_path)
        plt.close()
        logger.info(f"Precision-Recall curves plot saved to: {prc_path}")

    def save_results(self, run_dir: str):
        """
        Saves all evaluation artifacts (report, plots) to the specified run directory.
        """
        if self.report is None:
            logger.warning("No evaluation report to save. Please run evaluate() first.")
            return

        report_path = os.path.join(run_dir, "classification_report.txt")
        with open(report_path, 'w') as f:
            f.write("Classification Report\n=========================\n")
            f.write(self.report)
            f.write("\n\nArea Under Curve (AUC) Scores\n=========================\n")
            for i in range(self.num_classes):
                auc_score = self.roc_auc['auc'][i]
                f.write(f"AUC for class '{self.class_names[i]}': {auc_score:.4f}\n")
        logger.info(f"Classification report and AUC scores saved to: {report_path}")

        cm_path = os.path.join(run_dir, "confusion_matrix.png")
        cm = confusion_matrix(self.y_true, self.y_pred_classes)
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                    xticklabels=self.class_names, yticklabels=self.class_names)
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted Label')
        plt.ylabel('True Label')
        plt.savefig(cm_path)
        plt.close()
        logger.info(f"Confusion matrix plot saved to: {cm_path}")

        roc_path = os.path.join(run_dir, "roc_curves.png")
        plt.figure(figsize=(10, 8))
        for i in range(self.num_classes):
            if self.roc_auc["fpr"][i].size > 0:

                plt.plot(self.roc_auc["fpr"][i], self.roc_auc["tpr"][i],
                         label=f'ROC curve for {self.class_names[i]} (AUC = {self.roc_auc["auc"][i]:.2f})')

        plt.plot([0, 1], [0, 1], 'k--') # Dashed diagonal
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Multi-Class ROC Curves (One-vs-Rest)')
        plt.legend(loc="lower right")
        plt.grid()
        plt.savefig(roc_path)
        plt.close()
        logger.info(f"ROC curves plot saved to: {roc_path}")

        self._plot_precision_recall_curves(run_dir)

        predictions_path = os.path.join(run_dir, "raw_predictions.npz")
        np.savez_compressed(predictions_path,
                            y_true=self.y_true,
                            y_pred_probs=self.y_pred_probs,
                            y_pred_classes=self.y_pred_classes)
        logger.info(f"Raw predictions saved to: {predictions_path}")