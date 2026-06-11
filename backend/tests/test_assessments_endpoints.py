"""Endpoint tests para los reads de assessment usados por la vista de alumno/admin."""

from app.modules.assessments.models import Assessment
from app.modules.courses.models import Course, Module


def _seed_module(db) -> int:
    c = Course(slug="sdr-ep")
    db.add(c)
    db.commit()
    db.refresh(c)
    m = Module(course_id=c.id, slug="m4-ep", order_index=3)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m.id


def _seed_assessment(db, **overrides) -> Assessment:
    base = dict(
        module_id=_seed_module(db),
        type="final_test",
        title="Prueba Final",
        config={"questions": [{"id": "q1", "type": "single", "correct": ["a"]}]},
        passing_score=60.0,
    )
    base.update(overrides)
    a = Assessment(**base)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


class TestFinalEndpoint:
    def test_returns_404_when_no_final_configured(self, client):
        assert client.get("/assessments/final").status_code == 404

    def test_returns_the_final_test(self, client, db):
        _seed_assessment(db, type="final_test", title="Prueba Final — Caso")
        r = client.get("/assessments/final")
        assert r.status_code == 200, r.text
        assert r.json()["type"] == "final_test"
        assert r.json()["title"] == "Prueba Final — Caso"


class TestGetAssessmentById:
    def test_returns_assessment(self, client, db):
        a = _seed_assessment(db, type="capa_2", title="Prueba M4", passing_score=65.0)
        r = client.get(f"/assessments/{a.id}")
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["id"] == a.id
        assert body["type"] == "capa_2"
        assert body["passing_score"] == 65.0

    def test_returns_404_for_unknown_id(self, client):
        assert client.get("/assessments/999999").status_code == 404
