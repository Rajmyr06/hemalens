from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.config import PROJECT_ROOT, get_settings
from app.core.logging import configure_logging
from app.ml.artifacts import load_artifact_bundle
from app.ml.inference import verify_golden_sample
from app.routers import health, prediction, ui


settings = get_settings()
configure_logging(settings.log_level)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    bundle = load_artifact_bundle(
        artifact_dir=settings.artifact_dir,
        expected_model_version=settings.expected_model_version,
        verify_bundle_checksums=settings.verify_checksums,
    )
    verify_golden_sample(bundle, tolerance=settings.golden_score_tolerance)
    app.state.artifact_bundle = bundle
    logger.info("HemaLens startup validation completed")
    yield
    app.state.artifact_bundle = None
    logger.info("HemaLens shutdown completed")


app = FastAPI(
    title=settings.app_name,
    description="Explainable hematology pattern analysis research application.",
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory=PROJECT_ROOT / "app" / "static"), name="static")

app.include_router(ui.router)
app.include_router(health.router)
app.include_router(prediction.router)
