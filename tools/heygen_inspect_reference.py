"""Inspecciona un video existente en HeyGen y exporta sus parámetros
(avatar_id, voice_id, dimensión, etc.) para reutilizarlos al generar
los videos del curso sin armar brandbook desde cero.

Endpoints usados:
  - GET /v1/video_status.get?video_id=<id> -> metadata del video
  - GET /v2/avatars (fallback si el status no devuelve avatar_id)
  - GET /v2/voices (fallback si el status no devuelve voice_id)

Requiere HEYGEN_API_KEY en el entorno (o en .env del repo root).

Uso:
    python tools/heygen_inspect_reference.py <video_id>
    # ej:
    python tools/heygen_inspect_reference.py 7e21a035510b45c2870ec540e4f0be52

Output: .tmp/heygen_reference.json
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_PATH = REPO_ROOT / ".tmp" / "heygen_reference.json"

API_BASE = "https://api.heygen.com"


def _get_api_key() -> str:
    load_dotenv(REPO_ROOT / ".env")
    key = os.environ.get("HEYGEN_API_KEY")
    if not key:
        sys.exit(
            "HEYGEN_API_KEY no está en el entorno ni en .env del repo root. "
            "Setealo y reintenta."
        )
    return key


def _client(api_key: str) -> httpx.Client:
    return httpx.Client(
        base_url=API_BASE,
        headers={"X-Api-Key": api_key, "accept": "application/json"},
        timeout=30,
    )


def inspect_video(client: httpx.Client, video_id: str) -> dict:
    r = client.get("/v1/video_status.get", params={"video_id": video_id})
    r.raise_for_status()
    return r.json()


def list_avatars(client: httpx.Client) -> dict:
    r = client.get("/v2/avatars")
    r.raise_for_status()
    return r.json()


def list_voices(client: httpx.Client) -> dict:
    r = client.get("/v2/voices")
    r.raise_for_status()
    return r.json()


def main() -> int:
    if len(sys.argv) != 2:
        sys.exit("Uso: python tools/heygen_inspect_reference.py <video_id>")
    video_id = sys.argv[1].strip()

    api_key = _get_api_key()
    with _client(api_key) as c:
        status_data = inspect_video(c, video_id)
        avatars = list_avatars(c)
        voices = list_voices(c)

    payload = {
        "video_id": video_id,
        "video_status": status_data,
        "avatars": avatars,
        "voices": voices,
    }
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK guardado en {OUT_PATH.relative_to(REPO_ROOT)}")
    print(f"  video_status keys: {list(status_data.get('data', {}).keys()) if isinstance(status_data.get('data'), dict) else 'n/a'}")
    avatars_count = len((avatars.get("data") or {}).get("avatars", []) if isinstance(avatars.get("data"), dict) else (avatars.get("data") or []))
    voices_count = len((voices.get("data") or {}).get("voices", []) if isinstance(voices.get("data"), dict) else (voices.get("data") or []))
    print(f"  avatars listados: {avatars_count}")
    print(f"  voices listados: {voices_count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
