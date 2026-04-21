"""Generación y validación de certificados.

Fase 0: genera un "PDF" trivial (HTML→PDF se habilita en Fase 1 con WeasyPrint).
Por ahora solo guardamos verification_code + metadata. El PDF real se genera
en background cuando haya storage configurado.
"""

import secrets
from datetime import UTC, datetime

from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.modules.certificates.models import Certificate
from app.modules.cohorts.models import Cohort
from app.modules.enrollment.models import Enrollment
from app.modules.notifications.services import send_email
from app.modules.users.models import User

log = get_logger("app.certificates")


def _send_cert_email(user: User, cohort: Cohort, cert: Certificate) -> None:
    """Best-effort: logs if SMTP is not configured (Fase 0)."""
    holder = user.display_name or user.email
    locale = (user.locale or "es").lower()
    verify_url_hint = f"/academy/certificates/{cert.verification_code}"
    if locale.startswith("pt"):
        subject = f"Seu certificado Siete Academy — {cohort.name}"
        body = (
            f"Olá {holder},\n\n"
            f"Você concluiu a turma {cohort.name}. "
            "Aqui está seu certificado — compartilhe como quiser.\n\n"
            f"Código de verificação: {cert.verification_code}\n"
            f"Link público: {verify_url_hint}\n\n"
            "Parabéns.\n\n"
            "— Siete Academy"
        )
    elif locale.startswith("en"):
        subject = f"Your Siete Academy certificate — {cohort.name}"
        body = (
            f"Hi {holder},\n\n"
            f"You finished the {cohort.name} cohort. "
            "Your certificate is ready — share it anywhere.\n\n"
            f"Verification code: {cert.verification_code}\n"
            f"Public link: {verify_url_hint}\n\n"
            "Congrats.\n\n"
            "— Siete Academy"
        )
    else:
        subject = f"Tu certificado Siete Academy — {cohort.name}"
        body = (
            f"Hola {holder},\n\n"
            f"Culminaste la cohorte {cohort.name}. "
            "Aquí tienes tu certificado — compártelo donde quieras.\n\n"
            f"Código de verificación: {cert.verification_code}\n"
            f"Link público: {verify_url_hint}\n\n"
            "Felicidades.\n\n"
            "— Siete Academy"
        )
    try:
        send_email(to=user.email, subject=subject, body_text=body)
    except Exception as e:  # noqa: BLE001
        log.warning(
            "certificate.email_failed",
            extra={
                "certificate_id": cert.id,
                "user_id": user.id,
                "error": str(e),
            },
        )


def _gen_code() -> str:
    return secrets.token_urlsafe(12).replace("_", "").replace("-", "")[:16].upper()


def issue_if_eligible(
    db: Session, *, user_id: int, cohort_id: int
) -> Certificate | None:
    """Emite certificado solo si el alumno completó la cohorte (progress_pct >= 100)."""
    enrollment = (
        db.query(Enrollment)
        .filter_by(user_id=user_id, cohort_id=cohort_id)
        .first()
    )
    if enrollment is None:
        log.warning(
            "certificate.no_enrollment",
            extra={"user_id": user_id, "cohort_id": cohort_id},
        )
        return None
    if enrollment.progress_pct < 100.0:
        log.info(
            "certificate.not_yet_eligible",
            extra={
                "user_id": user_id,
                "cohort_id": cohort_id,
                "progress_pct": enrollment.progress_pct,
            },
        )
        return None

    existing = (
        db.query(Certificate).filter_by(user_id=user_id, cohort_id=cohort_id).first()
    )
    if existing:
        return existing

    cert = Certificate(
        user_id=user_id,
        cohort_id=cohort_id,
        verification_code=_gen_code(),
    )
    db.add(cert)
    enrollment.status = "completed"
    enrollment.completed_at = datetime.now(UTC)
    db.commit()
    db.refresh(cert)
    log.info(
        "certificate.issued",
        extra={
            "certificate_id": cert.id,
            "user_id": user_id,
            "cohort_id": cohort_id,
            "verification_code": cert.verification_code,
        },
    )
    user = db.get(User, user_id)
    cohort = db.get(Cohort, cohort_id)
    if user and cohort:
        _send_cert_email(user, cohort, cert)
    return cert


def get_public(db: Session, verification_code: str) -> dict | None:
    cert = (
        db.query(Certificate)
        .filter(Certificate.verification_code == verification_code)
        .first()
    )
    if cert is None:
        return None
    user = db.get(User, cert.user_id)
    cohort = db.get(Cohort, cert.cohort_id)
    return {
        "verification_code": cert.verification_code,
        "holder_name": user.display_name or user.email if user else "—",
        "cohort_name": cohort.name if cohort else "—",
        "issued_at": cert.issued_at,
        "valid": True,
    }
