"""Regression tests for CORS middleware contract.

Prevents regressions like:
  - Olvidar agregar el origen de producción a ALLOWED_ORIGINS.
  - Cambiar el orden de middlewares y romper preflight.
  - Restringir headers permitidos y romper Authorization/X-Request-ID.

El conftest setea ALLOWED_ORIGINS default ("http://localhost:5173").
Estos tests asumen ese valor.
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

ALLOWED_ORIGIN = "http://localhost:5173"
DISALLOWED_ORIGIN = "https://evil.example.com"


def _preflight_headers(method: str = "GET", extra_headers: str = "authorization,content-type,x-request-id") -> dict:
    return {
        "Origin": ALLOWED_ORIGIN,
        "Access-Control-Request-Method": method,
        "Access-Control-Request-Headers": extra_headers,
    }


def test_preflight_allowed_origin_echoes_origin():
    with TestClient(app) as tc:
        r = tc.options("/auth/me", headers=_preflight_headers())
    assert r.status_code == 200
    assert r.headers.get("access-control-allow-origin") == ALLOWED_ORIGIN
    assert r.headers.get("access-control-allow-credentials") == "true"


def test_preflight_allowed_methods_includes_crud():
    with TestClient(app) as tc:
        r = tc.options("/auth/me", headers=_preflight_headers())
    methods = r.headers.get("access-control-allow-methods", "")
    for m in ("GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"):
        assert m in methods, f"{m} missing in Allow-Methods: {methods}"


def test_preflight_allowed_headers_includes_auth_and_request_id():
    with TestClient(app) as tc:
        r = tc.options("/auth/me", headers=_preflight_headers())
    allow = (r.headers.get("access-control-allow-headers") or "").lower()
    assert "authorization" in allow
    assert "content-type" in allow
    assert "x-request-id" in allow


def test_preflight_disallowed_origin_does_not_echo_header():
    with TestClient(app) as tc:
        r = tc.options(
            "/auth/me",
            headers={
                "Origin": DISALLOWED_ORIGIN,
                "Access-Control-Request-Method": "GET",
            },
        )
    # Starlette responde 400 al preflight de un origen no permitido y omite Allow-Origin.
    assert r.headers.get("access-control-allow-origin") != DISALLOWED_ORIGIN


def test_actual_request_includes_cors_header_for_allowed_origin():
    """Aún en respuestas 401 (sin auth), el header CORS debe estar presente."""
    with TestClient(app) as tc:
        r = tc.get("/auth/me", headers={"Origin": ALLOWED_ORIGIN})
    assert r.status_code == 401
    assert r.headers.get("access-control-allow-origin") == ALLOWED_ORIGIN


def test_actual_request_no_cors_header_for_disallowed_origin():
    with TestClient(app) as tc:
        r = tc.get("/auth/me", headers={"Origin": DISALLOWED_ORIGIN})
    assert r.headers.get("access-control-allow-origin") != DISALLOWED_ORIGIN
