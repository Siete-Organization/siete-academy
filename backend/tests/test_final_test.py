"""Tests para la Prueba Final del curso (Capa 3 — caso GestaLogix)."""
import pytest

from app.modules.assessments.models import Assessment
from app.modules.assessments.services import auto_grade_mcq
from app.modules.courses.models import Course, Module, ModuleTranslation
from app.modules.grading.services import (
    classify_tier,
    differentiator_score,
    final_case_score,
)
from app.scripts.final_test_questions import (
    CASE_BRIEF,
    DIFFERENTIATOR_IDS,
    MCQ,
    PASSING_SCORE,
    SHORT_ANSWERS,
    TABLES,
    VIDEO_RUBRIC_15,
    WEIGHTS,
    differentiator_questions,
    total_case_points,
    total_mcq_count,
    total_short_answers,
)
from app.scripts.seed_final_test import _upsert_final, MODULE_SLUG


@pytest.fixture
def module_m4_for_final(db) -> Module:
    course = Course(slug="sdr-academy-v1")
    db.add(course)
    db.commit()
    db.refresh(course)
    m = Module(course_id=course.id, slug=MODULE_SLUG, order_index=3)
    m.translations.append(
        ModuleTranslation(locale="es", title="M4", summary="El sistema")
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


class TestContent:
    def test_mcq_present(self):
        # Rediseño NICO (v1): 16 MCQ de respuesta única, todas autocorregibles.
        assert total_mcq_count() == 16

    def test_case_points_total_42(self):
        # 6 ítems × 2 pts + 10 ítems × 3 pts = 42.
        assert total_case_points() == 42

    def test_no_manual_components(self):
        # El caso es 100% MCQ: sin respuestas cortas ni tablas manuales.
        assert total_short_answers() == 0
        assert len(TABLES) == 0

    def test_points_are_2_or_3(self):
        for q in MCQ:
            assert q.get("points") in (2, 3), q["id"]

    def test_ids_unique_across_all_questions(self):
        ids = (
            [q["id"] for q in MCQ]
            + [q["id"] for q in SHORT_ANSWERS]
            + [t["id"] for t in TABLES]
        )
        assert len(ids) == len(set(ids))

    def test_mcq_single_correct_in_choices(self):
        for q in MCQ:
            choice_ids = [c["id"] for c in q["choices"]]
            assert q["correct"] in choice_ids, q["id"]

    def test_stages_are_1_to_6(self):
        for q in MCQ + SHORT_ANSWERS + TABLES:
            assert q.get("stage") in (1, 2, 3, 4, 5, 6), q["id"]

    def test_differentiator_ids_match_marker(self):
        # Las 4 diferenciadoras del doc deben estar marcadas como differentiator=True
        assert set(DIFFERENTIATOR_IDS) == {"P1.4", "P5.2", "P6.1", "P6.3"}
        flagged = {q["id"] for q in differentiator_questions()}
        assert flagged == set(DIFFERENTIATOR_IDS)

    def test_video_rubric_has_15_dimensions(self):
        assert len(VIDEO_RUBRIC_15["dimensions"]) == 15

    def test_video_critical_dims_are_first_six(self):
        criticals = [d for d in VIDEO_RUBRIC_15["dimensions"] if d.get("critical")]
        assert {d["id"] for d in criticals} == {1, 2, 3, 4, 5, 6}
        assert set(VIDEO_RUBRIC_15["critical_dimensions_for_distinction"]) == {1, 2, 3, 4, 5, 6}
        assert VIDEO_RUBRIC_15["min_critical_points"] == 11

    def test_weights_sum_to_one(self):
        assert WEIGHTS["case"] + WEIGHTS["video"] == 1.0

    def test_passing_score_is_60(self):
        assert PASSING_SCORE == 60.0

    def test_case_brief_has_summary(self):
        assert "summary" in CASE_BRIEF
        assert "GestaLogix" in CASE_BRIEF["summary"]

    def test_all_differentiators_are_mcq(self):
        # En el rediseño, las 4 diferenciadoras son MCQ (no respuestas cortas).
        mcq_ids = {q["id"] for q in MCQ}
        assert set(DIFFERENTIATOR_IDS) <= mcq_ids


class TestSeed:
    def test_upsert_creates_final_assessment(self, db, module_m4_for_final):
        a = _upsert_final(db, module_m4_for_final)
        assert a.type == "final_test"
        assert a.lesson_id is None
        assert a.module_id == module_m4_for_final.id
        assert a.passing_score == PASSING_SCORE
        assert len(a.config["questions"]) == 16
        assert len(a.config["short_answers"]) == 0
        assert len(a.config["tables"]) == 0
        assert a.config["tier"] == "capa_3"
        assert a.config["weights"] == {"case": 0.7, "video": 0.3}

    def test_upsert_is_idempotent(self, db, module_m4_for_final):
        a1 = _upsert_final(db, module_m4_for_final)
        a2 = _upsert_final(db, module_m4_for_final)
        assert a1.id == a2.id
        count = (
            db.query(Assessment)
            .filter(Assessment.type == "final_test")
            .count()
        )
        assert count == 1


class TestIntegration:
    def test_classifies_as_capa_3(self, db, module_m4_for_final):
        """La prueba final debe quedar clasificada como capa_3 por el motor de grading."""
        a = _upsert_final(db, module_m4_for_final)
        assert classify_tier(a) == "capa_3"

    def test_auto_grade_mcq_all_correct(self, db, module_m4_for_final):
        """La porción MCQ del final_test auto-grada al 100% cuando todas son correctas."""
        a = _upsert_final(db, module_m4_for_final)
        student_answers = {q["id"]: q["correct"] for q in MCQ}
        score = auto_grade_mcq(a, {"answers": student_answers})
        assert score == 100.0

    def test_auto_grade_mcq_zero_when_all_wrong(self, db, module_m4_for_final):
        a = _upsert_final(db, module_m4_for_final)
        wrong = {
            q["id"]: next(c["id"] for c in q["choices"] if c["id"] != q["correct"])
            for q in MCQ
        }
        score = auto_grade_mcq(a, {"answers": wrong})
        assert score == 0.0

    def test_case_score_autocomputes_without_professor_details(self, db, module_m4_for_final):
        """El caso 100% MCQ se autocalifica sin esperar el grading manual del profesor."""
        a = _upsert_final(db, module_m4_for_final)
        all_correct = {q["id"]: q["correct"] for q in MCQ}
        # details=None: antes devolvía None; ahora computa porque no hay componentes manuales.
        assert final_case_score(a.config, {"answers": all_correct}, None) == 100.0

    def test_case_score_is_weighted_by_points(self, db, module_m4_for_final):
        """Acertar solo los ítems de 2 pts da 12/42; el puntaje es ponderado, no por conteo."""
        a = _upsert_final(db, module_m4_for_final)
        only_2pt = {q["id"]: q["correct"] for q in MCQ if q.get("points") == 2}
        expected = round(12 / 42 * 100, 2)  # 6 ítems × 2 pts = 12 de 42
        assert final_case_score(a.config, {"answers": only_2pt}, None) == expected

    def test_differentiator_score_three_of_four_is_distinction_floor(self, db, module_m4_for_final):
        """3 de 4 diferenciadoras (todas de 3 pts) = 9/12 = 75% — el piso de distinción."""
        a = _upsert_final(db, module_m4_for_final)
        answers = {q["id"]: q["correct"] for q in MCQ}
        # Romper una diferenciadora a propósito.
        broken = DIFFERENTIATOR_IDS[0]
        q = next(x for x in MCQ if x["id"] == broken)
        answers[broken] = next(c["id"] for c in q["choices"] if c["id"] != q["correct"])
        assert differentiator_score(a.config, {"answers": answers}, None) == 75.0
