from __future__ import annotations

import math
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator


class PredictionFormInput(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)

    rbc: float
    hb: float
    mcv: float
    mch: float
    mchc: float
    rdwcv: float

    @field_validator("*", mode="before")
    @classmethod
    def normalize_form_number(cls, value: Any) -> Any:
        if isinstance(value, bool):
            raise ValueError("Nilai harus berupa angka")
        if isinstance(value, str):
            normalized = value.strip().replace(",", ".")
            if not normalized:
                raise ValueError("Field wajib diisi")
            return normalized
        return value

    @field_validator("*")
    @classmethod
    def require_finite_number(cls, value: float) -> float:
        if not math.isfinite(value):
            raise ValueError("Nilai harus berupa angka terbatas")
        return float(value)
