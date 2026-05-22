from pathlib import Path
from uuid import uuid4

from app.logging_store import fetch_recent_logs, hash_text, log_prediction, preview_text


def make_log_path() -> Path:
    db_dir = Path("artifacts/test-logs")
    db_dir.mkdir(parents=True, exist_ok=True)
    return db_dir / f"{uuid4()}.jsonl"


def test_log_prediction_writes_privacy_aware_entry() -> None:
    log_path = make_log_path()

    log_prediction(
        log_path,
        request_id="req-123",
        text="This text should not be stored in full because it might contain PII.",
        label="POSITIVE",
        score=0.91,
        model_version="test-model",
        latency_ms=12,
    )

    logs = fetch_recent_logs(log_path)

    assert len(logs) == 1
    assert logs[0]["request_id"] == "req-123"
    assert logs[0]["text_hash"] == hash_text(
        "This text should not be stored in full because it might contain PII."
    )
    assert logs[0]["text_preview"] == preview_text(
        "This text should not be stored in full because it might contain PII."
    )


def test_fetch_recent_logs_respects_limit() -> None:
    log_path = make_log_path()

    for index in range(3):
        log_prediction(
            log_path,
            request_id=f"req-{index}",
            text=f"sample {index}",
            label="NEGATIVE",
            score=0.75,
            model_version="test-model",
            latency_ms=10,
        )

    logs = fetch_recent_logs(log_path, limit=2)

    assert [entry["request_id"] for entry in logs] == ["req-2", "req-1"]
