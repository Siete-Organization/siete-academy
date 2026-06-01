"""Tests para Capa 2 Módulo 3 — contenido + seed + auto_grade integration."""
import pytest

from app.modules.assessments.models import Assessment
from app.modules.assessments.services import auto_grade_mcq
from app.modules.courses.models import Course, Module, ModuleTranslation
from app.scripts.capa2_m3_questions import (
    MCQ,
    PASSING_SCORE,
    VIDEO_CASES,
    VIDEO_RUBRIC,
    WEIGHTS,
    total_question_count,
)
from app.scripts.seed_capa2_m3 import _upsert_capa2, MODULE_SLUG


@pytest.fixture
def module_m3(db) -> Module:
    course = Course(slug="sdr-academy-v1")
    db.add(course)
    db.commit()
    db.refresh(course)
    m = Module(course_id=course.id, slug=MODULE_SLUG, order_index=2)
    m.translations.append(
        ModuleTranslation(locale="es", title="M3", summary="La conexión")
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


class TestContent:
    def test_mcq_count_is_16(self):
        assert total_question_count() == 16

    def test_ids_use_m3_prefix(self):
        for q in MCQ:
            assert q["id"].startswith("M3."), q["id"]

    def test_ids_unique(self):
        ids = [q["id"] for q in MCQ]
        assert len(ids) == len(set(ids))

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

    def test_match_correct_keys_are_left_ids(self):
        for q in MCQ:
            if q["type"] != "match":
                continue
            left_ids = {item["id"] for item in q["left"]}
            right_ids = {item["id"] for item in q["right"]}
            assert set(q["correct"].keys()) == left_ids, q["id"]
            for right_id in q["correct"].values():
                assert right_id in right_ids, q["id"]

    def test_sections_are_sem5_or_sem6(self):
        for q in MCQ:
            assert q.get("section") in ("sem5", "sem6"), q["id"]

    def test_4_video_cases(self):
        assert len(VIDEO_CASES) == 4

    def test_video_rubric_has_3_criteria(self):
        assert len(VIDEO_RUBRIC["criteria"]) == 3

    def test_weights_sum_to_one(self):
        assert WEIGHTS["mcq"] + WEIGHTS["video"] == 1.0


class TestSeed:
    def test_upsert_creates_capa2_assessment(self, db, module_m3):
        a = _upsert_capa2(db, module_m3)
        assert a.type == "capa_2"
        assert a.lesson_id is None
        assert a.module_id == module_m3.id
        assert a.passing_score == PASSING_SCORE
        assert len(a.config["questions"]) == 16
        assert len(a.config["video_cases"]) == 4

    def test_upsert_is_idempotent(self, db, module_m3):
        a1 = _upsert_capa2(db, module_m3)
        a2 = _upsert_capa2(db, module_m3)
        assert a1.id == a2.id


class TestAutoGradeIntegration:
    def test_auto_grade_all_correct(self, db, module_m3):
        a = _upsert_capa2(db, module_m3)
        student_answers = {q["id"]: q["correct"] for q in MCQ}
        score = auto_grade_mcq(a, {"answers": student_answers})
        assert score == 100.0
