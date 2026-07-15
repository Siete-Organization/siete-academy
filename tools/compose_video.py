"""Compone el video final de un tramo del curso (formato 'presentador por tramos').

Arma la línea de tiempo a partir del .json de narración (prep_narration) + el audio por
segmento (gen_segment_audio) + las slides (build_slides) + los clips de avatar (HeyGen
Avatar IV). Por cada segmento construye un clip de la duración exacta de su audio:
  - mode 'avatar' -> usa el clip de avatar del grupo (avatar IV trae su propio audio).
  - mode 'slide'  -> slide PNG (o un b-roll si se override) + el audio de voz en off.
Los segmentos 'avatar' consecutivos comparten UN clip de avatar (avatarA, avatarB, ...).

Subtítulos: opcional (--subs), quemados con libass desde el sub_text de cada segmento.

Salida: .tmp/videos_prueba/<out>.mp4

Uso:
    python tools/compose_video.py .tmp/narracion/sem01/contenido_1.json \
        --audio-dir .tmp/audio/sem01/contenido_1 \
        --slides-dir .tmp/slides/sem01_contenido_1 \
        --avatar avatarA=.tmp/videos_prueba/avA.mp4 --avatar avatarB=.tmp/videos_prueba/avB.mp4 \
        --broll 2=.tmp/broll/comite_reunion/6951601.mp4 \
        --out PATRON_sem01_contenido_1 --subs
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / ".tmp" / "videos_prueba"
WORK = REPO_ROOT / ".tmp" / "_compose"
W, H = 1920, 1080


def find_bin(name: str) -> str:
    exe = shutil.which(name)
    if exe:
        return exe
    base = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Packages"
    hits = list(base.glob(f"Gyan.FFmpeg_*/ffmpeg-*/bin/{name}.exe"))
    if not hits:
        sys.exit(f"No encuentro {name}. Instalá ffmpeg.")
    return str(hits[0])


def dur(ffprobe: str, path: Path) -> float:
    out = subprocess.run([ffprobe, "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
                         capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def ass_escape(t: str) -> str:
    return t.replace("\\", "\\\\").replace("{", "(").replace("}", ")").replace("\n", " ")


def write_ass(path: Path, cues: list[tuple[float, float, str]]) -> None:
    """ASS con banda inferior: Montserrat-like, blanco, caja negra semitransp."""
    head = (
        "[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\n\n"
        "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, "
        "BackColour, Bold, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV\n"
        "Style: Sub,Montserrat,46,&H00FFFFFF,&H40FF7A00,&H40FF7A00,1,3,3,0,2,120,120,70\n\n"
        "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )

    def ts(s: float) -> str:
        h = int(s // 3600); m = int(s % 3600 // 60); sec = s % 60
        return f"{h:d}:{m:02d}:{sec:05.2f}"

    lines = [f"Dialogue: 0,{ts(a)},{ts(b)},Sub,,0,0,0,,{ass_escape(t)}" for a, b, t in cues]
    path.write_text(head + "\n".join(lines) + "\n", encoding="utf-8")


def chunk_subs(text: str, total: float, start: float, maxchars: int = 84) -> list[tuple]:
    """Parte el texto del segmento en cues cortas, repartiendo la duración por longitud."""
    import re
    parts, cur = [], ""
    for piece in re.split(r"(?<=[\.\?\!])\s+", text.strip()):
        if len(cur) + len(piece) + 1 <= maxchars:
            cur = (cur + " " + piece).strip()
        else:
            if cur:
                parts.append(cur)
            cur = piece
    if cur:
        parts.append(cur)
    if not parts:
        return []
    tot_chars = sum(len(p) for p in parts) or 1
    cues, t = [], start
    for p in parts:
        d = total * len(p) / tot_chars
        cues.append((t, t + d, p))
        t += d
    return cues


def build_segment_clip(ffmpeg: str, visual: Path, is_video: bool, audio: Path,
                       d: float, out: Path) -> None:
    """Un clip de duración d: visual (img loop o video) escalado a 1920x1080 + audio."""
    scale = (f"scale={W}:{H}:force_original_aspect_ratio=increase,"
             f"crop={W}:{H},setsar=1,fps=25,format=yuv420p")
    if is_video:
        vin = ["-stream_loop", "-1", "-i", str(visual)]
    else:
        vin = ["-loop", "1", "-i", str(visual)]
    subprocess.run(
        [ffmpeg, "-y", "-loglevel", "error", *vin, "-i", str(audio),
         "-t", f"{d:.3f}", "-vf", scale, "-map", "0:v", "-map", "1:a",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
         "-shortest", str(out)],
        check=True, capture_output=True)


def build_avatar_clip(ffmpeg: str, clip: Path, out: Path) -> None:
    """Tramo de avatar: el Photo Avatar de HeyGen YA viene en 1920x1080 con su fondo de
    oficina y su audio + lip-sync. Solo normalizamos a 1920x1080 y conservamos su audio."""
    scale = (f"scale={W}:{H}:force_original_aspect_ratio=increase,"
             f"crop={W}:{H},setsar=1,fps=25,format=yuv420p")
    subprocess.run(
        [ffmpeg, "-y", "-loglevel", "error", "-i", str(clip), "-vf", scale,
         "-map", "0:v", "-map", "0:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", str(out)],
        check=True, capture_output=True)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("narracion_json")
    p.add_argument("--audio-dir", required=True)
    p.add_argument("--slides-dir", required=True)
    p.add_argument("--avatar", action="append", default=[], help="<idx_segmento>=ruta.mp4 (clip Avatar IV de ese tramo)")
    p.add_argument("--broll", action="append", default=[], help="<idx_segmento>=ruta.mp4 (override de slide)")
    p.add_argument("--out", required=True)
    p.add_argument("--subs", action="store_true")
    args = p.parse_args()

    ffmpeg, ffprobe = find_bin("ffmpeg"), find_bin("ffprobe")
    avatars = {int(k): v for k, v in (a.split("=", 1) for a in args.avatar)}
    brolls = {int(k): v for k, v in (b.split("=", 1) for b in args.broll)}

    data = json.loads(Path(args.narracion_json).read_text(encoding="utf-8"))
    segs = data["segments"]
    audio_dir = REPO_ROOT / args.audio_dir if not Path(args.audio_dir).is_absolute() else Path(args.audio_dir)
    slides_dir = REPO_ROOT / args.slides_dir if not Path(args.slides_dir).is_absolute() else Path(args.slides_dir)

    WORK.mkdir(parents=True, exist_ok=True)
    for f in WORK.glob("*"):
        f.unlink()

    clips, cues, t = [], [], 0.0
    for i, s in enumerate(segs):
        out = WORK / f"seg{i:02d}.mp4"
        if s["mode"] == "avatar":
            av = avatars.get(i)
            if not av:
                sys.exit(f"Falta clip de avatar para el segmento {i}. Pasá --avatar {i}=ruta.mp4")
            clip = Path(av) if Path(av).is_absolute() else REPO_ROOT / av
            d = dur(ffprobe, clip)            # duración real del clip de avatar (su propio audio)
            build_avatar_clip(ffmpeg, clip, out)
        else:
            a = audio_dir / f"{i:02d}_{s['mode']}.mp3"
            d = dur(ffprobe, a)
            visual = (Path(brolls[i]) if Path(brolls[i]).is_absolute() else REPO_ROOT / brolls[i]) \
                if i in brolls else slides_dir / f"{i:02d}_slide.png"
            build_segment_clip(ffmpeg, visual, i in brolls, a, d, out)
        clips.append(out)
        if args.subs:
            cues += chunk_subs(s["sub_text"], d, t)
        t += d
        print(f"  seg{i:02d} {s['mode']:6s} {d:5.1f}s  {s['segment'][:42]}")

    # concat
    listf = WORK / "concat.txt"
    listf.write_text("".join(f"file '{c.as_posix()}'\n" for c in clips), encoding="utf-8")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    raw = WORK / "raw.mp4"
    subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                    "-i", str(listf), "-c", "copy", str(raw)], check=True, capture_output=True)

    final = OUT_DIR / f"{args.out}.mp4"
    if args.subs and cues:
        assf = WORK / "subs.ass"
        write_ass(assf, cues)
        # rutas RELATIVAS a REPO_ROOT: el filtro subtitles de ffmpeg rompe con el ':'
        # de 'C:' en Windows. Corremos con cwd=REPO_ROOT y referimos sin unidad.
        ass_rel = assf.relative_to(REPO_ROOT).as_posix()
        fonts_rel = (Path("tools") / "brand" / "fonts").as_posix()
        vf = f"subtitles={ass_rel}:fontsdir={fonts_rel}"
        subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", str(raw), "-vf", vf,
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                        "-c:a", "copy", str(final)], check=True, capture_output=True, cwd=str(REPO_ROOT))
    else:
        shutil.copy(raw, final)

    print(f"\n>>> {final.relative_to(REPO_ROOT)}  ({round(final.stat().st_size/1024/1024,1)} MB · {t:.1f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
