"""Grading formulas — puro, sin acceso a DB.

Fuente: SDR_Academy_Siete_Documento_Maestro.md, líneas 1032-1043 (umbrales),
4715 (módulo), 13488 (final), 13500 (curso).

Taxonomía de evaluaciones (clasificada en `classify_tier`):
- **capa_1** — micro-prueba semanal: Assessment.type == "mcq" con lesson_id.
- **capa_2** — prueba de módulo: Assessment.type == "capa_2", lesson_id NULL.
- **capa_3** — prueba final del curso: Assessment.type == "final_test".

Las fórmulas devuelven None cuando faltan piezas (no inferimos ni completamos).
La UI/aggregator decide cómo mostrar incompletos.
"""
from __future__ import annotations

from typing import Literal

from app.modules.assessments.models import Assessment

Tier = Literal["capa_1", "capa_2", "capa_3", "other"]


# Pesos del documento maestro
_CAPA2_WEIGHTS = {"mcq": 0.7, "video": 0.3}
_FINAL_WEIGHTS = {"case": 0.7, "video": 0.3}
_COURSE_WEIGHTS = {"micros": 0.20, "modules": 0.50, "final": 0.30}

# Umbrales de graduación (doc líneas 1032-1043)
GRAD_BASIC_COURSE = 70.0
GRAD_BASIC_MODULE = 65.0
GRAD_BASIC_FINAL = 60.0
GRAD_DISTINCTION_COURSE = 85.0
GRAD_DISTINCTION_MODULE = 80.0
GRAD_DISTINCTION_FINAL = 85.0


def classify_tier(assessment: Assessment) -> Tier:
    """Clasifica un Assessment en su capa (1/2/3) sin necesidad de un nuevo campo en DB."""
    if assessment.type == "mcq" and assessment.lesson_id is not None:
        return "capa_1"
    if assessment.type == "capa_2":
        return "capa_2"
    if assessment.type == "final_test":
        return "capa_3"
    return "other"


def module_test_score(mcq_pct: float | None, video_pct: float | None) -> float | None:
    """Nota de la prueba del módulo (Capa 2): (MCQ × 0.7) + (Video × 0.3).

    Doc maestro línea 4715. Devuelve None si falta cualquier componente.
    """
    if mcq_pct is None or video_pct is None:
        return None
    return round(mcq_pct * _CAPA2_WEIGHTS["mcq"] + video_pct * _CAPA2_WEIGHTS["video"], 2)


def final_test_score(case_pct: float | None, video_pct: float | None) -> float | None:
    """Nota de la Prueba Final (Capa 3): (Caso × 0.7) + (Video × 0.3).

    Doc maestro línea 13488. Devuelve None si falta cualquier componente.
    """
    if case_pct is None or video_pct is None:
        return None
    return round(case_pct * _FINAL_WEIGHTS["case"] + video_pct * _FINAL_WEIGHTS["video"], 2)


def course_final_score(
    *,
    micros_avg: float | None,
    modules_avg: float | None,
    final_pct: float | None,
) -> float | None:
    """Nota final del curso: (Micros × 0.20) + (Módulos × 0.50) + (Final × 0.30).

    Doc maestro línea 13500. Devuelve None si falta cualquier componente — no
    promediamos parcial porque la nota final no tiene sentido sin las 3 capas.
    """
    if micros_avg is None or modules_avg is None or final_pct is None:
        return None
    return round(
        micros_avg * _COURSE_WEIGHTS["micros"]
        + modules_avg * _COURSE_WEIGHTS["modules"]
        + final_pct * _COURSE_WEIGHTS["final"],
        2,
    )


def graduation_status(
    *,
    course_final: float | None,
    per_module_scores: list[float | None],
    final_pct: float | None,
) -> Literal["distinction", "basic", "failing", "in_progress"]:
    """Determina el estatus de graduación según umbrales del doc (líneas 1032-1043).

    - **distinction**: nota final ≥85% + los 4 módulos ≥80% + prueba final ≥85%.
    - **basic**: nota final ≥70% + ≥3 de 4 módulos ≥65% + prueba final ≥60%.
    - **failing**: terminó el curso (todas las capas presentes) y no llega a básico.
    - **in_progress**: aún no completó (alguna capa con None).
    """
    if course_final is None or final_pct is None:
        return "in_progress"
    if any(s is None for s in per_module_scores):
        return "in_progress"
    modules = [s for s in per_module_scores if s is not None]

    if (
        course_final >= GRAD_DISTINCTION_COURSE
        and final_pct >= GRAD_DISTINCTION_FINAL
        and all(s >= GRAD_DISTINCTION_MODULE for s in modules)
    ):
        return "distinction"

    if (
        course_final >= GRAD_BASIC_COURSE
        and final_pct >= GRAD_BASIC_FINAL
        and sum(1 for s in modules if s >= GRAD_BASIC_MODULE) >= 3
    ):
        return "basic"

    return "failing"


def average(scores: list[float | None]) -> float | None:
    """Promedio que ignora None. Devuelve None si la lista entera es None/vacía."""
    valid = [s for s in scores if s is not None]
    if not valid:
        return None
    return round(sum(valid) / len(valid), 2)
