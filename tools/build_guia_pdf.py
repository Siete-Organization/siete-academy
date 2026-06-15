"""
build_guia_pdf.py — Convierte las guías markdown de la academia en PDFs con la
marca de Siete (Montserrat + paleta institucional), portada propia y DRM básico
(restricción de copia de texto).

Pipeline:  guia_semana_N.md  ->  HTML + brand.css  ->  Chromium (Playwright)  ->  PDF  ->  pikepdf (DRM)

Uso:
    python tools/build_guia_pdf.py 1                 # semana 1
    python tools/build_guia_pdf.py 1 2 3             # varias semanas
    python tools/build_guia_pdf.py --all             # las 8
    python tools/build_guia_pdf.py guiones_videos/v2/sem01/guia_semana_1.md
    python tools/build_guia_pdf.py 1 --no-drm        # sin protección (para revisar)
"""

import argparse
import re
import sys
from pathlib import Path

import markdown as md_lib
import pikepdf
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
BRAND_DIR = ROOT / "tools" / "brand"
CSS_PATH = BRAND_DIR / "guia_brand.css"
ASSETS = BRAND_DIR / "assets"
V2_DIR = ROOT / "guiones_videos" / "v2"
TMP_DIR = ROOT / ".tmp"

# Password "dueño" para el DRM. El usuario abre sin password; copiar texto queda bloqueado.
DRM_OWNER_PASSWORD = "siete-academy-2026"


# ----------------------------------------------------------------------------- helpers

def split_frontmatter(text: str):
    """Devuelve (dict_frontmatter, cuerpo_markdown)."""
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if not m:
        return {}, text
    front, body = m.group(1), m.group(2)
    data = {}
    for line in front.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            data[key.strip()] = val.strip()
    return data, body


def strip_duplicate_header(body: str) -> str:
    """Quita H1, línea de módulo y primer divisor (van en la portada).
    Conserva desde el primer '## '."""
    idx = body.find("\n## ")
    if idx != -1:
        return body[idx + 1:]
    return body


def cover_html(front: dict) -> str:
    documento = front.get("documento", "Guía")
    # tema = lo que va después del primer guión largo
    tema = documento.split("—", 1)[1].strip() if "—" in documento else documento
    modulo = front.get("modulo", "").strip()
    modulo_label = f"Módulo {modulo}" if modulo and not modulo.lower().startswith("módulo") else modulo
    semana = front.get("semana", "").strip()
    logo = (ASSETS / "logo-black.png").as_uri()
    return f"""
<section class="cover">
  <div class="cover__top">
    <img class="cover__logo" src="{logo}" alt="Siete">
    <div class="cover__kicker">SDR Academy · Guía de estudio</div>
  </div>
  <div class="cover__weeknum">{semana}</div>
  <div class="cover__center">
    <div class="cover__module">{modulo_label}</div>
    <h1 class="cover__title">{tema}</h1>
    <div class="cover__rule"></div>
    <div class="cover__week">Semana {semana}</div>
  </div>
  <div class="cover__bottom">
    <div class="cover__brand">SIE7E ACADEMY</div>
    <div class="cover__sub">© Siete Academy. Uso exclusivo para participantes inscritos del programa.</div>
  </div>
</section>
"""


def build_html(md_path: Path) -> tuple[str, dict]:
    raw = md_path.read_text(encoding="utf-8")
    front, body = split_frontmatter(raw)
    body = strip_duplicate_header(body)

    body_html = md_lib.markdown(
        body,
        extensions=["tables", "sane_lists", "attr_list"],
        output_format="html5",
    )

    css = CSS_PATH.read_text(encoding="utf-8").replace("__ASSET_BASE__", BRAND_DIR.as_uri())

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<style>{css}</style>
</head>
<body>
{cover_html(front)}
<main class="content">
{body_html}
</main>
</body>
</html>"""
    return html, front


def render_pdf(html: str, html_path: Path, pdf_path: Path, week_label: str = ""):
    html_path.write_text(html, encoding="utf-8")
    doc_label = f"Guía Semana {week_label}" if week_label else "Guía"
    footer = (
        '<div style="width:100%;font-family:Arial,sans-serif;font-size:7.5px;'
        'color:#8a93a0;padding:0 17mm;display:flex;justify-content:space-between;">'
        '<span>© Siete Academy — Uso exclusivo de participantes inscritos</span>'
        f'<span>{doc_label} · pág. <span class="pageNumber"></span></span>'
        '</div>'
    )
    header = '<span></span>'
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(html_path.as_uri(), wait_until="networkidle")
        page.pdf(
            path=str(pdf_path),
            format="A4",
            print_background=True,
            display_header_footer=True,
            header_template=header,
            footer_template=footer,
            margin={"top": "19mm", "bottom": "16mm", "left": "17mm", "right": "17mm"},
        )
        browser.close()


def apply_drm(pdf_path: Path):
    """Restringe copia/extracción de texto (DRM básico a nivel PDF)."""
    with pikepdf.open(pdf_path, allow_overwriting_input=True) as pdf:
        pdf.save(
            pdf_path,
            encryption=pikepdf.Encryption(
                owner=DRM_OWNER_PASSWORD,
                user="",  # se abre sin password
                allow=pikepdf.Permissions(
                    extract=False,                  # no copiar texto/gráficos
                    modify_annotation=False,
                    modify_assembly=False,
                    modify_form=False,
                    modify_other=False,
                ),
                R=6,  # AES-256
            ),
        )


# ----------------------------------------------------------------------------- resolución de inputs

def resolve_inputs(tokens: list[str]) -> list[Path]:
    paths = []
    for t in tokens:
        if t.isdigit():
            p = V2_DIR / f"sem{int(t):02d}" / f"guia_semana_{int(t)}.md"
            if not p.exists():
                sys.exit(f"No existe: {p}")
            paths.append(p)
        else:
            p = Path(t)
            if not p.exists():
                sys.exit(f"No existe: {p}")
            paths.append(p)
    return paths


def all_guias() -> list[Path]:
    return sorted(V2_DIR.glob("sem*/guia_semana_*.md"),
                  key=lambda p: int(re.search(r"_(\d+)\.md$", p.name).group(1)))


def main():
    ap = argparse.ArgumentParser(description="Genera PDFs de marca de las guías de la academia.")
    ap.add_argument("weeks", nargs="*", help="Números de semana o rutas .md")
    ap.add_argument("--all", action="store_true", help="Procesar las 8 guías")
    ap.add_argument("--no-drm", action="store_true", help="Sin restricción de copia (revisión)")
    args = ap.parse_args()

    if args.all:
        inputs = all_guias()
    elif args.weeks:
        inputs = resolve_inputs(args.weeks)
    else:
        ap.error("Indicá una semana (ej: 1), rutas .md, o --all")

    TMP_DIR.mkdir(exist_ok=True)
    for md_path in inputs:
        stem = md_path.stem
        html, front = build_html(md_path)
        html_path = TMP_DIR / f"{stem}.html"
        pdf_path = md_path.with_suffix(".pdf")
        print(f"-> {md_path.relative_to(ROOT)}  ...generando PDF")
        render_pdf(html, html_path, pdf_path, front.get("semana", ""))
        if not args.no_drm:
            apply_drm(pdf_path)
            print(f"   OK {pdf_path.relative_to(ROOT)}  (con DRM)")
        else:
            print(f"   OK {pdf_path.relative_to(ROOT)}  (sin DRM)")


if __name__ == "__main__":
    main()
