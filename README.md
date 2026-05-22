# Case 9: Model Serving Lite

**Live API:** coming soon
**Demo video:** coming soon

Turn a pretrained sentiment model into a small production-minded ML service with API, logging, drift checks, containerization, CI, and a demo that proves we can detect failure before users complain.

## What This Is

This project wraps a sentiment-classification model in a FastAPI service and adds the production basics around it: observability, drift checks, tests, and a retrain/evaluation gate.

## Current Status

- FastAPI app scaffolded.
- `/health` endpoint added.
- `/predict` endpoint added with a deterministic fallback sentiment model.
- `/logs/recent` endpoint added for privacy-aware request/response debugging.
- `/monitoring/summary` endpoint added for drift-monitoring signals.
- Initial tests added.

## How To Run Locally

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs`.

By default, prediction logs are written to `logs/predictions.jsonl`. To override this path:

```bash
set CASE9_LOG_PATH=artifacts\local-predictions.jsonl
```

## Example API Call

```bash
curl -X POST http://localhost:8000/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"I loved this excellent product\"}"
```

Recent prediction logs:

```bash
curl http://localhost:8000/logs/recent
```

Monitoring summary:

```bash
curl http://localhost:8000/monitoring/summary
```

Drift simulation:

```bash
python scripts/simulate_drift.py
```

## How To Test

```bash
pytest
```

## Stack

- FastAPI: typed API service with automatic docs.
- JSONL logs: local request/response log store for demo-friendly debugging.
- Drift checks: text length, label distribution, language/script ratio, and vocabulary novelty.
- pytest: contract tests for the service.
- A deterministic fallback model provides a stable API contract before adding Hugging Face model loading.
- Docker, GitHub Actions, and model tooling will be added in later commits.

## What's Not Done

- Hugging Face model wrapper.
- Retrain/evaluation CI gate.
