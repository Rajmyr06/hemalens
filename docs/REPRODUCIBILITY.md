# Reproducibility Guide

## Scope

HemaLens is a serving repository for a frozen academic research model. It is
designed to reproduce inference from an approved artifact bundle, not to retrain
the model or reproduce every research experiment from raw data.

## Development and serving separation

The model-development workflow is responsible for:

1. loading and auditing the source dataset;
2. mapping the binary research target;
3. creating an 80:20 stratified train-test split;
4. fitting median imputation and preprocessing on training data;
5. applying SMOTE only to training data;
6. comparing Random Forest and XGBoost experiments;
7. selecting the frozen XGBoost candidate and decision threshold;
8. exporting evaluation, SHAP summaries, metadata, and serving artifacts.

The HemaLens application is responsible only for:

1. verifying artifact checksums and the expected model version;
2. validating six ordered numeric inputs;
3. applying the frozen preprocessing object;
4. running the frozen estimator;
5. applying the stored decision threshold;
6. returning a non-diagnostic research result without retaining input history.

Public requests are never used for model training or model updates.

## Frozen artifact contract

The `artifacts/` directory contains:

| File | Purpose |
|---|---|
| `model.joblib` | Frozen fitted XGBoost estimator |
| `preprocessor.joblib` | Frozen fitted preprocessing object |
| `model_metadata.json` | Version, feature order, parameters, package versions, and decision record |
| `feature_schema.json` | Ordered features, units, and descriptive training distributions |
| `metrics.json` | Frozen held-out evaluation metrics |
| `golden_samples.csv` | Reference inputs and scores for parity verification |
| `checksums.txt` | SHA-256 integrity manifest for the bundle |

## Verify the serving bundle

Create the documented Python environment, then run:

```bash
python -m scripts.verify_bundle
pytest
```

Verification fails when a required artifact checksum, model version, feature
order, or golden prediction differs from the frozen contract. The golden-score
tolerance is `1e-12`.

## Environment contract

Exact model package versions are stored in `artifacts/model_metadata.json`.
Runtime dependencies are pinned in `requirements.txt`. The frozen model was
exported with Python 3.13.5, NumPy 2.3.5, pandas 2.2.3, scikit-learn 1.8.0,
imbalanced-learn 0.14.1, XGBoost 3.1.3, SHAP 0.50.0, and Joblib 1.5.3.

## Reproducibility limits

- Raw source data is not included in this web repository.
- The full training notebook is not part of the serving application.
- The study has no external validation dataset.
- The frozen evaluation uses one held-out split.
- Duplicate feature-target rows and extreme values are documented in the model
  and dataset cards.
- Reproducing serving predictions is not equivalent to validating clinical
  usefulness or generalization.

See [MODEL_CARD.md](MODEL_CARD.md) and [DATASET_CARD.md](DATASET_CARD.md) before
interpreting the model or its evaluation results.
