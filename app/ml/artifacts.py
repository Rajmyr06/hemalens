from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any
import json
import logging

import joblib
import pandas as pd


logger = logging.getLogger(__name__)


class ArtifactError(RuntimeError):
    """Raised when the frozen inference bundle is missing or invalid."""


@dataclass(frozen=True)
class ArtifactBundle:
    preprocessor: Any
    model: Any
    metadata: dict[str, Any]
    feature_schema: dict[str, Any]
    metrics: dict[str, Any]
    golden_samples: pd.DataFrame

    @property
    def feature_order(self) -> list[str]:
        return list(self.metadata["feature_order"])

    @property
    def threshold(self) -> float:
        return float(self.metadata["threshold"])

    @property
    def positive_class_index(self) -> int:
        return int(self.metadata["positive_class_index"])

    @property
    def model_version(self) -> str:
        return str(self.metadata["model_version"])


REQUIRED_FILES = (
    "preprocessor.joblib",
    "model.joblib",
    "model_metadata.json",
    "feature_schema.json",
    "metrics.json",
    "golden_samples.csv",
    "checksums.txt",
)


def _load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError) as exc:
        raise ArtifactError(f"Failed to read JSON artifact: {path.name}") from exc


def _sha256(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_checksums(artifact_dir: Path) -> None:
    checksum_path = artifact_dir / "checksums.txt"

    try:
        lines = checksum_path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ArtifactError("Unable to read checksums.txt") from exc

    if not lines:
        raise ArtifactError("checksums.txt is empty")

    for line in lines:
        expected_hash, filename = line.split(maxsplit=1)
        target = artifact_dir / filename.strip()
        if not target.is_file():
            raise ArtifactError(f"Checksum target is missing: {target.name}")

        actual_hash = _sha256(target)
        if actual_hash != expected_hash:
            raise ArtifactError(f"Checksum mismatch: {target.name}")


def _validate_contract(
    metadata: dict[str, Any],
    schema: dict[str, Any],
    expected_model_version: str,
) -> None:
    model_version = metadata.get("model_version")
    if model_version != expected_model_version:
        raise ArtifactError(
            f"Unexpected model version: {model_version!r}; "
            f"expected {expected_model_version!r}"
        )

    feature_order = metadata.get("feature_order")
    schema_features = [
        feature["name"]
        for feature in sorted(schema.get("features", []), key=lambda item: item["position"])
    ]

    if feature_order != schema_features:
        raise ArtifactError(
            "Feature order mismatch between model metadata and feature schema"
        )

    if metadata.get("positive_class_index") != 1:
        raise ArtifactError("Positive class index must remain 1")

    threshold = metadata.get("threshold")
    if not isinstance(threshold, (int, float)) or not 0 <= float(threshold) <= 1:
        raise ArtifactError("Model threshold must be between 0 and 1")


def load_artifact_bundle(
    artifact_dir: Path,
    expected_model_version: str,
    verify_bundle_checksums: bool = True,
) -> ArtifactBundle:
    artifact_dir = artifact_dir.resolve()

    missing = [name for name in REQUIRED_FILES if not (artifact_dir / name).is_file()]
    if missing:
        raise ArtifactError(f"Missing inference artifacts: {', '.join(missing)}")

    if verify_bundle_checksums:
        verify_checksums(artifact_dir)

    metadata = _load_json(artifact_dir / "model_metadata.json")
    feature_schema = _load_json(artifact_dir / "feature_schema.json")
    metrics = _load_json(artifact_dir / "metrics.json")
    _validate_contract(metadata, feature_schema, expected_model_version)

    try:
        preprocessor = joblib.load(artifact_dir / "preprocessor.joblib")
        model = joblib.load(artifact_dir / "model.joblib")
        golden_samples = pd.read_csv(artifact_dir / "golden_samples.csv")
    except Exception as exc:
        raise ArtifactError("Unable to deserialize the frozen inference bundle") from exc

    bundle = ArtifactBundle(
        preprocessor=preprocessor,
        model=model,
        metadata=metadata,
        feature_schema=feature_schema,
        metrics=metrics,
        golden_samples=golden_samples,
    )

    logger.info(
        "Loaded model bundle version=%s features=%s",
        bundle.model_version,
        ",".join(bundle.feature_order),
    )
    return bundle
