from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.modules.placement.models import STAGES, PlacementCandidate, PlacementEvent

log = get_logger("app.placement")


def _record_event(
    db: Session,
    candidate: PlacementCandidate,
    *,
    event_type: str,
    data: dict,
    actor_id: int | None,
) -> PlacementEvent:
    e = PlacementEvent(
        candidate_id=candidate.id,
        event_type=event_type,
        data=data,
        actor_id=actor_id,
    )
    db.add(e)
    return e


def create_or_get_candidate(
    db: Session,
    *,
    user_id: int,
    cohort_id: int | None,
    summary: str | None,
    portfolio_url: str | None,
    actor_id: int | None,
) -> PlacementCandidate:
    existing = db.query(PlacementCandidate).filter_by(user_id=user_id).first()
    if existing:
        log.info(
            "placement.candidate_exists",
            extra={"candidate_id": existing.id, "user_id": user_id},
        )
        return existing
    c = PlacementCandidate(
        user_id=user_id,
        cohort_id=cohort_id,
        stage="applying",
        summary=summary,
        portfolio_url=portfolio_url,
    )
    db.add(c)
    db.flush()
    _record_event(
        db,
        c,
        event_type="created",
        data={"cohort_id": cohort_id},
        actor_id=actor_id,
    )
    db.commit()
    db.refresh(c)
    log.info(
        "placement.candidate_created",
        extra={"candidate_id": c.id, "user_id": user_id, "cohort_id": cohort_id},
    )
    return c


def move_stage(
    db: Session,
    *,
    candidate_id: int,
    stage: str,
    note: str | None,
    actor_id: int | None,
) -> PlacementCandidate | None:
    if stage not in STAGES:
        raise ValueError(f"Invalid stage '{stage}'")
    c = db.get(PlacementCandidate, candidate_id)
    if c is None:
        log.warning("placement.move_not_found", extra={"candidate_id": candidate_id})
        return None
    prior = c.stage
    if prior == stage:
        return c
    c.stage = stage
    _record_event(
        db,
        c,
        event_type="stage_changed",
        data={"from": prior, "to": stage, "note": note},
        actor_id=actor_id,
    )
    db.commit()
    db.refresh(c)
    log.info(
        "placement.stage_changed",
        extra={
            "candidate_id": candidate_id,
            "from_stage": prior,
            "to_stage": stage,
        },
    )
    return c


def assign_admin(
    db: Session, *, candidate_id: int, admin_id: int | None, actor_id: int | None
) -> PlacementCandidate | None:
    c = db.get(PlacementCandidate, candidate_id)
    if c is None:
        return None
    prior = c.assigned_admin_id
    c.assigned_admin_id = admin_id
    _record_event(
        db,
        c,
        event_type="assigned",
        data={"from": prior, "to": admin_id},
        actor_id=actor_id,
    )
    db.commit()
    db.refresh(c)
    log.info(
        "placement.assigned",
        extra={"candidate_id": candidate_id, "admin_id": admin_id},
    )
    return c


def add_note(
    db: Session, *, candidate_id: int, note: str, actor_id: int | None
) -> PlacementCandidate | None:
    c = db.get(PlacementCandidate, candidate_id)
    if c is None:
        return None
    c.notes = (c.notes + "\n\n" if c.notes else "") + note
    _record_event(
        db,
        c,
        event_type="note_added",
        data={"note": note[:500]},
        actor_id=actor_id,
    )
    db.commit()
    db.refresh(c)
    log.info("placement.note_added", extra={"candidate_id": candidate_id})
    return c


def update_profile(
    db: Session,
    *,
    candidate_id: int,
    summary: str | None,
    portfolio_url: str | None,
    notes: str | None,
    actor_id: int | None,
) -> PlacementCandidate | None:
    c = db.get(PlacementCandidate, candidate_id)
    if c is None:
        return None
    if summary is not None:
        c.summary = summary
    if portfolio_url is not None:
        c.portfolio_url = portfolio_url
    if notes is not None:
        c.notes = notes
    _record_event(db, c, event_type="profile_updated", data={}, actor_id=actor_id)
    db.commit()
    db.refresh(c)
    return c
