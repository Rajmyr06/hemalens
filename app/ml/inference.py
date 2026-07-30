from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping
import math

import pandas as pd

from app.ml.artifacts import ArtifactBundle


@dataclass(frozen=True)
class PredictionResult:
    model_version: str
    model_score: float
    threshold: float
    predicted_class: str
    predicted_class_index: int


def predict(bundle: ArtifactBundle, values: Mapping[str, float]) -> PredictionResult:
    missing = [feature for feature in bundle.feature_order if feature not in values]
    if missing:
        raise ValueError(f"Missing features: {', '.join(missing)}")

    unexpected = sorted(set(values) - set(bundle.feature_order))
    if unexpected:
        raise ValueError(f"Unexpected features: {', '.join(unexpected)}")

    row = {feature: float(values[feature]) for feature in bundle.feature_order}
    if not all(math.isfinite(value) for value in row.values()):
        raise ValueError("All feature values must be finite numbers")

    frame = pd.DataFrame([row], columns=bundle.feature_order)
    transformed = bundle.preprocessor.transform(frame)
    score = float(
        bundle.model.predict_proba(transformed)[0, bundle.positive_class_index]
    )
    predicted_index = int(score >= bundle.threshold)
    label_mapping = bundle.metadata["label_mapping"]
    predicted_class = str(label_mapping[str(predicted_index)])

    return PredictionResult(
        model_version=bundle.model_version,
        model_score=score,
        threshold=bundle.threshold,
        predicted_class=predicted_class,
        predicted_class_index=predicted_index,
    )


def verify_golden_sample(
    bundle: ArtifactBundle,
    tolerance: float,
    row_index: int = 0,
) -> None:
    if bundle.golden_samples.empty:
        raise RuntimeError("Golden samples artifact is empty")

    row = bundle.golden_samples.iloc[row_index]
    values = {feature: float(row[feature]) for feature in bundle.feature_order}
    result = predict(bundle, values)

    expected_score = float(row["expected_score"])
    expected_prediction = int(row["expected_prediction"])
    expected_version = str(row["model_version"])

    if abs(result.model_score - expected_score) > tolerance:
        raise RuntimeError("Golden sample score parity check failed")
    if result.predicted_class_index != expected_prediction:
        raise RuntimeError("Golden sample class parity check failed")
    if result.model_version != expected_version:
        raise RuntimeError("Golden sample model version check failed")
