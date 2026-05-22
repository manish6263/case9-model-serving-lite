from contextlib import asynccontextmanager
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI

from app.config import get_log_path
from app.drift import summarize_drift
from app.logging_store import fetch_recent_logs, initialize_log_store, log_prediction
from app.model import get_model_version, predict_sentiment
from app.schemas import DriftSummary, PredictRequest, PredictResponse, PredictionLogEntry


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_log_store(get_log_path())
    yield


app = FastAPI(
    title="Case 9 Model Serving Lite",
    description="A production-minded sentiment model service.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    started_at = perf_counter()
    label, score = predict_sentiment(request.text)
    latency_ms = int((perf_counter() - started_at) * 1000)
    request_id = str(uuid4())
    rounded_score = round(score, 4)

    log_prediction(
        get_log_path(),
        request_id=request_id,
        text=request.text,
        label=label,
        score=rounded_score,
        model_version=get_model_version(),
        latency_ms=latency_ms,
    )

    return PredictResponse(
        request_id=request_id,
        label=label,
        score=rounded_score,
        model_version=get_model_version(),
        latency_ms=latency_ms,
    )


@app.get("/logs/recent", response_model=list[PredictionLogEntry])
def recent_logs(limit: int = 20) -> list[dict[str, object]]:
    safe_limit = min(max(limit, 1), 100)
    return fetch_recent_logs(get_log_path(), limit=safe_limit)


@app.get("/monitoring/summary", response_model=DriftSummary)
def monitoring_summary(limit: int = 100) -> dict[str, object]:
    safe_limit = min(max(limit, 1), 500)
    logs = fetch_recent_logs(get_log_path(), limit=safe_limit)
    return summarize_drift(logs)
