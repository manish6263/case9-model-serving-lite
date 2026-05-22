# Decisions Log - Case 9

## Assumptions I Made

1. The production app needs a simple HTTP API first because the brief asks for a live `/predict` endpoint.
2. The first version should optimize for observability and evaluation over model novelty because the case tests operational nuance.
3. Free-tier deployment reliability matters more than loading the heaviest possible model in the live demo.
4. The retraining workflow can use a lightweight candidate model as long as the promotion gate is explicit, reproducible, and easy to inspect.

## Trade-offs

| Choice | Alternative | Why I Picked This |
|---|---|---|
| FastAPI | Flask | Built-in validation, typed schemas, and automatic API docs help make the service easier to test and demo. |
| JSONL prediction logs | Plain console logs | JSONL makes the demo inspectable after multiple requests and avoids extra infrastructure for a one-day case study. |
| Configurable log path | Hard-coded repo-local log only | Local synced folders can be unreliable, while deployments may need writable ephemeral storage. |
| Hash plus short preview | Store full raw text | Sentiment inputs can contain PII, so the log keeps enough information to debug patterns without storing the full payload. |
| Simple drift heuristics | Full production drift platform | The brief asks for a basic stub, so clear signals are more valuable than overbuilding infrastructure. |
| DistilBERT SST-2 | Train a model from scratch | The brief asks to productionize a pretrained model; DistilBERT is small enough for CPU demos and familiar to evaluators. |
| `CASE9_DISABLE_HF` fallback switch | Always load Hugging Face in every environment | Tests and constrained deployments should stay fast and predictable, while the normal app path still supports DistilBERT. |
| Optional Hugging Face Docker layer | Always install PyTorch in the base image | PyTorch makes free-tier builds slow and heavy, so the base image stays deployable while an `INSTALL_HF=true` image remains available. |
| Python slim Docker image | Full CUDA image | The brief allows CPU free-tier compute, and a slim image is smaller and cheaper to deploy. |
| CI tests fallback mode | CI loads DistilBERT every run | The CI goal is to catch API contract regressions quickly; full model loading is verified separately and can be enabled when needed. |
| Lightweight keyword retraining gate | Expensive transformer fine-tuning in CI | The brief tests the promotion mechanism. A small reproducible model makes the pass/fail gate easy to inspect in a demo. |
| Render fallback deployment | Heavy default Hugging Face deployment | The live URL should be reliable on free-tier infrastructure; the optional Hugging Face image remains available for fuller local or paid deployments. |
| Rule-based fallback first | Hugging Face model in the first API commit | The API contract can be tested before introducing model download/runtime risk. The fallback will remain useful if deployment cannot load the pretrained model. |
| Small, incremental commits | One large final commit | The student pack says evaluators may inspect commit history, so steady progress is part of the submission story. |

## What I De-scoped And Why

- Always-on Hugging Face in the default container - PyTorch made free-tier builds slow, so the default deployment uses fallback mode while keeping an optional Hugging Face image.
- Full model registry - replaced with a transparent JSON candidate model plus metrics gate to keep the case study focused and demoable.
- Real alerting integration - documented in the playbook, but not wired to Slack/PagerDuty because the brief only requires a working monitored service and demo.
- Raw text retention - avoided because sentiment inputs can contain PII.

## What I'd Do Differently With Another Day

- Add a model registry and canary rollout.
- Add shadow traffic evaluation for candidate models.
- Add dashboard screenshots for latency, drift, and label distribution.
- Add a larger, messier validation set with neutral/mixed sentiment examples.

## AI Assistance Disclosure

I used an AI coding assistant to help scaffold code, tests, and documentation. I reviewed the implementation choices and kept the project intentionally small enough to explain line by line.
