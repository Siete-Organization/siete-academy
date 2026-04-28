# Production image — multi-stage, non-root, healthcheck.
# Build context: repo root (NOT backend/). Coolify config:
#   - Build context: /
#   - Dockerfile path: backend/Dockerfile
# For local dev (hot reload), see backend/Dockerfile.dev + docker-compose.yml.

# ---------- builder ----------
FROM python:3.12-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY backend/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ---------- runtime ----------
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app" \
    APP_ENV=production

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 1001 siete

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY --chown=siete:siete backend/ /app/
COPY --chown=siete:siete --chmod=755 deploy/entrypoint-api.sh /usr/local/bin/entrypoint-api.sh
COPY --chown=siete:siete --chmod=755 deploy/entrypoint-worker.sh /usr/local/bin/entrypoint-worker.sh

USER siete

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=20s --retries=4 \
  CMD curl -fsS http://127.0.0.1:8000/health || exit 1

CMD ["/usr/local/bin/entrypoint-api.sh"]
