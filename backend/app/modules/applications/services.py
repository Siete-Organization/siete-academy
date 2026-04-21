from datetime import datetime

from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.modules.applications.models import Application
from app.modules.applications.schemas import ApplicationCreate

log = get_logger("app.applications")


def create_application(db: Session, data: ApplicationCreate) -> Application:
    answers_dict = {a.question_id: a.text for a in data.answers}
    app = Application(
        applicant_name=data.applicant_name,
        applicant_email=str(data.applicant_email),
        applicant_phone=data.applicant_phone,
        linkedin_url=data.linkedin_url,
        country=data.country,
        locale=data.locale,
        answers=answers_dict,
        video_url=data.video_url,
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
        },
    )
    return app


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
