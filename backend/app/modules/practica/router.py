from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logging import get_logger
from app.modules.auth.dependencies import CurrentUser, get_current_user, require_roles
from app.modules.practica import services
from app.modules.practica.criteria import STAGE_DEFINITIONS
from app.modules.practica.models import PracticaCandidate
from app.modules.practica.schemas import (
    CandidateDetailOut,
    CandidateOut,
    InviteCandidate,
    StageTransition,
)

log = get_logger("app.practica.router")
router = APIRouter()


# ──────────────── Lectura abierta a alumnos ────────────────
# Stages + criterios son contenido descriptivo del programa — el alumno
# debe poder leerlos para entender qué le espera.


@router.get("/stages")
def list_stage_definitions() -> dict:
    return {"stages": STAGE_DEFINITIONS}


@router.get("/me", response_model=CandidateDetailOut | None)
def my_practica_status(
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PracticaCandidate | None:
    """Devuelve el candidato del usuario logueado, o null si no fue invitado."""
    return (
        db.query(PracticaCandidate)
        .filter_by(user_id=current.user.id)
        .first()
    )


# ──────────────── Admin ────────────────


@router.post("/candidates", response_model=CandidateOut, status_code=201)
def invite_candidate(
    body: InviteCandidate,
    current: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> PracticaCandidate:
    try:
        return services.invite(
            db,
            user_id=body.user_id,
            country_deel_ok=body.country_deel_ok,
            notes=body.notes,
            actor_id=current.user.id,
        )
    except ValueError as e:
        raise HTTPException(409, str(e))


@router.get("/candidates", response_model=list[CandidateOut])
def list_candidates(
    stage: str | None = None,
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> list[PracticaCandidate]:
    q = db.query(PracticaCandidate).order_by(PracticaCandidate.created_at.desc())
    if stage:
        q = q.filter(PracticaCandidate.stage == stage)
    return q.all()


@router.get("/candidates/{candidate_id}", response_model=CandidateDetailOut)
def get_candidate(
    candidate_id: int,
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> PracticaCandidate:
    c = db.get(PracticaCandidate, candidate_id)
    if not c:
        raise HTTPException(404, "candidate not found")
    return c


@router.post("/candidates/{candidate_id}/transition", response_model=CandidateDetailOut)
def transition_candidate(
    candidate_id: int,
    body: StageTransition,
    current: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> PracticaCandidate:
    c = db.get(PracticaCandidate, candidate_id)
    if not c:
        raise HTTPException(404, "candidate not found")
    try:
        return services.transition(
            db,
            c,
            to_stage=body.to_stage,
            reason=body.reason,
            monthly_usd=body.monthly_usd,
            actor_id=current.user.id,
        )
    except services.TransitionError as e:
        raise HTTPException(422, str(e))
