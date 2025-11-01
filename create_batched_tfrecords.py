# create_batched_tfrecords.py (Fixed Version)
# Author: [Your Name/Organization] - Corrected by AI Assistant
# Date: 2025-08-19
# Description: This corrected version resolves the "CUDA_ERROR_NOT_INITIALIZED"
# by making the helper functions TensorFlow-agnostic during multiprocessing.
# It prevents child processes from unnecessarily initializing the GPU, ensuring
# that the data preprocessing runs smoothly on the CPU without conflicts.

import json
import logging
import multiprocessing
import time
from pathlib import Path
from typing import List, Dict, Any

import h5py
import numpy as np
import tensorflow as tf
from tqdm import tqdm
import concurrent.futures
import os

# --- Configuration ---
SEQUENCE_LEN = 3
BATCH_SIZE_PER_CHUNK = 256
INPUT_H5_DIR = Path("preprocessed_data_h5_raw")
OUTPUT_TFRECORD_DIR = Path("tfrecord_data_batched")
METADATA_FILENAME = "metadata.json"

# --- Setup Logging ---
logger = logging.getLogger(__name__)

# --- TFRecord Helper Functions (Corrected) ---
def _bytes_feature(value):
    """
    Returns a bytes_list from a string / byte.
    This version is simplified to avoid calling tf.constant in child processes.
    """
    # The input 'value' is already in bytes format from numpy's .tobytes()
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _int64_feature(value):
    """Returns an int64_list from a bool / enum / int / uint."""
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

# --- Core Logic ---
def create_sequences_from_record(scalograms: np.ndarray, labels: np.ndarray, seq_len: int):
    """
    Efficiently creates overlapping sequences and their corresponding labels from
    a full record's data.
    """
    num_beats = scalograms.shape[0]
    if num_beats < seq_len:
        return np.array([]), np.array([])

    sequences = np.array([scalograms[i : i + seq_len] for i in range(num_beats - seq_len + 1)])
    sequence_labels = np.array([labels[i + seq_len - 1] for i in range(num_beats - seq_len + 1)])
    
    return sequences.astype(np.float32), sequence_labels.astype(np.int32)


def process_record_to_batched_tfrecord(
    rec_name: str,
    record_metadata: List[Dict[str, Any]],
    input_h5_dir: Path,
    output_tfrecord_dir: Path
):
    """
    Worker function: Processes a single HDF5 record, generates all sequences,
    and saves them in batched TFRecord format.
    """
    # --- CRITICAL FIX: Hide GPUs from this specific worker process ---
    # This ensures TensorFlow operations inside this function do not attempt
    # to initialize CUDA, which is the source of the error.
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

    h5_path = input_h5_dir / f"{rec_name}.h5"
    output_path = output_tfrecord_dir / f"{rec_name}.tfrecord"

    try:
        with h5py.File(h5_path, 'r') as hf:
            scalograms = hf['scalograms'][:]
        
        record_metadata.sort(key=lambda x: x['beat_index'])
        labels = np.array([item['label'] for item in record_metadata])

        sequences, sequence_labels = create_sequences_from_record(scalograms, labels, SEQUENCE_LEN)

        if sequences.shape[0] == 0:
            return f"Record {rec_name} had insufficient beats. Skipped."

        _, _, height, width = sequences.shape
        
        with tf.io.TFRecordWriter(str(output_path)) as writer:
            for i in range(0, sequences.shape[0], BATCH_SIZE_PER_CHUNK):
                seq_chunk = sequences[i : i + BATCH_SIZE_PER_CHUNK]
                label_chunk = sequence_labels[i : i + BATCH_SIZE_PER_CHUNK]
                num_in_chunk = seq_chunk.shape[0]

                feature = {
                    'num_in_batch': _int64_feature(num_in_chunk),
                    'sequence_len': _int64_feature(SEQUENCE_LEN),
                    'height': _int64_feature(height),
                    'width': _int64_feature(width),
                    'sequences_raw': _bytes_feature(seq_chunk.tobytes()),
                    'labels_raw': _bytes_feature(label_chunk.tobytes())
                }
                example = tf.train.Example(features=tf.train.Features(feature=feature))
                writer.write(example.SerializeToString())
        
        return f"Successfully processed record {rec_name}."

    except Exception as e:
        # Log the full traceback for better debugging
        logger.error(f"Worker failed for record {rec_name}: {e}", exc_info=True)
        return f"Failed to process record {rec_name}."

def main():
    """Main execution function for the parallel batched TFRecord conversion."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)-8s] %(message)s')
    logger.info("--- Starting Optimized Preprocessing: HDF5 to Batched TFRecords (Corrected) ---")
    start_time = time.time()

    OUTPUT_TFRECORD_DIR.mkdir(parents=True, exist_ok=True)

    metadata_path = INPUT_H5_DIR / METADATA_FILENAME
    try:
        with open(metadata_path, 'r') as f:
            all_metadata = json.load(f)
    except FileNotFoundError:
        logger.error(f"FATAL: Metadata file not found at {metadata_path}. Please run preprocess_data.py first. Exiting.")
        return

    metadata_map = {}
    for item in all_metadata:
        rec_name = item['record_name']
        if rec_name not in metadata_map:
            metadata_map[rec_name] = []
        metadata_map[rec_name].append(item)
    
    record_names = sorted(metadata_map.keys())
    if not record_names:
        logger.error(f"No records found in metadata. Cannot proceed.")
        return
    logger.info(f"Found metadata for {len(record_names)} records.")

    num_processes = max(1, multiprocessing.cpu_count() - 1)
    logger.info(f"Initializing process pool with {num_processes} workers.")
    
    # Using ProcessPoolExecutor which is generally more robust
    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = [
            executor.submit(
                process_record_to_batched_tfrecord,
                rec,
                metadata_map[rec],
                INPUT_H5_DIR,
                OUTPUT_TFRECORD_DIR
            )
            for rec in record_names
        ]
        
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(record_names), desc="Converting to Batched TFRecords"):
            pass

    end_time = time.time()
    logger.info(f"--- Preprocessing Complete in {end_time - start_time:.2f} seconds ---")
    logger.info(f"Optimized Batched TFRecord files are saved in '{OUTPUT_TFRECORD_DIR}'.")

if __name__ == "__main__":
    # It's good practice to set the start method for multiprocessing, especially on macOS/Windows
    try:
        multiprocessing.set_start_method('spawn')
    except RuntimeError:
        # The start method can only be set once.
        pass
    main()
