import re
from collections import Counter
from typing import Any


REFERENCE_AVG_LENGTH = 75
REFERENCE_POSITIVE_RATE = 0.55
MAX_AVG_LENGTH_RATIO = 2.0
MAX_POSITIVE_RATE_DELTA = 0.35
MAX_NON_ASCII_RATE = 0.25
MAX_VOCAB_NOVELTY_RATE = 0.55

REFERENCE_VOCAB = {
    "amazing",
    "awful",
    "bad",
    "best",
    "broken",
    "delivery",
    "excellent",
    "fast",
    "good",
    "great",
    "happy",
    "love",
    "order",
    "perfect",
    "poor",
    "product",
    "refund",
    "recommend",
    "service",
    "support",
    "terrible",
    "worst",
}


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z']+", text.lower())


def non_ascii_ratio(text: str) -> float:
    if not text:
        return 0.0
    return sum(1 for char in text if ord(char) > 127) / len(text)


def vocab_novelty_rate(texts: list[str]) -> float:
    tokens = [token for text in texts for token in tokenize(text)]
    if not tokens:
        return 0.0
    novel_count = sum(1 for token in tokens if token not in REFERENCE_VOCAB)
    return novel_count / len(tokens)


def summarize_drift(logs: list[dict[str, Any]]) -> dict[str, Any]:
    if not logs:
        return {
            "total_requests": 0,
            "status": "insufficient_data",
            "flags": ["no_requests_logged"],
            "metrics": {},
        }

    previews = [str(entry["text_preview"]) for entry in logs]
    labels = [str(entry["label"]) for entry in logs]
    label_counts = Counter(labels)
    avg_length = sum(len(text) for text in previews) / len(previews)
    positive_rate = label_counts.get("POSITIVE", 0) / len(labels)
    avg_non_ascii_rate = sum(non_ascii_ratio(text) for text in previews) / len(previews)
    novelty_rate = vocab_novelty_rate(previews)

    flags = []
    if avg_length > REFERENCE_AVG_LENGTH * MAX_AVG_LENGTH_RATIO:
        flags.append("text_length_drift")
    if abs(positive_rate - REFERENCE_POSITIVE_RATE) > MAX_POSITIVE_RATE_DELTA:
        flags.append("label_distribution_drift")
    if avg_non_ascii_rate > MAX_NON_ASCII_RATE:
        flags.append("language_or_script_drift")
    if novelty_rate > MAX_VOCAB_NOVELTY_RATE:
        flags.append("vocabulary_drift")

    return {
        "total_requests": len(logs),
        "status": "drift_detected" if flags else "healthy",
        "flags": flags,
        "metrics": {
            "avg_text_length": round(avg_length, 2),
            "positive_rate": round(positive_rate, 4),
            "avg_non_ascii_rate": round(avg_non_ascii_rate, 4),
            "vocab_novelty_rate": round(novelty_rate, 4),
            "label_counts": dict(label_counts),
        },
    }
