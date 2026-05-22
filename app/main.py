from fastapi import FastAPI


app = FastAPI(
    title="Case 9 Model Serving Lite",
    description="A production-minded sentiment model service.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
