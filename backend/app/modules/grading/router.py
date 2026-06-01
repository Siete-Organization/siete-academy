"""Endpoint de resultados — usado por admin y teacher (read-only)."""
from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logging import get_logger
from app.modules.auth.dependencies import CurrentUser, require_roles
from app.modules.grading.aggregator import get_cohort_results
from app.modules.grading.schemas import CohortResultsOut

log = get_logger("app.grading")
router = APIRouter()


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
