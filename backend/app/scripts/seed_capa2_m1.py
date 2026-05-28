"""Seed: Prueba del Módulo 1 — Capa 2.

Crea/actualiza una Assessment de type="capa_2" sin lesson_id (a nivel módulo),
con las 16 MCQ + banco de 4 casos de video + rúbrica + pesos 70/30.

Asume que el schema ya está migrado y que el Módulo 1 ya existe en DB
(typically creado por seed_w1.py). Idempotente: re-ejecutable.

Uso:
    cd backend && .venv/bin/python -m app.scripts.seed_capa2_m1
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
from app.scripts.capa2_m1_questions import (
    MCQ,
    PASSING_SCORE,
    VIDEO_CASES,
    VIDEO_RUBRIC,
    WEIGHTS,
)

configure_logging()
log = get_logger("seed_capa2_m1")

MODULE_SLUG = "m1-juego-y-jugador"
ASSESSMENT_TITLE = "Prueba del Módulo 1 (Capa 2)"


def _capa2_config() -> dict:
    return {
        "tier": "capa_2",
        "weights": WEIGHTS,
        "questions": MCQ,
        "video_cases": VIDEO_CASES,
        "video_rubric": VIDEO_RUBRIC,
        "rules": {
            "single_attempt": True,
            "seconds_per_question": 90,
            "video_min_minutes": 3,
            "video_max_minutes": 5,
            "submission_window_hours": 48,
        },
    }


def _upsert_capa2(db, module: Module) -> Assessment:
    existing = (
        db.query(Assessment)
        .filter(
            Assessment.module_id == module.id,
            Assessment.type == "capa_2",
            Assessment.lesson_id.is_(None),
        )
        .first()
    )
    config = _capa2_config()
    if existing is None:
        a = Assessment(
            module_id=module.id,
            lesson_id=None,
            type="capa_2",
            title=ASSESSMENT_TITLE,
            config=config,
            passing_score=PASSING_SCORE,
        )
        db.add(a)
        db.commit()
        db.refresh(a)
        log.info("capa2.created", extra={"assessment_id": a.id, "module_id": module.id})
        return a
    existing.title = ASSESSMENT_TITLE
    existing.config = config
    existing.passing_score = PASSING_SCORE
    db.commit()
    db.refresh(existing)
    log.info("capa2.updated", extra={"assessment_id": existing.id, "module_id": module.id})
    return existing


def run() -> None:
    db = SessionLocal()
    try:
        module = db.query(Module).filter(Module.slug == MODULE_SLUG).first()
        if module is None:
            raise RuntimeError(
                f"Module '{MODULE_SLUG}' no existe. Corré seed_w1 antes."
            )
        a = _upsert_capa2(db, module)
        log.info(
            "seed_capa2_m1.done",
            extra={
                "assessment_id": a.id,
                "module_id": module.id,
                "mcq_count": len(MCQ),
                "video_cases": len(VIDEO_CASES),
            },
        )
    finally:
        db.close()


if __name__ == "__main__":
    run()
