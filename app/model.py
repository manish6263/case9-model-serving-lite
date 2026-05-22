import re


MODEL_VERSION = "rule-based-fallback-v0"

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


def predict_sentiment(text: str) -> tuple[str, float]:
    tokens = set(re.findall(r"[a-z']+", text.lower()))
    positive_hits = len(tokens & POSITIVE_WORDS)
    negative_hits = len(tokens & NEGATIVE_WORDS)

    if positive_hits >= negative_hits:
        score = 0.55 + min(positive_hits, 5) * 0.08
        return "POSITIVE", min(score, 0.95)

    score = 0.55 + min(negative_hits, 5) * 0.08
    return "NEGATIVE", min(score, 0.95)
