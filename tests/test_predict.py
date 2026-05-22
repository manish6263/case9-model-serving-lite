import os
from pathlib import Path

os.environ["CASE9_LOG_PATH"] = str(
    Path("artifacts/test-logs/api.jsonl")
)

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_predict_returns_sentiment_contract() -> None:
    response = client.post("/predict", json={"text": "I loved this excellent product"})

    assert response.status_code == 200
    body = response.json()
    assert body["label"] == "POSITIVE"
    assert 0.0 <= body["score"] <= 1.0
    assert body["model_version"] == "rule-based-fallback-v0"
    assert isinstance(body["request_id"], str)
    assert isinstance(body["latency_ms"], int)


def test_predict_writes_recent_log_entry() -> None:
    response = client.post("/predict", json={"text": "This product is good"})

    assert response.status_code == 200
    request_id = response.json()["request_id"]

    logs_response = client.get("/logs/recent?limit=1")

    assert logs_response.status_code == 200
    logs = logs_response.json()
    assert logs[0]["request_id"] == request_id
    assert logs[0]["text_preview"] == "This product is good"
    assert len(logs[0]["text_hash"]) == 64


def test_monitoring_summary_returns_status() -> None:
    client.post("/predict", json={"text": "This product is good"})

    response = client.get("/monitoring/summary")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] in {"healthy", "drift_detected", "insufficient_data"}
    assert body["total_requests"] >= 1


def test_predict_rejects_empty_text() -> None:
    response = client.post("/predict", json={"text": ""})

    assert response.status_code == 422


def test_predict_can_return_negative_sentiment() -> None:
    response = client.post("/predict", json={"text": "This was terrible and I want a refund"})

    assert response.status_code == 200
    assert response.json()["label"] == "NEGATIVE"
