"""Tests del módulo library/industries (Documento Maestro Parte II).

Cubre:
- Endpoint público GET /library/industries (lista ordenada por order_index).
- Endpoint público GET /library/industries/{slug} (detalle con 8 campos).
- 404 cuando el slug no existe.
- Seed idempotente: re-ejecutarlo no duplica filas.
- Seed: 10 industrias del doc presentes y bien estructuradas.
"""
from __future__ import annotations

import pytest

from app.modules.library.models import IndustryCard, IndustryCardTranslation
from app.scripts.seed_library_industries import INDUSTRIES, run as run_seed


@pytest.fixture
def seeded(db):
    """Corre el seed real una vez para los tests de endpoint."""
    run_seed()
    yield


def test_seed_creates_ten_industries(db, seeded):
    cards = db.query(IndustryCard).all()
    assert len(cards) == 10

    slugs = {c.slug for c in cards}
    expected = {entry["slug"] for entry in INDUSTRIES}
    assert slugs == expected


def test_seed_is_idempotent(db, seeded):
    # Re-ejecutar no debería duplicar tarjetas ni traducciones
    run_seed()
    assert db.query(IndustryCard).count() == 10
    assert db.query(IndustryCardTranslation).count() == 10  # 1 es por tarjeta


def test_seed_populates_translatable_fields(db, seeded):
    retail = (
        db.query(IndustryCard).filter(IndustryCard.slug == "retail-cpg").first()
    )
    assert retail is not None
    es = next(t for t in retail.translations if t.locale == "es")
    assert es.name == "Retail y consumo masivo"
    # Cita del doc — si esto cambia es porque alguien tocó el seed
    assert "consumidor final" in (es.what_is or "")
    assert "Falabella" in (retail.examples or [""])[0]
    assert retail.tags and "b2c" in retail.tags


def test_list_industries_returns_ordered(client, seeded):
    r = client.get("/library/industries")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 10
    orders = [c["order_index"] for c in data]
    assert orders == sorted(orders)
    # El primer item debe ser retail-cpg (order_index=1 en el doc)
    assert data[0]["slug"] == "retail-cpg"


def test_list_uses_summary_shape(client, seeded):
    r = client.get("/library/industries")
    first = r.json()[0]
    # Summary expone solo lo necesario para la grilla
    assert set(first.keys()) == {
        "slug",
        "order_index",
        "name",
        "what_is",
        "examples",
        "tags",
    }


def test_get_industry_by_slug(client, seeded):
    r = client.get("/library/industries/salud-farmaceutica")
    assert r.status_code == 200
    body = r.json()
    assert body["slug"] == "salud-farmaceutica"
    assert body["order_index"] == 10
    # Detalle expone los 8 campos del doc
    for field in (
        "what_is",
        "how_makes_money",
        "what_sells",
        "sells_to",
        "buys_to_operate",
        "dynamics",
        "deepen_in",
    ):
        assert field in body
    # Verifica que el contenido viene del doc maestro, no inventado
    assert "COFEPRIS" in body["buys_to_operate"]


def test_get_industry_404_on_unknown_slug(client, seeded):
    r = client.get("/library/industries/no-existe")
    assert r.status_code == 404


def test_list_falls_back_to_default_locale(client, seeded):
    # Pedimos en="en" pero solo seedeamos "es" → debe caer al default
    r = client.get("/library/industries", params={"locale": "en"})
    assert r.status_code == 200
    first = r.json()[0]
    # Como no hay traducción en, devuelve la es como fallback
    assert first["name"] == "Retail y consumo masivo"


def test_invalid_locale_normalized_to_default(client, seeded):
    r = client.get("/library/industries", params={"locale": "fr"})
    assert r.status_code == 200
    # No revienta — simplemente cae a 'es'
    assert len(r.json()) == 10
