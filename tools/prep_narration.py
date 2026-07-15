"""Prepara la narración de un guion .md para producción de video.

Por cada video genera, a partir del .md (fuente con estructura):
  - segmentos clasificados en modo 'avatar' (a cámara) o 'slide' (voz en off),
    según los headers `## [GANCHO]`, `## [BLOQUE ...]`, etc.
  - texto-TTS  : narración limpia con SIGLAS REESCRITAS (para ElevenLabs).
  - texto-sub  : narración limpia con siglas ORIGINALES (para subtítulos).

Regla de clasificación: un segmento cuyo header empieza con "BLOQUE" va en modo
'slide'; todo lo demás (gancho, contexto, ejercicio, síntesis, puentes, cierre) va
en modo 'avatar'.

Salida: .tmp/narracion/<carpeta>/<video>.json  + <video>.tts.txt

Uso:
    python tools/prep_narration.py guiones_videos/v2/sem01/contenido_1.md
    python tools/prep_narration.py guiones_videos/v2/sem01/*.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = REPO_ROOT / ".tmp" / "narracion"

# Mapa de pronunciación de siglas (uso real de ventas).
# Confirmadas por el doc de producción; las marcadas (*) son propuestas a validar de oído.
ACRONYMS = {
    "B2B": "bi tu bi",
    "B2C": "bi tu ci",
    "SDR": "es di ar",
    "LOB": "el ou bi",
    "AE": "ei i",
    "MQL": "eme cu ele",
    "SQL": "ese cu ele",
    "ICP": "i ci pi",
    "CRM": "ce ere eme",  # corregido por el equipo (no "ci ar eme")
    "ROI": "roi",         # corregido por el equipo (palabra, no "erre o i")
    "IT": "ai ti",       # (*)
    "CEO": "ci i ou",    # (*)
    "VP": "vi pi",       # (*)
    "PO": "pi ou",       # (*)
    "KPI": "ka pi i",    # (*)
}


def respell(text: str) -> str:
    """Reescribe las siglas conocidas para que el TTS las pronuncie bien."""
    for sig in sorted(ACRONYMS, key=len, reverse=True):
        text = re.sub(rf"\b{re.escape(sig)}\b", ACRONYMS[sig], text)
    return text


def clean_line(line: str) -> str:
    """Quita markdown de énfasis y comillas tipográficas que no aportan al habla."""
    line = re.sub(r"\*\*(.+?)\*\*", r"\1", line)   # **negrita**
    line = re.sub(r"(?<!\*)\*(?!\*)(.+?)\*", r"\1", line)  # *cursiva*
    return line.strip()


def parse(md_path: Path) -> dict:
    raw = md_path.read_text(encoding="utf-8")

    # 1. quitar frontmatter YAML (--- ... ---)
    if raw.startswith("---"):
        raw = raw.split("---", 2)[-1]

    # 2. cortar la sección "Fuentes ..." (no se narra)
    raw = re.split(r"\n\s*\*\*Fuentes", raw, maxsplit=1)[0]

    segments: list[dict] = []
    cur_name = "INTRO"
    cur_mode = "avatar"
    cur_lines: list[str] = []

    def flush():
        if not cur_lines:
            return
        body = "\n\n".join(p for p in "\n".join(cur_lines).split("\n\n") if p.strip())
        body = body.strip()
        if body:
            segments.append({"segment": cur_name, "mode": cur_mode, "sub_text": body})

    for line in raw.splitlines():
        s = line.strip()
        # nuevo segmento: header ## [NOMBRE ...]
        m = re.match(r"^#{1,6}\s*\[?\s*([^\]\n]+?)\s*\]?\s*$", s)
        if m and (s.startswith("#")):
            flush()
            cur_lines = []
            cur_name = re.sub(r"\s*~.*$", "", m.group(1)).strip().upper()
            cur_mode = "slide" if cur_name.startswith("BLOQUE") else "avatar"
            continue
        # descartes
        if not s:
            cur_lines.append("")  # mantiene separación de párrafos
            continue
        if s.startswith("**[SLIDE") or s.startswith("[SLIDE"):
            continue
        if re.match(r"^\*?\[\s*Pausa", s, re.IGNORECASE):
            continue
        if s.startswith("#") or s == "---":
            continue
        cur_lines.append(clean_line(line))

    flush()

    # construir versiones TTS (siglas reescritas) por segmento
    for seg in segments:
        seg["tts_text"] = respell(seg["sub_text"])

    avatar = sum(len(s["tts_text"]) for s in segments if s["mode"] == "avatar")
    slide = sum(len(s["tts_text"]) for s in segments if s["mode"] == "slide")
    return {
        "source": str(md_path.relative_to(REPO_ROOT)),
        "segments": segments,
        "chars_avatar": avatar,
        "chars_slide": slide,
        "chars_total": avatar + slide,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("files", nargs="+")
    args = p.parse_args()

    for f in args.files:
        md = Path(f) if Path(f).is_absolute() else REPO_ROOT / f
        if not md.exists() or md.name.startswith("_") or md.name.startswith("guia"):
            continue
        data = parse(md)
        out_dir = OUT_ROOT / md.parent.name
        out_dir.mkdir(parents=True, exist_ok=True)
        stem = md.stem
        (out_dir / f"{stem}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        full_tts = "\n\n".join(s["tts_text"] for s in data["segments"])
        (out_dir / f"{stem}.tts.txt").write_text(full_tts, encoding="utf-8")
        n_av = sum(1 for s in data["segments"] if s["mode"] == "avatar")
        n_sl = sum(1 for s in data["segments"] if s["mode"] == "slide")
        print(f"{data['source']}: {len(data['segments'])} seg "
              f"({n_av} avatar / {n_sl} slide) · "
              f"{data['chars_total']} car (avatar {data['chars_avatar']} / slide {data['chars_slide']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
