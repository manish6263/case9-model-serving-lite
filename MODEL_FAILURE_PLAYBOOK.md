# Model Failure Playbook

## How I Would Know The Model Is Failing Before Customers Do

This service will track three kinds of signals:

1. Quality signals: confidence collapse, unusual label distribution, and repeated low-confidence predictions.
2. Data signals: text length drift, vocabulary novelty, and language/script drift.
3. System signals: latency, error rate, and failed model loads.

When a signal crosses a threshold, the response should be to inspect recent logs, compare against the baseline distribution, rollback if needed, and retrain only after the failure mode is understood.

If the Hugging Face model cannot load, the service falls back to a deterministic rule-based classifier. That is not meant to be equally accurate; it keeps the API alive and makes the degraded state visible through `model_version`.

## What I Would Check First

1. Recent logs: match the failing `request_id` to label, score, model version, latency, hash, and preview.
2. Drift summary: check whether input length, language/script mix, vocabulary novelty, or label distribution shifted.
3. Model version: confirm whether the service is using DistilBERT or fallback mode.
4. CI gate: verify whether a recent candidate model was promoted or rejected.
5. Error budget: compare current latency/error rate to expected production thresholds.

## Model Update Gate

Every candidate model must beat the production F1 tolerance on the held-out validation set before promotion. If the gate rejects a model, the next step is to inspect changed training data, class balance, and error examples before retraining again.

Current gate:

- Baseline production F1: `0.83`
- Allowed F1 tolerance: `-0.01`
- Candidate accepted if F1 does not regress beyond tolerance.
- Deliberately bad candidate is available through `training/make_bad_candidate.py` for demo purposes.

## Current Drift Signals

- Text length drift: recent inputs are much longer than the reference baseline.
- Label distribution drift: the positive/negative mix shifts sharply.
- Language/script drift: recent inputs contain a high non-ASCII ratio.
- Vocabulary drift: recent inputs contain many tokens outside the reference vocabulary.

## Immediate Response Plan

- If drift is detected but latency/errors are normal: sample logs, inspect input changes, and update validation data before retraining.
- If latency spikes: force fallback mode or roll back to the previous image.
- If label distribution shifts after a model update: revert the model and run the promotion gate against the new examples.
- If bad predictions include sensitive text: disable previews and keep only hashes until redaction is added.
