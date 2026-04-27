#!/usr/bin/env sh
# Entrypoint for the `worker` service in production.
# IMPORTANT: the worker does NOT run migrations. Only the `api` service does.
# Two services trying to migrate concurrently fight for the alembic_version
# lock and one will crash on a clean start.
set -eu

echo "[entrypoint-worker] starting celery worker (concurrency=${CELERY_CONCURRENCY:-2})"
exec celery -A app.core.celery_app.celery_app worker \
    --loglevel=info \
    --concurrency="${CELERY_CONCURRENCY:-2}"
