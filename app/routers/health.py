from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.dependencies import get_artifact_bundle
from app.ml.artifacts import ArtifactBundle
from app.schemas.health import HealthResponse


router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health(
    bundle: ArtifactBundle = Depends(get_artifact_bundle),
    settings: Settings = Depends(get_settings),
) -> HealthResponse:
    return HealthResponse(
        status="healthy",
        application=settings.app_name,
        application_version=settings.app_version,
        model_loaded=True,
        model_version=bundle.model_version,
    )
