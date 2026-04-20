"""Direct Anthropic SDK wrapper with full request/response audit.

No abstraction framework (LangChain/LlamaIndex/etc.) per project principles.
Every call is persisted in `ai_call_logs` for traceability.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

from anthropic import Anthropic
from anthropic.types import Message
from sqlalchemy.orm import Session
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import get_settings

log = logging.getLogger(__name__)


class AnthropicClient:
    """Thin wrapper around anthropic.Anthropic that logs every call.

    Use from services like:
        client = AnthropicClient()
        resp = client.messages(db, stage_run_id, messages=[...], system=...)
    """

    def __init__(self) -> None:
        settings = get_settings()
        if not settings.anthropic_api_key:
            log.warning("ANTHROPIC_API_KEY not set — AI features disabled.")
            self._client = None
        else:
            self._client = Anthropic(api_key=settings.anthropic_api_key)
        self._model = settings.anthropic_model

    @property
    def model(self) -> str:
        return self._model

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def messages(
        self,
        db: Session,
        *,
        messages: list[dict[str, Any]],
        system: str | None = None,
        max_tokens: int = 2048,
        temperature: float = 0.3,
        stage_run_id: int | None = None,
        purpose: str = "generic",
    ) -> Message:
        if self._client is None:
            raise RuntimeError("Anthropic client not configured.")

        from app.modules.audit.models import AICallLog

        request_payload = {
            "model": self._model,
            "messages": messages,
            "system": system,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        started = time.monotonic()
        error: str | None = None
        response: Message | None = None
        try:
            response = self._client.messages.create(
                model=self._model,
                messages=messages,
                system=system or "",
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response
        except Exception as e:
            error = f"{type(e).__name__}: {e}"
            raise
        finally:
            duration_ms = int((time.monotonic() - started) * 1000)
            try:
                log_entry = AICallLog(
                    stage_run_id=stage_run_id,
                    purpose=purpose,
                    model=self._model,
                    request_payload=_safe_json(request_payload),
                    response_payload=_safe_json(response.model_dump()) if response else None,
                    duration_ms=duration_ms,
                    error=error,
                )
                db.add(log_entry)
                db.commit()
            except Exception as log_err:
                log.exception("Failed to persist AICallLog: %s", log_err)


def _safe_json(obj: Any) -> dict:
    try:
        return json.loads(json.dumps(obj, default=str))
    except Exception:
        return {"__unserializable__": str(obj)[:500]}
