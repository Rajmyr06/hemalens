from __future__ import annotations

import math
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    rbc: float
    hb: float
    mcv: float
    mch: float
    mchc: float
    rdwcv: float

    @field_validator("*", mode="before")
    @classmethod
    def reject_strings_and_booleans(cls, value: Any) -> Any:
        if isinstance(value, (str, bool)):
            raise ValueError("Value must be a numeric JSON value")
        return value

    @field_validator("*")
    @classmethod
    def require_finite_number(cls, value: float) -> float:
        if not math.isfinite(value):
            raise ValueError("Value must be finite")
        return float(value)


class PredictionResponse(BaseModel):
    model_version: str
    model_score: float
    threshold: float
    predicted_class: str
    predicted_class_index: int
