from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI

from app.model import MODEL_VERSION, predict_sentiment
from app.schemas import PredictRequest, PredictResponse


app = FastAPI(
    title="Case 9 Model Serving Lite",
    description="A production-minded sentiment model service.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    started_at = perf_counter()
    label, score = predict_sentiment(request.text)
    latency_ms = int((perf_counter() - started_at) * 1000)

    return PredictResponse(
        request_id=str(uuid4()),
        label=label,
        score=round(score, 4),
        model_version=MODEL_VERSION,
        latency_ms=latency_ms,
    )
