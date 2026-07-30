from app.core.config import get_settings
from app.ml.artifacts import load_artifact_bundle
from app.ml.inference import verify_golden_sample


def test_frozen_bundle_and_all_golden_samples() -> None:
    settings = get_settings()
    bundle = load_artifact_bundle(
        settings.artifact_dir,
        settings.expected_model_version,
        settings.verify_checksums,
    )

    assert bundle.model_version == settings.expected_model_version
    assert bundle.feature_order == ["rbc", "hb", "mcv", "mch", "mchc", "rdwcv"]

    for index in range(len(bundle.golden_samples)):
        verify_golden_sample(
            bundle,
            tolerance=settings.golden_score_tolerance,
            row_index=index,
        )
