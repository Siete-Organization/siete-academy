"""Genera slides de marca (1920x1080 PNG) para los tramos 'slide' de un video.

Lee una spec JSON (lista de placas) y renderiza cada una con HTML->PNG (Playwright),
usando la identidad Siete: fondo blanco, Montserrat, título negro, barra de acento azul,
y un dato grande opcional. Pensado para el formato 'presentador por tramos'.

Salida: .tmp/slides/<carpeta>/<file>.png

Uso:
    python tools/build_slides.py tools/slides_spec_sem01_contenido_1.json --out-name sem01_contenido_1
"""

from __future__ import annotations

import argparse
import base64
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = REPO_ROOT / ".tmp" / "slides"


def data_uri(path: Path, mime: str) -> str:
    """file:// no carga en set_content (sin base URL) -> embebemos en base64."""
    b64 = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{b64}"


FONT = data_uri(REPO_ROOT / "tools" / "brand" / "fonts" / "Montserrat-Variable.ttf", "font/ttf")
LOGO = data_uri(REPO_ROOT / "tools" / "brand" / "assets" / "logo-black.png", "image/png")

# Paleta Siete (de _INSTRUCCIONES_PRODUCCION_VIDEO.md §2.1)
BLUE = "#007AFF"
INK = "#0A0A0A"
GREY = "#5B6470"

HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family:'Montserrat'; src:url('{font}'); font-weight:100 900; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:1920px; height:1080px; }}
body {{ font-family:'Montserrat',sans-serif; background:#FFFFFF; color:{ink};
        display:flex; flex-direction:column; justify-content:center;
        padding:140px 160px; position:relative; }}
.kicker {{ font-size:34px; font-weight:700; letter-spacing:.18em; color:{grey};
           text-transform:uppercase; margin-bottom:28px; }}
.bar {{ width:140px; height:10px; background:{blue}; border-radius:6px; margin-bottom:40px; }}
h1 {{ font-size:104px; font-weight:800; line-height:1.05; max-width:1400px; }}
.sub {{ font-size:46px; font-weight:500; color:{grey}; margin-top:36px; max-width:1040px;
        line-height:1.25; }}
.stat {{ position:absolute; right:160px; bottom:150px; text-align:right; }}
.stat .num {{ font-size:240px; font-weight:800; color:{blue}; line-height:.9; }}
.stat .lbl {{ font-size:38px; font-weight:600; color:{ink}; max-width:560px; margin-top:8px; }}
.logo {{ position:absolute; top:70px; right:160px; height:46px; opacity:.9; }}
</style></head><body>
  <img class="logo" src="{logo}">
  {kicker}
  <div class="bar"></div>
  <h1>{title}</h1>
  {sub}
  {stat}
</body></html>"""


def render_html(spec: dict) -> str:
    kicker = f'<div class="kicker">{spec["kicker"]}</div>' if spec.get("kicker") else ""
    sub = f'<div class="sub">{spec["subtitle"]}</div>' if spec.get("subtitle") else ""
    stat = ""
    if spec.get("stat"):
        lbl = f'<div class="lbl">{spec.get("stat_label", "")}</div>' if spec.get("stat_label") else ""
        stat = f'<div class="stat"><div class="num">{spec["stat"]}</div>{lbl}</div>'
    return HTML.format(font=FONT, logo=LOGO, blue=BLUE, ink=INK, grey=GREY,
                       kicker=kicker, title=spec["title"], sub=sub, stat=stat)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("spec")
    p.add_argument("--out-name", required=True, help="subcarpeta de salida, ej. sem01_contenido_1")
    args = p.parse_args()

    spec_path = Path(args.spec) if Path(args.spec).is_absolute() else REPO_ROOT / args.spec
    specs = json.loads(spec_path.read_text(encoding="utf-8"))
    out_dir = OUT_ROOT / args.out_name
    out_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        for s in specs:
            page.set_content(render_html(s), wait_until="networkidle")
            dst = out_dir / f"{s['file']}.png"
            page.screenshot(path=str(dst))
            print(f"  {dst.relative_to(REPO_ROOT)}  ({s['title']})")
        browser.close()
    print(f">>> {len(specs)} slides -> {out_dir.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
