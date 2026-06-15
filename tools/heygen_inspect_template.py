"""Inspección read-only del template de HeyGen y de los Brand Voices/Glossaries.

NO gasta créditos (solo GET). Sirve para, antes de generar videos:
  - listar las variables del template (cuáles puedo reemplazar por API vs cuáles
    son visuales horneados en Studio),
  - encontrar el brand_voice_id (Brand Glossary) para pasarlo a /generate,
  - ver la voz/idioma que trae el template.

El param en /v2/template/{id}/generate se llama `brand_voice_id`
("Brand Glossary ID for translation and pronunciation rules").

Como la doc pública no fija los paths exactos, probamos varios candidatos GET
y reportamos cuál responde 200.

Uso:
    python tools/heygen_inspect_template.py            # usa template_id de heygen_defaults.json
    python tools/heygen_inspect_template.py <template_id>

Output: .tmp/heygen_template_inspect.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULTS = REPO_ROOT / "tools" / "heygen_defaults.json"
OUT_PATH = REPO_ROOT / ".tmp" / "heygen_template_inspect.json"
API_BASE = "https://api.heygen.com"


def _api_key() -> str:
    import os

    load_dotenv(REPO_ROOT / ".env")
    key = os.environ.get("HEYGEN_API_KEY")
    if not key:
        sys.exit("HEYGEN_API_KEY no está en .env")
    return key


def _try(client: httpx.Client, method: str, path: str) -> dict:
    try:
        r = client.request(method, path)
        body: object
        try:
            body = r.json()
        except Exception:
            body = r.text[:500]
        return {"path": path, "status": r.status_code, "ok": r.is_success, "body": body}
    except Exception as e:  # noqa: BLE001
        return {"path": path, "status": None, "ok": False, "error": str(e)}


def main() -> int:
    if len(sys.argv) > 1:
        template_id = sys.argv[1].strip()
    else:
        template_id = json.loads(DEFAULTS.read_text(encoding="utf-8")).get("template_id")
        if not template_id:
            sys.exit("No hay template_id (pasalo como argumento o en heygen_defaults.json)")

    key = _api_key()
    with httpx.Client(
        base_url=API_BASE,
        headers={"X-Api-Key": key, "accept": "application/json"},
        timeout=30,
    ) as c:
        template_candidates = [
            ("GET", f"/v2/template/{template_id}"),
            ("GET", f"/v2/templates/{template_id}"),
            ("GET", "/v2/templates"),
        ]
        brand_candidates = [
            ("GET", "/v2/brand_voice/list"),
            ("GET", "/v2/brand_voice"),
            ("GET", "/v1/brand_voice/list"),
            ("GET", "/v2/brand_voices"),
        ]
        results = {
            "template_id": template_id,
            "template": [_try(c, m, p) for m, p in template_candidates],
            "brand_voice": [_try(c, m, p) for m, p in brand_candidates],
        }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"OK -> {OUT_PATH.relative_to(REPO_ROOT)}\n")
    for group in ("template", "brand_voice"):
        print(f"== {group} ==")
        for r in results[group]:
            mark = "OK " if r.get("ok") else "-- "
            print(f"  {mark}{r['status']}  {r['path']}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
