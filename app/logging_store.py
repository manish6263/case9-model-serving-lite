import hashlib
import json
from collections.abc import Iterable
from datetime import UTC, datetime
from pathlib import Path
from threading import Lock
from typing import Any


_LOG_LOCK = Lock()


def initialize_log_store(log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.touch(exist_ok=True)


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def preview_text(text: str, max_chars: int = 80) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= max_chars:
        return normalized
    return f"{normalized[: max_chars - 3]}..."


def log_prediction(
    log_path: Path,
    *,
    request_id: str,
    text: str,
    label: str,
    score: float,
    model_version: str,
    latency_ms: int,
) -> None:
    initialize_log_store(log_path)
    entry = {
        "request_id": request_id,
        "created_at": datetime.now(UTC).isoformat(),
        "text_hash": hash_text(text),
        "text_preview": preview_text(text),
        "label": label,
        "score": score,
        "model_version": model_version,
        "latency_ms": latency_ms,
    }

    with _LOG_LOCK:
        with log_path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(entry, sort_keys=True) + "\n")


def _parse_log_lines(lines: Iterable[str]) -> list[dict[str, Any]]:
    entries = []
    for line in lines:
        stripped = line.strip()
        if stripped:
            entries.append(json.loads(stripped))
    return entries


def fetch_recent_logs(log_path: Path, limit: int = 20) -> list[dict[str, Any]]:
    initialize_log_store(log_path)
    with _LOG_LOCK:
        entries = _parse_log_lines(log_path.read_text(encoding="utf-8").splitlines())

    return list(reversed(entries[-limit:]))
