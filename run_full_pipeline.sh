#!/bin/bash
# This script automates the entire pipeline:
# 1. Downloads the MIT-BIH Arrhythmia Database.
# 2. Preprocesses raw signals into HDF5 scalograms.
# 3. Creates batched TFRecords from the scalograms.
# 4. Runs hyperparameter tuning for a model.
# 5. Runs k-fold evaluation for the same model.
# 6. Runs the final training and evaluation on the test set.
# It repeats stages 4-6 for all models listed in the MODELS array.

# --- Download and preprocess data ---
echo "================================================================="
echo "=== DOWNLOADING RAW DATA ==="
echo "================================================================="
python download_data.py || exit 1

echo "================================================================="
echo "=== PREPROCESSING RAW SIGNALS ==="
echo "================================================================="
python preprocess_data.py || exit 1

echo "================================================================="
echo "=== CREATING BATCHED TFRECORDS ==="
echo "================================================================="
python create_batched_tfrecords.py || exit 1

# --- Define all models you want to run here ---
MODELS=(
    #"Main_Model"
    "AttentionOnly" "Baseline_Model" "CNNLSTM_Model")

# Loop through each model in the array
for model in "${MODELS[@]}"
do
    echo "================================================================="
    echo "=== STARTING PIPELINE FOR MODEL: $model ==="
    echo "================================================================="

    # --- STAGE 1: Hyperparameter Tuning ---
    echo "--- Running Hyperparameter Tuning for $model ---"
    python run_hyperparameter_tuning.py --model_name "$model"

    # Check if the last command was successful before proceeding
    if [ $? -eq 0 ]; then
        echo "--- Tuning for $model completed successfully. ---"
    else
        echo "--- ERROR: Hyperparameter tuning for $model failed. Stopping pipeline. ---"
        exit 1 # Exit the script with an error code
    fi

    # --- STAGE 2: K-Fold Evaluation ---
    echo "--- Running K-Fold Evaluation for $model ---"
    python run_kfold_evaluation.py --model_name "$model"

    if [ $? -eq 0 ]; then
        echo "--- K-Fold Evaluation for $model completed successfully. ---"
    else
        echo "--- ERROR: K-Fold Evaluation for $model failed. Stopping pipeline. ---"
        exit 1 # Exit the script with an error code
    fi

    # --- STAGE 3: Final Training & Evaluation ---
    # This new stage runs the final evaluation on the hold-out test set.
    echo "--- Running Final Evaluation for $model ---"
    python run_final_evaluation.py --model_name "$model"

    if [ $? -eq 0 ]; then
        echo "--- Final Evaluation for $model completed successfully. ---"
    else
        echo "--- ERROR: Final Evaluation for $model failed. Stopping pipeline. ---"
        exit 1 # Exit the script with an error code
    fi

    echo "=== PIPELINE FOR MODEL: $model COMPLETED ==="
    echo ""
done

echo "================================================================="
echo "====== ALL PIPELINE JOBS HAVE COMPLETED SUCCESSFULLY! ======"
echo "================================================================="