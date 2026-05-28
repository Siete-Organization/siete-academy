"""Tests para Capa 2 Módulo 1 — contenido + seed + auto_grade integration."""
import pytest

from app.modules.assessments.models import Assessment
from app.modules.assessments.services import auto_grade_mcq
from app.modules.courses.models import Course, Module, ModuleTranslation
from app.scripts.capa2_m1_questions import (
    MCQ,
    PASSING_SCORE,
    VIDEO_CASES,
    VIDEO_RUBRIC,
    WEIGHTS,
    total_question_count,
)
from app.scripts.seed_capa2_m1 import _upsert_capa2, MODULE_SLUG


@pytest.fixture
def module_m1(db) -> Module:
    course = Course(slug="sdr-academy-v1")
    db.add(course)
    db.commit()
    db.refresh(course)
    m = Module(course_id=course.id, slug=MODULE_SLUG, order_index=0)
    m.translations.append(
        ModuleTranslation(locale="es", title="M1", summary="El juego y el jugador")
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

    def test_4_video_cases(self):
        assert len(VIDEO_CASES) == 4
        for c in VIDEO_CASES:
            assert "id" in c
            assert "expected_key_point" in c
            assert "expected_decision" in c

    def test_video_rubric_has_3_criteria_each_with_3_levels(self):
        assert len(VIDEO_RUBRIC["criteria"]) == 3
        for crit in VIDEO_RUBRIC["criteria"]:
            assert len(crit["scale"]) == 3

    def test_weights_sum_to_one(self):
        assert WEIGHTS["mcq"] + WEIGHTS["video"] == 1.0


class TestSeed:
    def test_upsert_creates_capa2_assessment(self, db, module_m1):
        a = _upsert_capa2(db, module_m1)
        assert a.type == "capa_2"
        assert a.lesson_id is None
        assert a.module_id == module_m1.id
        assert a.passing_score == PASSING_SCORE
        assert len(a.config["questions"]) == 16
        assert len(a.config["video_cases"]) == 4
        assert a.config["weights"] == {"mcq": 0.7, "video": 0.3}

    def test_upsert_is_idempotent(self, db, module_m1):
        a1 = _upsert_capa2(db, module_m1)
        a2 = _upsert_capa2(db, module_m1)
        assert a1.id == a2.id
        count = (
            db.query(Assessment)
            .filter(Assessment.module_id == module_m1.id, Assessment.type == "capa_2")
            .count()
        )
        assert count == 1


class TestAutoGradeIntegration:
    def test_auto_grade_mcq_handles_capa_2_type(self, db, module_m1):
        """auto_grade_mcq se extendió para soportar type='capa_2' además de 'mcq'."""
        a = _upsert_capa2(db, module_m1)
        # Construir un payload donde acierta todo
        student_answers = {}
        for q in MCQ:
            if q["type"] == "single":
                student_answers[q["id"]] = q["correct"]
            elif q["type"] == "multi":
                student_answers[q["id"]] = q["correct"]
            elif q["type"] == "match":
                student_answers[q["id"]] = q["correct"]
        score = auto_grade_mcq(a, {"answers": student_answers})
        assert score == 100.0

    def test_auto_grade_partial_correct(self, db, module_m1):
        a = _upsert_capa2(db, module_m1)
        # Acierta solo la primera (single)
        first = next(q for q in MCQ if q["type"] == "single")
        score = auto_grade_mcq(a, {"answers": {first["id"]: first["correct"]}})
        # 1 correcta de 16 → 6.25%
        assert score == round((1 / 16) * 100, 2)

    def test_auto_grade_zero_when_all_wrong(self, db, module_m1):
        a = _upsert_capa2(db, module_m1)
        wrong = {}
        for q in MCQ:
            if q["type"] == "single":
                # primera choice que no sea la correcta
                wrong[q["id"]] = next(c["id"] for c in q["choices"] if c["id"] != q["correct"])
            elif q["type"] == "multi":
                wrong[q["id"]] = []
            elif q["type"] == "match":
                wrong[q["id"]] = {}
        score = auto_grade_mcq(a, {"answers": wrong})
        assert score == 0.0
