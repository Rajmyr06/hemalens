# Model Card — Hematology Pattern Analysis

## Model identity

- **Model version:** `hematology-xgb-smote-thr091-v1.0.0`
- **Algorithm:** XGBoost binary classifier
- **Training scenario:** Median imputation followed by SMOTE on training data
- **Decision threshold:** 0.91
- **Positive class:** `Thalassemia_related`
- **Features:** RBC, Hb, MCV, MCH, MCHC, RDW-CV
- **Dataset fingerprint:** `51a5729c9864a5292c134fb911e199d628fb4812e19367c8cc503363b009daee`

## Training and serving boundary

Model development is intentionally separated from this web-serving repository.
The research workflow performs data preparation, model comparison, threshold
selection, evaluation, and SHAP analysis. HemaLens only loads the approved,
frozen inference bundle and never trains or updates a model from public input.

The serving bundle contains:

- the fitted preprocessing object;
- the fitted XGBoost estimator;
- ordered feature schema and units;
- model metadata and package versions;
- frozen evaluation metrics;
- checksums and 18 golden-parity samples.

This boundary reduces accidental training-serving drift. It does not make the
original training study independently reproducible from this repository alone;
the source dataset and research workflow remain separate and subject to their
own access and licensing requirements.

## Intended use

This artifact supports an academic research demonstration and portfolio website.
It classifies an input pattern into `Normal` or `Thalassemia_related` according
to the trained research model.

It is not intended for diagnosis, clinical risk estimation, treatment decisions,
or medical-device use.

## Data

- Source rows: 13,031
- Modeling rows: 12,386
- Normal: 11,783
- Thalassemia-related: 603
- Train-test split: 80:20 stratified, random state 42
- Test data was not balanced
- SMOTE was applied only to training data

The original target labels were mapped into `Normal`, `Thalassemia_related`, and
`Other`; `Other` was excluded from the binary model.

## Frozen test performance

| Metric | Value |
|---|---:|
| Accuracy | 0.969330 |
| Macro-F1 | 0.828163 |
| Precision, Thalassemia-related | 0.702703 |
| Recall, Thalassemia-related | 0.644628 |
| F1, Thalassemia-related | 0.672414 |
| ROC-AUC | 0.974214 |
| PR-AUC | 0.757274 |

Confusion matrix: `[[2324, 33], [43, 78]]`.

These values describe one frozen held-out split of the source dataset. They are
not prospective clinical performance estimates and must not be generalized to
new hospitals, instruments, regions, or patient populations without external
validation.

## Selection rationale and trade-offs

The deployment candidate reproduces the final research decision that prioritized
macro-F1. It does not dominate all alternatives:

- XGBoost baseline has a higher PR-AUC.
- XGBoost SMOTE at threshold 0.5 has a higher minority recall.
- The frozen threshold 0.91 improves precision and macro-F1 but reduces minority recall.

The website must disclose these trade-offs.

## Explainability

SHAP is computed from the same fitted estimator used for prediction. SHAP values
in the exported analysis are raw tree-model margin contributions. Their signs
describe the direction of the model output; they are not causal medical effects.

Global mean absolute SHAP ranking for the frozen estimator:

| feature   |   mean_abs_shap |
|:----------|----------------:|
| mcv       |        2.08603  |
| mch       |        1.26757  |
| rdwcv     |        0.844802 |
| hb        |        0.477198 |
| mchc      |        0.396338 |
| rbc       |        0.198333 |

## Input units

| Feature | Unit |
|---|---|
| RBC | 10^6 cells/µL |
| Hb | g/dL |
| MCV | fL |
| MCH | pg/cell |
| MCHC | g/dL |
| RDW-CV | % |

The dataset card does not explicitly state units. Units follow standard CBC
conventions and observed value scales. Clinical reference ranges are not encoded
in the serving artifact.

## Limitations

- No external validation.
- One held-out test split.
- Strong class imbalance.
- Binary target derived through rule-based label mapping.
- Seven duplicated feature-target rows; three exact duplicate groups cross the
  original train-test split.
- Extreme values exist and require manual source-data review.
- Model score is not calibrated clinical risk.
- Performance may not generalize beyond the source population.
- Random Forest reproduced with one prediction difference, likely due to library
  version drift; the frozen XGBoost result reproduced exactly.

## Privacy

The model requires only six numeric features. The website must not request
identifying information, persist inputs, log request bodies, or use public inputs
for retraining.
