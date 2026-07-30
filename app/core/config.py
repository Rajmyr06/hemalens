from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env."""

    app_name: str = "HemaLens"
    app_slug: str = "hemalens"
    app_version: str = "0.1.0"
    app_env: str = "development"
    debug: bool = False
    log_level: str = "INFO"

    artifact_dir: Path = PROJECT_ROOT / "artifacts"
    expected_model_version: str = "hematology-xgb-smote-thr091-v1.0.0"
    verify_checksums: bool = True
    golden_score_tolerance: float = 1e-12

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_prefix="HEMALENS_",
        extra="ignore",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
