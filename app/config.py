import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_PATH = BASE_DIR / "logs" / "predictions.jsonl"


def get_log_path() -> Path:
    configured_path = os.getenv("CASE9_LOG_PATH")
    if configured_path:
        return Path(configured_path)
    return LOG_PATH
