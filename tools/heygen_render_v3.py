"""Renderiza clips de avatar con HeyGen /v3/videos (engines avatar_v / avatar_iv).

A diferencia de heygen_render_av4.py (foto suelta), acá el avatar es un LOOK ya
creado en la cuenta (photo_avatar / digital_twin) referido por --avatar-id.
La voz es audio externo (ElevenLabs) -> lip-sync via audio_asset_id.

Acepta VARIOS audios: sube todos, lanza todos los jobs en paralelo, y hace un
solo loop de polling. Descarga cada clip a .tmp/videos_prueba/<prefix><stem>.mp4

Uso:
    python tools/heygen_render_v3.py --avatar-id 47d59e4737b944b490d286680d01ef60 \
        --engine avatar_v --prefix AV5_s01c1_ \
        .tmp/audio/sem01/contenido_1/00_avatar.mp3 .tmp/audio/sem01/contenido_1/01_avatar.mp3
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

MIME = {".mp3": "audio/mpeg", ".wav": "audio/wav", ".m4a": "audio/mp4"}


def upload_audio(api_key: str, path: Path) -> str:
    mime = MIME.get(path.suffix.lower())
    if not mime:
        sys.exit(f"Extensión no soportada: {path.suffix}")
    r = httpx.post(UPLOAD_URL, headers={"X-Api-Key": api_key, "Content-Type": mime},
                   content=path.read_bytes(), timeout=180)
    r.raise_for_status()
    return (r.json().get("data") or {})["id"]


def submit(client: httpx.Client, avatar_id: str, audio_asset_id: str, engine: str,
           title: str, resolution: str, aspect: str) -> str:
    payload = {
        "type": "avatar",
        "avatar_id": avatar_id,
        "audio_asset_id": audio_asset_id,
        "engine": {"type": engine},
        "resolution": resolution,
        "aspect_ratio": aspect,
        "title": title,
    }
    r = client.post("/v3/videos", json=payload)
    if r.status_code >= 400:
        sys.exit(f"submit {title}: HTTP {r.status_code}: {r.text[:400]}")
    return (r.json().get("data") or {})["video_id"]


def get_status(client: httpx.Client, video_id: str) -> dict:
    r = client.get(f"/v3/videos/{video_id}")
    if r.status_code == 404:  # fallback al endpoint viejo
        r = client.get("/v1/video_status.get", params={"video_id": video_id})
    r.raise_for_status()
    return r.json().get("data") or {}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("audios", nargs="+")
    p.add_argument("--avatar-id", required=True)
    p.add_argument("--engine", default="avatar_v", choices=["avatar_v", "avatar_iv", "avatar_iii"])
    p.add_argument("--resolution", default="1080p", choices=["4k", "1080p", "720p"])
    p.add_argument("--aspect", default="16:9")
    p.add_argument("--prefix", default="V3_", help="prefijo del nombre de salida")
    p.add_argument("--timeout", type=int, default=2400, help="timeout total de polling (s)")
    args = p.parse_args()

    load_dotenv(REPO_ROOT / ".env")
    api_key = os.environ.get("HEYGEN_API_KEY")
    if not api_key:
        sys.exit("HEYGEN_API_KEY no está en .env")

    jobs: list[dict] = []
    with httpx.Client(base_url=API_BASE,
                      headers={"X-Api-Key": api_key, "accept": "application/json"},
                      timeout=60) as c:
        for a in args.audios:
            ap = Path(a) if Path(a).is_absolute() else REPO_ROOT / a
            if not ap.exists():
                sys.exit(f"No existe: {ap}")
            title = f"{args.prefix}{ap.stem}"
            print(f">>> Subiendo {ap.name}...", flush=True)
            asset = upload_audio(api_key, ap)
            vid = submit(c, args.avatar_id, asset, args.engine, title, args.resolution, args.aspect)
            print(f"    {title}: video_id={vid}", flush=True)
            jobs.append({"title": title, "video_id": vid, "done": False})

        start = time.time()
        while not all(j["done"] for j in jobs):
            if time.time() - start > args.timeout:
                print("!!! timeout de polling"); break
            time.sleep(15)
            for j in jobs:
                if j["done"]:
                    continue
                st = get_status(c, j["video_id"])
                status = st.get("status")
                if status in ("completed", "failed"):
                    j["done"] = True
                    j["status"] = status
                    j["url"] = st.get("video_url")
                    j["error"] = st.get("error")
                    print(f"    {j['title']}: {status}", flush=True)

        OUT_DIR.mkdir(parents=True, exist_ok=True)
        fails = 0
        for j in jobs:
            if j.get("status") == "completed" and j.get("url"):
                dst = OUT_DIR / f"{j['title']}.mp4"
                with httpx.stream("GET", j["url"], timeout=300) as resp:
                    resp.raise_for_status()
                    with open(dst, "wb") as f:
                        for chunk in resp.iter_bytes():
                            f.write(chunk)
                print(f"    OK {dst.relative_to(REPO_ROOT)} ({round(dst.stat().st_size/1024/1024,2)} MB)")
            else:
                fails += 1
                print(f"    FAIL {j['title']}: {j.get('status')} {j.get('error')}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
