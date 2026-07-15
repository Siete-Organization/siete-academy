"""Clona una voz (Instant Voice Clone) en ElevenLabs desde audio de referencia.

Sube uno o más archivos de audio y crea una voz nueva. Devuelve el voice_id.

Uso:
    python tools/elevenlabs_clone.py --name "Nico v2" --files .tmp/voces/nico_voz_limpio.wav
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]
ADD_URL = "https://api.elevenlabs.io/v1/voices/add"


def clone(api_key: str, name: str, files: list[Path], remove_noise: bool) -> dict:
    data = {"name": name, "remove_background_noise": str(remove_noise).lower()}
    file_handles = [("files", (f.name, f.read_bytes(), "audio/wav")) for f in files]
    r = httpx.post(
        ADD_URL,
        headers={"xi-api-key": api_key},
        data=data,
        files=file_handles,
        timeout=300,
    )
    if r.status_code >= 400:
        raise RuntimeError(f"clone {r.status_code}: {r.text[:500]}")
    return r.json()


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--name", required=True)
    p.add_argument("--files", nargs="+", required=True)
    p.add_argument("--no-denoise", action="store_true", help="no aplicar remove_background_noise")
    args = p.parse_args()

    load_dotenv(REPO_ROOT / ".env")
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        sys.exit("ELEVENLABS_API_KEY no está en .env")

    files = []
    for f in args.files:
        fp = Path(f) if Path(f).is_absolute() else REPO_ROOT / f
        if not fp.exists():
            sys.exit(f"No existe: {fp}")
        files.append(fp)

    print(f">>> Clonando '{args.name}' desde {len(files)} archivo(s), denoise={not args.no_denoise}")
    res = clone(api_key, args.name, files, remove_noise=not args.no_denoise)
    print(f"    voice_id: {res.get('voice_id')}")
    print(f"    respuesta: {res}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
