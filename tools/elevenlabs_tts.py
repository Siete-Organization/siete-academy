"""Genera audio TTS con una voz clonada de ElevenLabs.

La voz es la voz real clonada (Instant Voice Clone). El MP3 resultante se usa
luego como audio externo para el lip-sync del avatar de HeyGen.

Uso:
    python tools/elevenlabs_tts.py --voice-id <id> --text-file <ruta.txt> --out .tmp/voces/nico_piloto.mp3
    python tools/elevenlabs_tts.py --voice-id <id> --text "Hola, soy Nico..." --out salida.mp3
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]
TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"


def tts(api_key: str, voice_id: str, text: str, out: Path, model: str,
        stability: float, similarity: float, style: float,
        dict_id: str | None = None, dict_version: str | None = None,
        seed: int | None = None) -> None:
    payload = {
        "text": text,
        "model_id": model,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity,
            "style": style,
            "use_speaker_boost": True,
        },
    }
    if seed is not None:
        payload["seed"] = seed
    if dict_id:
        loc = {"pronunciation_dictionary_id": dict_id}
        if dict_version:
            loc["version_id"] = dict_version
        payload["pronunciation_dictionary_locators"] = [loc]
    r = httpx.post(
        TTS_URL.format(voice_id=voice_id),
        headers={"xi-api-key": api_key, "Content-Type": "application/json", "accept": "audio/mpeg"},
        json=payload,
        timeout=180,
    )
    if r.status_code >= 400:
        raise RuntimeError(f"tts {r.status_code}: {r.text[:500]}")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(r.content)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--voice-id", required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--text")
    g.add_argument("--text-file")
    p.add_argument("--out", required=True)
    p.add_argument("--model", default="eleven_multilingual_v2")
    p.add_argument("--stability", type=float, default=0.5)
    p.add_argument("--similarity", type=float, default=0.85)
    p.add_argument("--style", type=float, default=0.0)
    p.add_argument("--dict-id", default=None)
    p.add_argument("--dict-version", default=None)
    p.add_argument("--seed", type=int, default=None)
    args = p.parse_args()

    load_dotenv(REPO_ROOT / ".env")
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        sys.exit("ELEVENLABS_API_KEY no está en .env")

    if args.text_file:
        text = Path(args.text_file).read_text(encoding="utf-8").strip()
    else:
        text = args.text

    out = Path(args.out)
    if not out.is_absolute():
        out = REPO_ROOT / out

    print(f">>> TTS voice={args.voice_id} model={args.model} chars={len(text)}")
    tts(api_key, args.voice_id, text, out, args.model, args.stability, args.similarity, args.style,
        args.dict_id, args.dict_version, args.seed)
    print(f"    OK -> {out.relative_to(REPO_ROOT)} ({round(out.stat().st_size/1024,1)} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
