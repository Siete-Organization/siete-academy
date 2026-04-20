from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logging import get_logger
from app.modules.auth.dependencies import CurrentUser, get_current_user, require_roles
from app.modules.cohorts.models import Cohort
from app.modules.enrollment.models import Enrollment, LessonProgress
from app.modules.enrollment.schemas import (
    EnrollmentCreate,
    EnrollmentOut,
    LessonProgressOut,
    LessonProgressUpdate,
)
from app.modules.users.models import User

log = get_logger("app.enrollment")
router = APIRouter()


@router.post("", response_model=EnrollmentOut, status_code=201)
def create_enrollment(
    body: EnrollmentCreate,
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> Enrollment:
    if not db.get(User, body.user_id):
        raise HTTPException(404, "User not found")
    if not db.get(Cohort, body.cohort_id):
        raise HTTPException(404, "Cohort not found")
    existing = (
        db.query(Enrollment)
        .filter(Enrollment.user_id == body.user_id, Enrollment.cohort_id == body.cohort_id)
        .first()
    )
    if existing:
        log.info(
            "enrollment.reused",
            extra={"user_id": body.user_id, "cohort_id": body.cohort_id, "enrollment_id": existing.id},
        )
        return existing
    e = Enrollment(user_id=body.user_id, cohort_id=body.cohort_id)
    db.add(e)
    db.commit()
    db.refresh(e)
    log.info(
        "enrollment.created",
        extra={"enrollment_id": e.id, "user_id": body.user_id, "cohort_id": body.cohort_id},
    )
    return e


@router.get("/me", response_model=list[EnrollmentOut])
def my_enrollments(
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Enrollment]:
    return (
        db.query(Enrollment)
        .filter(Enrollment.user_id == current.user.id)
        .order_by(Enrollment.enrolled_at.desc())
        .all()
    )


@router.post("/{enrollment_id}/progress", response_model=LessonProgressOut)
def update_progress(
    enrollment_id: int,
    body: LessonProgressUpdate,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> LessonProgress:
    enrollment = db.get(Enrollment, enrollment_id)
    if not enrollment:
        raise HTTPException(404, "Enrollment not found")
    if enrollment.user_id != current.user.id and current.role != "admin":
        raise HTTPException(403, "Not allowed")

    lp = (
        db.query(LessonProgress)
        .filter(
            LessonProgress.enrollment_id == enrollment_id,
            LessonProgress.lesson_id == body.lesson_id,
        )
        .first()
    )
    if lp is None:
        lp = LessonProgress(enrollment_id=enrollment_id, lesson_id=body.lesson_id)
        db.add(lp)

    lp.watched_pct = max(lp.watched_pct or 0.0, body.watched_pct)
    newly_completed = body.completed and lp.completed_at is None
    if newly_completed:
        lp.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(lp)
    if newly_completed:
        log.info(
            "lesson.completed",
            extra={
                "enrollment_id": enrollment_id,
                "lesson_id": body.lesson_id,
                "watched_pct": lp.watched_pct,
            },
        )
    return lp
