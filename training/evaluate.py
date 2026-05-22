import csv
import json
import re
from pathlib import Path


TOKEN_PATTERN = re.compile(r"[a-z']+")


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower())


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def predict(model: dict, text: str) -> str:
    score = sum(model["weights"].get(token, 0.0) for token in tokenize(text))
    return "POSITIVE" if score >= model["threshold"] else "NEGATIVE"


def binary_metrics(y_true: list[str], y_pred: list[str]) -> dict[str, float]:
    tp = sum(true == pred == "POSITIVE" for true, pred in zip(y_true, y_pred))
    tn = sum(true == pred == "NEGATIVE" for true, pred in zip(y_true, y_pred))
    fp = sum(true == "NEGATIVE" and pred == "POSITIVE" for true, pred in zip(y_true, y_pred))
    fn = sum(true == "POSITIVE" and pred == "NEGATIVE" for true, pred in zip(y_true, y_pred))

    accuracy = (tp + tn) / len(y_true)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0

    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
    }


def main() -> None:
    root = Path(__file__).resolve().parent
    model = json.loads((root / "candidate_model.json").read_text(encoding="utf-8"))
    rows = read_rows(root / "validation.csv")
    y_true = [row["label"] for row in rows]
    y_pred = [predict(model, row["text"]) for row in rows]
    metrics = binary_metrics(y_true, y_pred)
    metrics["model_version"] = model["model_version"]
    output_path = root / "candidate_metrics.json"
    output_path.write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
