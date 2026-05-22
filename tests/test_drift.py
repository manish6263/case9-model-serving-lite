from app.drift import summarize_drift


def test_summarize_drift_returns_insufficient_data_for_empty_logs() -> None:
    summary = summarize_drift([])

    assert summary["status"] == "insufficient_data"
    assert "no_requests_logged" in summary["flags"]


def test_summarize_drift_reports_healthy_for_reference_like_logs() -> None:
    logs = [
        {"text_preview": "good product and fast delivery", "label": "POSITIVE"},
        {"text_preview": "bad support but good product", "label": "NEGATIVE"},
        {"text_preview": "great service and perfect order", "label": "POSITIVE"},
        {"text_preview": "poor delivery but refund support", "label": "NEGATIVE"},
    ]

    summary = summarize_drift(logs)

    assert summary["status"] == "healthy"
    assert summary["flags"] == []


def test_summarize_drift_flags_language_and_vocab_shift() -> None:
    logs = [
        {
            "text_preview": "बहुत खराब अनुभव बिल्कुल अजीब समस्या zyxqv frobnicate splarn",
            "label": "NEGATIVE",
        },
        {
            "text_preview": "यह पूरी तरह अलग और confusing समस्या zyxqv splarn",
            "label": "NEGATIVE",
        },
    ]

    summary = summarize_drift(logs)

    assert summary["status"] == "drift_detected"
    assert "language_or_script_drift" in summary["flags"]
    assert "vocabulary_drift" in summary["flags"]
