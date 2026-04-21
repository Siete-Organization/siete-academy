from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logging import get_logger
from app.modules.auth.dependencies import CurrentUser, get_current_user, require_roles
from app.modules.cohorts.models import Cohort
from app.modules.enrollment.models import Enrollment, LessonProgress
from app.modules.enrollment.schemas import (
    EnrollmentAdminOut,
    EnrollmentCreate,
    EnrollmentOut,
    EnrollmentUpdate,
    LessonProgressOut,
    LessonProgressUpdate,
)
from app.modules.notifications.services import send_email
from app.modules.users.models import User


def _send_welcome_email(user: User, cohort: Cohort) -> None:
    """Email de bienvenida al enrolar un alumno — incluye link de Slack si existe."""
    holder = user.display_name or user.email.split("@")[0]
    locale = (user.locale or "es").lower()
    slack_line = ""
    if cohort.slack_invite_url:
        if locale.startswith("pt"):
            slack_line = (
                f"\n\nEntre na comunidade Slack da sua turma: {cohort.slack_invite_url}"
                "\n(Guarde esse link — está também no seu perfil em Siete Academy.)"
            )
        elif locale.startswith("en"):
            slack_line = (
                f"\n\nJoin your cohort's Slack community: {cohort.slack_invite_url}"
                "\n(Save the link — it's also in your profile inside Siete Academy.)"
            )
        else:
            slack_line = (
                f"\n\nÚnete a la comunidad Slack de tu cohorte: {cohort.slack_invite_url}"
                "\n(Guarda el link — también está en tu perfil dentro de Siete Academy.)"
            )

    if locale.startswith("pt"):
        subject = f"Boas-vindas à {cohort.name} — Siete Academy"
        body = (
            f"Olá {holder},\n\n"
            f"Você foi matriculado na turma {cohort.name}.\n"
            "Seu acesso já está pronto em Siete Academy — você pode entrar agora "
            "com o mesmo email." + slack_line + "\n\nNos vemos lá.\n\n— Siete Academy"
        )
    elif locale.startswith("en"):
        subject = f"Welcome to {cohort.name} — Siete Academy"
        body = (
            f"Hi {holder},\n\n"
            f"You've been enrolled in {cohort.name}.\n"
            "Your access is live on Siete Academy — log in with the same email to start."
            + slack_line + "\n\nSee you inside.\n\n— Siete Academy"
        )
    else:
        subject = f"Bienvenido a {cohort.name} — Siete Academy"
        body = (
            f"Hola {holder},\n\n"
            f"Te enrolamos en la cohorte {cohort.name}.\n"
            "Tu acceso ya está listo en Siete Academy — entra con el mismo email para "
            "empezar." + slack_line + "\n\nNos vemos adentro.\n\n— Siete Academy"
        )
    try:
        send_email(to=user.email, subject=subject, body_text=body)
    except Exception as e:  # noqa: BLE001
        log.warning(
            "enrollment.welcome_email_failed",
            extra={"user_id": user.id, "cohort_id": cohort.id, "error": str(e)},
        )

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
    user = db.get(User, body.user_id)
    cohort = db.get(Cohort, body.cohort_id)
    if user and cohort:
        _send_welcome_email(user, cohort)
    return e


@router.get("/me", response_model=list[EnrollmentOut])
def my_enrollments(
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[dict]:
    rows = (
        db.query(Enrollment, Cohort)
        .join(Cohort, Cohort.id == Enrollment.cohort_id)
        .filter(Enrollment.user_id == current.user.id)
        .order_by(Enrollment.enrolled_at.desc())
        .all()
    )
    return [
        {
            "id": e.id,
            "user_id": e.user_id,
            "cohort_id": e.cohort_id,
            "cohort_name": c.name,
            "slack_invite_url": c.slack_invite_url,
            "status": e.status,
            "progress_pct": e.progress_pct,
            "enrolled_at": e.enrolled_at,
            "completed_at": e.completed_at,
        }
        for e, c in rows
    ]


@router.get("/by-cohort/{cohort_id}", response_model=list[EnrollmentAdminOut])
def list_by_cohort(
    cohort_id: int,
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> list[dict]:
    if not db.get(Cohort, cohort_id):
        raise HTTPException(404, "Cohort not found")
    rows = db.execute(
        select(Enrollment, User)
        .join(User, User.id == Enrollment.user_id)
        .where(Enrollment.cohort_id == cohort_id)
        .order_by(Enrollment.enrolled_at.desc())
    ).all()
    return [
        {
            "id": e.id,
            "user_id": u.id,
            "user_name": u.display_name,
            "user_email": u.email,
            "cohort_id": e.cohort_id,
            "status": e.status,
            "progress_pct": e.progress_pct,
            "enrolled_at": e.enrolled_at,
            "completed_at": e.completed_at,
        }
        for e, u in rows
    ]


@router.patch("/{enrollment_id}", response_model=EnrollmentOut)
def update_enrollment(
    enrollment_id: int,
    body: EnrollmentUpdate,
    current: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> Enrollment:
    """Admin: mover alumno de cohorte o cambiar status."""
    e = db.get(Enrollment, enrollment_id)
    if not e:
        raise HTTPException(404, "Enrollment not found")
    if body.cohort_id is not None and body.cohort_id != e.cohort_id:
        if not db.get(Cohort, body.cohort_id):
            raise HTTPException(404, "Target cohort not found")
        # Respetar el unique(user_id, cohort_id)
        conflict = (
            db.query(Enrollment)
            .filter(
                Enrollment.user_id == e.user_id,
                Enrollment.cohort_id == body.cohort_id,
            )
            .first()
        )
        if conflict:
            raise HTTPException(
                409, "Student already has an enrollment in the target cohort."
            )
        prior = e.cohort_id
        e.cohort_id = body.cohort_id
        log.info(
            "enrollment.moved",
            extra={
                "enrollment_id": e.id,
                "user_id": e.user_id,
                "from_cohort": prior,
                "to_cohort": body.cohort_id,
                "actor_id": current.user.id,
            },
        )
    if body.status is not None:
        if body.status not in ("active", "paused", "dropped", "completed"):
            raise HTTPException(422, "Invalid status")
        e.status = body.status
    db.commit()
    db.refresh(e)
    return e


@router.delete("/{enrollment_id}", status_code=204)
def delete_enrollment(
    enrollment_id: int,
    current: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> None:
    e = db.get(Enrollment, enrollment_id)
    if not e:
        raise HTTPException(404, "Enrollment not found")
    db.delete(e)
    db.commit()
    log.info(
        "enrollment.deleted",
        extra={"enrollment_id": enrollment_id, "actor_id": current.user.id},
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
