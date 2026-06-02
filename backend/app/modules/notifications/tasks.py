from app.core.celery_app import celery_app
from app.modules.notifications.services import send_email, send_slack_video_notify


@celery_app.task(name="notifications.send_email")
def send_email_task(to: str, subject: str, body_text: str, body_html: str | None = None) -> None:
    send_email(to=to, subject=subject, body_text=body_text, body_html=body_html)


@celery_app.task(name="notifications.send_slack_video_notify")
def send_slack_video_notify_task(
    *,
    student_name: str,
    student_email: str,
    module_label: str,
    video_url: str,
    assessment_title: str,
) -> None:
    send_slack_video_notify(
        student_name=student_name,
        student_email=student_email,
        module_label=module_label,
        video_url=video_url,
        assessment_title=assessment_title,
    )
