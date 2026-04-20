from app.core.celery_app import celery_app
from app.modules.notifications.services import send_email


@celery_app.task(name="notifications.send_email")
def send_email_task(to: str, subject: str, body_text: str, body_html: str | None = None) -> None:
    send_email(to=to, subject=subject, body_text=body_text, body_html=body_html)
