"""Genera la spec de slides de un video (para build_slides.py) automáticamente.

Empareja los segmentos 'slide' del .json de narración con los headers de BLOQUE del
.md (que conservan mayúsculas/minúsculas y siglas correctas) y toma la primera marca
[SLIDE: ...] de cada bloque como subtítulo. Así los slides escalan a los 24 videos sin
escribirlos a mano; después se pueden retocar las placas 'hero' manualmente.

Salida: .tmp/slides_specs/<sem>_<video>.json

Uso:
    python tools/gen_slide_specs.py guiones_videos/v2/sem05/contenido_1.md
    python tools/gen_slide_specs.py guiones_videos/v2/sem0*/contenido_*.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
NARR_ROOT = REPO_ROOT / ".tmp" / "narracion"
OUT_ROOT = REPO_ROOT / ".tmp" / "slides_specs"

BLOCK_RE = re.compile(r"^#{1,6}\s*\[?\s*(BLOQUE\s+\d+)\s*[—\-]\s*(.+?)\s*(?:~[^\]]*)?\]?\s*$")
SLIDE_RE = re.compile(r"\[SLIDE:\s*(.+?)\s*\]")


def parse_blocks(md_path: Path) -> list[dict]:
    """Bloques en orden del .md: kicker (BLOQUE N), título (case original), 1er hint SLIDE."""
    blocks: list[dict] = []
    cur = None
    for line in md_path.read_text(encoding="utf-8").splitlines():
        m = BLOCK_RE.match(line.strip())
        if m:
            cur = {"kicker": m.group(1).upper(), "title": m.group(2).strip(), "subtitle": None}
            blocks.append(cur)
            continue
        if cur and cur["subtitle"] is None:
            hint = SLIDE_RE.search(line)
            if hint:
                cur["subtitle"] = hint.group(1).strip()
    return blocks


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("mds", nargs="+")
    args = p.parse_args()
    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    for f in args.mds:
        md = Path(f) if Path(f).is_absolute() else REPO_ROOT / f
        sem = md.parent.name
        narr = NARR_ROOT / sem / f"{md.stem}.json"
        if not narr.exists():
            print(f"! sin narración: {narr.relative_to(REPO_ROOT)} (corré prep_narration antes)")
            continue
        data = json.loads(narr.read_text(encoding="utf-8"))
        slide_idx = [i for i, s in enumerate(data["segments"]) if s["mode"] == "slide"]
        blocks = parse_blocks(md)
        if len(blocks) != len(slide_idx):
            print(f"⚠ {sem}/{md.stem}: {len(blocks)} bloques vs {len(slide_idx)} segmentos slide "
                  f"(uso el mínimo, revisar)")
        spec = []
        for i, b in zip(slide_idx, blocks):
            spec.append({"file": f"{i:02d}_slide", "kicker": b["kicker"], "title": b["title"],
                         "subtitle": b["subtitle"], "stat": None})
        out = OUT_ROOT / f"{sem}_{md.stem}.json"
        out.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{sem}/{md.stem}: {len(spec)} slides -> {out.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
