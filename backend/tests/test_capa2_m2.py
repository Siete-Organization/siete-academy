"""Tests para Capa 2 Módulo 2 — contenido + seed + auto_grade integration."""
import pytest

from app.modules.assessments.models import Assessment
from app.modules.assessments.services import auto_grade_mcq
from app.modules.courses.models import Course, Module, ModuleTranslation
from app.scripts.capa2_m2_questions import (
    MCQ,
    PASSING_SCORE,
    VIDEO_CASES,
    VIDEO_RUBRIC,
    WEIGHTS,
    total_question_count,
)
from app.scripts.seed_capa2_m2 import _upsert_capa2, MODULE_SLUG


@pytest.fixture
def module_m2(db) -> Module:
    course = Course(slug="sdr-academy-v1")
    db.add(course)
    db.commit()
    db.refresh(course)
    m = Module(course_id=course.id, slug=MODULE_SLUG, order_index=1)
    m.translations.append(
        ModuleTranslation(locale="es", title="M2", summary="El otro lado")
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


class TestContent:
    def test_mcq_count_is_16(self):
        assert total_question_count() == 16

    def test_each_question_has_required_fields(self):
        for q in MCQ:
            assert "id" in q
            assert "type" in q
            assert "prompt" in q
            assert "correct" in q
            assert q["type"] in ("single", "multi", "match")

    def test_ids_unique(self):
        ids = [q["id"] for q in MCQ]
        assert len(ids) == len(set(ids))

    def test_ids_use_m2_prefix(self):
        for q in MCQ:
            assert q["id"].startswith("M2."), q["id"]

    def test_single_choice_correct_is_in_choices(self):
        for q in MCQ:
            if q["type"] != "single":
                continue
            choice_ids = [c["id"] for c in q["choices"]]
            assert q["correct"] in choice_ids, q["id"]

    def test_multi_choice_correct_all_in_choices(self):
        for q in MCQ:
            if q["type"] != "multi":
                continue
            choice_ids = {c["id"] for c in q["choices"]}
            assert set(q["correct"]).issubset(choice_ids), q["id"]

    def test_sections_are_sem3_or_sem4(self):
        for q in MCQ:
            assert q.get("section") in ("sem3", "sem4"), q["id"]

    def test_4_video_cases(self):
        assert len(VIDEO_CASES) == 4
        for c in VIDEO_CASES:
            assert "id" in c
            assert "expected_key_point" in c
            assert "expected_decision" in c

    def test_video_rubric_has_3_criteria(self):
        assert len(VIDEO_RUBRIC["criteria"]) == 3
        for crit in VIDEO_RUBRIC["criteria"]:
            assert len(crit["scale"]) == 3

    def test_weights_sum_to_one(self):
        assert WEIGHTS["mcq"] + WEIGHTS["video"] == 1.0


class TestSeed:
    def test_upsert_creates_capa2_assessment(self, db, module_m2):
        a = _upsert_capa2(db, module_m2)
        assert a.type == "capa_2"
        assert a.lesson_id is None
        assert a.module_id == module_m2.id
        assert a.passing_score == PASSING_SCORE
        assert len(a.config["questions"]) == 16
        assert len(a.config["video_cases"]) == 4
        assert a.config["weights"] == {"mcq": 0.7, "video": 0.3}

    def test_upsert_is_idempotent(self, db, module_m2):
        a1 = _upsert_capa2(db, module_m2)
        a2 = _upsert_capa2(db, module_m2)
        assert a1.id == a2.id
        count = (
            db.query(Assessment)
            .filter(Assessment.module_id == module_m2.id, Assessment.type == "capa_2")
            .count()
        )
        assert count == 1


class TestAutoGradeIntegration:
    def test_auto_grade_all_correct(self, db, module_m2):
        a = _upsert_capa2(db, module_m2)
        student_answers = {}
        for q in MCQ:
            student_answers[q["id"]] = q["correct"]
        score = auto_grade_mcq(a, {"answers": student_answers})
        assert score == 100.0

    def test_auto_grade_zero_when_all_wrong(self, db, module_m2):
        a = _upsert_capa2(db, module_m2)
        wrong = {}
        for q in MCQ:
            if q["type"] == "single":
                wrong[q["id"]] = next(c["id"] for c in q["choices"] if c["id"] != q["correct"])
            elif q["type"] == "multi":
                wrong[q["id"]] = []
        score = auto_grade_mcq(a, {"answers": wrong})
        assert score == 0.0
