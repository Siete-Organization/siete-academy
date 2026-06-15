"""Genera videos batch desde guiones_videos/v2/sem<N>/ usando un template de HeyGen.

Lee los archivos .md de la semana, extrae el texto hablable (quita frontmatter,
marcadores [SLIDE:...], headers de sección [GANCHO ~15s], formato markdown),
y dispara una generación por video vía /v2/template/{template_id}/generate.
Polea status hasta completed/failed y guarda los resultados.

Asume que el template fue creado en Studio con un único variable `script` (text)
que recibe el contenido a hablar. Si el template usa otro nombre, cambiar
`SCRIPT_VAR_NAME` o pasar `--script-var <nombre>`.

Uso:
    # dry-run (no llama API, solo muestra qué se enviaría)
    python tools/heygen_generate_videos.py --sem 1 --template-id <id> --dry-run

    # test mode (HeyGen no cobra créditos, video sale con marca de agua)
    python tools/heygen_generate_videos.py --sem 1 --template-id <id> --test

    # producción
    python tools/heygen_generate_videos.py --sem 1 --template-id <id>

Output: .tmp/heygen_sem<NN>_results.json con video_url, status, errores.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]
API_BASE = "https://api.heygen.com"
GUIONES_ROOT = REPO_ROOT / "guiones_videos" / "v2"
RESULTS_DIR = REPO_ROOT / ".tmp"
SCRIPT_VAR_NAME = "script"  # default variable en el template


def strip_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    fm_text, body = parts[1], parts[2]
    fm: dict[str, str] = {}
    for line in fm_text.strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, body


def script_to_spoken(body: str) -> str:
    """Convierte el body markdown a texto plano hablable por el avatar."""
    # Quitar líneas con marcadores [SLIDE:...] (van solas en su propia línea)
    body = re.sub(r"^\s*\*?\*?\[SLIDE:[^\]]+\]\*?\*?\s*$", "", body, flags=re.MULTILINE)
    # Quitar headers de sección [GANCHO ~15s], [CIERRE ~30s], etc.
    body = re.sub(r"^\s*##\s*\[[^\]]+\].*$", "", body, flags=re.MULTILINE)
    # Quitar headers markdown sueltos
    body = re.sub(r"^\s*#{1,6}\s+.+$", "", body, flags=re.MULTILINE)
    # Quitar negritas/itálicas (manteniendo el texto)
    body = re.sub(r"\*\*([^*]+)\*\*", r"\1", body)
    body = re.sub(r"\*([^*]+)\*", r"\1", body)
    # Compactar 3+ newlines a 2
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


def load_guiones(sem: int) -> list[dict]:
    semdir = GUIONES_ROOT / f"sem{sem:02d}"
    if not semdir.exists():
        sys.exit(f"No existe {semdir}")
    out = []
    for f in sorted(semdir.glob("*.md")):
        if f.stem.startswith("guia_"):
            continue  # guia_semana_X.md es para PDF, no video
        text = f.read_text(encoding="utf-8")
        fm, body = strip_frontmatter(text)
        spoken = script_to_spoken(body)
        out.append(
            {
                "slug": f.stem,
                "title": fm.get("titulo") or fm.get("video") or f.stem,
                "path": str(f.relative_to(REPO_ROOT)),
                "script": spoken,
                "word_count": len(spoken.split()),
                "estimated_duration_min": round(len(spoken.split()) / 150, 1),
            }
        )
    return out


def generate_from_template(
    client: httpx.Client,
    template_id: str,
    title: str,
    script: str,
    script_var: str,
    test_mode: bool,
) -> str:
    payload: dict[str, Any] = {
        "title": title,
        "variables": {
            script_var: {
                "name": script_var,
                "type": "text",
                "properties": {"content": script},
            }
        },
        "test": test_mode,
    }
    r = client.post(f"/v2/template/{template_id}/generate", json=payload)
    r.raise_for_status()
    data = r.json().get("data") or {}
    vid = data.get("video_id")
    if not vid:
        raise RuntimeError(f"No video_id en respuesta: {r.text[:300]}")
    return vid


def poll_status(client: httpx.Client, video_id: str, timeout_s: int = 1800) -> dict:
    start = time.time()
    while True:
        r = client.get("/v1/video_status.get", params={"video_id": video_id})
        r.raise_for_status()
        data = r.json().get("data") or {}
        status = data.get("status")
        if status in ("completed", "failed"):
            return data
        if time.time() - start > timeout_s:
            return {**data, "status": "timeout"}
        time.sleep(15)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--sem", type=int, required=True, help="Número de semana (1..8)")
    p.add_argument("--template-id", help="HeyGen template_id (no requerido en --dry-run)")
    p.add_argument("--script-var", default=SCRIPT_VAR_NAME, help=f"Nombre de la variable del template (default: {SCRIPT_VAR_NAME})")
    p.add_argument("--dry-run", action="store_true", help="Solo parsear y mostrar; no llama API")
    p.add_argument("--test", action="store_true", help="Modo test de HeyGen (no consume créditos, marca de agua)")
    args = p.parse_args()

    guiones = load_guiones(args.sem)
    print(f"Sem {args.sem}: {len(guiones)} videos a generar")
    for g in guiones:
        print(f"  - {g['slug']}: {g['word_count']} palabras (~{g['estimated_duration_min']} min)")

    if args.dry_run:
        out = RESULTS_DIR / f"heygen_sem{args.sem:02d}_dryrun.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(guiones, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\nDry run guardado en {out.relative_to(REPO_ROOT)}")
        return 0

    if not args.template_id:
        sys.exit("--template-id es requerido (o usar --dry-run)")

    load_dotenv(REPO_ROOT / ".env")
    api_key = os.environ.get("HEYGEN_API_KEY")
    if not api_key:
        sys.exit("HEYGEN_API_KEY no está en .env")

    results = []
    with httpx.Client(
        base_url=API_BASE,
        headers={"X-Api-Key": api_key, "accept": "application/json"},
        timeout=60,
    ) as c:
        for g in guiones:
            print(f"\n>>> {g['slug']}")
            try:
                video_id = generate_from_template(
                    c, args.template_id, g["title"], g["script"], args.script_var, args.test
                )
                print(f"    video_id: {video_id}, polling cada 15s...")
                status = poll_status(c, video_id)
                print(f"    status: {status.get('status')}")
                results.append(
                    {
                        "slug": g["slug"],
                        "title": g["title"],
                        "video_id": video_id,
                        "status": status.get("status"),
                        "video_url": status.get("video_url"),
                        "thumbnail_url": status.get("thumbnail_url"),
                        "duration_sec": status.get("duration"),
                        "error": status.get("error"),
                    }
                )
            except httpx.HTTPStatusError as e:
                print(f"    ERROR HTTP {e.response.status_code}: {e.response.text[:200]}")
                results.append({"slug": g["slug"], "status": "error", "error": e.response.text[:500]})
            except Exception as e:
                print(f"    ERROR: {e}")
                results.append({"slug": g["slug"], "status": "error", "error": str(e)})

    out = RESULTS_DIR / f"heygen_sem{args.sem:02d}_results.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nResultados guardados en {out.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
