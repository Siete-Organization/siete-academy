"""Endpoint tests para los reads de assessment usados por la vista de alumno/admin."""

from app.modules.assessments.models import Assessment
from app.modules.courses.models import Course, Lesson, Module


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
    def test_returns_assessment_with_raw_config_for_staff(self, client, db, login_as):
        login_as("admin")
        a = _seed_assessment(db, type="capa_2", title="Prueba M4", passing_score=65.0)
        r = client.get(f"/assessments/{a.id}")
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["id"] == a.id
        assert body["type"] == "capa_2"
        assert body["passing_score"] == 65.0
        # Staff ve el config crudo (lo necesita el preview / corrector / editor).
        assert body["config"]["questions"][0]["correct"] == ["a"]

    def test_returns_404_for_unknown_id(self, client, login_as):
        login_as("admin")
        assert client.get("/assessments/999999").status_code == 404

    def test_forbidden_for_students(self, client, db):
        # `client` está logueado como student por defecto → 403 (cierra el leak).
        a = _seed_assessment(db, type="capa_2")
        assert client.get(f"/assessments/{a.id}").status_code == 403


class TestAnswerLeakIsClosed:
    """capa_2 / final_test no deben filtrar respuestas ni rúbricas al alumno."""

    LEAKY_CONFIG = {
        "questions": [
            {
                "id": "q1",
                "type": "single",
                "prompt": "¿?",
                "choices": [{"id": "a", "text": "A"}, {"id": "b", "text": "B"}],
                "correct": "a",
                "explanation": "porque sí",
                "differentiator": True,
            }
        ],
        "short_answers": [
            {"id": "s1", "prompt": "redactá", "expected_answer": "modelo", "rubric": "0-2"}
        ],
        "tables": [
            {
                "id": "t1",
                "prompt": "clasificá",
                "rows": [{"id": "1", "label": "fila", "correct": "duro"}],
                "options": [{"id": "duro", "label": "Duro"}],
                "expected_sequence": [{"paso": 1}],
                "rubric": "0-3",
            }
        ],
        "video_rubric": {"dimensions": [{"id": 1}]},
        "short_rubric": {"scale": "0-2"},
        "differentiator_ids": ["q1"],
        # No-secretos que SÍ deben sobrevivir:
        "case_brief": {"title": "Caso"},
        "rules": {"open_book": True},
    }

    def _assert_stripped(self, body: dict):
        cfg = body["config"]
        q = cfg["questions"][0]
        assert "correct" not in q
        assert "explanation" not in q
        assert "differentiator" not in q
        # El enunciado y las opciones sí se conservan.
        assert q["choices"][0]["id"] == "a"
        assert "expected_answer" not in cfg["short_answers"][0]
        assert "rubric" not in cfg["short_answers"][0]
        tbl = cfg["tables"][0]
        assert "expected_sequence" not in tbl
        assert "rubric" not in tbl
        assert "correct" not in tbl["rows"][0]
        assert "video_rubric" not in cfg
        assert "short_rubric" not in cfg
        assert "differentiator_ids" not in cfg
        # Contexto necesario para rendir sí se conserva.
        assert cfg["case_brief"]["title"] == "Caso"
        assert cfg["rules"]["open_book"] is True

    def test_final_endpoint_strips_answers(self, client, db):
        _seed_assessment(db, type="final_test", config=dict(self.LEAKY_CONFIG))
        r = client.get("/assessments/final")
        assert r.status_code == 200, r.text
        self._assert_stripped(r.json())

    def test_module_endpoint_strips_answers(self, client, db):
        a = _seed_assessment(db, type="capa_2", config=dict(self.LEAKY_CONFIG))
        r = client.get(f"/assessments/module/{a.module_id}")
        assert r.status_code == 200, r.text
        bodies = r.json()
        assert len(bodies) == 1
        self._assert_stripped(bodies[0])

    def test_lesson_endpoint_strips_answers(self, client, db):
        # Capa 1: la corrección vive server-side → `correct` ya no viaja.
        a = _seed_mcq_lesson(db)
        r = client.get(f"/assessments/lesson/{a.lesson_id}")
        assert r.status_code == 200, r.text
        q = r.json()[0]["config"]["questions"][0]
        assert "correct" not in q
        assert "explanation" not in q
        # El enunciado y las opciones sí se conservan.
        assert q["prompt"] == "¿?"
        assert q["choices"][0]["id"] == "a"


def _seed_mcq_lesson(db) -> Assessment:
    m_id = _seed_module(db)
    lesson = Lesson(module_id=m_id, order_index=0)
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    a = Assessment(
        module_id=m_id,
        lesson_id=lesson.id,
        type="mcq",
        title="Microprueba",
        config={
            "questions": [
                {
                    "id": "q1",
                    "type": "single",
                    "prompt": "¿?",
                    "choices": [{"id": "a", "text": "A"}, {"id": "b", "text": "B"}],
                    "correct": ["a"],
                    "explanation": "porque sí",
                },
                {
                    "id": "q2",
                    "type": "multi",
                    "prompt": "¿multi?",
                    "choices": [
                        {"id": "a", "text": "A"},
                        {"id": "b", "text": "B"},
                        {"id": "c", "text": "C"},
                    ],
                    "correct": ["a", "b"],
                },
            ]
        },
        passing_score=70.0,
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


class TestSubmissionReview:
    """El POST de una microprueba devuelve la corrección pregunta a pregunta."""

    def test_mcq_submission_returns_review(self, client, db):
        a = _seed_mcq_lesson(db)
        r = client.post(
            "/assessments/submissions",
            json={
                "assessment_id": a.id,
                "payload": {"answers": {"q1": "a", "q2": ["a", "c"]}},
            },
        )
        assert r.status_code == 201, r.text
        body = r.json()
        assert body["status"] == "auto_graded"
        review = body["review"]
        assert [x["id"] for x in review] == ["q1", "q2"]
        assert review[0]["is_correct"] is True
        assert review[0]["correct"] == ["a"]
        assert review[0]["explanation"] == "porque sí"
        assert review[1]["is_correct"] is False
        assert review[1]["correct"] == ["a", "b"]

    def test_capa2_submission_has_no_review(self, client, db):
        a = _seed_assessment(db, type="capa_2", config=dict(TestAnswerLeakIsClosed.LEAKY_CONFIG))
        r = client.post(
            "/assessments/submissions",
            json={"assessment_id": a.id, "payload": {"answers": {"q1": "a"}}},
        )
        assert r.status_code == 201, r.text
        assert r.json()["review"] is None
