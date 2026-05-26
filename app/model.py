import os
import re
from functools import lru_cache
from typing import Any


HF_MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
FALLBACK_MODEL_VERSION = "rule-based-fallback-v0"
_MODEL_LOAD_ERROR: str | None = None
_MODEL_BACKEND: str = "not_loaded"

POSITIVE_WORDS = {
    "amazing",
    "best",
    "excellent",
    "good",
    "great",
    "happy",
    "love",
    "loved",
    "perfect",
    "recommend",
}

NEGATIVE_WORDS = {
    "awful",
    "bad",
    "broken",
    "disappointing",
    "hate",
    "hated",
    "poor",
    "refund",
    "terrible",
    "worst",
}


def predict_with_rule_based_fallback(text: str) -> tuple[str, float]:
    tokens = set(re.findall(r"[a-z']+", text.lower()))
    positive_hits = len(tokens & POSITIVE_WORDS)
    negative_hits = len(tokens & NEGATIVE_WORDS)

    if positive_hits >= negative_hits:
        score = 0.55 + min(positive_hits, 5) * 0.08
        return "POSITIVE", min(score, 0.95)

    score = 0.55 + min(negative_hits, 5) * 0.08
    return "NEGATIVE", min(score, 0.95)


@lru_cache(maxsize=1)
def get_huggingface_pipeline() -> Any | None:
    global _MODEL_BACKEND, _MODEL_LOAD_ERROR

    if os.getenv("CASE9_DISABLE_HF", "").lower() in {"1", "true", "yes"}:
        _MODEL_BACKEND = "fallback"
        _MODEL_LOAD_ERROR = "CASE9_DISABLE_HF is enabled"
        return None

    try:
        from transformers import pipeline

        classifier = pipeline("sentiment-analysis", model=HF_MODEL_NAME)
        _MODEL_BACKEND = "huggingface"
        _MODEL_LOAD_ERROR = None
        return classifier
    except Exception as exc:
        _MODEL_BACKEND = "fallback"
        _MODEL_LOAD_ERROR = f"{type(exc).__name__}: {exc}"
        return None


def get_model_version() -> str:
    if get_huggingface_pipeline() is None:
        return FALLBACK_MODEL_VERSION
    return f"{HF_MODEL_NAME}-v1"


def get_model_status() -> dict[str, object]:
    get_huggingface_pipeline()
    return {
        "backend": _MODEL_BACKEND,
        "model_version": get_model_version(),
        "hf_model_name": HF_MODEL_NAME,
        "hf_disabled": os.getenv("CASE9_DISABLE_HF", "").lower()
        in {"1", "true", "yes"},
        "load_error": _MODEL_LOAD_ERROR,
    }


def predict_sentiment(text: str) -> tuple[str, float]:
    classifier = get_huggingface_pipeline()
    if classifier is None:
        return predict_with_rule_based_fallback(text)

    result = classifier(text, truncation=True)[0]
    label = str(result["label"]).upper()
    score = float(result["score"])
    if label not in {"POSITIVE", "NEGATIVE"}:
        return predict_with_rule_based_fallback(text)
    return label, score
