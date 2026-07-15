"""Rate limit de /applications + contrato de errores con CORS.

Contexto (incidente 2026-07-14): al excederse el límite, prod devolvía 500
text/plain SIN headers CORS — el navegador lo bloqueaba y el aspirante veía
un error de red en la página final. Estos tests fijan el contrato:
  - límite excedido => 429 JSON con Retry-After (nunca 500)
  - excepción no manejada => 500 JSON que atraviesa CORSMiddleware
"""

from __future__ import annotations

import pytest

from app.core.limiter import limiter

PAYLOAD = {
    "applicant_name": "Rate Limit Test",
    "applicant_email": "ratelimit@test.dev",
    "linkedin_url": "https://www.linkedin.com/in/rate-limit",
    "country": "Peru",
    "locale": "es",
    "answers": [],
    "video_url": "https://loom.com/x",
}


@pytest.fixture(autouse=True)
def _reset_limiter():
    """Cada test arranca con contadores en cero (storage in-memory en tests)."""
    limiter.reset()
    yield
    limiter.reset()


def test_apply_over_limit_returns_429_json(client, monkeypatch):
    # Sin broker en tests: que los .delay() del primer 201 no toquen red.
    from app.modules.applications import router as apps_router

    monkeypatch.setattr(apps_router, "notify_submitted", _NoopTask())
    monkeypatch.setattr(apps_router, "score_application_task", _NoopTask())

    codes = [client.post("/applications", json=PAYLOAD).status_code for _ in range(61)]
    assert codes[0] == 201
    assert set(codes[1:60]) == {200}  # dedup idempotente
    last = client.post("/applications", json=PAYLOAD)
    assert last.status_code == 429
    assert last.headers["content-type"].startswith("application/json")
    assert last.json() == {"detail": "rate_limited"}
    assert last.headers.get("retry-after") == "3600"


def test_unhandled_exception_returns_json_500_with_cors(client):
    """Un crash cualquiera debe salir como JSON 500 CON headers CORS."""
    from app.main import app

    @app.get("/__boom_test")
    def _boom():
        raise RuntimeError("kaput")

    try:
        r = client.get(
            "/__boom_test",
            headers={"Origin": "http://localhost:5173"},
        )
        assert r.status_code == 500
        assert r.json() == {"detail": "internal_error"}
        assert r.headers.get("access-control-allow-origin") == "http://localhost:5173"
    finally:
        app.router.routes[:] = [
            route
            for route in app.router.routes
            if getattr(route, "path", None) != "/__boom_test"
        ]


class _NoopTask:
    def delay(self, *args, **kwargs):
        return None
