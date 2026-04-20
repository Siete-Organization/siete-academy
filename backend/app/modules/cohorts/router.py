from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logging import get_logger
from app.modules.auth.dependencies import CurrentUser, require_roles
from app.modules.cohorts.models import Cohort, ModuleWindow
from app.modules.cohorts.schemas import (
    CohortCreate,
    CohortOut,
    ModuleWindowCreate,
    ModuleWindowOut,
    ModuleWindowUpdate,
)

log = get_logger("app.cohorts")
router = APIRouter()


@router.post("", response_model=CohortOut, status_code=201)
def create_cohort(
    body: CohortCreate,
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> Cohort:
    cohort = Cohort(**body.model_dump())
    db.add(cohort)
    db.commit()
    db.refresh(cohort)
    log.info(
        "cohort.created",
        extra={"cohort_id": cohort.id, "cohort_name": cohort.name, "locale": cohort.locale},
    )
    return cohort


@router.get("", response_model=list[CohortOut])
def list_cohorts(db: Session = Depends(get_db)) -> list[Cohort]:
    return db.query(Cohort).order_by(Cohort.start_date.desc()).all()


@router.get("/{cohort_id}", response_model=CohortOut)
def get_cohort(cohort_id: int, db: Session = Depends(get_db)) -> Cohort:
    c = db.get(Cohort, cohort_id)
    if not c:
        raise HTTPException(404, "Cohort not found")
    return c


@router.post("/{cohort_id}/windows", response_model=ModuleWindowOut, status_code=201)
def add_module_window(
    cohort_id: int,
    body: ModuleWindowCreate,
    _staff: CurrentUser = Depends(require_roles("admin", "teacher")),
    db: Session = Depends(get_db),
) -> ModuleWindow:
    if not db.get(Cohort, cohort_id):
        raise HTTPException(404, "Cohort not found")
    w = ModuleWindow(cohort_id=cohort_id, **body.model_dump())
    db.add(w)
    db.commit()
    db.refresh(w)
    log.info(
        "module_window.created",
        extra={
            "window_id": w.id,
            "cohort_id": cohort_id,
            "module_id": w.module_id,
            "opens_at": w.opens_at.isoformat(),
            "closes_at": w.closes_at.isoformat(),
        },
    )
    return w


@router.get("/{cohort_id}/windows", response_model=list[ModuleWindowOut])
def list_module_windows(cohort_id: int, db: Session = Depends(get_db)) -> list[ModuleWindow]:
    return (
        db.query(ModuleWindow)
        .filter(ModuleWindow.cohort_id == cohort_id)
        .order_by(ModuleWindow.opens_at)
        .all()
    )


@router.patch("/{cohort_id}/windows/{window_id}", response_model=ModuleWindowOut)
def update_module_window(
    cohort_id: int,
    window_id: int,
    body: ModuleWindowUpdate,
    _staff: CurrentUser = Depends(require_roles("admin", "teacher")),
    db: Session = Depends(get_db),
) -> ModuleWindow:
    w = db.get(ModuleWindow, window_id)
    if not w or w.cohort_id != cohort_id:
        raise HTTPException(404, "Window not found")
    changes: dict = {}
    if body.opens_at is not None:
        changes["opens_at"] = {"from": w.opens_at.isoformat(), "to": body.opens_at.isoformat()}
        w.opens_at = body.opens_at
    if body.closes_at is not None:
        changes["closes_at"] = {"from": w.closes_at.isoformat(), "to": body.closes_at.isoformat()}
        w.closes_at = body.closes_at
    if body.live_session_at is not None:
        changes["live_session_at"] = {
            "from": w.live_session_at.isoformat() if w.live_session_at else None,
            "to": body.live_session_at.isoformat(),
        }
        w.live_session_at = body.live_session_at
    db.commit()
    db.refresh(w)
    log.info(
        "module_window.updated",
        extra={"window_id": window_id, "cohort_id": cohort_id, "changes": changes},
    )
    return w


@router.post("/{cohort_id}/windows/{window_id}/open", response_model=ModuleWindowOut)
def open_window_now(
    cohort_id: int,
    window_id: int,
    _staff: CurrentUser = Depends(require_roles("admin", "teacher")),
    db: Session = Depends(get_db),
) -> ModuleWindow:
    """Abre un módulo inmediatamente."""
    w = db.get(ModuleWindow, window_id)
    if not w or w.cohort_id != cohort_id:
        raise HTTPException(404, "Window not found")
    prior = w.opens_at
    w.opens_at = datetime.utcnow() - timedelta(minutes=1)
    if w.closes_at <= w.opens_at:
        w.closes_at = w.opens_at + timedelta(days=14)
    db.commit()
    db.refresh(w)
    log.info(
        "module_window.opened",
        extra={"window_id": window_id, "cohort_id": cohort_id, "prior_opens_at": prior.isoformat()},
    )
    return w


@router.post("/{cohort_id}/windows/{window_id}/close", response_model=ModuleWindowOut)
def close_window_now(
    cohort_id: int,
    window_id: int,
    _staff: CurrentUser = Depends(require_roles("admin", "teacher")),
    db: Session = Depends(get_db),
) -> ModuleWindow:
    """Cierra un módulo inmediatamente."""
    w = db.get(ModuleWindow, window_id)
    if not w or w.cohort_id != cohort_id:
        raise HTTPException(404, "Window not found")
    prior = w.closes_at
    w.closes_at = datetime.utcnow()
    db.commit()
    db.refresh(w)
    log.info(
        "module_window.closed",
        extra={"window_id": window_id, "cohort_id": cohort_id, "prior_closes_at": prior.isoformat()},
    )
    return w
