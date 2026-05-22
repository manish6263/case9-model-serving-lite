# Decisions Log - Case 9

## Assumptions I Made

1. The production app needs a simple HTTP API first because the brief asks for a live `/predict` endpoint.
2. The first version should optimize for observability and evaluation over model novelty because the case tests operational nuance.

## Trade-offs

| Choice | Alternative | Why I Picked This |
|---|---|---|
| FastAPI | Flask | Built-in validation, typed schemas, and automatic API docs help make the service easier to test and demo. |
| Small, incremental commits | One large final commit | The student pack says evaluators may inspect commit history, so steady progress is part of the submission story. |

## What I De-scoped And Why

- Full model loading in the first scaffold commit - keeping the initial commit focused on project structure and health checks.

## What I'd Do Differently With Another Day

- Add a real model registry and canary rollout instead of a lightweight promotion gate.
