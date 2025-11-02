# HistoryManager.py (Final Version for saving training history)
import json
import os
import logging
import tensorflow as tf
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)

class HistoryManager:
    """
    Manages the saving of Keras model training history to a JSON file.
    """
    def __init__(self, history_path: str):
        """
        Initializes the HistoryManager with the path for the history JSON file.
        """
        self.history_path = history_path

    def save_history(self, keras_history_obj: tf.keras.callbacks.History):
        """
        Saves the training history from a Keras History object to a JSON file.
        """
        if not hasattr(keras_history_obj, 'history') or not isinstance(keras_history_obj.history, dict):
            logger.error("Invalid Keras History object provided. Cannot save.")
            return

        # Convert all numpy types to native Python types for JSON serialization
        history_dict_to_save = {k: [float(vi) for vi in v] for k, v in keras_history_obj.history.items()}
        
        try:
            with open(self.history_path, 'w') as f:
                json.dump(history_dict_to_save, f, indent=4)
            logger.info(f"💾 Training history saved successfully to: {self.history_path}")
        except Exception as e:
            logger.error(f"❌ Could not write history to {self.history_path}: {e}", exc_info=True)