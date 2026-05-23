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


class PredictionLogEntry(BaseModel):
    request_id: str
    created_at: str
    text_hash: str
    text_preview: str
    label: Literal["POSITIVE", "NEGATIVE"]
    score: float = Field(..., ge=0.0, le=1.0)
    model_version: str
    latency_ms: int = Field(..., ge=0)


class DriftSummary(BaseModel):
    total_requests: int = Field(..., ge=0)
    status: Literal["healthy", "drift_detected", "insufficient_data"]
    flags: list[str]
    metrics: dict


class ServiceInfo(BaseModel):
    service: str
    status: str
    docs_url: str
    endpoints: dict[str, str]
