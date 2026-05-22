# Decisions Log - Case 9

## Assumptions I Made

1. The production app needs a simple HTTP API first because the brief asks for a live `/predict` endpoint.
2. The first version should optimize for observability and evaluation over model novelty because the case tests operational nuance.

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
| Rule-based fallback first | Hugging Face model in the first API commit | The API contract can be tested before introducing model download/runtime risk. The fallback will remain useful if deployment cannot load the pretrained model. |
| Small, incremental commits | One large final commit | The student pack says evaluators may inspect commit history, so steady progress is part of the submission story. |

## What I De-scoped And Why

- Full Hugging Face model loading in the first prediction commit - keeping this step focused on API contract, validation, and tests.

## What I'd Do Differently With Another Day

- Add a real model registry and canary rollout instead of a lightweight promotion gate.
