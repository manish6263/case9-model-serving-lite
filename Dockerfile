FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    CASE9_LOG_PATH=/tmp/case9-predictions.jsonl

WORKDIR /app

ARG INSTALL_HF=true

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY requirements-hf.txt .
RUN if [ "$INSTALL_HF" = "true" ]; then pip install --no-cache-dir -r requirements-hf.txt; fi

COPY app ./app

EXPOSE 8000

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
