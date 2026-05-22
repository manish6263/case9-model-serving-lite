import os
import re
from functools import lru_cache
from typing import Any


HF_MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
FALLBACK_MODEL_VERSION = "rule-based-fallback-v0"

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
    if os.getenv("CASE9_DISABLE_HF", "").lower() in {"1", "true", "yes"}:
        return None

    try:
        from transformers import pipeline

        return pipeline("sentiment-analysis", model=HF_MODEL_NAME)
    except Exception:
        return None


def get_model_version() -> str:
    if get_huggingface_pipeline() is None:
        return FALLBACK_MODEL_VERSION
    return f"{HF_MODEL_NAME}-v1"


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
