from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.core.firebase import verify_id_token
from app.core.logging import bind_user_id, get_logger
from app.modules.applications.models import Application
from app.modules.users.models import User

log = get_logger("app.auth")


def _resolve_initial_role(db: Session, email: str, admin_emails: list[str]) -> str | None:
    """Decide qué rol asignar a un usuario que loguea por primera vez.

    Devuelve None si el email no está autorizado (ni en allowlist de admins
    ni en applications con status 'approved').
    """
    email_l = (email or "").lower()
    if not email_l:
        return None
    if email_l in admin_emails:
        return "admin"
    approved = (
        db.query(Application)
        .filter(Application.applicant_email.ilike(email_l), Application.status == "approved")
        .first()
    )
    if approved is not None:
        return "student"
    return None


class CurrentUser:
    def __init__(self, user: User, claims: dict) -> None:
        self.user = user
        self.claims = claims

    @property
    def role(self) -> str:
        return self.claims.get("role") or self.user.role


def get_current_user(
    authorization: str | None = Header(None),
    x_dev_user: str | None = Header(None, alias="X-Dev-User"),
    db: Session = Depends(get_db),
) -> CurrentUser:
    settings = get_settings()

    # Dev-only bypass: allow login-by-email without Firebase so we can demo
    # locally without configuring a Firebase project. Disabled in production.
    if (
        settings.dev_auth_bypass
        and settings.app_env == "development"
        and x_dev_user
    ):
        user = db.query(User).filter_by(email=x_dev_user).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Dev user '{x_dev_user}' not found. Run `make seed` first.",
            )
        bind_user_id(user.id)
        log.debug("auth.dev_bypass", extra={"email": x_dev_user, "role": user.role})
        return CurrentUser(
            user=user, claims={"role": user.role, "uid": user.firebase_uid, "_dev": True}
        )

    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    token = authorization.split(" ", 1)[1]
    try:
        claims = verify_id_token(token)
    except Exception as e:
        log.warning("auth.token_invalid", extra={"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {e}"
        ) from e

    uid = claims.get("uid") or claims.get("sub")
    email = (claims.get("email") or "").lower()
    admin_emails = settings.admin_emails_list

    user = db.query(User).filter_by(firebase_uid=uid).first()
    if user is None and email:
        # Si el firebase_uid es nuevo, intenta enganchar a un User existente por email
        # (caso: admin seedeado en demo o aplicante que ya tenía cuenta).
        user = db.query(User).filter(User.email.ilike(email)).first()
        if user is not None and not user.firebase_uid:
            user.firebase_uid = uid

    if user is None:
        # Provisioning: solo si el email está autorizado.
        initial_role = _resolve_initial_role(db, email, admin_emails)
        if initial_role is None:
            log.info("auth.not_invited", extra={"email": email})
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"code": "not_invited", "email": email},
            )
        user = User(
            firebase_uid=uid,
            email=email,
            display_name=claims.get("name"),
            role=initial_role,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        log.info(
            "auth.user_provisioned",
            extra={"firebase_uid": uid, "email": user.email, "role": user.role},
        )
    else:
        # Promote existing user to admin if email matches admin_emails.
        if email and email in admin_emails and user.role != "admin":
            prior = user.role
            user.role = "admin"
            db.commit()
            db.refresh(user)
            log.info(
                "auth.role_promoted",
                extra={"user_id": user.id, "from": prior, "to": "admin"},
            )

    bind_user_id(user.id)
    return CurrentUser(user=user, claims=claims)


def require_roles(*roles: str):
    allowed: tuple[str, ...] = tuple(roles)

    def _dep(current: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if current.role not in allowed:
            log.warning(
                "auth.forbidden",
                extra={"required_roles": list(allowed), "user_role": current.role},
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of roles: {allowed}",
            )
        return current

    return _dep
