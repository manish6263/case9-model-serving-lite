from app.drift import summarize_drift


def test_summarize_drift_returns_insufficient_data_for_empty_logs() -> None:
    summary = summarize_drift([])

    assert summary["status"] == "insufficient_data"
    assert "no_requests_logged" in summary["flags"]


def test_summarize_drift_waits_for_minimum_request_count() -> None:
    summary = summarize_drift(
        [{"text_preview": "I loved this excellent product", "label": "POSITIVE"}]
    )

    assert summary["status"] == "insufficient_data"
    assert "not_enough_requests" in summary["flags"]


def test_summarize_drift_reports_healthy_for_reference_like_logs() -> None:
    logs = [
        {"text_preview": "good product and fast delivery", "label": "POSITIVE"},
        {"text_preview": "bad support but good product", "label": "NEGATIVE"},
        {"text_preview": "great service and perfect order", "label": "POSITIVE"},
        {"text_preview": "poor delivery but refund support", "label": "NEGATIVE"},
        {"text_preview": "excellent product and fast service", "label": "POSITIVE"},
    ]

    summary = summarize_drift(logs)

    assert summary["status"] == "healthy"
    assert summary["flags"] == []


def test_summarize_drift_flags_language_and_vocab_shift() -> None:
    logs = [
        {"text_preview": "bahut kharab anubhav zyxqv frobnicate splarn", "label": "NEGATIVE"},
        {"text_preview": "yeh service alag confusing zyxqv splarn", "label": "NEGATIVE"},
        {"text_preview": "ajeeeb samasya zyxqv splarn unknownterm", "label": "NEGATIVE"},
        {"text_preview": "refund blorptastic qwertonium zyxqv", "label": "NEGATIVE"},
        {"text_preview": "delivery snargle splarn unknownterm", "label": "NEGATIVE"},
    ]

    summary = summarize_drift(logs)

    assert summary["status"] == "drift_detected"
    assert "label_distribution_drift" in summary["flags"]
    assert "vocabulary_drift" in summary["flags"]
