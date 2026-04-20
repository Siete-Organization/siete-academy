"""Structured JSON logging.

One line per log event, parseable by any log aggregator (Loki, Datadog, ELK).
Each record automatically carries:
  * timestamp (UTC, ISO-8601)
  * level
  * logger name
  * message
  * request_id (when inside an HTTP request, via ContextVar)
  * any extra={...} passed at the call site

Usage:
    from app.core.logging import configure_logging, get_logger
    configure_logging()
    log = get_logger(__name__)
    log.info("application.reviewed", extra={"application_id": 42, "status": "approved"})
"""

from __future__ import annotations

import logging
import sys
from contextvars import ContextVar
from typing import Any

from pythonjsonlogger import jsonlogger

from app.core.config import get_settings

# ContextVar lets async handlers share a request_id without thread-locals
request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)
user_id_var: ContextVar[int | None] = ContextVar("user_id", default=None)


class ContextFilter(logging.Filter):
    """Inject contextual fields into every record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get() or "-"
        record.user_id = user_id_var.get()
        record.app_env = get_settings().app_env
        return True


class JsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(
        self,
        log_record: dict[str, Any],
        record: logging.LogRecord,
        message_dict: dict[str, Any],
    ) -> None:
        super().add_fields(log_record, record, message_dict)
        log_record["ts"] = self.formatTime(record, "%Y-%m-%dT%H:%M:%S.%fZ")
        log_record["level"] = record.levelname
        log_record["logger"] = record.name
        log_record.setdefault("message", record.getMessage())
        # Always-on context fields
        log_record["request_id"] = getattr(record, "request_id", "-")
        log_record["user_id"] = getattr(record, "user_id", None)
        log_record["app_env"] = getattr(record, "app_env", "unknown")
        # Strip empty/None noise
        for k in list(log_record.keys()):
            if log_record[k] in (None, "", "-") and k not in {"message", "level", "ts"}:
                log_record.pop(k)


class HumanFormatter(logging.Formatter):
    """Readable format for local development."""

    def format(self, record: logging.LogRecord) -> str:
        rid = getattr(record, "request_id", "-")
        uid = getattr(record, "user_id", None)
        prefix = f"[{record.levelname:<5}] [{record.name}] rid={rid}"
        if uid is not None:
            prefix += f" uid={uid}"
        extras = {
            k: v
            for k, v in record.__dict__.items()
            if k
            not in {
                "args",
                "asctime",
                "created",
                "exc_info",
                "exc_text",
                "filename",
                "funcName",
                "levelname",
                "levelno",
                "lineno",
                "message",
                "module",
                "msecs",
                "msg",
                "name",
                "pathname",
                "process",
                "processName",
                "relativeCreated",
                "stack_info",
                "thread",
                "threadName",
                "request_id",
                "user_id",
                "app_env",
                "taskName",
            }
        }
        extra_str = ""
        if extras:
            extra_str = " " + " ".join(f"{k}={v!r}" for k, v in extras.items())
        line = f"{prefix} {record.getMessage()}{extra_str}"
        if record.exc_info:
            line += "\n" + self.formatException(record.exc_info)
        return line


_CONFIGURED = False


def configure_logging(level: str | None = None) -> None:
    """Idempotent root-logger setup. Call once at process startup."""
    global _CONFIGURED
    if _CONFIGURED:
        return

    settings = get_settings()
    level = level or ("DEBUG" if settings.app_env == "development" else "INFO")

    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.addFilter(ContextFilter())

    if settings.app_env == "development":
        handler.setFormatter(HumanFormatter())
    else:
        handler.setFormatter(
            JsonFormatter("%(message)s", rename_fields={"levelname": "level"})
        )

    root.addHandler(handler)

    # Tame noisy libraries
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


def bind_request_id(request_id: str | None) -> None:
    request_id_var.set(request_id)


def bind_user_id(user_id: int | None) -> None:
    user_id_var.set(user_id)


def clear_context() -> None:
    request_id_var.set(None)
    user_id_var.set(None)
