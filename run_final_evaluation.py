# ======================================================================================
# run_final_evaluation.py (Final Corrected & Optimized Version)
#
# Author: [Your Name/Organization] - Refactored by AI Assistant
# Date: 2025-08-22
#
# Description:
# This is the final stage of the research pipeline. This script loads the best
# model configuration and trains it on the entire training dataset (all k-fold records).
# It then performs a final, unbiased evaluation on the held-out test set. All
# data pipeline and memory usage bugs have been resolved.
# ======================================================================================

import os
import sys
import logging
import json
from pathlib import Path
import numpy as np
import tensorflow as tf
import keras_tuner as kt
from tqdm import tqdm
import h5py
from sklearn.preprocessing import StandardScaler
import datetime
import argparse

# --- Custom Module Imports ---
from ModelBuilder import ModelBuilder
from DataLoader import create_dataset, get_all_labels
from Evaluator import Evaluator # Assumes you are using the corrected version of Evaluator.py
from HistoryManager import HistoryManager
from sklearn.utils.class_weight import compute_class_weight

# --- Configuration (Loaded from file) ---
CONFIG = {}

# --- Setup & Helper Functions ---
def setup_environment(model_name: str):
    """Initializes logging, GPU, and random seeds for the final run."""
    run_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_path = Path("Research_Runs") / f"final_run_{model_name}_{run_timestamp}"
    run_path.mkdir(parents=True, exist_ok=True)

    log_formatter = logging.Formatter('%(asctime)s [%(levelname)-8s] %(name)s: %(message)s (%(filename)s:%(lineno)d)')
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    file_handler = logging.FileHandler(run_path / "final_run_log.txt")
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
            logging.info(f"✅ GPU memory growth and Mixed Precision enabled.")
        except RuntimeError as e:
            logging.error(f"❌ Could not configure GPU: {e}")
    
    return run_path

def find_latest_tuning_artifacts(model_name: str) -> (Path, Path, Path):
    """Finds all required artifacts from the most recent tuning run for a specific model."""
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

# --- FINAL FIX 1: Memory-efficient normalization stats calculation ---
def calculate_final_normalization_stats(train_records: list, data_config: dict, chunk_size: int = 128) -> (np.ndarray, np.ndarray):
    """
    Calculates the final mean and std deviation in a memory-efficient way by processing data in chunks.
    This is the most critical fix to prevent the OS from killing the process due to high RAM usage.
    """
    logger = logging.getLogger(__name__)
    scaler = StandardScaler()
    h5_dir = Path(data_config["preprocessed_dir"])

    logger.info("Calculating final normalization statistics in memory-efficient chunks...")
    for rec_name in tqdm(train_records, desc="Calculating Final Scaler Stats"):
        h5_path = h5_dir / f"{rec_name}.h5"
        try:
            with h5py.File(h5_path, 'r') as hf:
                if 'scalograms' not in hf:
                    continue
                
                dataset = hf['scalograms']
                num_samples = dataset.shape[0]

                # Process the HDF5 dataset in smaller chunks
                for i in range(0, num_samples, chunk_size):
                    end_index = min(i + chunk_size, num_samples)
                    data_chunk = dataset[i:end_index] # Reads only a small part into memory
                    
                    reshaped_chunk = data_chunk.reshape(-1, data_chunk.shape[-1])
                    scaler.partial_fit(reshaped_chunk)

        except (IOError, KeyError, FileNotFoundError) as e:
            logger.warning(f"⚠️ Could not process {h5_path} for scaler stats: {e}")

    if not hasattr(scaler, 'mean_') or scaler.mean_ is None:
        logger.error("❌ Scaler could not be fitted. Not enough valid training data found.")
        return None, None

    logger.info("✅ Final normalization statistics calculated successfully (memory-efficiently).")
    return scaler.mean_.astype(np.float32), scaler.scale_.astype(np.float32)

# --- Main Execution Block ---
def main():
    """Main function for final training, evaluation, and artifact generation."""
    parser = argparse.ArgumentParser(description="Run the final evaluation stage of the model.")
    parser.add_argument('--model_name', type=str, default='Main_Model', choices=['Main_Model','AttentionOnly', 'Baseline_Model', 'CNNLSTM_Model'], help='The name of the model to train and evaluate.')
    parser.add_argument('--epochs', type=int, help='Override the number of training epochs for the final model.')
    parser.add_argument('--batch_size', type=int, help='Override the batch size for creating the final datasets.')
    args = parser.parse_args()
    model_name_to_finalize = args.model_name

    final_run_path = setup_environment(model_name_to_finalize)
    logger = logging.getLogger(__name__)
    logger.info(f"=== FINAL STAGE: Training & Evaluation for {model_name_to_finalize} ===")

    logger.info("STEP 1: Locating artifacts from the most recent tuning run...")
    hp_path, config_path, splits_path = find_latest_tuning_artifacts(model_name_to_finalize)
    if not hp_path:
        logger.error(f"❌ Critical Error: Could not find artifacts for '{model_name_to_finalize}'.")
        logger.error(f"Please run 'run_hyperparameter_tuning.py --model_name {model_name_to_finalize}' first. Exiting.")
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

    logger.info("STEP 2: Preparing final datasets and building the champion model...")
    train_records = data_splits['kfold_records']
    test_records = data_splits['final_test_records']
    logger.info(f"Using {len(train_records)} records for final training and {len(test_records)} for final testing.")

    mean, scale = calculate_final_normalization_stats(train_records, CONFIG["data"])
    if mean is None:
        logger.error("❌ Halting execution due to failure in normalization statistics calculation.")
        sys.exit(1)

    batch_size = args.batch_size if args.batch_size else CONFIG["training"]['batch_size']
    logger.info(f"Using batch size: {batch_size}")

    train_ds = create_dataset(train_records, CONFIG["data"], batch_size, is_training=True, mean=mean, scale=scale)
    test_ds = create_dataset(test_records, CONFIG["data"], batch_size, is_training=False, mean=mean, scale=scale)
    
    # --- FINAL FIX 2: Explicitly repeat the training dataset ---
    train_ds = train_ds.repeat()

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
    final_model = model_functions[model_name_to_finalize](best_hps)
    logger.info("✅ Champion model built successfully.")

    logger.info("STEP 3: Training the final model on the entire training dataset...")
    try:
        final_training_epochs = args.epochs if args.epochs else CONFIG["training"].get("final_training_epochs", 20)
        logger.info(f"Starting final training for {final_training_epochs} epochs.")
        
        # --- FINAL FIX 3: Calculate precise steps for training ---
        y_train_full = get_all_labels(train_records, CONFIG["data"])
        steps_per_epoch = max(1, int(np.ceil(len(y_train_full) / batch_size)))
        
        class_weights = dict(enumerate(compute_class_weight('balanced', classes=np.unique(y_train_full), y=y_train_full)))
        logger.info(f"Applying class weights for final training: {class_weights}")
        
        history = final_model.fit(
            train_ds, 
            epochs=final_training_epochs, 
            steps_per_epoch=steps_per_epoch,
            class_weight=class_weights,
            verbose=1
        )
        logger.info(f"✅ Final model training completed.")

        model_path = final_run_path / f"final_model_{model_name_to_finalize}.keras"
        final_model.save(model_path)
        logger.info(f"💾 Final trained model saved to: {model_path}")

        history_manager = HistoryManager(history_path=str(final_run_path / "final_model_training_history.json"))
        history_manager.save_history(history)

        logger.info("STEP 4: Evaluating the final model on the hold-out test set...")
        # --- FINAL FIX 4: Calculate precise steps for the test set and pass them to the Evaluator ---
        y_test = get_all_labels(test_records, CONFIG["data"])
        test_steps = max(1, int(np.ceil(len(y_test) / batch_size)))
        
        evaluator = Evaluator(final_model, test_ds, test_steps, CONFIG["data"]["class_names"])
        evaluator.evaluate()
        evaluator.save_results(str(final_run_path))

    except Exception as e:
        logger.error(f"❌ A critical error occurred during final training or evaluation: {e}", exc_info=True)
        sys.exit(1)

    logger.info("==========================================================")
    logger.info("=== RESEARCH PIPELINE COMPLETED SUCCESSFULLY           ===")
    logger.info(f"All final results are saved in: {final_run_path}")
    logger.info("==========================================================")

if __name__ == '__main__':
    main()