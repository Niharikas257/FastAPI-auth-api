FROM python:3.11-slim

WORKDIR /app

# System deps (psycopg2 needs gcc & pg headers to build wheels occasionally)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default command (alembic then start server). Overridable in compose.
CMD bash -lc "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"
