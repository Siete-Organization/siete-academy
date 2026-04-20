from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.firebase import set_custom_role
from app.core.logging import get_logger
from app.modules.auth.dependencies import CurrentUser, get_current_user, require_roles
from app.modules.users.models import User
from app.modules.users.schemas import RoleChange, UserOut, UserUpdate

log = get_logger("app.users")
router = APIRouter()


@router.get("", response_model=list[UserOut])
def list_users(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> list[User]:
    return db.query(User).order_by(User.id.desc()).offset(offset).limit(limit).all()


@router.patch("/me", response_model=UserOut)
def update_me(
    body: UserUpdate,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    user = current.user
    if body.display_name is not None:
        user.display_name = body.display_name
    if body.locale is not None:
        user.locale = body.locale
    db.commit()
    db.refresh(user)
    return user


@router.patch("/{user_id}/role", response_model=UserOut)
def change_role(
    user_id: int,
    body: RoleChange,
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    if body.role not in ("admin", "teacher", "student", "recruiter"):
        raise HTTPException(422, "Invalid role")
    prior = user.role
    user.role = body.role
    db.commit()
    db.refresh(user)
    try:
        set_custom_role(user.firebase_uid, body.role)
        log.info(
            "user.role_changed",
            extra={"user_id": user.id, "from": prior, "to": body.role, "firebase_synced": True},
        )
    except Exception as e:
        log.warning(
            "user.role_change_firebase_failed",
            extra={"user_id": user.id, "from": prior, "to": body.role, "error": str(e)},
        )
    return user
