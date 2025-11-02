# preprocess_data.py (Rewritten - Stage 1)
# Author: [Your Name/Organization]
# Date: 2025-08-18
# Description: This rewritten script removes all data normalization (StandardScaler)
# to prevent data leakage. It now computes scalograms from the raw signals and
# stores them in HDF5 format, one file per record.

import json
import logging
import time
from pathlib import Path
from typing import List, Dict, Any, Tuple
from functools import partial
import multiprocessing

import numpy as np
import wfdb
import pywt
import h5py
from tqdm import tqdm

# --- Configuration ---
class Config:
    """Holds all static configuration parameters for the preprocessing script."""
    DB_DIRECTORY = "mit-bih-arrhythmia-database-1.0.0"
    RECORD_NAMES = [
        '100', '101', '103', '105', '106', '108', '109', '111', '112', '113', '114',
        '115', '116', '117', '118', '119', '121', '122', '123', '124', '200', '201',
        '202', '203', '205', '207', '208', '209', '210', '212', '213', '214', '215',
        '217', '219', '220', '221', '222', '223', '228', '230', '231', '232', '233', '234'
    ]
    TIME_STEPS_PER_BEAT = 187
    WAVELET_NAME = 'morl'
    WAVELET_SCALES = list(range(1, 33))
    OUTPUT_DIRECTORY = "preprocessed_data_h5_raw" # Directory for non-normalized HDF5 files
    METADATA_FILENAME = "metadata.json"
    AAMI_MAP = {
        'N': 0, 'L': 0, 'R': 0, 'e': 0, 'j': 0, 'n': 0, 'B': 0,
        'A': 1, 'a': 1, 'J': 1, 'S': 1,
        'V': 2, 'E': 2,
        'F': 3,
        '/': 4, 'f': 4, 'Q': 4, '?': 4
    }

# --- Setup Logging ---
def setup_logging():
    """Configures the root logger for the script."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)-8s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

# --- Core Functions ---

def process_record_worker(rec_name: str, config: Config) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Worker function to be run in a separate process. It processes a single
    record, computes scalograms from the RAW signal, and saves them into an HDF5 file.
    The StandardScaler has been removed from this function.
    """
    record_metadata = []
    record_scalograms = []
    half_window = config.TIME_STEPS_PER_BEAT // 2
    output_dir = Path(config.OUTPUT_DIRECTORY)

    try:
        # Load record and annotations
        record = wfdb.rdrecord(f"{config.DB_DIRECTORY}/{rec_name}")
        annotation = wfdb.rdann(f"{config.DB_DIRECTORY}/{rec_name}", 'atr')
        r_peaks, symbols = annotation.sample, annotation.symbol

        # The signal is used directly without scaling
        raw_signal = record.p_signal[:, 0].flatten()

        # Extract valid beats and compute their scalograms
        beat_index = 0
        for peak, symbol in zip(r_peaks, symbols):
            if symbol in config.AAMI_MAP:
                # Boundary check to ensure the window is within signal limits
                if half_window < peak < len(raw_signal) - half_window:
                    start, end = peak - half_window, peak + half_window + 1
                    heartbeat_signal = raw_signal[start:end]

                    # Compute CWT on the raw heartbeat signal
                    coeffs, _ = pywt.cwt(heartbeat_signal, config.WAVELET_SCALES, config.WAVELET_NAME)
                    scalogram = np.abs(coeffs).astype(np.float32)
                    
                    # Collect scalograms and metadata
                    record_scalograms.append(scalogram)
                    record_metadata.append({
                        "record_name": rec_name,
                        "beat_index": beat_index, # This is the index within the HDF5 dataset
                        "label": config.AAMI_MAP[symbol]
                    })
                    beat_index += 1
        
        # After collecting all beats, save them to a single HDF5 file
        if record_scalograms:
            output_path = output_dir / f"{rec_name}.h5"
            with h5py.File(output_path, 'w') as hf:
                hf.create_dataset("scalograms", data=np.array(record_scalograms))
        
        return rec_name, record_metadata
    except Exception as e:
        # Log the error and return an empty list to indicate failure
        logging.error(f"Worker failed to process record {rec_name}: {e}")
        return rec_name, []

def main():
    """Main execution function for the parallel HDF5 preprocessing pipeline."""
    logger = setup_logging()
    config = Config()
    output_dir = Path(config.OUTPUT_DIRECTORY)
    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("--- Starting Parallel HDF5 Preprocessing (Scaler Removed) ---")
    start_time = time.time()

    # Step 1: Process all records in parallel using a process pool
    all_metadata = []
    num_processes = max(1, multiprocessing.cpu_count() - 1)
    logger.info(f"Initializing process pool with {num_processes} workers.")

    # Use 'partial' to create a callable with fixed arguments for the pool
    worker_func = partial(process_record_worker, config=config)

    with multiprocessing.Pool(processes=num_processes) as pool:
        # Use imap_unordered for efficiency and tqdm for a progress bar
        results = list(tqdm(
            pool.imap_unordered(worker_func, config.RECORD_NAMES),
            total=len(config.RECORD_NAMES),
            desc="Processing all records (raw signals)"
        ))

    # Step 2: Consolidate metadata from all successful worker processes
    for rec_name, metadata in results:
        if metadata:
            all_metadata.extend(metadata)
        else:
            logger.warning(f"Record {rec_name} produced no metadata, likely due to a processing error.")

    # Step 3: Save the consolidated metadata to a single JSON file
    metadata_path = output_dir / config.METADATA_FILENAME
    logger.info(f"Saving metadata for {len(all_metadata)} total beats to {metadata_path}...")
    try:
        # Sort metadata to ensure a consistent and readable order
        all_metadata.sort(key=lambda x: (x['record_name'], x['beat_index']))
        with open(metadata_path, 'w') as f:
            json.dump(all_metadata, f, indent=4)
        logger.info("Metadata file saved successfully.")
    except IOError as e:
        logger.error(f"Could not write metadata file: {e}")

    end_time = time.time()
    logger.info(f"--- Preprocessing Complete in {end_time - start_time:.2f} seconds ---")

if __name__ == "__main__":
    # Ensure the script is runnable from the command line
    main()