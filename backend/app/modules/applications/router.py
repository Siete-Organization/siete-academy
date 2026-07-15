from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.limiter import limiter
from app.core.logging import get_logger
from app.modules.ai_review.tasks import score_application_task
from app.modules.applications import services
from app.modules.applications.models import Application
from app.modules.applications.schemas import (
    ApplicationCreate,
    ApplicationListOut,
    ApplicationOut,
    ApplicationReview,
)
from app.modules.applications.tasks import notify_decision, notify_submitted
from app.modules.auth.dependencies import CurrentUser, require_roles

log = get_logger("app.applications.router")
router = APIRouter()


@router.post("", response_model=ApplicationOut, status_code=201)
# 60/hour/IP: las universidades comparten una IP pública (NAT), así que el
# límite tiene que dar aire a un aula entera postulando en la misma hora. El
# "una aplicación por persona" lo garantiza la dedup por email, no este
# límite, que solo frena spam de bots. Requiere que gunicorn corra con
# --forwarded-allow-ips para ver la IP real (si no, TODOS los alumnos
# comparten la IP del proxy y el bucket es global — incidente 2026-07-14).
@limiter.limit("60/hour")
def submit_application(
    body: ApplicationCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
) -> Application:
    """Endpoint público — no requiere auth. El aspirante aún no tiene cuenta.

    Rate-limited to 20/hour/IP to prevent bot spam (shared university NATs need
    headroom; duplicate real applications are prevented by per-email dedup).

    Devuelve 201 cuando se crea la aplicación y 200 cuando el email ya había
    aplicado (el front usa ese status para avisar amigablemente al aspirante).
    """
    app, created = services.create_application(db, body)
    # Reenvío del mismo email: devolvemos la aplicación existente sin
    # re-notificar ni re-scorear (idempotente). 200 ⇒ "ya aplicaste".
    if not created:
        response.status_code = 200
        return app
    # La aplicación ya está persistida: un fallo al encolar notificaciones o
    # scoring no debe romper el envío del aspirante (si no, ve "Network Error").
    try:
        notify_submitted.delay(app.id)
    except Exception as e:
        log.warning(
            "notify.submit_queue_failed",
            extra={"application_id": app.id, "error": str(e)},
        )
    try:
        score_application_task.delay(app.id)
    except Exception as e:
        log.warning(
            "ai.score_queue_failed",
            extra={"application_id": app.id, "error": str(e)},
        )
    return app


@router.get("", response_model=list[ApplicationListOut])
def list_applications(
    status: str | None = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> list[Application]:
    q = db.query(Application).order_by(Application.created_at.desc())
    if status:
        q = q.filter(Application.status == status)
    return q.offset(offset).limit(limit).all()


@router.get("/{application_id}", response_model=ApplicationOut)
def get_application(
    application_id: int,
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> Application:
    app = db.get(Application, application_id)
    if not app:
        raise HTTPException(404, "Application not found")
    return app


@router.post("/{application_id}/review", response_model=ApplicationOut)
def review(
    application_id: int,
    body: ApplicationReview,
    current: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> Application:
    app = services.review_application(
        db,
        application_id,
        status=body.status,
        admin_notes=body.admin_notes,
        reviewer_id=current.user.id,
    )
    if not app:
        raise HTTPException(404, "Application not found")
    if body.status in ("approved", "rejected"):
        notify_decision.delay(app.id)
    return app
