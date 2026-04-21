"""Teacher-facing endpoints: enriched review queue + cohort/student dashboard.

Isolated from `assessments` to keep the review-queue shape unchanged for
the admin analytics counters that still consume the lean SubmissionOut.
"""

from datetime import datetime

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logging import get_logger
from app.modules.assessments.models import Assessment, Submission, TeacherReview
from app.modules.auth.dependencies import CurrentUser, require_roles
from app.modules.certificates.models import Certificate
from app.modules.cohorts.models import Cohort
from app.modules.courses.models import Lesson, Module, ModuleTranslation
from app.modules.enrollment.models import Enrollment, LessonProgress
from app.modules.users.models import User

log = get_logger("app.teacher")
router = APIRouter()


class PendingReviewOut(BaseModel):
    submission_id: int
    assessment_id: int
    assessment_title: str
    assessment_type: str
    module_id: int | None
    module_title: str | None
    user_id: int
    user_name: str | None
    user_email: str | None
    submitted_at: datetime
    has_file: bool
    cohort_id: int | None


class CohortStats(BaseModel):
    cohort_id: int
    cohort_name: str
    status: str
    students_count: int
    avg_progress_pct: float
    pending_reviews: int


class StudentStats(BaseModel):
    user_id: int
    user_name: str | None
    user_email: str
    cohort_id: int
    cohort_name: str
    progress_pct: float
    lessons_completed: int
    avg_score: float | None
    last_activity_at: datetime | None
    has_certificate: bool


class DashboardOut(BaseModel):
    pending_reviews: int
    cohorts: list[CohortStats]
    students: list[StudentStats]


@router.get("/pending", response_model=list[PendingReviewOut])
def pending_enriched(
    q: str | None = Query(None, description="Búsqueda por nombre alumno o título de entrega"),
    assessment_id: int | None = Query(None),
    user_id: int | None = Query(None),
    limit: int = Query(100, ge=1, le=300),
    _teacher: CurrentUser = Depends(require_roles("teacher", "admin")),
    db: Session = Depends(get_db),
) -> list[dict]:
    """Cola enriquecida con nombre del alumno + título del entregable + módulo.

    Soporta filtros por alumno, por entregable, y búsqueda libre.
    """
    # Joins: Submission → Assessment → Module → User → Enrollment (cohort)
    stmt = (
        select(Submission, Assessment, Module, User, Enrollment)
        .join(Assessment, Assessment.id == Submission.assessment_id)
        .join(Module, Module.id == Assessment.module_id, isouter=True)
        .join(User, User.id == Submission.user_id)
        .join(Enrollment, Enrollment.user_id == User.id, isouter=True)
        .where(Submission.status == "pending_review")
        .order_by(Submission.submitted_at.asc())
        .limit(limit)
    )
    if assessment_id is not None:
        stmt = stmt.where(Submission.assessment_id == assessment_id)
    if user_id is not None:
        stmt = stmt.where(Submission.user_id == user_id)
    if q:
        needle = f"%{q.lower()}%"
        stmt = stmt.where(
            func.lower(User.display_name).like(needle)
            | func.lower(User.email).like(needle)
            | func.lower(Assessment.title).like(needle)
        )

    # Preload module translations (best-effort, en español default)
    mod_titles: dict[int, str] = {}
    module_ids = set()
    rows = db.execute(stmt).all()
    for _, _, m, _, _ in rows:
        if m:
            module_ids.add(m.id)
    if module_ids:
        trans = (
            db.query(ModuleTranslation)
            .filter(
                ModuleTranslation.module_id.in_(module_ids),
                ModuleTranslation.locale == "es",
            )
            .all()
        )
        mod_titles = {t.module_id: t.title for t in trans}

    return [
        {
            "submission_id": s.id,
            "assessment_id": a.id,
            "assessment_title": a.title,
            "assessment_type": a.type,
            "module_id": m.id if m else None,
            "module_title": mod_titles.get(m.id) if m else None,
            "user_id": u.id,
            "user_name": u.display_name,
            "user_email": u.email,
            "submitted_at": s.submitted_at,
            "has_file": bool(s.file_url),
            "cohort_id": e.cohort_id if e else None,
        }
        for s, a, m, u, e in rows
    ]


@router.get("/dashboard", response_model=DashboardOut)
def dashboard(
    _teacher: CurrentUser = Depends(require_roles("teacher", "admin")),
    db: Session = Depends(get_db),
) -> dict:
    """Snapshot del progreso por cohorte y por alumno. Pensado para una carga por pantalla."""
    # Pending reviews global
    pending_total = (
        db.query(func.count(Submission.id))
        .filter(Submission.status == "pending_review")
        .scalar()
        or 0
    )

    # Per-cohort stats
    cohorts = db.query(Cohort).order_by(Cohort.start_date.desc()).all()
    cohort_stats: list[dict] = []

    # Pre-compute pending per cohort via join through enrollment
    per_cohort_pending: dict[int, int] = {}
    pending_rows = db.execute(
        select(Enrollment.cohort_id, func.count(Submission.id))
        .select_from(Submission)
        .join(Enrollment, Enrollment.user_id == Submission.user_id)
        .where(Submission.status == "pending_review")
        .group_by(Enrollment.cohort_id)
    ).all()
    for cohort_id, cnt in pending_rows:
        if cohort_id is not None:
            per_cohort_pending[int(cohort_id)] = int(cnt)

    for c in cohorts:
        enrollments = (
            db.query(Enrollment).filter(Enrollment.cohort_id == c.id).all()
        )
        students_count = len(enrollments)
        avg_progress = (
            sum(e.progress_pct for e in enrollments) / students_count
            if students_count
            else 0.0
        )
        cohort_stats.append(
            {
                "cohort_id": c.id,
                "cohort_name": c.name,
                "status": c.status,
                "students_count": students_count,
                "avg_progress_pct": round(avg_progress, 1),
                "pending_reviews": per_cohort_pending.get(c.id, 0),
            }
        )

    # Per-student stats
    stmt = (
        select(Enrollment, User, Cohort)
        .join(User, User.id == Enrollment.user_id)
        .join(Cohort, Cohort.id == Enrollment.cohort_id)
        .where(User.role == "student")
        .order_by(Cohort.start_date.desc(), User.display_name.asc())
    )
    student_rows = db.execute(stmt).all()

    # Lessons completed per enrollment
    completed_rows = db.execute(
        select(LessonProgress.enrollment_id, func.count(LessonProgress.id))
        .where(LessonProgress.completed_at.is_not(None))
        .group_by(LessonProgress.enrollment_id)
    ).all()
    completed_by_enrollment = {int(eid): int(cnt) for eid, cnt in completed_rows}

    # Last activity per enrollment (max last_seen_at)
    activity_rows = db.execute(
        select(LessonProgress.enrollment_id, func.max(LessonProgress.last_seen_at))
        .group_by(LessonProgress.enrollment_id)
    ).all()
    last_activity_by_enrollment = {int(eid): ts for eid, ts in activity_rows}

    # Avg score per user (average of teacher reviews)
    score_rows = db.execute(
        select(Submission.user_id, func.avg(TeacherReview.score))
        .join(TeacherReview, TeacherReview.submission_id == Submission.id)
        .group_by(Submission.user_id)
    ).all()
    avg_score_by_user = {int(uid): float(score) for uid, score in score_rows}

    # Certificates issued per (user, cohort)
    cert_rows = db.execute(
        select(Certificate.user_id, Certificate.cohort_id)
    ).all()
    certs_by_pair = {(int(uid), int(cid)) for uid, cid in cert_rows}

    students = [
        {
            "user_id": u.id,
            "user_name": u.display_name,
            "user_email": u.email,
            "cohort_id": c.id,
            "cohort_name": c.name,
            "progress_pct": round(e.progress_pct, 1),
            "lessons_completed": completed_by_enrollment.get(e.id, 0),
            "avg_score": (
                round(avg_score_by_user[u.id], 1)
                if u.id in avg_score_by_user
                else None
            ),
            "last_activity_at": last_activity_by_enrollment.get(e.id),
            "has_certificate": (u.id, c.id) in certs_by_pair,
        }
        for e, u, c in student_rows
    ]

    return {
        "pending_reviews": int(pending_total),
        "cohorts": cohort_stats,
        "students": students,
    }
