from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.core.logging import get_logger
from app.modules.auth.dependencies import CurrentUser, require_roles
from app.modules.placement import services
from app.modules.placement.models import PlacementCandidate
from app.modules.placement.schemas import (
    AssignAdmin,
    CandidateCreate,
    CandidateDetailOut,
    CandidateOut,
    CandidateRecruiterOut,
    CandidateUpdate,
    EventOut,
    StageChange,
)
from app.modules.users.models import User

log = get_logger("app.placement.router")
router = APIRouter()


def _detail(c: PlacementCandidate, db: Session) -> dict:
    user = db.get(User, c.user_id)
    return {
        **{
            "id": c.id,
            "user_id": c.user_id,
            "cohort_id": c.cohort_id,
            "stage": c.stage,
            "assigned_admin_id": c.assigned_admin_id,
            "notes": c.notes,
            "summary": c.summary,
            "portfolio_url": c.portfolio_url,
            "created_at": c.created_at,
            "updated_at": c.updated_at,
        },
        "user_name": user.display_name if user else None,
        "user_email": user.email if user else None,
        "events": [
            EventOut.model_validate(e).model_dump()
            for e in sorted(c.events, key=lambda x: x.created_at, reverse=True)
        ],
    }


@router.post("/candidates", response_model=CandidateOut, status_code=201)
def create_candidate(
    body: CandidateCreate,
    current: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> PlacementCandidate:
    if not db.get(User, body.user_id):
        raise HTTPException(404, "User not found")
    return services.create_or_get_candidate(
        db,
        user_id=body.user_id,
        cohort_id=body.cohort_id,
        summary=body.summary,
        portfolio_url=body.portfolio_url,
        actor_id=current.user.id,
    )


@router.get("/candidates", response_model=list[CandidateOut])
def list_candidates(
    stage: str | None = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> list[PlacementCandidate]:
    q = db.query(PlacementCandidate)
    if stage:
        q = q.filter(PlacementCandidate.stage == stage)
    return (
        q.order_by(PlacementCandidate.updated_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.get("/candidates/{candidate_id}", response_model=CandidateDetailOut)
def get_candidate(
    candidate_id: int,
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> dict:
    c = db.get(PlacementCandidate, candidate_id)
    if not c:
        raise HTTPException(404, "Candidate not found")
    return _detail(c, db)


@router.patch("/candidates/{candidate_id}/stage", response_model=CandidateOut)
def change_stage(
    candidate_id: int,
    body: StageChange,
    current: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> PlacementCandidate:
    try:
        updated = services.move_stage(
            db,
            candidate_id=candidate_id,
            stage=body.stage,
            note=body.note,
            actor_id=current.user.id,
        )
    except ValueError as e:
        raise HTTPException(422, str(e)) from e
    if not updated:
        raise HTTPException(404, "Candidate not found")
    return updated


@router.patch("/candidates/{candidate_id}/assign", response_model=CandidateOut)
def assign(
    candidate_id: int,
    body: AssignAdmin,
    current: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> PlacementCandidate:
    if body.admin_id is not None:
        admin = db.get(User, body.admin_id)
        if not admin or admin.role != "admin":
            raise HTTPException(422, "Admin user not found")
    updated = services.assign_admin(
        db, candidate_id=candidate_id, admin_id=body.admin_id, actor_id=current.user.id
    )
    if not updated:
        raise HTTPException(404, "Candidate not found")
    return updated


@router.patch("/candidates/{candidate_id}", response_model=CandidateOut)
def update_candidate(
    candidate_id: int,
    body: CandidateUpdate,
    current: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> PlacementCandidate:
    updated = services.update_profile(
        db,
        candidate_id=candidate_id,
        summary=body.summary,
        portfolio_url=body.portfolio_url,
        notes=body.notes,
        actor_id=current.user.id,
    )
    if not updated:
        raise HTTPException(404, "Candidate not found")
    return updated


@router.get("/recruiter/candidates", response_model=list[CandidateRecruiterOut])
def list_for_recruiter(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    _recruiter: CurrentUser = Depends(require_roles("recruiter", "admin")),
    db: Session = Depends(get_db),
) -> list[dict]:
    """Vista pública del reclutador: solo candidatos aprobados o presentados, sin notas internas."""
    from sqlalchemy import select

    visible_stages = ("approved", "presented", "placed")

    # Single round-trip: candidates + user + events preloaded
    stmt = (
        select(PlacementCandidate, User)
        .join(User, User.id == PlacementCandidate.user_id)
        .options(selectinload(PlacementCandidate.events))
        .where(PlacementCandidate.stage.in_(visible_stages))
        .order_by(PlacementCandidate.updated_at.desc())
        .offset(offset)
        .limit(limit)
    )

    out: list[dict] = []
    for c, user in db.execute(stmt).all():
        approved_at = next(
            (
                e.created_at
                for e in sorted(c.events, key=lambda x: x.created_at)
                if e.event_type == "stage_changed" and e.data.get("to") == "approved"
            ),
            None,
        )
        out.append(
            {
                "id": c.id,
                "user_name": user.display_name if user else None,
                "cohort_id": c.cohort_id,
                "stage": c.stage,
                "summary": c.summary,
                "portfolio_url": c.portfolio_url,
                "approved_at": approved_at,
            }
        )
    return out
