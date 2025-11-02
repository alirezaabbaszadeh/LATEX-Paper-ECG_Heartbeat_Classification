# MainClass.py (Optimal Version - Modified for Flexibility)
# Author: [Your Name/Organization] - Modified by AI Assistant
# Date: 2025-08-19
# Description: This version removes the hardcoded 'tfrecord_dir' path.
# This makes the class more flexible and allows the run script to specify
# which TFRecord directory to use (either the old raw one or the new batched one)
# via the main CONFIG dictionary.

import os
import sys
import logging
import datetime
import json
import h5py
import numpy as np
import tensorflow as tf
from sklearn.model_selection import KFold, train_test_split
from sklearn.preprocessing import StandardScaler
from scipy import stats
from tqdm import tqdm
import keras_tuner as kt
from typing import Dict, List, Optional, Callable
import numpy as np


# Import all custom pipeline components
from DataLoader import create_dataset, get_all_labels
from HistoryManager import HistoryManager
from sklearn.utils.class_weight import compute_class_weight


logger = logging.getLogger(__name__)

class TimeSeriesModel:
    """
    Orchestrates a hyperparameter tuning process for a single fold using an
    optimal on-the-fly data normalization strategy.
    """
    def __init__(self,
                 data_params: Dict, model_params: Dict, training_params: Dict,
                 callbacks_params: Dict, train_records: List[str], val_records: List[str],
                 fold_num: int, run_timestamp: str, model_builder_function: Callable):
        self.data_params = data_params
        self.model_params = model_params
        self.training_params = training_params
        self.callbacks_params = callbacks_params
        self.train_records = train_records
        self.val_records = val_records
        self.fold_num = fold_num
        self.run_timestamp = run_timestamp
        self.model_builder_function = model_builder_function

        self.run_dir = self._setup_run_directory()
        self._setup_logging()
        self._save_configurations()

    def _calculate_scaler_stats(self, chunk_size: int = 128) -> (np.ndarray, np.ndarray):
        """
        Quickly and memory-efficiently calculates the mean and standard deviation
        for the training data of the current fold by processing data in chunks.
        """
        logger.info(f"[Fold {self.fold_num}] Calculating normalization stats in memory-efficient chunks...")
        scaler = StandardScaler()
        h5_dir = self.data_params["preprocessed_dir"]
        
        for rec_name in tqdm(self.train_records, desc=f"Calculating Stats (Fold {self.fold_num})"):
            try:
                with h5py.File(os.path.join(h5_dir, f"{rec_name}.h5"), 'r') as hf:
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

            except (IOError, KeyError) as e:
                logger.warning(f"Could not read {rec_name}.h5 for scaler stats: {e}")

        if not hasattr(scaler, 'mean_') or scaler.mean_ is None:
            logger.error(f"FATAL: Scaler could not be fitted for Fold {self.fold_num}.")
            raise RuntimeError(f"Scaler fitting failed for Fold {self.fold_num}.")

        logger.info(f"[Fold {self.fold_num}] Normalization stats calculated successfully (memory-efficiently).")
        return scaler.mean_.astype(np.float32), scaler.scale_.astype(np.float32)

    def _setup_run_directory(self) -> str:
        """Creates a unique directory for the fold."""
        run_dir = os.path.join("Research_Runs", f"run_{self.run_timestamp}", f"fold_{self.fold_num}")
        os.makedirs(run_dir, exist_ok=True)
        return run_dir

    def _setup_logging(self):
        """Configures file-based logging for the current fold."""
        log_file_path = os.path.join(self.run_dir, f'fold_{self.fold_num}_log.txt')
        if not any(isinstance(h, logging.FileHandler) and h.baseFilename == log_file_path for h in logging.getLogger().handlers):
            file_handler = logging.FileHandler(log_file_path, mode='w')
            formatter = logging.Formatter('%(asctime)s [%(levelname)-8s] %(name)s: %(message)s (%(filename)s:%(lineno)d)')
            file_handler.setFormatter(formatter)
            logging.getLogger().addHandler(file_handler)

    def _save_configurations(self):
        """Saves all configurations for this fold."""
        with open(os.path.join(self.run_dir, 'configuration.json'), 'w') as f:
            config_to_save = {k: v for k, v in self.__dict__.items() if k not in ['model_builder_function']}
            json.dump(config_to_save, f, indent=4, default=str)

    def _create_callbacks(self) -> List[tf.keras.callbacks.Callback]:
        """Creates a list of Keras callbacks from the provided configuration."""
        callbacks_list = []
        if self.callbacks_params.get("early_stopping", {}).get("enabled", False):
            params = self.callbacks_params["early_stopping"].copy(); params.pop("enabled")
            callbacks_list.append(tf.keras.callbacks.EarlyStopping(**params))
        if self.callbacks_params.get("reduce_lr_on_plateau", {}).get("enabled", False):
            params = self.callbacks_params["reduce_lr_on_plateau"].copy(); params.pop("enabled")
            callbacks_list.append(tf.keras.callbacks.ReduceLROnPlateau(**params))
        return callbacks_list

    def run(self) -> Optional[Dict[str, float]]:
        """Executes the hyperparameter search for the configured model."""
        logger.info(f"🚀 Starting Tuning for Fold {self.fold_num}...")
        try:
            # Step 1: Quickly calculate normalization stats for this fold
            mean, scale = self._calculate_scaler_stats()
        except Exception as e:
            logger.error(f"FATAL: Stat calculation failed for Fold {self.fold_num}: {e}", exc_info=True)
            return None

        # Step 2: Create datasets with on-the-fly normalization
        # The data_params dictionary passed from the constructor is now used directly.
        # This allows the caller (run_kfold_tuning.py) to control which dataset is used.
        # --- CRITICAL CHANGE IS HERE ---
        # The following hardcoded line has been REMOVED:
        # data_params['tfrecord_dir'] = "tfrecord_data_raw"
        
        train_ds = create_dataset(self.train_records, self.data_params, self.training_params['batch_size'], is_training=True, mean=mean, scale=scale)
        val_ds = create_dataset(self.val_records, self.data_params, self.training_params['batch_size'], is_training=False, mean=mean, scale=scale)

        # Step 3: Run the tuner
        tuner = kt.Hyperband(
            hypermodel=self.model_builder_function, objective='val_accuracy',
            max_epochs=self.training_params['max_epochs_tuner'], factor=3,
            directory=self.run_dir, project_name='hyperparameter_tuning'
        )
        
        try:
            # Calculate steps_per_epoch to fix the "Unknown" progress bar.
            y_train = get_all_labels(self.train_records, self.data_params)
            y_val = get_all_labels(self.val_records, self.data_params)
            
            num_train_samples = len(y_train)
            num_val_samples = len(y_val)
            
            batch_size = self.training_params['batch_size']
            
            steps_per_epoch = max(1, int(np.ceil(num_train_samples / batch_size)))
            validation_steps = max(1, int(np.ceil(num_val_samples / batch_size)))

            if steps_per_epoch == 0: steps_per_epoch = 1
            if validation_steps == 0: validation_steps = 1
                
            logger.info(f"Calculated steps per epoch: {steps_per_epoch} for training, {validation_steps} for validation.")

            weights = dict(enumerate(compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)))
            
            tuner.search(
                train_ds, 
                validation_data=val_ds, 
                callbacks=self._create_callbacks(), 
                class_weight=weights,
                steps_per_epoch=steps_per_epoch,
                validation_steps=validation_steps
            )

        except Exception as e:
            logger.error(f"An exception occurred during tuner.search(): {e}", exc_info=True)
            return None

        # Step 4: Retrieve and save results
        try:
            best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]
            with open(os.path.join(self.run_dir, 'best_hyperparameters.json'), 'w') as f:
                json.dump(best_hps.get_config(), f, indent=4)
            
            best_model = tuner.get_best_models(num_models=1)[0]
            results = best_model.evaluate(val_ds, steps=validation_steps, verbose=0)
            return {'loss': results[0], 'accuracy': results[1]}
        except (IndexError, ValueError) as e:
             logger.error(f"Could not retrieve best model from tuner: {e}")
             return None
