"""Descarga b-roll (video stock) de Pexels para componer los videos del curso.

La API de Pexels es gratis y la licencia permite uso comercial sin atribución.
Este tool busca clips por tema, filtra por orientación/resolución/duración, baja el
mejor archivo de cada uno y lleva un manifest (id, query, autor, url) para no
re-descargar y para tener registro de fuentes.

Salida: .tmp/broll/<slug>/<id>.mp4  +  .tmp/broll/_manifest.json

Dos modos:
  1) Suelto:  python tools/pexels_fetch.py --query "business meeting" --slug reunion --count 3
  2) Plan:    python tools/pexels_fetch.py --plan tools/broll_plan_m1.json

Plan = lista JSON de entradas: [{"slug": "...", "query": "...", "count": 3,
       "min_duration": 5, "max_duration": 25, "orientation": "landscape"}, ...]

Usá --dry-run para ver qué bajaría sin descargar (Pexels es gratis, pero ahorra disco/tiempo).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = REPO_ROOT / ".tmp" / "broll"
MANIFEST = OUT_ROOT / "_manifest.json"
SEARCH_URL = "https://api.pexels.com/videos/search"

# Defaults pensados para video 16:9 1080p del curso.
DEF_COUNT = 3
DEF_MIN_DUR = 4
DEF_MAX_DUR = 30
DEF_MIN_WIDTH = 1920
DEF_ORIENT = "landscape"


def find_ffprobe() -> str | None:
    exe = shutil.which("ffprobe")
    if exe:
        return exe
    base = Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft" / "WinGet" / "Packages"
    hits = list(base.glob("Gyan.FFmpeg_*/ffmpeg-*/bin/ffprobe.exe"))
    return str(hits[0]) if hits else None


def real_height(ffprobe: str | None, path: Path) -> int | None:
    """Alto real del archivo (Pexels a veces sirve 720p bajo una URL '..1080..')."""
    if not ffprobe:
        return None
    try:
        out = subprocess.run([ffprobe, "-v", "error", "-select_streams", "v",
                              "-show_entries", "stream=height", "-of", "csv=p=0", str(path)],
                             capture_output=True, text=True, check=True).stdout.strip()
        return int(out.splitlines()[0])
    except (subprocess.CalledProcessError, ValueError, IndexError):
        return None


def slugify(s: str) -> str:
    s = re.sub(r"[^\w\s-]", "", s.lower()).strip()
    return re.sub(r"[\s_-]+", "_", s)[:48] or "broll"


def load_manifest() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {}


def save_manifest(m: dict) -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")


def search(client: httpx.Client, query: str, per_page: int, orientation: str) -> list[dict]:
    params = {"query": query, "per_page": per_page, "orientation": orientation, "size": "large"}
    r = client.get(SEARCH_URL, params=params, timeout=60)
    r.raise_for_status()
    return r.json().get("videos", [])


def candidates(video: dict, min_width: int) -> list[dict]:
    """Archivos mp4 landscape ordenados por preferencia: primero el más chico que
    cumple min_width (para no bajar 4K si alcanza 1080p), después los más grandes como
    fallback si el elegido viene mal etiquetado (720p bajo URL '..1080..')."""
    files = [f for f in video.get("video_files", [])
             if f.get("file_type") == "video/mp4" and f.get("width") and f.get("height")
             and f["width"] >= f["height"]]  # landscape
    ok = sorted((f for f in files if f["width"] >= min_width), key=lambda f: f["width"])
    rest = sorted((f for f in files if f["width"] < min_width), key=lambda f: -f["width"])
    return ok + rest


def download(client: httpx.Client, url: str, dst: Path) -> int:
    dst.parent.mkdir(parents=True, exist_ok=True)
    total = 0
    with client.stream("GET", url, timeout=300, follow_redirects=True) as resp:
        resp.raise_for_status()
        with open(dst, "wb") as fh:
            for chunk in resp.iter_bytes():
                fh.write(chunk)
                total += len(chunk)
    return total


def fetch_one(client: httpx.Client, ffprobe: str | None, cands: list[dict],
              dst: Path, min_height: int) -> dict | None:
    """Baja el primer candidato cuyo alto REAL >= min_height; sube al siguiente si
    Pexels sirvió uno mal etiquetado. Devuelve el file dict + alto real usado."""
    last = None
    for f in cands:
        download(client, f["link"], dst)
        h = real_height(ffprobe, dst)
        last = {**f, "real_height": h}
        if h is None or h >= min_height:   # sin ffprobe: confiar en metadata
            return last
    return last  # ninguno llegó: queda el último (el de mayor resolución)


def process_entry(client: httpx.Client, ffprobe: str | None, entry: dict,
                  manifest: dict, seen: set[int], dry: bool) -> int:
    query = entry["query"]
    slug = slugify(entry.get("slug") or query)
    count = int(entry.get("count", DEF_COUNT))
    min_dur = entry.get("min_duration", DEF_MIN_DUR)
    max_dur = entry.get("max_duration", DEF_MAX_DUR)
    orient = entry.get("orientation", DEF_ORIENT)
    min_width = entry.get("min_width", DEF_MIN_WIDTH)
    min_height = entry.get("min_height", 1080)

    # pedir de más para poder filtrar por duración y descartar repetidos
    videos = search(client, query, per_page=max(count * 4, 12), orientation=orient)
    got = 0
    print(f"\n[{slug}] '{query}' -> {len(videos)} resultados; objetivo {count}")
    for v in videos:
        if got >= count:
            break
        vid = v["id"]
        if vid in seen:
            continue
        dur = v.get("duration", 0)
        if dur < min_dur or dur > max_dur:
            continue
        cands = candidates(v, min_width)
        if not cands:
            continue
        seen.add(vid)
        got += 1
        dst = OUT_ROOT / slug / f"{vid}.mp4"
        author = v.get("user", {}).get("name", "?")
        if dry:
            f = cands[0]
            print(f"  - {vid}  {f['width']}x{f['height']} {dur}s  | {author}  (dry-run)")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        f = fetch_one(client, ffprobe, cands, dst, min_height)
        h = f.get("real_height") or f["height"]
        warn = "  ⚠ <1080p" if (f.get("real_height") and f["real_height"] < min_height) else ""
        print(f"  - {vid}  real {f['width']}x{h} {dur}s  | {author}"
              f"  ({round(dst.stat().st_size/1024/1024,1)} MB){warn}")
        manifest[str(vid)] = {
            "slug": slug, "query": query, "file": str(dst.relative_to(REPO_ROOT)),
            "width": f["width"], "height": h, "duration": dur,
            "author": author, "author_url": v.get("user", {}).get("url"),
            "pexels_url": v.get("url"),
        }
    if got < count:
        print(f"  ! solo {got}/{count} (afiná la query o subí max_duration)")
    return got


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--plan", help="JSON con lista de entradas {slug, query, count, ...}")
    p.add_argument("--query", help="modo suelto: término de búsqueda")
    p.add_argument("--slug", help="modo suelto: carpeta destino")
    p.add_argument("--count", type=int, default=DEF_COUNT)
    p.add_argument("--min-duration", type=int, default=DEF_MIN_DUR)
    p.add_argument("--max-duration", type=int, default=DEF_MAX_DUR)
    p.add_argument("--orientation", default=DEF_ORIENT, choices=["landscape", "portrait", "square"])
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    load_dotenv(REPO_ROOT / ".env")
    key = os.environ.get("PEXELS_API_KEY")
    if not key:
        sys.exit("PEXELS_API_KEY no está en .env")

    if args.plan:
        plan = json.loads((Path(args.plan) if Path(args.plan).is_absolute()
                           else REPO_ROOT / args.plan).read_text(encoding="utf-8"))
    elif args.query:
        plan = [{"slug": args.slug or args.query, "query": args.query, "count": args.count,
                 "min_duration": args.min_duration, "max_duration": args.max_duration,
                 "orientation": args.orientation}]
    else:
        sys.exit("Pasá --plan <file.json> o --query <texto>")

    ffprobe = find_ffprobe()
    if not ffprobe and not args.dry_run:
        print("  (ffprobe no hallado: no verifico resolución real, confío en metadata)")
    manifest = load_manifest()
    seen = {int(k) for k in manifest}  # no re-bajar lo ya descargado
    total = 0
    with httpx.Client(headers={"Authorization": key}) as client:
        for entry in plan:
            total += process_entry(client, ffprobe, entry, manifest, seen, args.dry_run)
    if not args.dry_run:
        save_manifest(manifest)
    print(f"\n>>> {total} clips {'(dry-run) ' if args.dry_run else ''}· manifest: {MANIFEST.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
