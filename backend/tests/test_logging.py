"""Regression tests for JSON logging.

Prevents:
  - KeyError en _perform_rename_log_fields cuando el formato no incluye
    campos que python-json-logger intenta renombrar.
  - Olvidar setear `level`, `ts`, `request_id`, `app_env` en cada record.

Estos tests instancian el JsonFormatter directamente porque conftest fuerza
APP_ENV=development (HumanFormatter), que no expone el bug.
"""

from __future__ import annotations

import json
import logging

from app.core.logging import JsonFormatter


def _make_record(msg: str = "http.request", level: int = logging.INFO) -> logging.LogRecord:
    return logging.LogRecord(
        name="http",
        level=level,
        pathname=__file__,
        lineno=1,
        msg=msg,
        args=(),
        exc_info=None,
    )


def test_json_formatter_does_not_crash_on_simple_message():
    """Reproduce el bug: KeyError 'levelname' en _perform_rename_log_fields."""
    fmt = JsonFormatter("%(message)s")
    rec = _make_record()
    # Antes del fix esto crasheaba con KeyError: 'levelname'
    out = fmt.format(rec)
    payload = json.loads(out)
    assert payload["message"] == "http.request"
    assert payload["level"] == "INFO"


def test_json_formatter_includes_required_context_fields():
    fmt = JsonFormatter("%(message)s")
    rec = _make_record()
    # Simula lo que hace ContextFilter en producción
    rec.request_id = "abc123"
    rec.user_id = 42
    rec.app_env = "production"
    payload = json.loads(fmt.format(rec))
    assert payload["request_id"] == "abc123"
    assert payload["user_id"] == 42
    assert payload["app_env"] == "production"
    assert "ts" in payload
    assert payload["logger"] == "http"


def test_json_formatter_preserves_extra_fields():
    """`log.info("http.request", extra={...})` debe llegar al JSON output."""
    fmt = JsonFormatter("%(message)s")
    rec = _make_record()
    rec.method = "GET"
    rec.path = "/auth/me"
    rec.status = 401
    payload = json.loads(fmt.format(rec))
    assert payload["method"] == "GET"
    assert payload["path"] == "/auth/me"
    assert payload["status"] == 401
