"""HTTP middleware: request-id propagation + access logging + catch-all 500."""

from __future__ import annotations

import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.core.logging import bind_request_id, clear_context, get_logger

log = get_logger("http")


class CatchAllExceptionMiddleware(BaseHTTPMiddleware):
    """Convierte excepciones no manejadas en un 500 JSON que SÍ atraviesa
    CORSMiddleware (debe agregarse ANTES que CORS para quedar más adentro).

    Sin esto, un crash llega al ServerErrorMiddleware de Starlette (afuera de
    CORS) y responde `Internal Server Error` en texto plano SIN headers CORS:
    el navegador lo bloquea y el usuario ve un error de red inexplicable.
    """

    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception:
            log.exception(
                "http.unhandled_exception",
                extra={"method": request.method, "path": request.url.path},
            )
            return JSONResponse({"detail": "internal_error"}, status_code=500)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Reads X-Request-ID from the incoming request or mints a new one.

    Stores it in a ContextVar so every log line emitted during the request
    is automatically correlated.
    """

    async def dispatch(self, request: Request, call_next):
        incoming = request.headers.get("x-request-id")
        rid = incoming or uuid.uuid4().hex[:16]
        bind_request_id(rid)

        started = time.monotonic()
        status_code = 500
        try:
            response: Response = await call_next(request)
            status_code = response.status_code
            response.headers["x-request-id"] = rid
            return response
        finally:
            duration_ms = int((time.monotonic() - started) * 1000)
            # Skip the extreme chatter of health/docs, but log everything else
            path = request.url.path
            if path not in {"/health", "/metrics"} and not path.startswith(
                ("/docs", "/openapi", "/redoc")
            ):
                log.info(
                    "http.request",
                    extra={
                        "method": request.method,
                        "path": path,
                        "query": str(request.url.query) or None,
                        "status": status_code,
                        "duration_ms": duration_ms,
                        "client": request.client.host if request.client else None,
                    },
                )
            clear_context()
