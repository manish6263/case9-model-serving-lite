from training.evaluate import binary_metrics, predict
from training.train import train_keyword_model


def test_training_gate_model_scores_validation_examples() -> None:
    rows = [
        {"text": "excellent product", "label": "POSITIVE"},
        {"text": "great support", "label": "POSITIVE"},
        {"text": "terrible product", "label": "NEGATIVE"},
        {"text": "bad support", "label": "NEGATIVE"},
    ]
    model = train_keyword_model(rows)

    assert predict(model, "excellent support") == "POSITIVE"
    assert predict(model, "terrible support") == "NEGATIVE"


def test_binary_metrics_reports_f1() -> None:
    metrics = binary_metrics(
        ["POSITIVE", "POSITIVE", "NEGATIVE", "NEGATIVE"],
        ["POSITIVE", "NEGATIVE", "NEGATIVE", "NEGATIVE"],
    )

    assert metrics["accuracy"] == 0.75
    assert metrics["f1"] == 0.6667
