"""Celery tasks for applications.

Fase 0: sólo envía email de confirmación al aspirante y notificación a admin.
Fase 1: agregar pipeline de scoring con Claude.
"""

from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.core.logging import get_logger
from app.modules.applications.models import Application
from app.modules.notifications.services import send_email

log = get_logger("app.applications.tasks")


@celery_app.task(name="applications.notify_submitted")
def notify_submitted(application_id: int) -> None:
    db = SessionLocal()
    try:
        app = db.get(Application, application_id)
        if app is None:
            log.warning("application.notify_submitted_missing", extra={"application_id": application_id})
            return
        log.info("application.notify_submitted", extra={"application_id": application_id})
        send_email(
            to=app.applicant_email,
            subject="Recibimos tu aplicación — Siete Academy",
            body_text=(
                f"Hola {app.applicant_name},\n\n"
                "Gracias por aplicar a Siete Academy. Revisaremos tu aplicación "
                "y te contactaremos en los próximos días.\n\nEquipo Siete"
            ),
        )
    finally:
        db.close()


@celery_app.task(name="applications.notify_decision")
def notify_decision(application_id: int) -> None:
    db = SessionLocal()
    try:
        app = db.get(Application, application_id)
        if app is None:
            log.warning("application.notify_decision_missing", extra={"application_id": application_id})
            return
        log.info(
            "application.notify_decision",
            extra={"application_id": application_id, "status": app.status},
        )
        if app.status == "approved":
            subject = "¡Fuiste aceptado en Siete Academy!"
            body = (
                f"Hola {app.applicant_name},\n\n"
                "¡Felicitaciones! Fuiste aceptado en la próxima cohorte. "
                "Pronto recibirás un link para completar tu registro."
            )
        elif app.status == "rejected":
            subject = "Actualización sobre tu aplicación a Siete Academy"
            body = (
                f"Hola {app.applicant_name},\n\n"
                "Gracias por aplicar. En esta ocasión no podremos avanzar contigo, "
                "pero te animamos a aplicar a futuras cohortes."
            )
        else:
            return
        send_email(to=app.applicant_email, subject=subject, body_text=body)
    finally:
        db.close()
