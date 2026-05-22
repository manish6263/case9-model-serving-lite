# Case 9: Model Serving Lite

**Live API:** coming soon
**Demo video:** coming soon

Turn a pretrained sentiment model into a small production-minded ML service with API, logging, drift checks, containerization, CI, and a demo that proves we can detect failure before users complain.

## What This Is

This project wraps a sentiment-classification model in a FastAPI service and adds the production basics around it: observability, drift checks, tests, and a retrain/evaluation gate.

## Current Status

- FastAPI app scaffolded.
- `/health` endpoint added.
- `/predict` endpoint added with Hugging Face DistilBERT loading and deterministic fallback.
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

## How To Run With Docker

```bash
docker build -t case9-model-serving-lite .
docker run -p 8000:8000 -e CASE9_DISABLE_HF=1 case9-model-serving-lite
```

Remove `-e CASE9_DISABLE_HF=1` when you want the container to load the Hugging Face model instead of the deterministic fallback.

By default, prediction logs are written to `logs/predictions.jsonl`. To override this path:

```bash
set CASE9_LOG_PATH=artifacts\local-predictions.jsonl
```

To force the deterministic fallback model during local debugging or tests:

```bash
set CASE9_DISABLE_HF=1
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
- Hugging Face Transformers: pretrained DistilBERT sentiment model.
- JSONL logs: local request/response log store for demo-friendly debugging.
- Drift checks: text length, label distribution, language/script ratio, and vocabulary novelty.
- pytest: contract tests for the service.
- A deterministic fallback model keeps the service usable if model loading fails on a free-tier host.
- Docker: containerized API for Render or any container host.
- GitHub Actions and model tooling will be added in later commits.

## What's Not Done

- Retrain/evaluation CI gate.
