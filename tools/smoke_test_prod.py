"""Smoke test funcional contra producción.

Verifica el contrato observable del deployment desde fuera de la red:
  - /health responde
  - CORS preflight para el frontend funciona
  - GET sin auth devuelve 401 CON header CORS
  - Origen no permitido NO recibe header CORS

Útil para distinguir "el código está roto" vs "el browser del usuario tiene
caché vieja / hay un proxy/CF en medio". Si este script pasa, el problema
está fuera del servidor.

Uso:
    python tools/smoke_test_prod.py
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Callable

import httpx

API = "https://api-academy.wearesiete.com"
FRONTEND_ORIGIN = "https://siete-academy.wearesiete.com"
EVIL_ORIGIN = "https://evil.example.com"


@dataclass
class Check:
    name: str
    fn: Callable[[], None]


def must(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def check_health() -> None:
    r = httpx.get(f"{API}/health", timeout=10)
    must(r.status_code == 200, f"/health status={r.status_code}, body={r.text!r}")
    body = r.json()
    must(body.get("status") == "ok", f"/health body={body}")


def check_preflight_allowed() -> None:
    r = httpx.options(
        f"{API}/auth/me",
        headers={
            "Origin": FRONTEND_ORIGIN,
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "authorization,content-type,x-request-id",
        },
        timeout=10,
    )
    must(r.status_code == 200, f"preflight status={r.status_code}")
    aco = r.headers.get("access-control-allow-origin")
    must(
        aco == FRONTEND_ORIGIN,
        f"preflight ACAO esperaba '{FRONTEND_ORIGIN}', got '{aco}'. "
        f"ALLOWED_ORIGINS en Coolify probablemente no incluye el dominio del frontend.",
    )
    acc = r.headers.get("access-control-allow-credentials")
    must(acc == "true", f"preflight ACAC esperaba 'true', got '{acc}'")
    allow_headers = (r.headers.get("access-control-allow-headers") or "").lower()
    for h in ("authorization", "content-type", "x-request-id"):
        must(h in allow_headers, f"preflight Allow-Headers no incluye {h}: {allow_headers!r}")
    allow_methods = (r.headers.get("access-control-allow-methods") or "").upper()
    for m in ("GET", "POST", "OPTIONS"):
        must(m in allow_methods, f"preflight Allow-Methods no incluye {m}: {allow_methods!r}")


def check_get_without_auth_returns_401_with_cors() -> None:
    r = httpx.get(
        f"{API}/auth/me",
        headers={"Origin": FRONTEND_ORIGIN},
        timeout=10,
    )
    must(
        r.status_code == 401,
        f"GET /auth/me sin auth: esperaba 401, got {r.status_code}, body={r.text[:200]!r}",
    )
    aco = r.headers.get("access-control-allow-origin")
    must(
        aco == FRONTEND_ORIGIN,
        f"GET ACAO ausente o incorrecto: '{aco}'. Aún en respuesta 401 debe estar.",
    )


def check_evil_origin_gets_no_cors_header() -> None:
    r = httpx.get(
        f"{API}/auth/me",
        headers={"Origin": EVIL_ORIGIN},
        timeout=10,
    )
    aco = r.headers.get("access-control-allow-origin")
    must(
        aco != EVIL_ORIGIN,
        f"Vulnerabilidad: origen no autorizado recibió ACAO='{aco}'",
    )


def check_path_without_prefix() -> None:
    """Verifica que la API está montada en raíz (Topology A), no bajo /api/academy."""
    r = httpx.get(f"{API}/api/academy/auth/me", timeout=10)
    must(
        r.status_code == 404,
        f"Si /api/academy/auth/me NO devuelve 404, hay un strip-prefix raro. "
        f"got status={r.status_code}",
    )


CHECKS: list[Check] = [
    Check("health endpoint responde", check_health),
    Check("preflight CORS para frontend funciona", check_preflight_allowed),
    Check("GET sin auth devuelve 401 con header CORS", check_get_without_auth_returns_401_with_cors),
    Check("origen no autorizado NO recibe header CORS", check_evil_origin_gets_no_cors_header),
    Check("ruta /api/academy/* devuelve 404 (sin prefix)", check_path_without_prefix),
]


def main() -> int:
    failed = 0
    print(f"Smoke test contra {API}")
    print(f"Origen frontend: {FRONTEND_ORIGIN}\n")
    for c in CHECKS:
        try:
            c.fn()
            print(f"  PASS  {c.name}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL  {c.name}\n        {e}")
        except httpx.HTTPError as e:
            failed += 1
            print(f"  FAIL  {c.name}\n        Network: {e}")
    print()
    if failed:
        print(f"{failed}/{len(CHECKS)} checks fallaron.")
        return 1
    print(f"Todos los {len(CHECKS)} checks pasaron. El deployment cumple el contrato.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
