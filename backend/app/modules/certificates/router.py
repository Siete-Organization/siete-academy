from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logging import get_logger
from app.modules.auth.dependencies import CurrentUser, get_current_user, require_roles
from app.modules.certificates import services
from app.modules.certificates.models import Certificate
from app.modules.certificates.schemas import CertificateOut, CertificatePublic


class IssueRequest(BaseModel):
    user_id: int
    cohort_id: int

log = get_logger("app.certificates.router")
router = APIRouter()


@router.get("/me", response_model=list[CertificateOut])
def my_certificates(
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> list[Certificate]:
    return (
        db.query(Certificate)
        .filter(Certificate.user_id == current.user.id)
        .order_by(Certificate.issued_at.desc())
        .all()
    )


@router.post("/issue", response_model=CertificateOut)
def issue(
    body: IssueRequest,
    current: CurrentUser = Depends(require_roles("admin", "teacher")),
    db: Session = Depends(get_db),
) -> Certificate:
    """Admin o profesor fuerza la emisión (piloto / reemisión). Envía email en cuanto se crea."""
    cert = services.issue_if_eligible(db, user_id=body.user_id, cohort_id=body.cohort_id)
    if cert is None:
        log.warning(
            "certificate.issue_not_eligible",
            extra={"user_id": body.user_id, "cohort_id": body.cohort_id},
        )
        raise HTTPException(422, "User is not eligible (no enrollment or progress < 100%)")
    log.info(
        "certificate.issued_by_staff",
        extra={
            "certificate_id": cert.id,
            "user_id": body.user_id,
            "cohort_id": body.cohort_id,
            "actor_id": current.user.id,
            "actor_role": current.role,
        },
    )
    return cert


def _verify_limiter_decorator():
    """Lazy-resolve limiter to avoid circular import on app startup."""
    from app.main import limiter

    return limiter.limit("30/minute")


@router.get("/verify/{code}", response_model=CertificatePublic)
def verify(code: str, request: Request, db: Session = Depends(get_db)) -> dict:
    """Endpoint público — cualquiera puede verificar un código.

    Rate-limited per IP to prevent scraping/brute-forcing verification codes.
    """
    data = services.get_public(db, code)
    if data is None:
        log.info("certificate.verify_miss", extra={"code": code[:16]})
        raise HTTPException(404, "Certificate not found")
    log.info("certificate.verify_hit", extra={"code": code[:16]})
    return data


# Apply the rate limit at import time (handler accepts Request param now)
verify = _verify_limiter_decorator()(verify)
router.routes[-1].endpoint = verify
