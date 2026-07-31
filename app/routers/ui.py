from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from pydantic import ValidationError

from app.core.config import get_settings
from app.dependencies import get_artifact_bundle
from app.ml.artifacts import ArtifactBundle
from app.ml.inference import predict
from app.schemas.ui import PredictionFormInput
from app.web.templates import templates


router = APIRouter(tags=["interface"])
settings = get_settings()
FEATURE_NAMES = ("rbc", "hb", "mcv", "mch", "mchc", "rdwcv")
ALLOWED_FORM_KEYS = set(FEATURE_NAMES) | {"acknowledged"}


def _base_context(request: Request) -> dict[str, Any]:
    return {
        "request": request,
        "app_name": settings.app_name,
        "app_version": settings.app_version,
    }


def _error_context(
    request: Request,
    message: str,
    *,
    values: dict[str, str] | None = None,
) -> dict[str, Any]:
    context = _base_context(request)
    context.update(
        {
            "message": message,
            "values": values or {},
        }
    )
    return context


@router.get("/", response_class=HTMLResponse)
def landing_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context=_base_context(request),
    )


@router.get("/partials/landing", response_class=HTMLResponse)
def landing_partial(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="partials/landing.html",
        context=_base_context(request),
    )


@router.get("/partials/form", response_class=HTMLResponse)
def prediction_form(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="partials/form.html",
        context=_base_context(request),
    )


@router.post("/ui/predict", response_class=HTMLResponse)
async def prediction_result(
    request: Request,
    bundle: ArtifactBundle = Depends(get_artifact_bundle),
) -> HTMLResponse:
    form = await request.form()
    submitted_keys = set(form.keys())
    unexpected_keys = sorted(submitted_keys - ALLOWED_FORM_KEYS)
    values = {name: str(form.get(name, "")) for name in FEATURE_NAMES}

    if unexpected_keys:
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context=_error_context(
                request,
                "Form berisi field yang tidak dikenali.",
                values=values,
            ),
            status_code=422,
        )

    if form.get("acknowledged") != "true":
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context=_error_context(
                request,
                "Persetujuan akademik wajib dicentang sebelum analisis dijalankan.",
                values=values,
            ),
            status_code=422,
        )

    try:
        payload = PredictionFormInput.model_validate(values)
    except ValidationError:
        return templates.TemplateResponse(
            request=request,
            name="partials/error.html",
            context=_error_context(
                request,
                "Periksa kembali keenam nilai. Seluruh field wajib berisi angka yang valid.",
                values=values,
            ),
            status_code=422,
        )

    result = predict(bundle, payload.model_dump())
    if result.predicted_class_index == 0:
        outcome_title = "Normal pattern"
        outcome_text = (
            "Pola input lebih konsisten dengan kelas Normal menurut model penelitian."
        )
    else:
        outcome_title = "Thalassemia-related pattern"
        outcome_text = (
            "Pola input lebih konsisten dengan kelas Thalassemia-related menurut "
            "model penelitian."
        )

    context = _base_context(request)
    context.update(
        {
            "result": result,
            "outcome_title": outcome_title,
            "outcome_text": outcome_text,
        }
    )
    return templates.TemplateResponse(
        request=request,
        name="partials/result.html",
        context=context,
    )

@router.get("/research", response_class=HTMLResponse)
def research_page(request: Request) -> HTMLResponse:
    context = _base_context(request)
    context["active_page"] = "research"
    return templates.TemplateResponse(
        request=request,
        name="research.html",
        context=context,
    )


@router.get("/about", response_class=HTMLResponse)
def about_page(request: Request) -> HTMLResponse:
    context = _base_context(request)
    context["active_page"] = "about"
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context=context,
    )

