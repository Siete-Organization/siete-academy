from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logging import get_logger
from app.modules.auth.dependencies import CurrentUser, require_roles
from app.modules.live_sessions.models import LiveSession
from app.modules.live_sessions.schemas import LiveSessionOut, LiveSessionUpsert

log = get_logger("app.live_sessions")
router = APIRouter()


@router.put("", response_model=LiveSessionOut)
def upsert_live_session(
    body: LiveSessionUpsert,
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> LiveSession:
    existing = (
        db.query(LiveSession)
        .filter(LiveSession.module_window_id == body.module_window_id)
        .first()
    )
    if existing:
        existing.title = body.title
        existing.zoom_url = str(body.zoom_url)
        existing.recording_url = str(body.recording_url) if body.recording_url else None
        db.commit()
        db.refresh(existing)
        log.info(
            "live_session.updated",
            extra={
                "live_session_id": existing.id,
                "module_window_id": body.module_window_id,
                "has_recording": bool(existing.recording_url),
            },
        )
        return existing
    ls = LiveSession(
        module_window_id=body.module_window_id,
        title=body.title,
        zoom_url=str(body.zoom_url),
        recording_url=str(body.recording_url) if body.recording_url else None,
    )
    db.add(ls)
    db.commit()
    db.refresh(ls)
    log.info(
        "live_session.created",
        extra={"live_session_id": ls.id, "module_window_id": body.module_window_id},
    )
    return ls


@router.get("/window/{module_window_id}", response_model=LiveSessionOut)
def get_for_window(module_window_id: int, db: Session = Depends(get_db)) -> LiveSession:
    ls = (
        db.query(LiveSession).filter(LiveSession.module_window_id == module_window_id).first()
    )
    if not ls:
        raise HTTPException(404, "No live session for this window")
    return ls
