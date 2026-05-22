from typing import Literal

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


class PredictResponse(BaseModel):
    request_id: str
    label: Literal["POSITIVE", "NEGATIVE"]
    score: float = Field(..., ge=0.0, le=1.0)
    model_version: str
    latency_ms: int = Field(..., ge=0)
