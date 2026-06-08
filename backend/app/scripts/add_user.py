"""Crea o actualiza un usuario con un rol específico en la BD.

Idempotente — re-ejecutable. Útil para sembrar admins / teachers /
recruiters antes de su primer login (el auth flow solo autoprovisiona
'student' vía Application aprobada).

Comportamiento:
- Si el email ya existe: actualiza su rol al solicitado (si difiere).
- Si no existe: crea el row con `firebase_uid="pending-<email>"`.
  En el primer login real, el auth flow (`auth/dependencies.py`)
  encuentra el row por email y reemplaza el uid placeholder por el
  uid real de Firebase.

Uso (local):
    cd backend && .venv/bin/python -m app.scripts.add_user natali@wearesiete.com "Natali" --role admin

Uso (prod, vía shell del contenedor api en Coolify):
    python -m app.scripts.add_user natali@wearesiete.com "Natali" --role admin
"""

from __future__ import annotations

import argparse
import sys

from app.core.database import SessionLocal
from app.core.logging import configure_logging, get_logger
from app.modules.users.models import User

VALID_ROLES = ("admin", "teacher", "student", "recruiter")

configure_logging()
log = get_logger("add_user")


def add_user(email: str, display_name: str | None, role: str) -> None:
    if role not in VALID_ROLES:
        raise SystemExit(f"role inválido: {role!r}. Válidos: {VALID_ROLES}")
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
                role=role,
                locale="es",
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            log.info(
                "add_user.created",
                extra={"email": email_l, "user_id": user.id, "role": role},
            )
            print(f"OK creado: {email_l} (id={user.id}, role={role})")
            return

        if user.role == role:
            log.info(
                "add_user.noop",
                extra={"email": email_l, "user_id": user.id, "role": role},
            )
            print(f"OK ya era {role}: {email_l} (id={user.id})")
            return

        prior = user.role
        user.role = role
        if display_name and not user.display_name:
            user.display_name = display_name
        db.commit()
        log.info(
            "add_user.role_changed",
            extra={"email": email_l, "user_id": user.id, "from": prior, "to": role},
        )
        print(f"OK actualizado: {email_l} (id={user.id}, {prior} -> {role})")
    finally:
        db.close()


def main() -> int:
    p = argparse.ArgumentParser(description="Crea o actualiza un usuario con un rol específico.")
    p.add_argument("email")
    p.add_argument("display_name", nargs="?", default=None)
    p.add_argument("--role", required=True, choices=VALID_ROLES)
    args = p.parse_args()
    add_user(args.email, args.display_name, args.role)
    return 0


if __name__ == "__main__":
    sys.exit(main())
