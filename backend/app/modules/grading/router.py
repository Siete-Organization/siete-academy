"""Endpoint de resultados — usado por admin y teacher (read-only)."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logging import get_logger
from app.modules.assessments.models import Assessment, Submission
from app.modules.assessments.services import _question_is_correct
from app.modules.auth.dependencies import CurrentUser, require_roles
from app.modules.grading.aggregator import get_cohort_results
from app.modules.grading.schemas import CohortResultsOut

log = get_logger("app.grading")
router = APIRouter()


def _answer_text(answer: Any, choices: list[dict]) -> str | None:
    """Resuelve ids de opción a su texto legible (single/multi/match)."""
    if answer is None:
        return None
    cmap = {str(c.get("id")): c.get("text", str(c.get("id"))) for c in choices if isinstance(c, dict)}
    if isinstance(answer, list):
        return " · ".join(cmap.get(str(a), str(a)) for a in answer)
    if isinstance(answer, dict):
        return " · ".join(f"{k} → {cmap.get(str(v), str(v))}" for k, v in answer.items())
    return cmap.get(str(answer), str(answer))


@router.get("/submissions/review")
def submissions_review(
    user_id: int = Query(..., ge=1),
    module_id: int = Query(..., ge=1),
    current: CurrentUser = Depends(require_roles("admin", "teacher")),
    db: Session = Depends(get_db),
) -> list[dict]:
    """Entregas de un alumno en las pruebas de un módulo, con la revisión
    pregunta por pregunta (respuesta del alumno vs. la correcta configurada).

    Para que el profesor audite la corrección automática desde la vista de
    notas. Roles: admin y teacher. Devuelve todas las entregas (la más
    reciente primero) — puede haber reintentos.
    """
    assessments = (
        db.query(Assessment).filter(Assessment.module_id == module_id).all()
    )
    by_id = {a.id: a for a in assessments}
    if not by_id:
        return []
    subs = (
        db.query(Submission)
        .filter(
            Submission.user_id == user_id,
            Submission.assessment_id.in_(by_id.keys()),
        )
        .order_by(Submission.submitted_at.desc())
        .all()
    )
    out: list[dict] = []
    for s in subs:
        a = by_id[s.assessment_id]
        answers = (s.payload or {}).get("answers", {}) or {}
        questions = []
        for q in (a.config or {}).get("questions", []):
            qid = q.get("id")
            given = answers.get(qid)
            choices = q.get("choices", []) or []
            questions.append(
                {
                    "id": qid,
                    "prompt": q.get("prompt"),
                    "type": q.get("type", "single"),
                    "student_answer": _answer_text(given, choices),
                    "correct_answer": _answer_text(q.get("correct"), choices),
                    "is_correct": _question_is_correct(
                        q.get("type", "single"), q.get("correct"), given
                    ),
                }
            )
        out.append(
            {
                "submission_id": s.id,
                "assessment_id": a.id,
                "assessment_title": a.title,
                "assessment_type": a.type,
                "submitted_at": s.submitted_at.isoformat() if s.submitted_at else None,
                "status": s.status,
                "auto_score": s.auto_score,
                "video_url": s.file_url or (s.payload or {}).get("video_url"),
                "questions": questions,
            }
        )
    log.info(
        "grading.review_fetched",
        extra={"user_id": user_id, "module_id": module_id, "submissions": len(out), "actor_role": current.role},
    )
    return out


@router.get("/results", response_model=CohortResultsOut)
def cohort_results(
    cohort_id: int = Query(..., ge=1),
    course_id: int | None = Query(None, ge=1),
    locale: str = Query("es"),
    current: CurrentUser = Depends(require_roles("admin", "teacher")),
    db: Session = Depends(get_db),
) -> CohortResultsOut:
    """Tabla alumno × módulo × capa para una cohorte.

    Roles: admin y teacher (los teachers ven a sus alumnos también).
    """
    result = get_cohort_results(
        db, cohort_id=cohort_id, course_id=course_id, locale=locale
    )
    log.info(
        "grading.results_fetched",
        extra={
            "cohort_id": cohort_id,
            "course_id": course_id,
            "actor_role": current.role,
            "students": len(result.students),
        },
    )
    return CohortResultsOut(
        cohort_id=result.cohort_id,
        modules=[
            {"id": m["id"], "title": m["title"], "order_index": m["order_index"]}
            for m in result.modules
        ],
        students=[
            {
                "user_id": s.user_id,
                "name": s.name,
                "email": s.email,
                "modules": [
                    {
                        "module_id": mr.module_id,
                        "module_title": mr.module_title,
                        "order_index": mr.order_index,
                        "capa_1_scores": mr.capa_1_scores,
                        "capa_1_avg": mr.capa_1_avg,
                        "capa_2_mcq": mr.capa_2_mcq,
                        "capa_2_video": mr.capa_2_video,
                        "capa_2_score": mr.capa_2_score,
                    }
                    for mr in s.modules
                ],
                "final": {
                    "case": s.final.case,
                    "video": s.final.video,
                    "score": s.final.score,
                },
                "course_total": s.course_total,
                "status": s.status,
            }
            for s in result.students
        ],
    )
