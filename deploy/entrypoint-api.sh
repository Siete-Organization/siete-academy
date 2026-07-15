#!/usr/bin/env sh
# Entrypoint for the `api` service in production.
# IMPORTANT: alembic upgrade head MUST fail loudly. Do NOT add `|| echo` here —
# a silent migration failure leaves the API serving on a stale schema (this
# burned us in AI-SDR with the search_learnings 500 bug).
set -eu

echo "[entrypoint-api] running alembic upgrade head"
alembic upgrade head

echo "[entrypoint-api] starting gunicorn (workers=${WEB_CONCURRENCY:-3})"
# --forwarded-allow-ips "*": el contenedor solo es alcanzable por Traefik
# (red interna de Docker), así que confiamos en su X-Forwarded-For para ver
# la IP real del cliente. Sin esto, el rate limit de /applications keyea por
# la IP del proxy y el bucket se comparte entre TODOS los alumnos
# (incidente 2026-07-14: postulaciones bloqueadas con 500).
exec gunicorn app.main:app \
    --workers "${WEB_CONCURRENCY:-3}" \
    --worker-class uvicorn.workers.UvicornWorker \
    --forwarded-allow-ips "*" \
    --bind 0.0.0.0:8000 \
    --access-logfile - \
    --error-logfile - \
    --timeout 60 \
    --keep-alive 5 \
    --graceful-timeout 30
