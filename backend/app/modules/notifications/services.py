"""SMTP email service.

Fase 0: stub que loguea el envío si SMTP no está configurado.
"""

import smtplib
from email.message import EmailMessage

from app.core.config import get_settings
from app.core.logging import get_logger

log = get_logger("app.notifications")


def send_email(*, to: str, subject: str, body_text: str, body_html: str | None = None) -> None:
    settings = get_settings()
    if not settings.smtp_host or not settings.smtp_user:
        log.info(
            "email.stubbed",
            extra={"to": to, "subject": subject, "reason": "smtp_not_configured"},
        )
        return

    msg = EmailMessage()
    msg["From"] = settings.smtp_from
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body_text)
    if body_html:
        msg.add_alternative(body_html, subtype="html")

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls()
            if settings.smtp_user and settings.smtp_password:
                server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(msg)
        log.info("email.sent", extra={"to": to, "subject": subject})
    except Exception as e:
        log.exception("email.failed", extra={"to": to, "subject": subject, "error": str(e)})
        raise
