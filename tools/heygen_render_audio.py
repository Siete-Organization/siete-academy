"""Renderiza un video de HeyGen con avatar en modo audio-driven (lip-sync a un audio externo).

Sube un archivo de audio (p.ej. el MP3 generado por ElevenLabs con la voz real clonada)
como asset a HeyGen, luego genera el video con el avatar sincronizando labios a ESE audio.
HeyGen solo pone la cara; la voz es 100% del audio que subimos.

Uso:
    # test (gratis, marca de agua) — para validar lip-sync
    python tools/heygen_render_audio.py --avatar-id <id> --audio <ruta.mp3> --title "Prueba Nico" --test

    # producción (consume créditos del pool API)
    python tools/heygen_render_audio.py --avatar-id <id> --audio <ruta.mp3> --title "Prueba Nico"

Output: imprime video_id, status y video_url. Descarga el mp4 a .tmp/videos_prueba/ si --download.
"""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]
API_BASE = "https://api.heygen.com"
UPLOAD_URL = "https://upload.heygen.com/v1/asset"
OUT_DIR = REPO_ROOT / ".tmp" / "videos_prueba"

MIME = {".mp3": "audio/mpeg", ".wav": "audio/wav", ".m4a": "audio/mp4", ".aac": "audio/aac"}


def upload_audio(api_key: str, audio_path: Path) -> str:
    mime = MIME.get(audio_path.suffix.lower())
    if not mime:
        sys.exit(f"Extensión de audio no soportada: {audio_path.suffix}")
    data = audio_path.read_bytes()
    r = httpx.post(
        UPLOAD_URL,
        headers={"X-Api-Key": api_key, "Content-Type": mime},
        content=data,
        timeout=120,
    )
    r.raise_for_status()
    j = r.json()
    asset_id = (j.get("data") or {}).get("id")
    if not asset_id:
        raise RuntimeError(f"No asset id en respuesta de upload: {r.text[:300]}")
    return asset_id


def generate_video(
    client: httpx.Client,
    avatar_id: str,
    audio_asset_id: str,
    title: str,
    test_mode: bool,
    width: int,
    height: int,
    bg: str,
    talking_photo: bool = False,
) -> str:
    if talking_photo:
        # Photo Avatar (Avatar IV): el fondo de oficina YA viene en el look generado,
        # así que NO mandamos 'background' (lo dejaría plano o recortaría la escena).
        character = {"type": "talking_photo", "talking_photo_id": avatar_id}
        scene = {"character": character,
                 "voice": {"type": "audio", "audio_asset_id": audio_asset_id}}
    else:
        scene = {
            "character": {"type": "avatar", "avatar_id": avatar_id, "avatar_style": "normal"},
            "voice": {"type": "audio", "audio_asset_id": audio_asset_id},
            "background": {"type": "color", "value": bg},
        }
    payload = {
        "title": title,
        "test": test_mode,
        "dimension": {"width": width, "height": height},
        "video_inputs": [scene],
    }
    r = client.post("/v2/video/generate", json=payload)
    if r.status_code >= 400:
        raise RuntimeError(f"generate {r.status_code}: {r.text[:500]}")
    data = r.json().get("data") or {}
    vid = data.get("video_id")
    if not vid:
        raise RuntimeError(f"No video_id en respuesta: {r.text[:300]}")
    return vid


def poll_status(client: httpx.Client, video_id: str, timeout_s: int = 1200) -> dict:
    start = time.time()
    while True:
        r = client.get("/v1/video_status.get", params={"video_id": video_id})
        r.raise_for_status()
        data = r.json().get("data") or {}
        status = data.get("status")
        if status in ("completed", "failed"):
            return data
        if time.time() - start > timeout_s:
            return {**data, "status": "timeout"}
        time.sleep(10)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--avatar-id", required=True, help="avatar_id, o look_id de Photo Avatar con --talking-photo")
    p.add_argument("--talking-photo", action="store_true", help="el id es un look de Photo Avatar (fondo ya incluido)")
    p.add_argument("--audio", required=True, help="Ruta al archivo de audio (mp3/wav)")
    p.add_argument("--title", default="Prueba avatar audio-driven")
    p.add_argument("--test", action="store_true", help="Modo test gratis (marca de agua)")
    p.add_argument("--width", type=int, default=1920)
    p.add_argument("--height", type=int, default=1080)
    p.add_argument("--bg", default="#FFFFFF")
    p.add_argument("--download", action="store_true", help="Descargar el mp4 al terminar")
    args = p.parse_args()

    load_dotenv(REPO_ROOT / ".env")
    api_key = os.environ.get("HEYGEN_API_KEY")
    if not api_key:
        sys.exit("HEYGEN_API_KEY no está en .env")

    audio_path = Path(args.audio)
    if not audio_path.is_absolute():
        audio_path = REPO_ROOT / audio_path
    if not audio_path.exists():
        sys.exit(f"No existe el audio: {audio_path}")

    print(f">>> Subiendo audio: {audio_path.name}")
    asset_id = upload_audio(api_key, audio_path)
    print(f"    audio_asset_id: {asset_id}")

    with httpx.Client(
        base_url=API_BASE,
        headers={"X-Api-Key": api_key, "accept": "application/json"},
        timeout=60,
    ) as c:
        print(f">>> Generando video (test={args.test}) avatar={args.avatar_id}")
        video_id = generate_video(
            c, args.avatar_id, asset_id, args.title, args.test, args.width, args.height, args.bg,
            talking_photo=args.talking_photo,
        )
        print(f"    video_id: {video_id} — polling cada 10s...")
        status = poll_status(c, video_id)
        st = status.get("status")
        url = status.get("video_url")
        print(f"    status: {st}")
        print(f"    duration: {status.get('duration')}")
        print(f"    video_url: {url}")
        if status.get("error"):
            print(f"    error: {status.get('error')}")

        if args.download and url and st == "completed":
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in args.title)
            dst = OUT_DIR / f"{safe}.mp4"
            print(f">>> Descargando a {dst.relative_to(REPO_ROOT)}")
            with httpx.stream("GET", url, timeout=300) as resp:
                resp.raise_for_status()
                with open(dst, "wb") as f:
                    for chunk in resp.iter_bytes():
                        f.write(chunk)
            print(f"    OK ({round(dst.stat().st_size/1024/1024,2)} MB)")

    return 0 if status.get("status") == "completed" else 1


if __name__ == "__main__":
    sys.exit(main())
