import os

import httpx


BASE_URL = os.getenv("CASE9_BASE_URL", "http://localhost:8000")


def print_response(title: str, response: httpx.Response) -> None:
    response.raise_for_status()
    print(f"\n## {title}")
    print(response.json())


def main() -> None:
    prediction = httpx.post(
        f"{BASE_URL}/predict",
        json={"text": "I loved this excellent product and the delivery was fast."},
        timeout=10,
    )
    print_response("Prediction", prediction)

    logs = httpx.get(f"{BASE_URL}/logs/recent?limit=1", timeout=10)
    print_response("Recent log", logs)

    monitoring = httpx.get(f"{BASE_URL}/monitoring/summary", timeout=10)
    print_response("Monitoring summary", monitoring)


if __name__ == "__main__":
    main()
