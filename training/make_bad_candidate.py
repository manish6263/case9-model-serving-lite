import json
from pathlib import Path


def main() -> None:
    root = Path(__file__).resolve().parent
    bad_model = {
        "model_type": "keyword_log_odds",
        "model_version": "keyword-bad-candidate-v1",
        "threshold": 0.0,
        "weights": {
            "bad": 2.0,
            "broken": 2.0,
            "excellent": -2.0,
            "good": -2.0,
            "great": -2.0,
            "poor": 2.0,
            "terrible": 2.0,
            "worst": 2.0,
        },
    }
    (root / "candidate_model.json").write_text(
        json.dumps(bad_model, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print("wrote deliberately regressed candidate_model.json")


if __name__ == "__main__":
    main()
