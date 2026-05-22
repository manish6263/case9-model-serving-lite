import json
import sys
from pathlib import Path


MIN_F1_DELTA = -0.01


def main() -> None:
    root = Path(__file__).resolve().parent
    production = json.loads((root / "production_metrics.json").read_text(encoding="utf-8"))
    candidate = json.loads((root / "candidate_metrics.json").read_text(encoding="utf-8"))

    f1_delta = candidate["f1"] - production["f1"]
    accuracy_delta = candidate["accuracy"] - production["accuracy"]

    print(
        json.dumps(
            {
                "production": production,
                "candidate": candidate,
                "f1_delta": round(f1_delta, 4),
                "accuracy_delta": round(accuracy_delta, 4),
            },
            indent=2,
            sort_keys=True,
        )
    )

    if f1_delta < MIN_F1_DELTA:
        print("candidate rejected: F1 regressed beyond allowed tolerance")
        sys.exit(1)

    print("candidate accepted: metrics meet promotion gate")


if __name__ == "__main__":
    main()
