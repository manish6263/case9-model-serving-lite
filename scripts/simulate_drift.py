import os
import sys

import httpx


BASE_URL = os.getenv("CASE9_BASE_URL", "http://localhost:8000")

NORMAL_TEXTS = [
    "The product is good and delivery was fast.",
    "Support was poor but the refund process worked.",
    "I love this service and recommend it.",
]

DRIFT_TEXTS = [
    "bahut kharab anubhav zyxqv frobnicate splarn unknownterm",
    "yeh service totally alag aur confusing zyxqv splarn",
    "Necesito ayuda con una orden rara blorptastic qwertonium",
]


def post_prediction(text: str) -> None:
    response = httpx.post(f"{BASE_URL}/predict", json={"text": text}, timeout=10)
    response.raise_for_status()
    print(response.json())


def main() -> None:
    try:
        for text in NORMAL_TEXTS + DRIFT_TEXTS:
            post_prediction(text)

        summary = httpx.get(f"{BASE_URL}/monitoring/summary", timeout=10)
        summary.raise_for_status()
        print(summary.json())
    except httpx.ConnectError:
        print(f"Could not connect to {BASE_URL}.")
        print("Start the local API with `uvicorn app.main:app --reload`,")
        print("or set CASE9_BASE_URL=https://case9-model-serving-lite.onrender.com")
        sys.exit(1)


if __name__ == "__main__":
    main()
