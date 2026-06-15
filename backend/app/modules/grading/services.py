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

from typing import Any, Literal

from app.modules.assessments import services as assess_services
from app.modules.assessments.models import Assessment

Tier = Literal["capa_1", "capa_2", "capa_3", "other"]


def _num(v: Any) -> float:
    """Coerción tolerante a número (los puntos del profesor pueden venir como str)."""
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


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
GRAD_DISTINCTION_DIFFERENTIATOR = 75.0  # ≥75% acumulado en preguntas diferenciadoras


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


def final_case_score(
    config: dict,
    payload: dict | None,
    details: dict | None,
) -> float | None:
    """Nota del CASO de la Prueba Final (híbrido por ítem, doc líneas 12671-13503).

    caso% = (puntos MCQ + puntos respuestas cortas + puntos tablas) ÷ máximo × 100.

    - MCQ: auto-gradable, ponderado por ``points`` (default 1).
    - Respuestas cortas + tablas: las califica el profesor (`details`). Si el caso
      tiene componentes manuales y todavía no hay `details`, está incompleto → None.
      Si el caso es 100% MCQ (sin componentes manuales — p.ej. el rediseño de NICO),
      se autocalifica sin esperar al profesor.
    """
    questions = config.get("questions") or []
    short = config.get("short_answers") or []
    tables = config.get("tables") or []

    needs_manual = bool(short or tables)
    if needs_manual and details is None:
        return None

    mcq_earned, mcq_max = assess_services.sum_mcq_points(
        questions, (payload or {}).get("answers", {}) or {}
    )

    d_short = (details or {}).get("short_answers") or {}
    d_tables = (details or {}).get("tables") or {}
    sa_points = sum(_num(d_short.get(sa.get("id"))) for sa in short)
    sa_max = sum(_num(sa.get("max_points", 2)) for sa in short)
    tbl_points = sum(_num(d_tables.get(tb.get("id"))) for tb in tables)
    tbl_max = sum(_num(tb.get("max_points", 0)) for tb in tables)

    total_max = mcq_max + sa_max + tbl_max
    if total_max <= 0:
        return None
    earned = mcq_earned + sa_points + tbl_points
    return round(earned / total_max * 100, 2)


def final_video_score(config: dict, details: dict | None) -> float | None:
    """Nota del VIDEO de defensa (rúbrica /30 → %). Doc: 15 dimensiones × 0-2."""
    rubric = config.get("video_rubric") or {}
    max_total = _num(rubric.get("max_total"))
    d_video = (details or {}).get("video_rubric")
    if not d_video or max_total <= 0:
        return None
    points = sum(_num(v) for v in d_video.values())
    return round(points / max_total * 100, 2)


def differentiator_score(
    config: dict,
    payload: dict | None,
    details: dict | None,
) -> float | None:
    """% acumulado en las preguntas diferenciadoras del caso (req. de distinción).

    `differentiator_ids` mezcla MCQ (1 pto c/u, auto) y respuestas cortas (puntos
    del profesor /max). Devuelve None si falta el grading manual (`details`).
    """
    diff_ids = config.get("differentiator_ids") or []
    if not diff_ids:
        return None

    questions = {q.get("id"): q for q in (config.get("questions") or [])}
    shorts = {s.get("id"): s for s in (config.get("short_answers") or [])}
    tables = {t.get("id"): t for t in (config.get("tables") or [])}

    # Si alguna diferenciadora es respuesta corta/tabla, necesita grading manual.
    # Si todas son MCQ (rediseño de NICO), se autocalifica sin esperar al profesor.
    needs_manual = any((qid in shorts or qid in tables) for qid in diff_ids)
    if needs_manual and details is None:
        return None

    answers = (payload or {}).get("answers", {}) or {}
    d_short = (details or {}).get("short_answers") or {}
    d_tables = (details or {}).get("tables") or {}

    earned = 0.0
    max_pts = 0.0
    for qid in diff_ids:
        if qid in questions:
            q = questions[qid]
            pts = float(q.get("points", 1) or 1)
            max_pts += pts
            if assess_services.count_mcq_correct([q], answers):
                earned += pts
        elif qid in shorts:
            m = _num(shorts[qid].get("max_points", 2))
            max_pts += m
            earned += min(_num(d_short.get(qid)), m)
        elif qid in tables:
            m = _num(tables[qid].get("max_points", 0))
            max_pts += m
            earned += min(_num(d_tables.get(qid)), m)
    if max_pts <= 0:
        return None
    return round(earned / max_pts * 100, 2)


def video_critical_ok(config: dict, details: dict | None) -> bool | None:
    """¿El video alcanza el piso en las dimensiones críticas (req. de distinción)?

    Lee `video_rubric.critical_dimensions_for_distinction` (ids de dimensión) y el
    umbral `video_rubric.min_critical_points`; si no está, exige ~90% del máximo
    crítico (el doc dice "11/12 o 12/12" — bar casi perfecto en las críticas).
    """
    rubric = config.get("video_rubric") or {}
    crit = rubric.get("critical_dimensions_for_distinction") or []
    if not crit:
        return None
    d_video = (details or {}).get("video_rubric")
    if not d_video:
        return None
    crit_max = 2 * len(crit)
    threshold = rubric.get("min_critical_points")
    threshold = _num(threshold) if threshold is not None else round(0.9 * crit_max)
    earned = sum(_num(d_video.get(str(dim))) for dim in crit)
    return earned >= threshold


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
    differentiator_pct: float | None = None,
    video_critical_ok: bool | None = None,
) -> Literal["distinction", "basic", "failing", "in_progress"]:
    """Determina el estatus de graduación según umbrales del doc (líneas 1032-1043).

    - **distinction** (5 condiciones): nota final ≥85% + los 4 módulos ≥80% +
      prueba final ≥85% + ≥75% en preguntas diferenciadoras + rúbrica de video
      por encima del piso en las dimensiones críticas.
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
        and differentiator_pct is not None
        and differentiator_pct >= GRAD_DISTINCTION_DIFFERENTIATOR
        and video_critical_ok is True
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
