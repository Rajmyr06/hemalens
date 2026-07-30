from app.core.config import get_settings
from app.ml.artifacts import load_artifact_bundle
from app.ml.inference import verify_golden_sample


def main() -> None:
    settings = get_settings()
    bundle = load_artifact_bundle(
        settings.artifact_dir,
        settings.expected_model_version,
        settings.verify_checksums,
    )

    for index in range(len(bundle.golden_samples)):
        verify_golden_sample(
            bundle,
            tolerance=settings.golden_score_tolerance,
            row_index=index,
        )

    print(
        f"Bundle verified: {bundle.model_version} "
        f"({len(bundle.golden_samples)} golden samples)"
    )


if __name__ == "__main__":
    main()
