"""SMTP email + Slack webhook services.

Fase 0: stubs que loguean el envío si las credenciales no están configuradas.
"""

import smtplib
from email.message import EmailMessage

import httpx

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


def send_slack_video_notify(
    *,
    student_name: str,
    student_email: str,
    module_label: str,
    video_url: str,
    assessment_title: str,
) -> None:
    """Notifica a Slack que un alumno subió el video de fin de módulo o Prueba Final.

    Si `SLACK_VIDEO_NOTIFY_URL` no está configurada, loguea y retorna sin error.
    Falla suave: cualquier excepción al POST se loguea pero no rompe la submission.
    """
    settings = get_settings()
    url = settings.slack_video_notify_url
    display_name = student_name or student_email

    if not url:
        log.info(
            "slack_video.stubbed",
            extra={
                "student_email": student_email,
                "module_label": module_label,
                "reason": "slack_url_not_configured",
            },
        )
        return

    text = (
        f":movie_camera: *{display_name}* subió el video de "
        f"*{module_label}* ({assessment_title})\n"
        f"<{video_url}|Ver entrega>"
    )
    payload = {"text": text}

    try:
        resp = httpx.post(url, json=payload, timeout=5.0)
        resp.raise_for_status()
        log.info(
            "slack_video.sent",
            extra={
                "student_email": student_email,
                "module_label": module_label,
            },
        )
    except Exception as e:
        # No re-raisear: una falla del webhook no debe romper la entrega del alumno.
        log.warning(
            "slack_video.failed",
            extra={
                "student_email": student_email,
                "module_label": module_label,
                "error": str(e),
            },
        )
