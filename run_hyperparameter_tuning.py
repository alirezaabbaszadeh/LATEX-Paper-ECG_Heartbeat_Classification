# python run_hyperparameter_tuning.py --model_name Main_Model
# python run_hyperparameter_tuning.py --model_name AttentionOnly
# python run_hyperparameter_tuning.py --model_name Baseline_Model
# python run_hyperparameter_tuning.py --model_name CNNLSTM_Model
# ======================================================================================
# run_hyperparameter_tuning.py (Advanced, Flexible Version)
#
# Author: [Your Name/Organization] - Enhanced by AI Assistant
# Date: 2025-08-22
#
# Description:
# This advanced version of the tuning script offers greater flexibility.
# It allows selecting the model architecture to be tuned via a command-line
# argument (--model_name). It also improves artifact management by copying the
# final best hyperparameters file to the main run directory with a descriptive name.
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
from sklearn.model_selection import KFold, train_test_split
import argparse # <-- New import for command-line arguments
import shutil   # <-- New import for file operations

# --- Custom Module Imports ---
from MainClass import TimeSeriesModel
from ModelBuilder import ModelBuilder
from create_batched_tfrecords import main as create_batched_tfrecords

# --- 1. CENTRALIZED CONFIGURATION ---
CONFIG = {
    "data": {
        "preprocessed_dir": "preprocessed_data_h5_raw",
        "tfrecord_dir_batched": "tfrecord_data_batched",
        "record_names": [
            '100', '101','103', '105', '106', '108', '109', '111', '112', '113', '114',
            '115', '116', '117', '118', '119', '121', '122', '123', '124', '200', '201',
            '202', '203', '205', '207', '208', '209', '210', '212', '213', '214', '215',
            '217', '219', '220', '221', '222', '223', '228', '230', '231', '232', '233', '234'
        ],
        "sequence_len": 3,
        "time_steps_per_beat": 187,
        "wavelet_scales": list(range(1, 33)),
        "class_names": ['Normal', 'SVEB', 'VEB', 'Fusion', 'Unknown']
    },
    "model": {
        "num_classes": 5
    },
    "training": {
        "max_epochs_tuner": 20,
        "batch_size": 128,
        "k_folds": 5 # Still used to create a representative split
    },
    "callbacks": {
        "early_stopping": {"enabled": True, "monitor": "val_loss", "patience": 5},
        "reduce_lr_on_plateau": {"enabled": True, "monitor": "val_loss", "factor": 0.2, "patience": 1, "min_lr": 1e-6}
    },
    "environment": {
        "random_seed": 42
    },
    "output_dir": "Research_Runs"
}

# --- 2. SETUP & HELPER FUNCTIONS ---
def setup_environment(model_name: str):
    """Initializes logging, GPU, and random seeds for a named run."""
    run_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    # Directory name now includes the model being tuned
    run_path = Path(CONFIG["output_dir"]) / f"tuning_{model_name}_{run_timestamp}"
    run_path.mkdir(parents=True, exist_ok=True)

    log_formatter = logging.Formatter('%(asctime)s [%(levelname)-8s] %(name)s: %(message)s (%(filename)s:%(lineno)d)')
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(run_path / "tuning_log.txt")
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_formatter)
    root_logger.addHandler(stream_handler)

    os.environ['TF_DETERMINISTIC_OPS'] = '1'
    tf.random.set_seed(CONFIG["environment"]["random_seed"])
    np.random.seed(CONFIG["environment"]["random_seed"])

    # GPU setup
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            policy = tf.keras.mixed_precision.Policy('mixed_float16')
            tf.keras.mixed_precision.set_global_policy(policy)
            logging.info(f"✅ GPU memory growth and Mixed Precision (float16) enabled for {len(gpus)} GPU(s).")
        except RuntimeError as e:
            logging.error(f"❌ Could not configure GPU: {e}")

    return run_timestamp, run_path

def check_data_prerequisites():
    """Checks for HDF5 data and creates batched TFRecords if they are missing."""
    logger = logging.getLogger(__name__)
    h5_dir = Path(CONFIG["data"]["preprocessed_dir"])
    tfrecord_dir = Path(CONFIG["data"]["tfrecord_dir_batched"])

    if not h5_dir.exists() or not any(h5_dir.glob("*.h5")):
        logger.error(f"❌ Critical Error: HDF5 directory '{h5_dir}' is missing. Run 'preprocess_data.py'. Exiting.")
        sys.exit(1)

    if not tfrecord_dir.exists() or not any(tfrecord_dir.iterdir()):
        logger.warning(f"⚠️ Batched TFRecord directory '{tfrecord_dir}' not found. Creating them now...")
        try:
            create_batched_tfrecords()
            logger.info("✅ Successfully created batched TFRecord files.")
        except Exception as e:
            logger.error(f"❌ Fatal Error: Failed to create batched TFRecords: {e}. Exiting.", exc_info=True)
            sys.exit(1)
    else:
        logger.info(f"✅ Batched TFRecord data found in '{tfrecord_dir}'.")

# --- 3. MAIN EXECUTION BLOCK ---
def main():
    """Main function to orchestrate the hyperparameter tuning process."""
    # --- New Feature: Command-line argument parsing ---
    parser = argparse.ArgumentParser(description="Run focused hyperparameter tuning for a specified model.")
    parser.add_argument(
        '--model_name',
        type=str,
        default='Main_Model',
        choices=['Main_Model','AttentionOnly', 'Baseline_Model', 'CNNLSTM_Model'],
        help='The name of the model architecture to tune.'
    )
    args = parser.parse_args()
    model_name_to_tune = args.model_name

    run_timestamp, run_path = setup_environment(model_name_to_tune)
    logger = logging.getLogger(__name__)
    logger.info("==========================================================")
    logger.info(f"=== STAGE 1: Focused Hyperparameter Tuning for: {model_name_to_tune} ===")
    logger.info("==========================================================")

    logger.info("STEP 1: Checking for required data files...")
    check_data_prerequisites()

    logger.info(f"STEP 2: All artifacts for this tuning run will be saved in: {run_path}")


    # STEP 3: Create and save the definitive data split
    logger.info("STEP 3: Creating and saving the definitive data split...")
    all_records = np.array(CONFIG["data"]["record_names"])
    kfold_records, final_test_records = train_test_split(
        all_records, test_size=0.15, random_state=CONFIG["environment"]["random_seed"]
    )

    split_info = {
        "kfold_records": kfold_records.tolist(),
        "final_test_records": final_test_records.tolist()
    }
    with open(run_path / "data_splits.json", "w") as f:
        json.dump(split_info, f, indent=4)
    logger.info(f"✅ Data splits saved to {run_path / 'data_splits.json'}")

    # Save the main configuration file that other scripts will need
    with open(run_path / "tuning_run_config.json", "w") as f:
        json.dump(CONFIG, f, indent=4)
    logger.info(f"✅ Tuning run configuration saved to {run_path / 'tuning_run_config.json'}")

    # STEP 4: Creating a single representative data split for tuning...
    logger.info("STEP 4: Creating a single representative data split for tuning...")
    kfold = KFold(n_splits=CONFIG["training"]["k_folds"], shuffle=True, random_state=CONFIG["environment"]["random_seed"])
    # Use kfold_records now, not all_records
    train_indices, val_indices = next(kfold.split(kfold_records))
    train_records_fold = kfold_records[train_indices].tolist()
    val_records_fold = kfold_records[val_indices].tolist()

    # 1. Instantiate the ModelBuilder FIRST
    # This creates an object with the necessary configuration.
    model_builder = ModelBuilder(
        scalogram_shape=(len(CONFIG["data"]["wavelet_scales"]), CONFIG["data"]["time_steps_per_beat"]),
        sequence_len=CONFIG["data"]["sequence_len"],
        num_classes=CONFIG["model"]["num_classes"]
    )

    # 2. Use the INSTANCE (model_builder) to get the methods
    # This ensures that 'self' is correctly passed when Keras Tuner calls the function.
    model_functions = {
        "Main_Model": model_builder.build_model,
        "AttentionOnly": model_builder.build_attention_only_model,
        "Baseline_Model": model_builder.build_baseline_model,
        "CNNLSTM_Model": model_builder.build_cnnlstm_model
    }
    selected_model_builder_func = model_functions.get(model_name_to_tune)
    if not selected_model_builder_func:
        logger.error(f"FATAL: Model name '{model_name_to_tune}' is not valid. Check choices.")
        sys.exit(1)

    logger.info(f"STEP 5: Starting hyperparameter search for the '{model_name_to_tune}'...")
    try:
        pipeline = TimeSeriesModel(
            data_params=CONFIG["data"],
            model_params=CONFIG["model"],
            training_params=CONFIG["training"],
            callbacks_params=CONFIG["callbacks"],
            train_records=train_records_fold,
            val_records=val_records_fold,
            fold_num=1,
            run_timestamp=f"tuning_{model_name_to_tune}_{run_timestamp}",
            model_builder_function=selected_model_builder_func
        )
        val_metrics = pipeline.run()

        if val_metrics:
            logger.info(f"✅ Hyperparameter tuning completed. Best validation accuracy: {val_metrics.get('accuracy', -1):.4f}")
            
            # --- New Feature: Manage output file for easier access ---
            source_hp_path = Path(pipeline.run_dir) / 'best_hyperparameters.json'
            if source_hp_path.exists():
                dest_hp_path = run_path / f"best_hyperparameters_{model_name_to_tune}.json"
                shutil.copy(source_hp_path, dest_hp_path)
                logger.info(f"✅ Copied best hyperparameters to: {dest_hp_path}")
            else:
                logger.warning(f"⚠️ Could not find best hyperparameters file at {source_hp_path} to copy.")
        else:
            logger.error(f"❌ Hyperparameter tuning for '{model_name_to_tune}' failed to produce valid metrics.")
            sys.exit(1)

    except Exception as e:
        logger.error(f"❌ An unexpected exception occurred during the tuning process: {e}", exc_info=True)
        sys.exit(1)

    logger.info("======================================================")
    logger.info(f"=== HYPERPARAMETER TUNING FOR {model_name_to_tune} COMPLETED SUCCESSFULLY ===")
    logger.info(f"Tuning results and logs are in: {run_path}")
    logger.info("You can now proceed to STAGE 2 by running 'run_kfold_evaluation.py'")
    logger.info("======================================================")

if __name__ == '__main__':
    main()
