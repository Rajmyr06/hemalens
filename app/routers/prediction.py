from fastapi import APIRouter, Depends

from app.dependencies import get_artifact_bundle
from app.ml.artifacts import ArtifactBundle
from app.ml.inference import predict
from app.schemas.prediction import PredictionRequest, PredictionResponse


router = APIRouter(prefix="/api/v1", tags=["prediction"])


@router.post("/predict", response_model=PredictionResponse)
def create_prediction(
    payload: PredictionRequest,
    bundle: ArtifactBundle = Depends(get_artifact_bundle),
) -> PredictionResponse:
    result = predict(bundle, payload.model_dump())
    return PredictionResponse(
        model_version=result.model_version,
        model_score=result.model_score,
        threshold=result.threshold,
        predicted_class=result.predicted_class,
        predicted_class_index=result.predicted_class_index,
    )
