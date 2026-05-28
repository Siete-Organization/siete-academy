"""Lógica de transiciones del path post-Academy.

Reglas de transición permitidas (Documento Maestro Parte IX):
- e1_invited → e1_active | declined | closed_camino_b
- e1_active → e2_active | closed_camino_b
- e2_active → e3_t2_active | closed_camino_b
- e3_t2_active → e3_t1_active | closed_camino_b
- e3_t1_active → closed_camino_b
- closed_camino_b → (terminal)
- declined → (terminal)

Stages remunerados (e2_active, e3_t2_active, e3_t1_active) requieren monthly_usd.
"""
from datetime import datetime

from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.modules.practica.models import PracticaCandidate, PracticaStageEvent

log = get_logger("app.practica")


ALLOWED_TRANSITIONS: dict[str, set[str]] = {
    "e1_invited": {"e1_active", "declined", "closed_camino_b"},
    "e1_active": {"e2_active", "closed_camino_b"},
    "e2_active": {"e3_t2_active", "closed_camino_b"},
    "e3_t2_active": {"e3_t1_active", "closed_camino_b"},
    "e3_t1_active": {"closed_camino_b"},
    "closed_camino_b": set(),
    "declined": set(),
}

PAID_STAGES: set[str] = {"e2_active", "e3_t2_active", "e3_t1_active"}


def invite(
    db: Session,
    *,
    user_id: int,
    country_deel_ok: bool,
    notes: str | None,
    actor_id: int,
) -> PracticaCandidate:
    """Crea un nuevo candidato en `e1_invited`. Si ya existe, levanta ValueError."""
    if db.query(PracticaCandidate).filter_by(user_id=user_id).first():
        raise ValueError("candidate already exists for this user")
    candidate = PracticaCandidate(
        user_id=user_id,
        stage="e1_invited",
        country_deel_ok=country_deel_ok,
        notes=notes,
    )
    db.add(candidate)
    db.flush()
    event = PracticaStageEvent(
        candidate_id=candidate.id,
        from_stage=None,
        to_stage="e1_invited",
        reason="invitación inicial",
        actor_id=actor_id,
    )
    db.add(event)
    db.commit()
    db.refresh(candidate)
    log.info(
        "practica.invited",
        extra={"candidate_id": candidate.id, "user_id": user_id, "actor_id": actor_id},
    )
    return candidate


class TransitionError(ValueError):
    """Transición inválida o falta info requerida (ej. monthly_usd)."""


def transition(
    db: Session,
    candidate: PracticaCandidate,
    *,
    to_stage: str,
    reason: str | None,
    monthly_usd: int | None,
    actor_id: int,
) -> PracticaCandidate:
    if to_stage not in ALLOWED_TRANSITIONS.get(candidate.stage, set()):
        raise TransitionError(
            f"transition {candidate.stage} -> {to_stage} not allowed"
        )
    if to_stage in PAID_STAGES and monthly_usd is None:
        raise TransitionError(f"stage {to_stage} requires monthly_usd")
    if not candidate.country_deel_ok and to_stage in PAID_STAGES:
        raise TransitionError(
            "country not supported by Deel — cannot enter paid stage"
        )

    event = PracticaStageEvent(
        candidate_id=candidate.id,
        from_stage=candidate.stage,
        to_stage=to_stage,
        reason=reason,
        actor_id=actor_id,
    )
    candidate.stage = to_stage
    candidate.entered_stage_at = datetime.utcnow()
    if to_stage in PAID_STAGES:
        candidate.monthly_usd = monthly_usd
    elif to_stage in {"closed_camino_b", "declined", "e1_invited", "e1_active"}:
        candidate.monthly_usd = None
    db.add(event)
    db.commit()
    db.refresh(candidate)
    log.info(
        "practica.transitioned",
        extra={
            "candidate_id": candidate.id,
            "from_stage": event.from_stage,
            "to_stage": to_stage,
            "actor_id": actor_id,
        },
    )
    return candidate
