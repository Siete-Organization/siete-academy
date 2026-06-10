from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.modules.applications.admission_grading import (
    decide_auto_decision,
    grade_mcq,
)
from app.modules.applications.models import Application
from app.modules.applications.schemas import ApplicationCreate

log = get_logger("app.applications")


def create_application(db: Session, data: ApplicationCreate) -> tuple[Application, bool]:
    """Crea la aplicación o devuelve la existente si el email ya aplicó.

    Una aplicación por email (la prueba da resultado al instante, así que
    permitir reenvíos abriría la puerta a re-tomar el MCQ). El reenvío del
    mismo email es idempotente: devuelve la fila original con su resultado.

    Returns (application, created): `created=False` cuando se devolvió una
    aplicación previa — el router usa esto para no re-notificar ni re-scorear.
    """
    existing = (
        db.query(Application)
        .filter(func.lower(Application.applicant_email) == str(data.applicant_email).lower())
        .order_by(Application.created_at.asc())
        .first()
    )
    if existing is not None:
        log.info(
            "application.duplicate_submit",
            extra={"application_id": existing.id, "email": existing.applicant_email},
        )
        return existing, False

    answers_dict = {a.question_id: a.text for a in data.answers}
    submitted_at = datetime.utcnow()
    # El front manda started_at en ISO con 'Z' (tz-aware); submitted_at y la
    # columna DateTime son naive-UTC. Normalizamos a naive-UTC para no romper
    # el speed check con "can't subtract offset-naive and offset-aware".
    started_at = data.started_at
    if started_at is not None and started_at.tzinfo is not None:
        started_at = started_at.astimezone(timezone.utc).replace(tzinfo=None)
    mcq_grade: dict[str, int] | None = None
    auto_decision: str | None = None
    if data.mcq_answers is not None:
        mcq_grade = grade_mcq(data.mcq_answers)
        auto_decision = decide_auto_decision(
            open_answers=answers_dict,
            mcq_score=mcq_grade["mcq_score"],
            mcq_excel_score=mcq_grade["mcq_excel_score"],
            started_at=started_at,
            submitted_at=submitted_at,
        )
    app = Application(
        applicant_name=data.applicant_name,
        applicant_email=str(data.applicant_email),
        applicant_phone=data.applicant_phone,
        linkedin_url=data.linkedin_url,
        country=data.country,
        locale=data.locale,
        answers=answers_dict,
        video_url=data.video_url,
        started_at=started_at,
        mcq_answers=data.mcq_answers,
        mcq_score=mcq_grade["mcq_score"] if mcq_grade else None,
        mcq_excel_score=mcq_grade["mcq_excel_score"] if mcq_grade else None,
        auto_decision=auto_decision,
        status="submitted",
    )
    db.add(app)
    db.commit()
    db.refresh(app)
    log.info(
        "application.created",
        extra={
            "application_id": app.id,
            "email": app.applicant_email,
            "locale": app.locale,
            "has_video": bool(app.video_url),
            "auto_decision": auto_decision,
            "mcq_score": app.mcq_score,
        },
    )
    return app, True


def review_application(
    db: Session,
    application_id: int,
    *,
    status: str,
    admin_notes: str | None,
    reviewer_id: int,
) -> Application | None:
    app = db.get(Application, application_id)
    if app is None:
        log.warning("application.review_not_found", extra={"application_id": application_id})
        return None
    prior = app.status
    app.status = status
    app.admin_notes = admin_notes
    app.reviewed_by_id = reviewer_id
    app.reviewed_at = datetime.utcnow()
    db.commit()
    db.refresh(app)
    log.info(
        "application.reviewed",
        extra={
            "application_id": app.id,
            "reviewer_id": reviewer_id,
            "from_status": prior,
            "to_status": status,
        },
    )
    return app
