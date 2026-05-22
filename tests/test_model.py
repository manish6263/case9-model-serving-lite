from app import model


def test_rule_based_fallback_predicts_negative() -> None:
    label, score = model.predict_with_rule_based_fallback("terrible support and refund")

    assert label == "NEGATIVE"
    assert 0.0 <= score <= 1.0


def test_predict_sentiment_uses_fallback_when_pipeline_unavailable(monkeypatch) -> None:
    monkeypatch.setattr(model, "get_huggingface_pipeline", lambda: None)

    label, score = model.predict_sentiment("excellent service")

    assert label == "POSITIVE"
    assert 0.0 <= score <= 1.0


def test_predict_sentiment_accepts_huggingface_style_output(monkeypatch) -> None:
    monkeypatch.delenv("CASE9_DISABLE_HF", raising=False)

    def fake_classifier(text: str, truncation: bool = True):
        return [{"label": "NEGATIVE", "score": 0.987}]

    monkeypatch.setattr(model, "get_huggingface_pipeline", lambda: fake_classifier)

    label, score = model.predict_sentiment("not good")

    assert label == "NEGATIVE"
    assert score == 0.987
