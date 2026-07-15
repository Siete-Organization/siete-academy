"""Genera el audio TTS de un video por SEGMENTOS, desde el .json de prep_narration.

Por cada segmento del .json crea un mp3 (avatar/slide), y arma un mp3 concatenado
del video completo para revisar (QA). La voz/settings se pasan por CLI.

Salida: .tmp/audio/<carpeta>/<video>/NN_MODE.mp3  +  <video>_full.mp3

Uso:
    python tools/gen_segment_audio.py .tmp/narracion/sem01/contenido_1.json \
        --voice-id RC0M8aafizdHe00eJBM7 --stability 0.45 --similarity 0.90 --style 0.15 --seed 7777
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from elevenlabs_tts import tts  # noqa: E402

from dotenv import load_dotenv  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = REPO_ROOT / ".tmp" / "audio"


def find_ffmpeg() -> str | None:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    base = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Packages"
    hits = list(base.glob("Gyan.FFmpeg_*/ffmpeg-*/bin/ffmpeg.exe"))
    return str(hits[0]) if hits else None


def concat(ffmpeg: str, parts: list[Path], out: Path) -> None:
    listfile = out.with_suffix(".txt")
    listfile.write_text("".join(f"file '{p.as_posix()}'\n" for p in parts), encoding="utf-8")
    subprocess.run([ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(listfile),
                    "-c", "copy", str(out)],
                   check=True, capture_output=True)
    listfile.unlink(missing_ok=True)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("jsons", nargs="+")
    p.add_argument("--voice-id", required=True)
    p.add_argument("--model", default="eleven_multilingual_v2")
    p.add_argument("--stability", type=float, default=0.45)
    p.add_argument("--similarity", type=float, default=0.90)
    p.add_argument("--style", type=float, default=0.15)
    p.add_argument("--seed", type=int, default=7777)
    args = p.parse_args()

    load_dotenv(REPO_ROOT / ".env")
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        sys.exit("ELEVENLABS_API_KEY no está en .env")
    ffmpeg = find_ffmpeg()

    for jf in args.jsons:
        jp = Path(jf) if Path(jf).is_absolute() else REPO_ROOT / jf
        data = json.loads(jp.read_text(encoding="utf-8"))
        carpeta = jp.parent.name
        stem = jp.stem
        out_dir = OUT_ROOT / carpeta / stem
        out_dir.mkdir(parents=True, exist_ok=True)

        parts: list[Path] = []
        for i, seg in enumerate(data["segments"]):
            name = f"{i:02d}_{seg['mode']}.mp3"
            dst = out_dir / name
            tts(api_key, args.voice_id, seg["tts_text"], dst, args.model,
                args.stability, args.similarity, args.style, seed=args.seed)
            parts.append(dst)
            print(f"  {carpeta}/{stem}/{name}  ({len(seg['tts_text'])} car · {seg['segment'][:40]})")

        if ffmpeg and parts:
            full = OUT_ROOT / carpeta / f"{stem}_full.mp3"
            concat(ffmpeg, parts, full)
            print(f">>> {carpeta}/{stem}: {len(parts)} segmentos · QA -> {full.relative_to(REPO_ROOT)}")
        else:
            print(f">>> {carpeta}/{stem}: {len(parts)} segmentos (sin concat: ffmpeg no hallado)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
