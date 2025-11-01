# ECG Heartbeat Classification

## Abstract
Leveraged the MIT‑BIH Arrhythmia Database of 48 half‑hour, two‑lead recordings sampled at 360 Hz, yielding about 109 000 annotated beats. Approximately 75 % were normal while the remainder encompassed supraventricular ectopic, ventricular ectopic, fusion, and unknown rhythms, covering five AAMI classes. The workflow isolated 187‑sample beats around each R‑peak, converted them to Morlet wavelet scalograms, and assembled three‑beat sequences to supply temporal context. A Conformer network—convolutional front‑end followed by stacked Conformer blocks with relative attention, residual feed‑forward layers, and dropout—learned joint temporal‑spectral features before a dense classifier. Training used class‑weighted cross‑entropy, normalization from training statistics, and five‑fold cross‑validation preceding a held‑out test. The final model reached 60 % accuracy, macro F1 0.26, weighted F1 0.68, and a mean one‑versus‑rest AUC of 0.66 (0.90 for normal beats). These findings indicated that a modest Conformer could distinguish common arrhythmias, pointing toward lightweight decision support for earlier clinical triage and remote monitoring in ambulatory and telemedicine settings, enabling scalable worldwide applications.

## Table of Contents
- [Clinical Relevance](#clinical-relevance)
- [Repository Overview](#repository-overview)
- [Installation](#installation)
- [Data Acquisition](#data-acquisition)
- [Ethics & Data Usage](#ethics--data-usage)
- [Preprocessing Pipeline](#preprocessing-pipeline)
- [Dataset Loading](#dataset-loading)
- [Model Architectures](#model-architectures)
- [Training](#training)
- [Evaluation](#evaluation)
- [Results](#results)
- [Hardware and Training Time](#hardware-and-training-time)
- [Diagnostic Plots](#diagnostic-plots)
- [One-Command End-to-End Pipeline](#one-command-end-to-end-pipeline)
- [Repository Structure](#repository-structure)
- [Reproducible Research](#reproducible-research)
- [Contributing](#contributing)
- [Citation](#citation)
- [Acknowledgments](#acknowledgments)
- [License](#license)
- [References](#references)

## Clinical Relevance
Electrocardiogram (ECG) analysis is central to detecting arrhythmias and other cardiac abnormalities. Accurate heartbeat classification helps clinicians identify life‑threatening conditions early, supports continuous patient monitoring, and guides timely intervention.

## Repository Overview
This repository investigates ECG heartbeat classification with a modern Conformer‑based architecture. It includes scripts for dataset preparation, focused hyperparameter tuning, and a comprehensive evaluation pipeline:

- **Hyperparameter tuning** – `run_hyperparameter_tuning.py` explores model configurations to optimize performance.
- **Conformer architecture** – `ModelBuilder.py` defines the CNN‑Conformer model and related ablation variants.
- **Evaluation workflow** – `run_kfold_evaluation.py` and `run_final_evaluation.py` provide reproducible k‑fold and held‑out evaluations.

## Installation

1. Ensure **Python 3.10 or newer** is installed. TensorFlow 2.20 requires Python ≥3.10.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Upgrade pip and install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. For GPU acceleration, install the NVIDIA driver and matching CUDA and cuDNN libraries for TensorFlow 2.20 (e.g., CUDA 12.2 and cuDNN 9.0). Refer to the official TensorFlow GPU documentation for details.

## Data Acquisition
### Data Summary & Availability

| Metric | Value |
| --- | --- |
| Record count | 48 |
| Total annotated beats | 110,919 |
| Normal (N) | 90,631 |
| Supraventricular ectopic (S) | 2,781 |
| Ventricular ectopic (V) | 7,236 |
| Fusion (F) | 803 |
| Unknown/Other (Q) | 9,468 |
| Sampling frequency | 360 Hz |
| Dataset version | 1.0.0 |

The MIT-BIH Arrhythmia Database is available from PhysioNet at [https://physionet.org/content/mitdb/1.0.0/](https://physionet.org/content/mitdb/1.0.0/) and should be cited as Moody and Mark (2001) [1]. It is released under the [Open Data Commons Attribution License v1.0](https://physionet.org/content/mitdb/view-license/1.0.0/). Preprocessed scalograms and the canonical training/validation/test splits used in this project can be regenerated with `preprocess_data.py` and `create_batched_tfrecords.py` or retrieved from the project’s `Research_Runs/` directory.

The experiments draw on the **MIT-BIH Arrhythmia Database**, a benchmark collection of 48 half‑hour two‑lead ambulatory ECG recordings originally published by the BIH Arrhythmia Laboratory and now distributed via PhysioNet [1]. The archive provides beat‑level annotations curated by expert electrophysiologists and is widely used for evaluating arrhythmia detection algorithms.

Download the raw signals and annotations with the provided helper script:

```bash
python download_data.py
```

By default the script retrieves the entire database (≈110 MB) and stores it in `mit-bih-arrhythmia-database-1.0.0/` adjacent to the repository root. After completion the directory contains one triplet of files per record:

```
mit-bih-arrhythmia-database-1.0.0/
├── 100.atr
├── 100.dat
├── 100.hea
├── …
├── 234.atr
├── 234.dat
├── 234.hea
└── README
```

Modify the `db_name` and `save_directory` variables in `download_data.py` to target alternative PhysioNet databases or custom storage locations.

## Ethics & Data Usage

The MIT‑BIH Arrhythmia Database is distributed by PhysioNet under the [Open Data Commons Attribution License v1.0](https://physionet.org/content/mitdb/view-license/1.0.0/). The records are de‑identified, yet they originate from real patients and must be handled with the same care as other sensitive health information.

- **Patient privacy.** Do not attempt to re‑identify participants. Any derived artifacts or shared models should remain free of information that could reveal individual identities. When publishing, present results in aggregate and avoid uploading raw ECG segments unless required and permissible.
- **Permissible use.** The license permits research and educational activities provided appropriate attribution is given. Using the data for clinical decision making, regulatory submissions, or commercial products may require additional permissions from the data custodians and adherence to jurisdiction‑specific regulations (e.g., HIPAA or GDPR).
- **IRB and consent.** The original data collection received institutional review board approval and informed consent. Because the released dataset is de‑identified, secondary analyses like those in this repository typically qualify for exemption from further IRB review. Investigators should nevertheless consult their local ethics committee, especially if combining these data with other sources or conducting human‑subjects research that could reintroduce identifiers.

## Preprocessing Pipeline

Convert the raw MIT‑BIH records into model‑ready examples with a two‑stage preprocessing workflow. Execute the scripts sequentially after downloading the database.

### 1. Generate scalograms and beat metadata

```bash
python preprocess_data.py
```

This script isolates 187‑sample beats, computes Morlet wavelet scalograms, and writes one HDF5 file per record to `preprocessed_data_h5_raw/`. A companion `metadata.json` in the same directory records, for every beat, its source record, index, and AAMI class label. Signals are deliberately kept **unnormalized** at this stage to avoid train–test leakage; normalization is applied later during dataset loading using statistics derived from the training set.

### 2. Package sequences into batched TFRecords

```bash
python create_batched_tfrecords.py
```

Using the stored metadata, this script forms overlapping sequences of three consecutive beats and serializes them in batches of 256 to `tfrecord_data_batched/`. Each TFRecord example embeds the batch size, sequence length, and scalogram dimensions alongside the raw byte arrays, producing a self‑describing format that streams efficiently through `tf.data`.

### Why batched TFRecords?

Batched TFRecords amortize file‑open overhead and permit large sequential reads, significantly accelerating I/O compared with per‑example files. When coupled with `tf.data` interleave and prefetch operations, the batched layout sustains high throughput on both CPUs and GPUs.

### Normalization strategy

Deferring normalization until dataset construction ensures that scaling parameters are computed exclusively from the training split. This on‑the‑fly approach preserves the integrity of validation and test sets and aligns with best practices for reproducible research.

## Dataset Loading

`DataLoader.py` assembles streaming datasets directly from the batched TFRecords and employs a two‑stage shuffling scheme that maximizes example diversity without incurring large memory overhead:

1. **File‑level shuffle** – when `is_training=True`, the list of TFRecord files is shuffled globally so that each epoch traverses records in a different order.
2. **Interleave shuffle** – `tf.data.Dataset.interleave` reads from several files concurrently (default `cycle_length=4`), mixing individual examples across files to disrupt local ordering.

After decoding, an optional light shuffle with a small buffer adds an additional layer of randomness before batching.

The loader also supports **on‑the‑fly normalization**. If per‑channel `mean` and `scale` arrays are supplied, they are converted to tensors and each scalogram is standardized as `(scalogram - mean) / scale` before being expanded to include a channel dimension.

```python
from DataLoader import create_dataset, get_all_labels

config = {...}  # paths and preprocessing parameters
record_names = ["100", "101", "102"]
mean, scale = train_mean, train_std  # tensors or NumPy arrays

train_ds = create_dataset(record_names, config, batch_size=32,
                          is_training=True, mean=mean, scale=scale)
for scalograms, labels in train_ds.take(1):
    pass  # training loop or debugging
```

## Model Architectures

### Conformer-Based Network

The primary model, implemented in `ModelBuilder.py`, couples a convolutional front end with stacked **Conformer** blocks (Figure 1 in [2]). Each scalogram passes through a 2‑D CNN feature extractor before being processed by a sequence of Conformer blocks that integrate three complementary modules:

- **Feed‑Forward Module** – two half‑step feed‑forward networks with Swish activation and dropout surround the attention and convolution layers, following the Macaron design.
- **Multi‑Head Self‑Attention** – captures global temporal context; positional embeddings are added before attention to encode beat order.
- **Convolution Module** – a depthwise separable 1‑D convolution with gated linear units and batch normalization models local dependencies and sharp morphological patterns.

```text
Input → ½ Feed‑Forward → Self‑Attention → Convolution → ½ Feed‑Forward → LayerNorm → Output
```

### Ablation Models

- **Attention‑Only** – removes the convolution module, yielding a Transformer‑style encoder used to quantify the incremental value of local convolutions.
- **CNN‑LSTM** – replaces Conformer blocks with a unidirectional LSTM after the CNN extractor, providing a classical recurrent baseline for temporal modeling.

```text
Attention‑Only:  Input → [Self‑Attention → Feed‑Forward] × N → Output
CNN‑LSTM:       Input scalograms → Time‑Distributed CNN → LSTM → Output
```

These controlled variants isolate the contribution of attention and convolution mechanisms, enabling rigorous scientific evaluation of architectural choices.

## Training

### Hyperparameter tuning

Explore model configurations with `run_hyperparameter_tuning.py`. The script accepts a `--model_name` argument to choose among the implemented architectures【F:run_hyperparameter_tuning.py†L134-L141】:

```bash
python run_hyperparameter_tuning.py --model_name Main_Model
```

Internally, the script partitions the available record names with scikit‑learn’s `KFold`, yielding fold‑specific training and validation lists that serve as input to the `TimeSeriesModel` pipeline【F:run_hyperparameter_tuning.py†L177-L183】.

### K‑fold strategy

`TimeSeriesModel` operates on a single fold at a time. For each fold it computes normalization statistics exclusively on the training subset, builds `tf.data` streams, and launches a Hyperband tuner, ensuring that hyperparameter search is free from data leakage【F:MainClass.py†L34-L91】【F:MainClass.py†L125-L149】.

### Tuning artifacts

Every tuning run creates a timestamped directory under `Research_Runs/` containing logs, data splits, and configuration files【F:run_hyperparameter_tuning.py†L72-L77】【F:run_hyperparameter_tuning.py†L154-L174】. Fold‑specific assets are stored deeper in `Research_Runs/run_<timestamp>/fold_<n>/`, and the script copies the best hyperparameter set to the top‑level run folder for convenient reuse【F:MainClass.py†L93-L97】【F:run_hyperparameter_tuning.py†L224-L229】.

## Evaluation

### K-fold cross-validation

Assess generalization by re‑using the tuned hyperparameters across stratified folds:

```bash
python run_kfold_evaluation.py --model_name Main_Model
```

The script writes fold‑specific histories and a summary of mean and standard‑deviation metrics to `Research_Runs/kfold_eval_<model>_<timestamp>/`【F:run_kfold_evaluation.py†L43-L47】【F:run_kfold_evaluation.py†L180-L183】. Use the aggregated statistics to compare models; significance can be examined via paired tests (e.g., t‑test or Wilcoxon signed‑rank) applied to matching fold metrics.

### Final held‑out evaluation

Train the champion model on all training records and evaluate on the untouched test set:

```bash
python run_final_evaluation.py --model_name Main_Model
```

Optional `--epochs` and `--batch_size` arguments override training length and batch size【F:run_final_evaluation.py†L137-L141】. Artifacts—including the final model and evaluation reports—are saved under `Research_Runs/final_run_<model>_<timestamp>/`【F:run_final_evaluation.py†L38-L43】【F:run_final_evaluation.py†L222-L236】.

### Evaluator outputs

`Evaluator.py` produces comprehensive diagnostics for each evaluation run:

- `classification_report.txt` with per‑class precision, recall, F1‑score, and AUC values【F:Evaluator.py†L140-L148】
- `confusion_matrix.png` visualizing correct versus incorrect classifications【F:Evaluator.py†L150-L160】
- `roc_curves.png` plotting one‑vs‑rest ROC curves with corresponding AUCs【F:Evaluator.py†L162-L178】

These files are written to the same run directory passed to `Evaluator.save_results`.

### Interpreting metrics and significance

Precision, recall, and F1‑score contextualize performance under class imbalance, while ROC/AUC summarizes discrimination across thresholds; the confusion matrix highlights systematic misclassifications. Report mean ± standard deviation across folds or repeated runs to convey variability. When comparing models, apply statistical tests on per‑fold metrics to determine whether observed differences exceed random variation (commonly using a significance threshold of *p* < 0.05).

## Results

The following table summarizes held‑out test performance for all evaluated architectures. Accuracy, macro‑averaged and class‑weighted F1‑scores, and one‑versus‑rest area under the ROC curve (AUC) are reported for each AAMI rhythm class.

| Model | Accuracy | Macro F1 | Weighted F1 | AUC Normal | AUC SVEB | AUC VEB | AUC Fusion | AUC Unknown |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Main_Model | 0.60【F:Research_Runs/final_run_Main_Model_20250824_154136/classification_report.txt†L11】 | 0.26【F:Research_Runs/final_run_Main_Model_20250824_154136/classification_report.txt†L12】 | 0.68【F:Research_Runs/final_run_Main_Model_20250824_154136/classification_report.txt†L13】 | 0.9009【F:Research_Runs/final_run_Main_Model_20250824_154136/classification_report.txt†L18】 | 0.6681【F:Research_Runs/final_run_Main_Model_20250824_154136/classification_report.txt†L19】 | 0.8431【F:Research_Runs/final_run_Main_Model_20250824_154136/classification_report.txt†L20】 | 0.3140【F:Research_Runs/final_run_Main_Model_20250824_154136/classification_report.txt†L21】 | 0.5837【F:Research_Runs/final_run_Main_Model_20250824_154136/classification_report.txt†L22】 |
| Baseline_Model | 0.14【F:Research_Runs/final_run_Baseline_Model_20250824_182728/classification_report.txt†L11】 | 0.07【F:Research_Runs/final_run_Baseline_Model_20250824_182728/classification_report.txt†L12】 | 0.23【F:Research_Runs/final_run_Baseline_Model_20250824_182728/classification_report.txt†L13】 | 0.6922【F:Research_Runs/final_run_Baseline_Model_20250824_182728/classification_report.txt†L18】 | 0.6521【F:Research_Runs/final_run_Baseline_Model_20250824_182728/classification_report.txt†L19】 | 0.7207【F:Research_Runs/final_run_Baseline_Model_20250824_182728/classification_report.txt†L20】 | 0.4057【F:Research_Runs/final_run_Baseline_Model_20250824_182728/classification_report.txt†L21】 | 0.8558【F:Research_Runs/final_run_Baseline_Model_20250824_182728/classification_report.txt†L22】 |
| CNNLSTM_Model | 0.18【F:Research_Runs/final_run_CNNLSTM_Model_20250824_213453/classification_report.txt†L11】 | 0.15【F:Research_Runs/final_run_CNNLSTM_Model_20250824_213453/classification_report.txt†L12】 | 0.29【F:Research_Runs/final_run_CNNLSTM_Model_20250824_213453/classification_report.txt†L13】 | 0.7307【F:Research_Runs/final_run_CNNLSTM_Model_20250824_213453/classification_report.txt†L18】 | 0.7342【F:Research_Runs/final_run_CNNLSTM_Model_20250824_213453/classification_report.txt†L19】 | 0.8586【F:Research_Runs/final_run_CNNLSTM_Model_20250824_213453/classification_report.txt†L20】 | 0.4711【F:Research_Runs/final_run_CNNLSTM_Model_20250824_213453/classification_report.txt†L21】 | 0.0278【F:Research_Runs/final_run_CNNLSTM_Model_20250824_213453/classification_report.txt†L22】 |
| AttentionOnly | 0.27【F:Research_Runs/final_run_AttentionOnly_20250824_090531/classification_report.txt†L11】 | 0.15【F:Research_Runs/final_run_AttentionOnly_20250824_090531/classification_report.txt†L12】 | 0.38【F:Research_Runs/final_run_AttentionOnly_20250824_090531/classification_report.txt†L13】 | 0.7650【F:Research_Runs/final_run_AttentionOnly_20250824_090531/classification_report.txt†L18】 | 0.7625【F:Research_Runs/final_run_AttentionOnly_20250824_090531/classification_report.txt†L19】 | 0.6883【F:Research_Runs/final_run_AttentionOnly_20250824_090531/classification_report.txt†L20】 | 0.4026【F:Research_Runs/final_run_AttentionOnly_20250824_090531/classification_report.txt†L21】 | 0.8049【F:Research_Runs/final_run_AttentionOnly_20250824_090531/classification_report.txt†L22】 |

Mean k‑fold accuracy for the Main_Model reached 0.44 ± 0.16 across five folds【F:Research_Runs/kfold_eval_Main_Model_20250823_204942/kfold_summary.json†L5-L6】.

*Table 1. Held‑out test metrics for evaluated architectures.*

Relative to the rudimentary Baseline, the Main_Model lifts accuracy from 14 % to 60 % (+46 pp) and macro‑F1 from 0.07 to 0.26 (+0.19)【F:Research_Runs/final_run_Baseline_Model_20250824_182728/classification_report.txt†L11-L12】【F:Research_Runs/final_run_Main_Model_20250824_154136/classification_report.txt†L11-L12】. The CNNLSTM and AttentionOnly variants reach only 18 % and 27 % accuracy with macro‑F1 scores of 0.15 each, leaving the Main_Model ahead by 42–33 pp in accuracy and 0.11 in macro‑F1【F:Research_Runs/final_run_CNNLSTM_Model_20250824_213453/classification_report.txt†L11-L12】【F:Research_Runs/final_run_AttentionOnly_20250824_090531/classification_report.txt†L11-L12】. These gains highlight the importance of combining convolutional and attention mechanisms, though fusion beats remain the most challenging class.

### Hardware and Training Time

| Resource | Details |
| --- | --- |
| GPU | NVIDIA GeForce GTX 1660 Ti (6 GB VRAM) |
| CPU | Intel Core i7 (6 cores) |
| RAM | 16 GB |
| OS | Ubuntu on Windows Subsystem for Linux |
| CUDA/cuDNN | CUDA 12.2 with cuDNN 9.0 |
| Python | 3.12.10 |
| TensorFlow | 2.20.0 |

The final training run on this GPU-enabled system started at 15:42:01 and ended at 16:48:20, for a total of approximately 66 minutes.
### Diagnostic Plots

Figures 1–3 visualize complementary aspects of model behavior. The confusion matrix in Figure 1 highlights that most misclassifications arise from confusion between supraventricular ectopic beats and normal rhythms, reflecting the heavy class imbalance. Figure 2 plots one‑versus‑rest ROC curves, demonstrating high separability for normal and ventricular ectopic beats (AUC > 0.84) but considerably lower discrimination for fusion beats (AUC ≈ 0.31). Precision–recall curves in Figure 3 reveal the trade‑off between sensitivity and positive predictive value, with rare rhythms exhibiting steep precision drop‑offs at moderate recall.

![Confusion matrix for the Main_Model](docs/figures/confusion_matrix.png)

*Figure 1. Confusion matrix summarizing predicted versus true label counts.*

![One‑vs‑rest ROC curves for the Main_Model](docs/figures/roc_curves.png)

*Figure 2. Receiver operating characteristic curves with per‑class area under the curve.*

![Precision–recall curves for the Main_Model](docs/figures/precision_recall_curves.png)

*Figure 3. Precision–recall trade‑offs across AAMI rhythm classes.*

## One‑Command End‑to‑End Pipeline

![End-to-end pipeline](docs/figures/pipeline.svg)

*Figure 4. Sequential stages from data acquisition to final evaluation.*
Execute the complete workflow—from raw PhysioNet records to held‑out test metrics—with a single command:

```bash
bash run_full_pipeline.sh
```

The script performs the following stages sequentially:

1. **Download** – `download_data.py` fetches the MIT‑BIH Arrhythmia Database using the `db_name` and `save_directory` variables defined at the top of the script【F:download_data.py†L5-L9】.
2. **Preprocess** – `preprocess_data.py` computes scalograms and beat metadata according to parameters in its `Config` class (e.g., `DB_DIRECTORY`, `OUTPUT_DIRECTORY`)【F:preprocess_data.py†L22-L36】.
3. **TFRecord creation** – `create_batched_tfrecords.py` packages the scalograms into batched TFRecords; constants such as `SEQUENCE_LEN`, `BATCH_SIZE_PER_CHUNK`, and `OUTPUT_TFRECORD_DIR` control this step【F:create_batched_tfrecords.py†L23-L28】.
4. **Hyperparameter tuning** – `run_hyperparameter_tuning.py` explores model configurations and sets `TF_DETERMINISTIC_OPS=1` for reproducibility【F:run_hyperparameter_tuning.py†L91-L93】.
5. **K‑fold evaluation** – `run_kfold_evaluation.py` reuses the tuned parameters to estimate variance across folds.
6. **Final evaluation** – `run_final_evaluation.py` trains on the full training set and reports test‑set metrics.

Architectures are listed in the `MODELS` array within `run_full_pipeline.sh`; edit this array to select which models to evaluate. The Python scripts rely on their internal configuration blocks rather than external config files, but environment variables such as `CUDA_VISIBLE_DEVICES` (set to `-1` during TFRecord creation to force CPU usage)【F:create_batched_tfrecords.py†L72-L75】 and `TF_DETERMINISTIC_OPS` (enabled during tuning) influence execution. Adjust these variables as needed for custom hardware setups.

## Repository Structure
- **Data preparation** – `download_data.py`, `preprocess_data.py`, and `create_batched_tfrecords.py` fetch the MIT‑BIH arrhythmia dataset, perform signal cleaning, and package examples into TFRecord batches.
- **Core modules** – `ModelBuilder.py`, `DataLoader.py`, and `Evaluator.py` implement the model architecture, streaming data pipeline, and evaluation metrics.
- **Run scripts** – automation helpers such as `run_full_pipeline.sh`, `run_hyperparameter_tuning.py`, `run_kfold_evaluation.py`, and `run_final_evaluation.py` orchestrate training, tuning, and assessment.
- **Research artifacts** – experiment outputs and logs are stored in `Research_Runs/`.

## Reproducible Research
Consistent configuration files, deterministic seeds, and scripted training/evaluation workflows align the project with reproducible research practices, enabling others to replicate and extend the results.

## Contributing
Contributions that refine the codebase, documentation, or scientific analyses are welcome. To report a bug or request a new feature, please open an issue through the [GitHub issue tracker](https://github.com/AlirezaAbbaszadeh/ECG_Heartbeat_Classification/issues).

To submit code changes:

1. Fork the repository and create a dedicated branch for your feature or fix.
2. Implement your changes with clear commit messages and update any relevant documentation.
3. Verify that the full pipeline or associated evaluation scripts run without errors.
4. Open a pull request detailing the motivation, proposed solution, and any related issues.

For questions or support, open an issue or contact the maintainer at [abbaszadeh79@gmail.com](mailto:abbaszadeh79@gmail.com).

## Citation
If you use this repository in your research, please cite it as follows:

```bibtex
@misc{abbaszadeh2025ecg,
  author       = {Alireza Abbaszadeh},
  title        = {ECG Heartbeat Classification},
  year         = {2025},
  publisher    = {GitHub},
  howpublished = {\url{https://github.com/AlirezaAbbaszadeh/ECG_Heartbeat_Classification}},
}
```

## Acknowledgments
This research leverages the MIT-BIH Arrhythmia Database and benefits from the open-source contributions of the Conformer community and the broader PhysioNet ecosystem. The project received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors.

## License

This repository is released under the permissive [MIT License](LICENSE). The license allows commercial and private use, modification, distribution, and sublicensing, provided that the original copyright and license notice are included with any copies of the software. The software is provided “as is,” without warranty of any kind, and the authors bear no liability for any damages arising from its use.

## References

[1] G. B. Moody and R. G. Mark, “The impact of the MIT-BIH Arrhythmia Database,” *IEEE Engineering in Medicine and Biology Magazine*, vol. 20, no. 3, pp. 45–50, 2001. doi:10.1109/51.932724
[2] A. Gulati, J. Qin, C.-C. Chiu, et al., “Conformer: Convolution-augmented Transformer for Speech Recognition,” in *Proceedings of Interspeech*, 2020, pp. 5036–5040. doi:10.21437/Interspeech.2020-3015
[3] P. Rajpurkar, A. Y. Hannun, M. Haghpanahi, C. Bourn, and A. Y. Ng, “Cardiologist-level arrhythmia detection with convolutional neural networks,” *arXiv preprint arXiv:1707.01836*, 2017.
[4] U. R. Acharya, S. L. Oh, Y. Hagiwara, J. H. Tan, and M. Adam, “A deep convolutional neural network model to classify heartbeats,” *Computers in Biology and Medicine*, vol. 89, pp. 389–396, 2017. doi:10.1016/j.compbiomed.2017.08.022
