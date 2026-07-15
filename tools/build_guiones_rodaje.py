"""Genera la carpeta `guiones/` con los 24 guiones de rodaje para presentador humano.

Convierte los .md de producción (guiones_videos/v2/semXX/{intro,contenido_1,contenido_2}.md)
en guiones claros para UNA PERSONA que graba a cámara:
  - segmentos marcados A CÁMARA vs VOZ EN OFF (slide en pantalla)
  - indicaciones [SLIDE: ...] y [Pausa] conservadas como acotaciones
  - guía de pronunciación de siglas y notas de ritmo
  - organizado por módulo / semana / número de video + índice general

Uso:
    python tools/build_guiones_rodaje.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "guiones_videos" / "v2"
OUT_ROOT = REPO_ROOT / "guiones"

# módulo -> semanas (estructura del curso: 4 módulos x 2 semanas x 3 videos = 24)
MODULO_DE_SEMANA = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4}
VIDEOS = [("intro", 1), ("contenido_1", 2), ("contenido_2", 3)]

PRONUNCIACION = [
    ("B2B", "bi tu bi (no «be dos be»)"),
    ("B2C", "bi tu ci"),
    ("SDR", "es di ar"),
    ("AE", "ei i"),
    ("MQL / SQL", "eme cu ele / ese cu ele"),
    ("ICP", "i ci pi"),
    ("CRM", "ce ere eme"),
    ("ROI", "roi (como palabra)"),
    ("LOB", "el ou bi"),
    ("CEO", "ci i ou"),
    ("KPI", "ka pi i"),
]


def parse_frontmatter(raw: str) -> dict:
    fm = {}
    if raw.startswith("---"):
        block = raw.split("---", 2)[1]
        for line in block.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip()
    return fm


def parse_segments(raw: str) -> list[dict]:
    """Segmentos con acotaciones ([SLIDE], [Pausa]) CONSERVADAS como indicaciones."""
    if raw.startswith("---"):
        raw = raw.split("---", 2)[-1]
    raw = re.split(r"\n\s*\*\*Fuentes", raw, maxsplit=1)[0]

    segments: list[dict] = []
    cur = None
    for line in raw.splitlines():
        s = line.strip()
        m = re.match(r"^#{2,6}\s*\[\s*([^\]\n]+?)\s*\]\s*$", s)
        if m:
            if cur and cur["lines"]:
                segments.append(cur)
            name = m.group(1)
            tm = re.search(r"~\s*([\d:s]+)", name)
            clean = re.sub(r"\s*~.*$", "", name).strip()
            cur = {"name": clean, "time": tm.group(1) if tm else None,
                   "mode": "slide" if clean.upper().startswith("BLOQUE") else "avatar",
                   "lines": []}
            continue
        if cur is None:
            if s and not s.startswith("#"):
                cur = {"name": "APERTURA", "time": None, "mode": "avatar", "lines": [s]}
            continue
        if s.startswith("#") or s == "---":
            continue
        if s.startswith("**[SLIDE") or s.startswith("[SLIDE"):
            txt = re.sub(r"^\**\[SLIDE:?\s*", "", s).rstrip("*]").strip()
            cur["lines"].append(f"> 🖼️ **EN PANTALLA — SLIDE:** {txt}")
            continue
        pm = re.match(r"^\*?\[\s*(Pausa[^\]]*)\]\*?$", s, re.IGNORECASE)
        if pm:
            cur["lines"].append(f"> ⏸️ **{pm.group(1).strip()}**")
            continue
        cur["lines"].append(line.rstrip())
    if cur and cur["lines"]:
        segments.append(cur)
    return segments


def render_video(fm: dict, segments: list[dict], modulo: int, semana: int,
                 n_video: int, global_n: int) -> str:
    titulo = fm.get("titulo", fm.get("video", ""))
    dur = fm.get("duracion_estimada", "—")
    tipo = {1: "Intro de la semana", 2: "Contenido 1", 3: "Contenido 2"}[n_video]

    out = [
        f"# Video {global_n:02d} · Módulo {modulo} · Semana {semana} · Video {n_video} — {tipo}",
        "",
        f"**Título:** {titulo}",
        f"**Duración objetivo:** {dur}",
        "",
        "| Marca | Qué significa |",
        "| --- | --- |",
        "| 🎥 A CÁMARA | Hablas mirando a cámara (tú en pantalla) |",
        "| 🎙️ VOZ EN OFF | Solo se oye tu voz; el alumno ve la slide |",
        "| 🖼️ EN PANTALLA | Qué slide/gráfico entra en ese momento |",
        "| ⏸️ Pausa | Silencio breve intencional (no lo leas) |",
        "",
        "---",
        "",
    ]
    for seg in segments:
        icon = "🎥 A CÁMARA" if seg["mode"] == "avatar" else "🎙️ VOZ EN OFF (slide en pantalla)"
        tm = f" · ~{seg['time']}" if seg["time"] else ""
        out.append(f"## {seg['name']}  —  {icon}{tm}")
        out.append("")
        body = "\n".join(seg["lines"])
        body = re.sub(r"\n{3,}", "\n\n", body).strip()
        out.append(body)
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    if not SRC_ROOT.exists():
        sys.exit(f"No existe {SRC_ROOT}")
    OUT_ROOT.mkdir(exist_ok=True)

    index_rows = []
    global_n = 0
    for semana in range(1, 9):
        modulo = MODULO_DE_SEMANA[semana]
        src_dir = SRC_ROOT / f"sem{semana:02d}"
        for stem, n_video in VIDEOS:
            global_n += 1
            src = src_dir / f"{stem}.md"
            if not src.exists():
                print(f"!! FALTA {src.relative_to(REPO_ROOT)}")
                continue
            raw = src.read_text(encoding="utf-8")
            fm = parse_frontmatter(raw)
            segments = parse_segments(raw)
            out_dir = OUT_ROOT / f"modulo_{modulo}" / f"semana_{semana}"
            out_dir.mkdir(parents=True, exist_ok=True)
            dst = out_dir / f"video_{n_video}_{stem}.md"
            dst.write_text(render_video(fm, segments, modulo, semana, n_video, global_n),
                           encoding="utf-8")
            n_cam = sum(1 for s in segments if s["mode"] == "avatar")
            n_off = sum(1 for s in segments if s["mode"] == "slide")
            index_rows.append((global_n, modulo, semana, n_video, fm.get("titulo", stem),
                               fm.get("duracion_estimada", "—"),
                               dst.relative_to(OUT_ROOT).as_posix(), n_cam, n_off))
            print(f"OK {dst.relative_to(REPO_ROOT)}  ({n_cam} a cámara / {n_off} en off)")

    # índice general
    idx = [
        "# Guiones de rodaje — SDR Academy Siete (24 videos)",
        "",
        "Guion por video para la persona que graba. Estructura del curso: **4 módulos ×",
        "2 semanas × 3 videos** (intro + contenido 1 + contenido 2).",
        "",
        "## Cómo leer cada guion",
        "",
        "- **🎥 A CÁMARA**: hablas mirando a cámara. **🎙️ VOZ EN OFF**: se graba solo audio,",
        "  el alumno ve la slide indicada en 🖼️.",
        "- **⏸️ Pausa**: silencio intencional (~1s). No se lee en voz alta.",
        "- Las **negritas** marcan énfasis al hablar, no gritos.",
        "- Ritmo: velocidad natural, sin apurar. En listas numeradas (\"Uno… Dos…\") deja",
        "  ~medio segundo entre ítems. Antes de revelar la respuesta de un ejercicio, ~1s.",
        "- Tono Siete: cercano y directo (se tutea al alumno), pero prolijo. Académico",
        "  relajado, nunca acartonado.",
        "",
        "## Pronunciación de siglas (LATAM)",
        "",
        "| Sigla | Se dice |",
        "| --- | --- |",
    ]
    idx += [f"| {a} | {b} |" for a, b in PRONUNCIACION]
    idx += ["", "## Los 24 videos", ""]
    idx += ["| # | Módulo | Semana | Video | Título | Duración | Archivo |",
            "| --- | --- | --- | --- | --- | --- | --- |"]
    for g, mo, se, nv, tit, dur, rel, _, _ in index_rows:
        idx.append(f"| {g:02d} | {mo} | {se} | {nv} | {tit} | {dur} | [{rel}]({rel}) |")
    (OUT_ROOT / "00_INDICE.md").write_text("\n".join(idx) + "\n", encoding="utf-8")
    print(f"\n>>> {len(index_rows)} guiones + 00_INDICE.md en {OUT_ROOT.relative_to(REPO_ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
