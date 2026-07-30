# Milestone 0 Final Execution Report

**Milestone:** Research and Model Readiness  
**Status:** Complete with documented limitations  
**Model version:** `hematology-xgb-smote-thr091-v1.0.0`  
**Execution timestamp:** `2026-07-30T15:29:36.503059+00:00`  
**Dataset SHA-256:** `51a5729c9864a5292c134fb911e199d628fb4812e19367c8cc503363b009daee`

---

## 1. Executive result

Milestone 0 has completed the engineering work required to convert the final
research notebook into a frozen inference artifact for an academic demonstration
website.

The frozen artifact is:

- XGBoost;
- median-imputation preprocessing;
- SMOTE applied only during training;
- threshold 0.91;
- feature order: RBC, Hb, MCV, MCH, MCHC, RDW-CV;
- positive class: `Thalassemia_related`.

This status does not mean the model is clinically validated.

---

## 2. Dataset audit

- Initial rows: 13,031
- Initial columns: 19
- Modeling rows: 12,386
- Normal rows: 11,783
- Thalassemia-related rows: 603
- Missing values in six features: none
- Numeric conversion failures: none
- Duplicate feature-target rows: 7
- Exact duplicate groups crossing train and test: 3

The duplicate rows were retained to reproduce the submitted research pipeline.
A deduplication sensitivity analysis is included separately.

---

## 3. Reproduction results

The six main scenarios were reproduced:

- Random Forest and XGBoost baseline;
- Random Forest and XGBoost with SMOTE;
- Random Forest and XGBoost with random undersampling.

Validation-only threshold tuning reproduced:

- Random Forest: 0.63
- XGBoost: 0.91

The frozen XGBoost result reproduced exactly:

| Metric | Value |
|---|---:|
| Accuracy | 0.969330 |
| Macro-F1 | 0.828163 |
| Precision, Thalassemia-related | 0.702703 |
| Recall, Thalassemia-related | 0.644628 |
| F1, Thalassemia-related | 0.672414 |
| ROC-AUC | 0.974214 |
| PR-AUC | 0.757274 |

Confusion matrix:

```text
[[2324, 33],
 [  43, 78]]
```

Random Forest SMOTE differs by one test prediction from the original notebook.
The most likely cause is library-version-sensitive behavior. This does not alter
the selected XGBoost artifact.

---

## 4. Hyperparameter tuning verification

The full RandomizedSearchCV process was not rerun to completion in this
environment because of computational cost. Instead:

1. the original notebook outputs were inspected;
2. its recorded best parameters were extracted;
3. both best estimators were refit;
4. their held-out confusion matrices and metrics were reproduced.

This validates the reported tuned estimators but not the complete stochastic
search process under the current library versions.

---

## 5. Model selection decision

The frozen candidate follows the final research decision, which prioritizes
macro-F1.

Trade-offs remain material:

- XGBoost baseline has higher PR-AUC;
- XGBoost SMOTE at threshold 0.5 has higher minority recall;
- threshold 0.91 improves precision and macro-F1 while reducing recall.

Therefore, the website must not claim that the frozen model is superior on every
metric.

---

## 6. SHAP correction

The old notebook could explain a tuned estimator while serving a different
threshold-tuned estimator.

This has been corrected:

```text
prediction estimator = SHAP estimator = frozen XGBoost estimator
```

Global and local SHAP outputs in this package come from the exact frozen model.
SHAP values are raw-margin contributions and must not be interpreted causally.

---

## 7. Serving artifact

The export contains:

```text
artifacts/
├── preprocessor.joblib
├── model.joblib
├── model_metadata.json
├── feature_schema.json
├── metrics.json
├── golden_samples.csv
└── checksums.txt
```

Golden parity result:

- samples: 18
- maximum score delta: 1.110e-16
- predictions match: True
- passed: True

---

## 8. Input units and bounds

Units are documented using standard CBC conventions:

- RBC: 10^6 cells/µL
- Hb: g/dL
- MCV: fL
- MCH: pg/cell
- MCHC: g/dL
- RDW-CV: %

The public dataset card does not explicitly state the units. Original
data-collector documentation was not available, so this remains a documented
provenance caveat.

Clinical reference ranges and hard technical bounds are intentionally not
encoded. The serving schema contains descriptive training-distribution
statistics only.

---

## 9. Data-quality sensitivity

Removing seven duplicate feature-target rows produced:

- threshold: 0.87
- macro-F1: 0.830384
- recall, Thalassemia-related: 0.685950
- PR-AUC: 0.748022

This is a sensitivity result only. It does not replace the frozen research
artifact because doing so would change the research pipeline after the fact.

---

## 10. Automated verification

Automated tests passed:

```text
4 passed
```

Coverage includes:

- artifact checksums;
- model metadata contract;
- synthetic pipeline smoke test;
- golden parity.

---

## 11. Definition of done

- [x] Original dataset loaded
- [x] Dataset fingerprint recorded
- [x] Target mapping audited
- [x] Main scenarios reproduced
- [x] Validation threshold reproduced
- [x] Final XGBoost result reproduced exactly
- [x] Tuned estimators reconstructed and verified
- [x] Model and SHAP aligned
- [x] Feature units documented
- [x] Inference bundle exported
- [x] Golden samples generated
- [x] Golden parity passed
- [x] Automated tests passed
- [x] Limitations documented
- [ ] External validation
- [ ] Clinical validation
- [ ] Clinical reference ranges

The last three items are intentionally outside Milestone 0 and outside the
current website scope.

---

## 12. Next project gate

Milestone 1 may begin using only the files inside `artifacts/`.

Website development must not:

- rerun SMOTE during inference;
- hardcode a different threshold;
- reorder features;
- label model score as clinical risk;
- explain predictions with another estimator;
- expose source data or identifying information.
