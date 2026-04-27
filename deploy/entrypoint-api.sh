#!/usr/bin/env sh
# Entrypoint for the `api` service in production.
# IMPORTANT: alembic upgrade head MUST fail loudly. Do NOT add `|| echo` here —
# a silent migration failure leaves the API serving on a stale schema (this
# burned us in AI-SDR with the search_learnings 500 bug).
set -eu

echo "[entrypoint-api] running alembic upgrade head"
alembic upgrade head

echo "[entrypoint-api] starting gunicorn (workers=${WEB_CONCURRENCY:-3})"
exec gunicorn app.main:app \
    --workers "${WEB_CONCURRENCY:-3}" \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --access-logfile - \
    --error-logfile - \
    --timeout 60 \
    --keep-alive 5 \
    --graceful-timeout 30
