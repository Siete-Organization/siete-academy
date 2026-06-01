"""Tests para la Prueba Final del curso (Capa 3 — caso GestaLogix)."""
import pytest

from app.modules.assessments.models import Assessment
from app.modules.assessments.services import auto_grade_mcq
from app.modules.courses.models import Course, Module, ModuleTranslation
from app.modules.grading.services import classify_tier
from app.scripts.final_test_questions import (
    CASE_BRIEF,
    DIFFERENTIATOR_IDS,
    GENERIC_SHORT_RUBRIC,
    MCQ,
    PASSING_SCORE,
    SHORT_ANSWERS,
    TABLES,
    VIDEO_RUBRIC_15,
    WEIGHTS,
    differentiator_questions,
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
        # 12 MCQ auto-gradables que cubren P1.1, P1.2, P1.4, P2.2, P3.A.1, P3.B.1,
        # P3.C, P3.D.1, P4.2, P5.1, P5.2, P6.1
        assert total_mcq_count() == 12

    def test_short_answers_present(self):
        # 8 respuestas cortas: P1.3, P3.A.2, P3.B.2, P3.D.2, P4.3, P5.3, P6.2, P6.3
        assert total_short_answers() == 8

    def test_tables_present(self):
        # 2 tablas: P2.1 (ICP) + P4.1 (secuencia)
        assert len(TABLES) == 2

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

    def test_video_critical_dims_are_first_four(self):
        criticals = [d for d in VIDEO_RUBRIC_15["dimensions"] if d.get("critical")]
        assert {d["id"] for d in criticals} == {1, 2, 3, 4}

    def test_weights_sum_to_one(self):
        assert WEIGHTS["case"] + WEIGHTS["video"] == 1.0

    def test_passing_score_is_60(self):
        assert PASSING_SCORE == 60.0

    def test_case_brief_has_summary(self):
        assert "summary" in CASE_BRIEF
        assert "GestaLogix" in CASE_BRIEF["summary"]

    def test_short_rubric_scale_is_0_to_2(self):
        scores = [s["score"] for s in GENERIC_SHORT_RUBRIC["scoring"]]
        assert scores == [0, 1, 2]


class TestSeed:
    def test_upsert_creates_final_assessment(self, db, module_m4_for_final):
        a = _upsert_final(db, module_m4_for_final)
        assert a.type == "final_test"
        assert a.lesson_id is None
        assert a.module_id == module_m4_for_final.id
        assert a.passing_score == PASSING_SCORE
        assert len(a.config["questions"]) == 12
        assert len(a.config["short_answers"]) == 8
        assert len(a.config["tables"]) == 2
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
