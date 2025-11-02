# DataLoader.py (Rewritten with Combined Shuffling Strategy)
# Author: [Your Name/Organization] - Enhanced by AI Assistant
# Date: 2025-08-23
# Description: This definitive version combines file-level shuffling with
# tf.data.Dataset.interleave to achieve maximum data randomization
# efficiently and without high memory usage.

import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

import numpy as np
import tensorflow as tf

logger = logging.getLogger(__name__)

# تابع get_all_labels بدون تغییر باقی می‌ماند
def get_all_labels(record_names: List[str], config: Dict[str, Any]) -> np.ndarray:
    """
    Quickly retrieves all labels for the sequences that will be generated
    from the given records by reading the precomputed metadata.json file.
    """
    metadata_path = Path(config["preprocessed_dir"]) / "metadata.json"
    sequence_len = config['sequence_len']
    try:
        with open(metadata_path, 'r') as f:
            all_metadata = json.load(f)
    except FileNotFoundError:
        logger.error(f"Metadata file not found at {metadata_path}. Please run preprocess_data.py first.")
        raise

    metadata_map = {item['record_name']: [] for item in all_metadata if item['record_name'] in record_names}
    for item in all_metadata:
        if item['record_name'] in metadata_map:
            metadata_map[item['record_name']].append(item)

    all_sequence_labels = []
    for rec_name in record_names:
        beats = sorted(metadata_map.get(rec_name, []), key=lambda x: x['beat_index'])
        if len(beats) >= sequence_len:
            for i in range(len(beats) - sequence_len + 1):
                all_sequence_labels.append(beats[i + sequence_len - 1]['label'])
                
    return np.array(all_sequence_labels, dtype=np.int32)


def create_dataset(
    record_names: List[str],
    config: Dict[str, Any],
    batch_size: int,
    is_training: bool = False,
    mean: Optional[np.ndarray] = None,
    scale: Optional[np.ndarray] = None
) -> tf.data.Dataset:
    """
    Creates a highly optimized tf.data.Dataset using a combined, two-stage
    shuffling strategy (file-level shuffle + interleave).
    """
    tfrecord_dir = Path(config.get("tfrecord_dir_batched", "tfrecord_data_batched"))
    tfrecord_files = [str(tfrecord_dir / f"{name}.tfrecord") for name in record_names if (tfrecord_dir / f"{name}.tfrecord").exists()]
    
    if not tfrecord_files:
        logger.error(f"No BATCHED TFRecord files found for the provided records in directory: {tfrecord_dir}")
        return tf.data.Dataset.from_tensor_slices(([], []))

    mean_tensor = tf.constant(mean, dtype=tf.float32) if mean is not None else None
    scale_tensor = tf.constant(scale, dtype=tf.float32) if scale is not None else None
    
    # --- START: Combined Shuffling Implementation ---

    # 1. Create a dataset from the file paths.
    files_dataset = tf.data.Dataset.from_tensor_slices(tfrecord_files)

    # 2. **Global Shuffle**: If training, shuffle the list of files. This is Solution 1.
    if is_training:
        files_dataset = files_dataset.shuffle(len(tfrecord_files))

    # 3. **Local Shuffle**: Use interleave to mix records from multiple files. This is Solution 2.
    dataset = files_dataset.interleave(
        lambda filepath: tf.data.TFRecordDataset(filepath),
        cycle_length=4,  # Adjust based on CPU cores, 4 is a safe default
        block_length=1,
        num_parallel_calls=tf.data.AUTOTUNE
    )
    
    # --- END: Combined Shuffling Implementation ---

    # The rest of the pipeline remains the same
    def _parse_batched_sequence(example_proto):
        feature_description = {
            'num_in_batch': tf.io.FixedLenFeature([], tf.int64),
            'sequence_len': tf.io.FixedLenFeature([], tf.int64),
            'height': tf.io.FixedLenFeature([], tf.int64),
            'width': tf.io.FixedLenFeature([], tf.int64),
            'sequences_raw': tf.io.FixedLenFeature([], tf.string),
            'labels_raw': tf.io.FixedLenFeature([], tf.string),
        }
        parsed = tf.io.parse_single_example(example_proto, feature_description)
        shape = [parsed['num_in_batch'], parsed['sequence_len'], parsed['height'], parsed['width']]
        sequences = tf.reshape(tf.io.decode_raw(parsed['sequences_raw'], tf.float32), shape)
        labels = tf.reshape(tf.io.decode_raw(parsed['labels_raw'], tf.int32), [parsed['num_in_batch']])
        return sequences, labels

    dataset = dataset.map(_parse_batched_sequence, num_parallel_calls=tf.data.AUTOTUNE)
    dataset = dataset.flat_map(lambda seq, lab: tf.data.Dataset.from_tensor_slices((seq, lab)))

    def normalize_and_format(scalogram_sequence, label):
        if mean_tensor is not None and scale_tensor is not None:
            scalogram_sequence = (scalogram_sequence - mean_tensor) / scale_tensor
        scalogram_sequence = tf.expand_dims(scalogram_sequence, axis=-1)
        return scalogram_sequence, label

    dataset = dataset.map(normalize_and_format, num_parallel_calls=tf.data.AUTOTUNE)

    if is_training:
        # Final shuffle with a small buffer. The heavy lifting is already done.
        dataset = dataset.shuffle(buffer_size=8)
        dataset = dataset.repeat()

    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(buffer_size=tf.data.AUTOTUNE)

    logger.info(f"Optimized tf.data.Dataset created using combined shuffling for {'training' if is_training else 'validation'}.")
    return dataset