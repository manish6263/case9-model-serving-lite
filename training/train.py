import csv
import json
import math
import re
from collections import Counter
from pathlib import Path


TOKEN_PATTERN = re.compile(r"[a-z']+")


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower())


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def train_keyword_model(rows: list[dict[str, str]]) -> dict:
    positive_counts: Counter[str] = Counter()
    negative_counts: Counter[str] = Counter()

    for row in rows:
        tokens = tokenize(row["text"])
        if row["label"] == "POSITIVE":
            positive_counts.update(tokens)
        else:
            negative_counts.update(tokens)

    vocab = sorted(set(positive_counts) | set(negative_counts))
    weights = {}
    for token in vocab:
        positive_score = positive_counts[token] + 1
        negative_score = negative_counts[token] + 1
        weights[token] = round(math.log(positive_score / negative_score), 4)

    return {
        "model_type": "keyword_log_odds",
        "model_version": "keyword-candidate-v1",
        "threshold": 0.0,
        "weights": weights,
    }


def main() -> None:
    root = Path(__file__).resolve().parent
    rows = read_rows(root / "train.csv")
    model = train_keyword_model(rows)
    output_path = root / "candidate_model.json"
    output_path.write_text(json.dumps(model, indent=2, sort_keys=True), encoding="utf-8")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
