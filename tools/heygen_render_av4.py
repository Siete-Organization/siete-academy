"""Renderiza un video con Avatar IV de HeyGen (image-to-video) usando audio externo.

Avatar IV genera el avatar a partir de UNA FOTO (image_key) y lo anima.
La voz es el audio que subimos (ElevenLabs, voz real clonada) -> lip-sync.

Flujo:
  1. sube la foto  -> image_key
  2. sube el audio -> audio_asset_id
  3. POST /v2/video/av4/generate con voz tipo audio
  4. polling de estado + descarga opcional

Uso:
    python tools/heygen_render_av4.py --image <foto.jpg> --audio <voz.mp3> --title "Piloto Nico" --download
"""

from __future__ import annotations

import argparse
import json
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

MIME = {
    ".mp3": "audio/mpeg", ".wav": "audio/wav", ".m4a": "audio/mp4",
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp",
}


def upload_asset(api_key: str, path: Path) -> dict:
    mime = MIME.get(path.suffix.lower())
    if not mime:
        sys.exit(f"Extensión no soportada: {path.suffix}")
    r = httpx.post(
        UPLOAD_URL,
        headers={"X-Api-Key": api_key, "Content-Type": mime},
        content=path.read_bytes(),
        timeout=180,
    )
    r.raise_for_status()
    return r.json().get("data") or {}


def generate_av4(client: httpx.Client, image_key: str, audio_asset_id: str,
                 title: str, test_mode: bool, width: int, height: int,
                 motion: str | None = None) -> httpx.Response:
    payload = {
        "video_title": title,
        "test": test_mode,
        "image_key": image_key,
        "audio_asset_id": audio_asset_id,
        "dimension": {"width": width, "height": height},
    }
    if motion:
        payload["custom_motion_prompt"] = motion
        payload["enhance_custom_motion_prompt"] = True
    return client.post("/v2/video/av4/generate", json=payload)


def poll_status(client: httpx.Client, video_id: str, timeout_s: int = 1200) -> dict:
    start = time.time()
    while True:
        r = client.get("/v1/video_status.get", params={"video_id": video_id})
        r.raise_for_status()
        data = r.json().get("data") or {}
        if data.get("status") in ("completed", "failed"):
            return data
        if time.time() - start > timeout_s:
            return {**data, "status": "timeout"}
        time.sleep(10)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--image", required=True)
    p.add_argument("--audio", required=True)
    p.add_argument("--title", default="Piloto Avatar IV")
    p.add_argument("--test", action="store_true")
    p.add_argument("--width", type=int, default=1080)
    p.add_argument("--height", type=int, default=1920)
    p.add_argument("--motion", default=None, help="custom_motion_prompt para gestos/movimiento")
    p.add_argument("--download", action="store_true")
    args = p.parse_args()

    load_dotenv(REPO_ROOT / ".env")
    api_key = os.environ.get("HEYGEN_API_KEY")
    if not api_key:
        sys.exit("HEYGEN_API_KEY no está en .env")

    image_path = Path(args.image) if Path(args.image).is_absolute() else REPO_ROOT / args.image
    audio_path = Path(args.audio) if Path(args.audio).is_absolute() else REPO_ROOT / args.audio
    for fp in (image_path, audio_path):
        if not fp.exists():
            sys.exit(f"No existe: {fp}")

    print(f">>> Subiendo foto: {image_path.name}")
    img = upload_asset(api_key, image_path)
    print(f"    respuesta upload imagen: {json.dumps(img)[:300]}")
    image_key = img.get("image_key") or img.get("id")

    print(f">>> Subiendo audio: {audio_path.name}")
    aud = upload_asset(api_key, audio_path)
    audio_asset_id = aud.get("id")
    print(f"    audio_asset_id: {audio_asset_id}")

    with httpx.Client(base_url=API_BASE,
                      headers={"X-Api-Key": api_key, "accept": "application/json"},
                      timeout=60) as c:
        print(f">>> av4/generate (test={args.test}) image_key={image_key}")
        r = generate_av4(c, image_key, audio_asset_id, args.title, args.test, args.width, args.height, args.motion)
        print(f"    HTTP {r.status_code}: {r.text[:600]}")
        if r.status_code >= 400:
            return 2
        vid = (r.json().get("data") or {}).get("video_id")
        if not vid:
            print("    No video_id en la respuesta.")
            return 2
        print(f"    video_id: {vid} — polling...")
        status = poll_status(c, vid)
        print(f"    status: {status.get('status')} | duration: {status.get('duration')}")
        url = status.get("video_url")
        print(f"    video_url: {url}")
        if status.get("error"):
            print(f"    error: {status.get('error')}")

        if args.download and url and status.get("status") == "completed":
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
