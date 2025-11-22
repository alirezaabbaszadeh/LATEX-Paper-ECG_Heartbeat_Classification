# MIT-BIH Record Split — Main\_Model Pipeline

Source configuration:
- Base record list (45 IDs): `Research_Runs/kfold_eval_Main_Model_20250823_204942/evaluation_run_config.json`.
- Split definition (`kfold_records`, `final_test_records`): `Research_Runs/tuning_Main_Model_20250823_145919/data_splits.json`.

Summary:
- K-fold train/val: 38 records (≈84.4% of 45).
- Hold-out test: 7 records (≈15.6% of 45).
- K-fold and test sets are disjoint; their union covers all 45 records in the base list.

Per-record assignment:

| Record ID | Split (train/val folds) | Split (final test) |
| --- | --- | --- |
| 100 | ✓ | — |
| 101 | ✓ | — |
| 103 | ✓ | — |
| 105 | ✓ | — |
| 106 | — | ✓ |
| 108 | ✓ | — |
| 109 | ✓ | — |
| 111 | ✓ | — |
| 112 | ✓ | — |
| 113 | ✓ | — |
| 114 | ✓ | — |
| 115 | ✓ | — |
| 116 | ✓ | — |
| 117 | ✓ | — |
| 118 | ✓ | — |
| 119 | ✓ | — |
| 121 | ✓ | — |
| 122 | ✓ | — |
| 123 | ✓ | — |
| 124 | ✓ | — |
| 200 | ✓ | — |
| 201 | ✓ | — |
| 202 | ✓ | — |
| 203 | ✓ | — |
| 205 | ✓ | — |
| 207 | — | ✓ |
| 208 | — | ✓ |
| 209 | ✓ | — |
| 210 | ✓ | — |
| 212 | ✓ | — |
| 213 | ✓ | — |
| 214 | ✓ | — |
| 215 | ✓ | — |
| 217 | ✓ | — |
| 219 | ✓ | — |
| 220 | — | ✓ |
| 221 | ✓ | — |
| 222 | ✓ | — |
| 223 | ✓ | — |
| 228 | — | ✓ |
| 230 | ✓ | — |
| 231 | — | ✓ |
| 232 | ✓ | — |
| 233 | — | ✓ |
| 234 | ✓ | — |

