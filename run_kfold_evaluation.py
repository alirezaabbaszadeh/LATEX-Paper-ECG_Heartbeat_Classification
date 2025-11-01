# ======================================================================================
# run_kfold_evaluation.py (Definitive & Optimized Version)
#
# Author: [Your Name/Organization] - Merged & Optimized by AI Assistant
# Date: 2025-08-23
#
# Description:
# This definitive version combines the best features of previous iterations.
# It uses a robust, external configuration loading mechanism to ensure consistency,
# employs a memory-efficient method for calculating normalization statistics to handle
# large datasets, and generates comprehensive artifacts, including the best model,
# performance plots, and a detailed summary JSON with both accuracy and loss metrics.
# ======================================================================================

import os
import sys
import logging
import datetime
import json
from pathlib import Path
import numpy as np
import tensorflow as tf
from sklearn.model_selection import KFold
import keras_tuner as kt
from sklearn.utils.class_weight import compute_class_weight
import argparse
import h5py
from tqdm import tqdm
import matplotlib.pyplot as plt


# --- Custom Module Imports ---
from ModelBuilder import ModelBuilder
from DataLoader import create_dataset, get_all_labels
from HistoryManager import HistoryManager

# --- 1. CENTRALIZED CONFIGURATION (Loaded from file) ---
# The CONFIG dictionary is intentionally left empty. It will always be
# loaded from the tuning artifact file to ensure perfect consistency.
CONFIG = {}

# --- 2. SETUP & HELPER FUNCTIONS ---
def setup_environment(model_name: str):
    """Initializes logging and GPU settings for the evaluation run."""
    run_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_path = Path("Research_Runs") / f"kfold_eval_{model_name}_{run_timestamp}"
    run_path.mkdir(parents=True, exist_ok=True)

    log_formatter = logging.Formatter('%(asctime)s [%(levelname)-8s] %(name)s: %(message)s (%(filename)s:%(lineno)d)')
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    file_handler = logging.FileHandler(run_path / "evaluation_log.txt")
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_formatter)
    root_logger.addHandler(stream_handler)

    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            policy = tf.keras.mixed_precision.Policy('mixed_float16')
            tf.keras.mixed_precision.set_global_policy(policy)
            logging.info(f"✅ GPU and Mixed Precision enabled.")
        except RuntimeError as e:
            logging.error(f"❌ Could not configure GPU: {e}")
    return run_timestamp, run_path

def find_latest_tuning_artifacts(model_name: str) -> (Path, Path, Path):
    """Finds all required artifacts from the most recent tuning run."""
    p = Path("Research_Runs")
    if not p.exists(): return None, None, None
    
    tuning_dirs = sorted(
        [d for d in p.iterdir() if d.is_dir() and d.name.startswith(f'tuning_{model_name}')],
        key=lambda d: d.name,
        reverse=True
    )
    if not tuning_dirs: return None, None, None
    latest_tuning_dir = tuning_dirs[0]
    
    hp_path = latest_tuning_dir / f"best_hyperparameters_{model_name}.json"
    config_path = latest_tuning_dir / "tuning_run_config.json"
    splits_path = latest_tuning_dir / "data_splits.json"

    if not all([hp_path.exists(), config_path.exists(), splits_path.exists()]):
        return None, None, None
        
    return hp_path, config_path, splits_path

def create_callbacks(callbacks_params: dict) -> list:
    """Creates a list of Keras callbacks from configuration."""
    callbacks_list = []
    if callbacks_params.get("early_stopping", {}).get("enabled", False):
        params = callbacks_params["early_stopping"].copy(); params.pop("enabled")
        callbacks_list.append(tf.keras.callbacks.EarlyStopping(**params))
    if callbacks_params.get("reduce_lr_on_plateau", {}).get("enabled", False):
        params = callbacks_params["reduce_lr_on_plateau"].copy(); params.pop("enabled")
        callbacks_list.append(tf.keras.callbacks.ReduceLROnPlateau(**params))
    return callbacks_list

def calculate_fold_normalization_stats(train_records: list, data_config: dict, chunk_size: int = 128) -> (np.ndarray, np.ndarray):
    """
    Calculates mean and std deviation in a memory-efficient way by processing data in chunks.
    This prevents Out-of-Memory errors on large datasets.
    """
    from sklearn.preprocessing import StandardScaler
    logger = logging.getLogger(__name__)
    scaler = StandardScaler()
    h5_dir = Path(data_config["preprocessed_dir"])
    
    logger.info("Calculating normalization stats in memory-efficient chunks...")
    
    for rec_name in tqdm(train_records, desc="Calculating Fold Scaler Stats", leave=False):
        h5_path = h5_dir / f"{rec_name}.h5"
        try:
            with h5py.File(h5_path, 'r') as hf:
                if 'scalograms' not in hf:
                    continue
                
                dataset = hf['scalograms']
                num_samples = dataset.shape[0]
                
                # Process the HDF5 dataset in smaller chunks to conserve memory
                for i in range(0, num_samples, chunk_size):
                    end_index = min(i + chunk_size, num_samples)
                    data_chunk = dataset[i:end_index]
                    
                    reshaped_chunk = data_chunk.reshape(-1, data_chunk.shape[-1])
                    scaler.partial_fit(reshaped_chunk)

        except (IOError, KeyError, FileNotFoundError) as e:
            logger.warning(f"⚠️ Could not process {h5_path} for scaler stats: {e}")
            
    if not hasattr(scaler, 'mean_') or scaler.mean_ is None:
        logger.error("❌ Scaler could not be fitted. Not enough valid training data found.")
        return None, None
        
    logger.info("✅ Fold-specific normalization statistics calculated successfully.")
    return scaler.mean_.astype(np.float32), scaler.scale_.astype(np.float32)

def save_summary_plot(results: list, mean_accuracy: float, run_path: Path, model_name: str):
    """Generates and saves a bar plot of K-Fold accuracies."""
    if not results: return

    fold_numbers = [f"Fold {r['fold']}" for r in results]
    accuracies = [r['accuracy'] for r in results]

    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.bar(fold_numbers, accuracies, color='skyblue', edgecolor='black')
    ax.axhline(mean_accuracy, color='crimson', linestyle='--', linewidth=2, label=f'Mean Acc: {mean_accuracy:.4f}')
    
    ax.set_ylim(bottom=max(0, min(accuracies) - 0.05), top=1.0)
    ax.set_xlabel('Fold Number', fontsize=12)
    ax.set_ylabel('Validation Accuracy', fontsize=12)
    ax.set_title(f'K-Fold Cross-Validation Accuracy for {model_name}', fontsize=14, fontweight='bold')
    ax.legend()

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2.0, yval + 0.005, f'{yval:.4f}', ha='center', va='bottom')

    plot_path = run_path / "kfold_accuracy_summary.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    logging.getLogger(__name__).info(f"✅ K-Fold summary plot saved to {plot_path}")

# --- 3. MAIN EXECUTION BLOCK ---
def main():
    """Main function to orchestrate the K-Fold evaluation."""
    parser = argparse.ArgumentParser(description="Run K-Fold evaluation using pre-tuned hyperparameters.")
    parser.add_argument('--model_name', type=str, default='Main_Model', choices=['Main_Model','AttentionOnly', 'Baseline_Model', 'CNNLSTM_Model'], help='The name of the tuned model to evaluate.')
    args = parser.parse_args()
    model_name_to_eval = args.model_name

    run_timestamp, run_path = setup_environment(model_name_to_eval)
    logger = logging.getLogger(__name__)
    logger.info(f"=== STAGE 2: K-Fold Evaluation for: {model_name_to_eval} ===")

    logger.info("STEP 1: Locating artifacts from the most recent tuning run...")
    hp_path, config_path, splits_path = find_latest_tuning_artifacts(model_name_to_eval)
    if not hp_path:
        logger.error(f"❌ Critical Error: Could not find artifacts for '{model_name_to_eval}'.")
        logger.error(f"Please run 'run_hyperparameter_tuning.py --model_name {model_name_to_eval}' first. Exiting.")
        sys.exit(1)
    logger.info(f"Found best hyperparameters, config, and data splits.")

    global CONFIG
    with open(config_path, 'r') as f: CONFIG = json.load(f)
    with open(hp_path, 'r') as f: best_hp_values = json.load(f)['values']
    with open(splits_path, 'r') as f: data_splits = json.load(f)

    best_hps = kt.HyperParameters()
    best_hps.values = best_hp_values
    logger.info(f"✅ Loaded optimal hyperparameters: {best_hp_values}")
    
    seed = CONFIG["environment"]["random_seed"]
    tf.random.set_seed(seed)
    np.random.seed(seed)

    logger.info(f"STEP 2: All artifacts for this run will be saved in: {run_path}")

    kfold_records = np.array(data_splits["kfold_records"])
    logger.info(f"STEP 3: Using {len(kfold_records)} records designated for K-Fold evaluation.")
    kfold = KFold(n_splits=CONFIG["training"]["k_folds"], shuffle=True, random_state=seed)
    
    with open(run_path / "evaluation_run_config.json", "w") as f: json.dump(CONFIG, f, indent=4)

    logger.info("STEP 4: Initializing the model builder...")
    model_builder = ModelBuilder(
        scalogram_shape=(len(CONFIG["data"]["wavelet_scales"]), CONFIG["data"]["time_steps_per_beat"]),
        sequence_len=CONFIG["data"]["sequence_len"], num_classes=CONFIG["model"]["num_classes"]
    )
    model_functions = {
        "Main_Model": model_builder.build_model,
        "AttentionOnly": model_builder.build_attention_only_model, 
        "Baseline_Model": model_builder.build_baseline_model, 
        "CNNLSTM_Model": model_builder.build_cnnlstm_model
    }
    selected_model_builder_func = model_functions.get(model_name_to_eval)

    logger.info(f"STEP 5: Starting K-Fold cross-validation...")
    all_fold_results = []
    best_fold_accuracy = 0.0
    best_fold_model_weights = None
    best_fold_num = -1

    for fold_num, (train_indices, val_indices) in enumerate(kfold.split(kfold_records), 1):
        logger.info(f"🚀 ========== STARTING FOLD {fold_num}/{CONFIG['training']['k_folds']} ==========")
        train_records_fold = kfold_records[train_indices].tolist()
        val_records_fold = kfold_records[val_indices].tolist()

        try:
            tf.keras.backend.clear_session()
            model = selected_model_builder_func(best_hps)
            
            mean, scale = calculate_fold_normalization_stats(train_records_fold, CONFIG["data"])
            if mean is None:
                logger.error(f"Skipping fold {fold_num} due to normalization error.")
                continue
                
            train_ds = create_dataset(train_records_fold, CONFIG["data"], CONFIG['training']['batch_size'], is_training=True, mean=mean, scale=scale)
            val_ds = create_dataset(val_records_fold, CONFIG["data"], CONFIG['training']['batch_size'], is_training=False, mean=mean, scale=scale)

            # Explicitly repeat the training dataset to ensure it doesn't run out of data.
            train_ds = train_ds.repeat()
            
            # Calculate precise steps for training and validation to prevent errors.
            y_train_fold = get_all_labels(train_records_fold, CONFIG["data"])
            y_val_fold = get_all_labels(val_records_fold, CONFIG["data"])
            
            class_weights = dict(enumerate(compute_class_weight('balanced', classes=np.unique(y_train_fold), y=y_train_fold)))
            
            batch_size = CONFIG['training']['batch_size']
            steps_per_epoch = max(1, int(np.ceil(len(y_train_fold) / batch_size)))
            validation_steps = max(1, int(np.ceil(len(y_val_fold) / batch_size)))

            logger.info(f"Calculated steps: {steps_per_epoch} for training, {validation_steps} for validation.")

            history = model.fit(
                train_ds, 
                epochs=CONFIG['training']['max_epochs_tuner'], 
                steps_per_epoch=steps_per_epoch, 
                validation_data=val_ds, 
                validation_steps=validation_steps,
                callbacks=create_callbacks(CONFIG['callbacks']), 
                class_weight=class_weights, 
                verbose=1 # Use progress bar for better user experience
            )
            
            history_manager = HistoryManager(str(run_path / f"fold_{fold_num}_history.json"))
            history_manager.save_history(history)
            
            logger.info(f"Evaluating model for fold {fold_num}...")
            results = model.evaluate(val_ds, steps=validation_steps, verbose=0)
            val_loss, val_accuracy = results[0], results[1]
            
            all_fold_results.append({'fold': fold_num, 'loss': val_loss, 'accuracy': val_accuracy})
            logger.info(f"✅ Fold {fold_num} completed. Val Loss: {val_loss:.4f}, Val Acc: {val_accuracy:.4f}")

            if val_accuracy > best_fold_accuracy:
                best_fold_accuracy = val_accuracy
                best_fold_model_weights = model.get_weights()
                best_fold_num = fold_num
                logger.info(f"🎉 New best model found in fold {fold_num} with accuracy: {val_accuracy:.4f}")

        except Exception as e:
            logger.error(f"❌ An exception occurred during Fold {fold_num}: {e}", exc_info=True)
            continue
    
    if best_fold_model_weights:
        logger.info(f"Saving the best model from fold {best_fold_num}...")
        tf.keras.backend.clear_session()
        best_model = selected_model_builder_func(best_hps)
        best_model.set_weights(best_fold_model_weights)
        best_model.save(run_path / f"best_kfold_model_{model_name_to_eval}.keras")
        logger.info(f"✅ Best model saved successfully.")

    if all_fold_results:
        fold_accuracies = [r['accuracy'] for r in all_fold_results]
        fold_losses = [r['loss'] for r in all_fold_results]
        mean_acc, std_acc = np.mean(fold_accuracies), np.std(fold_accuracies)
        mean_loss, std_loss = np.mean(fold_losses), np.std(fold_losses)
        
        summary = {
            "model_evaluated": model_name_to_eval, 
            "num_successful_folds": len(all_fold_results), 
            "best_fold": best_fold_num, 
            "mean_accuracy": mean_acc, 
            "std_accuracy": std_acc,
            "mean_loss": mean_loss,
            "std_loss": std_loss,
            "individual_fold_results": all_fold_results
        }
        
        with open(run_path / "kfold_summary.json", "w") as f: json.dump(summary, f, indent=4)
        logger.info(f"✅ K-Fold summary saved to kfold_summary.json")

        save_summary_plot(all_fold_results, mean_acc, run_path, model_name_to_eval)

        logger.info("📊 ========== K-FOLD EVALUATION SUMMARY ==========")
        logger.info(f"Model Evaluated: {model_name_to_eval}")
        logger.info(f"Mean Validation Accuracy: {mean_acc:.4f} ± {std_acc:.4f}")
        logger.info(f"Mean Validation Loss:     {mean_loss:.4f} ± {std_loss:.4f}")
        logger.info(f"Best performance was in Fold #{best_fold_num} with accuracy {best_fold_accuracy:.4f}")
        logger.info("===================================================")
    else:
        logger.error(f"❌ K-Fold evaluation for '{model_name_to_eval}' failed to produce any results.")

    logger.info("=== K-FOLD EVALUATION COMPLETED SUCCESSFULLY ===")
    logger.info(f"All results and logs are stored in: {run_path}")
    logger.info("You can now proceed to the final stage by running 'run_final_evaluation.py'")

if __name__ == '__main__':
    main()