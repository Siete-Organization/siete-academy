"""Tests unitarios de las fórmulas del módulo grading.

Replica los ejemplos numéricos del Doc Maestro:
- Módulo: línea 4715-4719 (M1: 87.5 + 83.33 → 86.25%).
- Final: línea 13488-13496 (caso 76.4 + video 80 → 77.5%).
- Curso: línea 13500 (micro 20% + módulos 50% + final 30%).
- Umbrales: línea 1032-1043 (básico/distinción).
"""
from __future__ import annotations

from app.modules.assessments.models import Assessment
from app.modules.grading import services as grading


def _make_assessment(*, type_: str, lesson_id: int | None = None) -> Assessment:
    a = Assessment()
    a.type = type_
    a.lesson_id = lesson_id
    a.module_id = 1
    a.title = "x"
    a.config = {}
    a.passing_score = 70.0
    return a


# ───────────────────────── classify_tier ─────────────────────────


def test_classify_mcq_with_lesson_is_capa1():
    a = _make_assessment(type_="mcq", lesson_id=10)
    assert grading.classify_tier(a) == "capa_1"


def test_classify_mcq_without_lesson_is_other():
    # MCQ a nivel módulo no es ni micro (no tiene lesson) ni prueba de módulo
    a = _make_assessment(type_="mcq", lesson_id=None)
    assert grading.classify_tier(a) == "other"


def test_classify_capa2_is_capa2():
    a = _make_assessment(type_="capa_2", lesson_id=None)
    assert grading.classify_tier(a) == "capa_2"


def test_classify_final_test_is_capa3():
    a = _make_assessment(type_="final_test", lesson_id=None)
    assert grading.classify_tier(a) == "capa_3"


def test_classify_unknown_is_other():
    a = _make_assessment(type_="written")
    assert grading.classify_tier(a) == "other"


# ───────────────────────── module_test_score ─────────────────────────


def test_module_score_matches_doc_example_m1():
    # Doc maestro línea 4715: MCQ 87.5 + Video 83.33 → 86.25
    assert grading.module_test_score(87.5, 83.33) == 86.25


def test_module_score_returns_none_when_mcq_missing():
    assert grading.module_test_score(None, 80.0) is None


def test_module_score_returns_none_when_video_missing():
    assert grading.module_test_score(80.0, None) is None


def test_module_score_perfect_inputs():
    assert grading.module_test_score(100.0, 100.0) == 100.0


# ───────────────────────── final_test_score ─────────────────────────


def test_final_score_matches_doc_example():
    # Doc maestro línea 13488: Caso 76.4 + Video 80 → 77.48 (redondeo a 2)
    assert grading.final_test_score(76.4, 80.0) == 77.48


def test_final_score_returns_none_when_case_missing():
    assert grading.final_test_score(None, 80.0) is None


def test_final_score_returns_none_when_video_missing():
    assert grading.final_test_score(70.0, None) is None


# ───────────────────────── course_final_score ─────────────────────────


def test_course_final_score_returns_none_if_any_missing():
    assert (
        grading.course_final_score(micros_avg=80.0, modules_avg=None, final_pct=90.0)
        is None
    )
    assert (
        grading.course_final_score(micros_avg=None, modules_avg=80.0, final_pct=90.0)
        is None
    )
    assert (
        grading.course_final_score(micros_avg=80.0, modules_avg=80.0, final_pct=None)
        is None
    )


def test_course_final_score_uses_weights():
    # 80 * 0.20 + 90 * 0.50 + 70 * 0.30 = 16 + 45 + 21 = 82
    assert (
        grading.course_final_score(micros_avg=80.0, modules_avg=90.0, final_pct=70.0)
        == 82.0
    )


# ───────────────────────── graduation_status ─────────────────────────


def test_grad_in_progress_when_course_total_none():
    assert (
        grading.graduation_status(
            course_final=None,
            per_module_scores=[80.0] * 4,
            final_pct=80.0,
        )
        == "in_progress"
    )


def test_grad_in_progress_when_any_module_none():
    assert (
        grading.graduation_status(
            course_final=82.0,
            per_module_scores=[80.0, None, 80.0, 80.0],
            final_pct=80.0,
        )
        == "in_progress"
    )


def test_grad_distinction_threshold():
    # Los 4 módulos ≥80, final ≥85, curso ≥85
    assert (
        grading.graduation_status(
            course_final=88.0,
            per_module_scores=[85.0, 82.0, 90.0, 88.0],
            final_pct=86.0,
        )
        == "distinction"
    )


def test_grad_distinction_fails_if_one_module_below_80():
    # Un módulo con 78 < 80 → no califica para distinción aun con curso alto
    assert (
        grading.graduation_status(
            course_final=88.0,
            per_module_scores=[85.0, 78.0, 90.0, 88.0],
            final_pct=86.0,
        )
        == "basic"  # cae a básico
    )


def test_grad_basic_threshold_three_modules_pass():
    # Doc: ≥3 de 4 módulos con ≥65%, curso ≥70%, final ≥60%
    assert (
        grading.graduation_status(
            course_final=72.0,
            per_module_scores=[68.0, 65.0, 70.0, 50.0],  # 3 de 4 pasan
            final_pct=62.0,
        )
        == "basic"
    )


def test_grad_failing_when_only_two_modules_pass():
    # Solo 2 de 4 módulos ≥65 → no llega a básico
    assert (
        grading.graduation_status(
            course_final=72.0,
            per_module_scores=[68.0, 50.0, 70.0, 50.0],
            final_pct=62.0,
        )
        == "failing"
    )


def test_grad_failing_when_final_below_60():
    assert (
        grading.graduation_status(
            course_final=72.0,
            per_module_scores=[70.0, 70.0, 70.0, 70.0],
            final_pct=55.0,
        )
        == "failing"
    )


# ───────────────────────── average ─────────────────────────


def test_average_ignores_none():
    assert grading.average([80.0, None, 100.0]) == 90.0


def test_average_returns_none_for_all_none():
    assert grading.average([None, None]) is None


def test_average_returns_none_for_empty():
    assert grading.average([]) is None
