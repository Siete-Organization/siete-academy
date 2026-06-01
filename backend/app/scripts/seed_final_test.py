"""Seed: Prueba Final del curso — Capa 3 (caso GestaLogix).

Crea/actualiza una Assessment de type="final_test" asociada al Módulo 4
(el examen final se entrega al cierre de Sem 8). Idempotente.

Uso:
    cd backend && .venv/bin/python -m app.scripts.seed_final_test
"""
from __future__ import annotations

from app.core.database import SessionLocal
from app.core.logging import configure_logging, get_logger
from app.modules.assessments.models import Assessment
from app.modules.assessments import models as _assess  # noqa: F401
from app.modules.audit import models as _audit  # noqa: F401
from app.modules.courses.models import Module
from app.modules.courses import models as _courses  # noqa: F401
from app.modules.users import models as _users  # noqa: F401
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
)

configure_logging()
log = get_logger("seed_final_test")

# Anclamos el examen final al Módulo 4 (cierre del curso).
# El motor de grading lo identifica por type="final_test", no por module_id.
MODULE_SLUG = "m4-el-sistema"
ASSESSMENT_TITLE = "Prueba Final del curso — Caso GestaLogix (Capa 3)"


def _final_config() -> dict:
    return {
        "tier": "capa_3",
        "weights": WEIGHTS,
        "case_brief": CASE_BRIEF,
        # MCQ auto-gradable (compatible con auto_grade_mcq):
        "questions": MCQ,
        # Resto del caso: respuestas cortas + tablas (manual):
        "short_answers": SHORT_ANSWERS,
        "tables": TABLES,
        "differentiator_ids": DIFFERENTIATOR_IDS,
        "short_rubric": GENERIC_SHORT_RUBRIC,
        "video_rubric": VIDEO_RUBRIC_15,
        "rules": {
            "single_attempt_case": True,
            "open_book": True,
            "no_ai_or_sharing": True,
            "stages_sequential": True,
            "video_attempts_max": 2,
            "video_duration_minutes": 15,
            "submission_window_days": 5,
            "total_case_hours": 2.5,
        },
    }


def _upsert_final(db, module: Module) -> Assessment:
    existing = (
        db.query(Assessment)
        .filter(Assessment.type == "final_test")
        .first()
    )
    config = _final_config()
    if existing is None:
        a = Assessment(
            module_id=module.id,
            lesson_id=None,
            type="final_test",
            title=ASSESSMENT_TITLE,
            config=config,
            passing_score=PASSING_SCORE,
        )
        db.add(a)
        db.commit()
        db.refresh(a)
        log.info("final_test.created", extra={"assessment_id": a.id, "module_id": module.id})
        return a
    existing.module_id = module.id
    existing.title = ASSESSMENT_TITLE
    existing.config = config
    existing.passing_score = PASSING_SCORE
    db.commit()
    db.refresh(existing)
    log.info("final_test.updated", extra={"assessment_id": existing.id, "module_id": module.id})
    return existing


def run() -> None:
    db = SessionLocal()
    try:
        module = db.query(Module).filter(Module.slug == MODULE_SLUG).first()
        if module is None:
            raise RuntimeError(
                f"Module '{MODULE_SLUG}' no existe. Corré seed_w7 antes."
            )
        a = _upsert_final(db, module)
        log.info(
            "seed_final_test.done",
            extra={
                "assessment_id": a.id,
                "module_id": module.id,
                "mcq_count": len(MCQ),
                "short_answers": len(SHORT_ANSWERS),
                "tables": len(TABLES),
                "differentiator_count": len(DIFFERENTIATOR_IDS),
            },
        )
    finally:
        db.close()


if __name__ == "__main__":
    run()
