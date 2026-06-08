"""Promueve (o crea) un usuario con rol 'admin' en la BD.

Idempotente — re-ejecutable. Útil para sembrar un admin en producción antes
de que haga su primer login (sin esperar a que el auth flow lo autoprovisione).

Si el usuario ya existe (por email), su rol se actualiza a 'admin'.
Si no existe, se crea con un firebase_uid placeholder; en su primer login,
el auth flow (auth/dependencies.py) lo encontrará por email y enganchará
el firebase_uid real.

IMPORTANTE: también hay que asegurarse de que el email esté en
ADMIN_EMAILS (env var) para que el allowlist de login lo deje pasar.

Uso (local):
    cd backend && .venv/bin/python -m app.scripts.add_admin natali@wearesiete.com "Natali"

Uso (prod, vía Coolify shell del contenedor api):
    python -m app.scripts.add_admin natali@wearesiete.com "Natali"
"""

from __future__ import annotations

import argparse
import sys

from app.core.database import SessionLocal
from app.core.logging import configure_logging, get_logger
from app.modules.users.models import User

configure_logging()
log = get_logger("add_admin")


def add_admin(email: str, display_name: str | None) -> None:
    email_l = email.strip().lower()
    if not email_l:
        raise SystemExit("email vacío")

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email.ilike(email_l)).first()
        if user is None:
            user = User(
                firebase_uid=f"pending-{email_l}",
                email=email_l,
                display_name=display_name,
                role="admin",
                locale="es",
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            log.info("add_admin.created", extra={"email": email_l, "user_id": user.id})
            print(f"OK creado: {email_l} (id={user.id}, role=admin)")
            return

        if user.role == "admin":
            log.info("add_admin.noop", extra={"email": email_l, "user_id": user.id})
            print(f"OK ya era admin: {email_l} (id={user.id})")
            return

        prior = user.role
        user.role = "admin"
        if display_name and not user.display_name:
            user.display_name = display_name
        db.commit()
        log.info(
            "add_admin.promoted",
            extra={"email": email_l, "user_id": user.id, "from": prior, "to": "admin"},
        )
        print(f"OK promovido: {email_l} (id={user.id}, {prior} -> admin)")
    finally:
        db.close()


def main() -> int:
    p = argparse.ArgumentParser(description="Crea o promueve un usuario a admin.")
    p.add_argument("email")
    p.add_argument("display_name", nargs="?", default=None)
    args = p.parse_args()
    add_admin(args.email, args.display_name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
