# Model Failure Playbook

## How I Would Know The Model Is Failing Before Customers Do

This service will track three kinds of signals:

1. Quality signals: confidence collapse, unusual label distribution, and repeated low-confidence predictions.
2. Data signals: text length drift, vocabulary novelty, and language/script drift.
3. System signals: latency, error rate, and failed model loads.

When a signal crosses a threshold, the response should be to inspect recent logs, compare against the baseline distribution, rollback if needed, and retrain only after the failure mode is understood.

## Current Drift Signals

- Text length drift: recent inputs are much longer than the reference baseline.
- Label distribution drift: the positive/negative mix shifts sharply.
- Language/script drift: recent inputs contain a high non-ASCII ratio.
- Vocabulary drift: recent inputs contain many tokens outside the reference vocabulary.
