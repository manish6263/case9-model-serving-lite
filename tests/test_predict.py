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


def test_predict_rejects_empty_text() -> None:
    response = client.post("/predict", json={"text": ""})

    assert response.status_code == 422


def test_predict_can_return_negative_sentiment() -> None:
    response = client.post("/predict", json={"text": "This was terrible and I want a refund"})

    assert response.status_code == 200
    assert response.json()["label"] == "NEGATIVE"
