import os

import httpx


BASE_URL = os.getenv("CASE9_BASE_URL", "http://localhost:8000")

NORMAL_TEXTS = [
    "The product is good and delivery was fast.",
    "Support was poor but the refund process worked.",
    "I love this service and recommend it.",
]

DRIFT_TEXTS = [
    "बहुत खराब अनुभव zyxqv frobnicate splarn unknownterm",
    "यह service totally अलग और confusing zyxqv splarn",
    "Necesito ayuda con una orden rara blorptastic qwertonium",
]


def post_prediction(text: str) -> None:
    response = httpx.post(f"{BASE_URL}/predict", json={"text": text}, timeout=10)
    response.raise_for_status()
    print(response.json())


def main() -> None:
    for text in NORMAL_TEXTS + DRIFT_TEXTS:
        post_prediction(text)

    summary = httpx.get(f"{BASE_URL}/monitoring/summary", timeout=10)
    summary.raise_for_status()
    print(summary.json())


if __name__ == "__main__":
    main()
