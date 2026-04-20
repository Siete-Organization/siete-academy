"""Shared fixtures.

Uses a temp-file SQLite so that ANY connection opened during a test — including
the ones Celery tasks open through the production `SessionLocal` — hits the
exact same database. In-memory SQLite would give each connection its own
isolated database, breaking anything that opens a session outside the fixture.

Firebase auth is stubbed via FastAPI dependency overrides.
"""

from __future__ import annotations

import os
import tempfile
from collections.abc import Generator

import pytest

# Point the app at a temp SQLite before any app.* import happens
_DB_FILE = tempfile.NamedTemporaryFile(suffix="-sieteacademy-test.db", delete=False)
_DB_FILE.close()
os.environ["DATABASE_URL"] = f"sqlite:///{_DB_FILE.name}"
os.environ.setdefault("APP_ENV", "development")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("ANTHROPIC_API_KEY", "")

from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import event  # noqa: E402
from sqlalchemy.orm import Session  # noqa: E402

from app.core import database as db_module  # noqa: E402
from app.core.database import Base  # noqa: E402

# Enable FK enforcement in SQLite
@event.listens_for(db_module.engine, "connect")
def _enable_fk(dbapi_connection, _):
    cur = dbapi_connection.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    cur.close()


# Import every model so Base.metadata sees all tables
from app.modules.applications import models as _apps  # noqa: F401, E402
from app.modules.assessments import models as _assess  # noqa: F401, E402
from app.modules.audit import models as _audit  # noqa: F401, E402
from app.modules.cohorts import models as _cohorts  # noqa: F401, E402
from app.modules.courses import models as _courses  # noqa: F401, E402
from app.modules.enrollment import models as _enroll  # noqa: F401, E402
from app.modules.live_sessions import models as _live  # noqa: F401, E402
from app.modules.users import models as _users  # noqa: F401, E402

from app.core.celery_app import celery_app as _celery_app  # noqa: E402

# Run Celery tasks inline so .delay() works without a broker
_celery_app.conf.task_always_eager = True
_celery_app.conf.task_eager_propagates = True

from app.main import app  # noqa: E402
from app.modules.auth.dependencies import CurrentUser, get_current_user  # noqa: E402
from app.modules.users.models import User  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _create_schema():
    Base.metadata.create_all(db_module.engine)
    yield
    try:
        os.unlink(_DB_FILE.name)
    except OSError:
        pass


@pytest.fixture
def db() -> Generator[Session, None, None]:
    """Per-test session with brutal cleanup.

    We can't wrap everything in a single outer transaction because Celery
    tasks open their own short-lived sessions that commit independently.
    Instead, at teardown we truncate every table — fast on SQLite, simple
    and robust.
    """
    session = db_module.SessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Truncate all tables
        with db_module.engine.begin() as conn:
            for table in reversed(Base.metadata.sorted_tables):
                conn.execute(table.delete())


@pytest.fixture
def default_student(db) -> User:
    u = User(
        firebase_uid="uid-student",
        email="student@test.dev",
        display_name="Test Student",
        role="student",
        locale="es",
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


@pytest.fixture
def client(db, default_student) -> Generator[TestClient, None, None]:
    """TestClient with DB + auth overrides. Default user is a student."""

    def _get_db_override():
        try:
            yield db
        finally:
            pass

    def _current_user_override():
        return CurrentUser(
            user=default_student,
            claims={"role": "student", "uid": "uid-student"},
        )

    app.dependency_overrides[db_module.get_db] = _get_db_override
    app.dependency_overrides[get_current_user] = _current_user_override

    with TestClient(app) as tc:
        yield tc

    app.dependency_overrides.clear()


@pytest.fixture
def login_as(db, default_student):
    """Swap the auth override to a user with a specific role.

    Reuses `default_student` for role='student' so we don't violate
    the email UNIQUE constraint.
    """

    def _login(role: str, *, email: str | None = None):
        if role == "student":
            u = default_student
        else:
            target_email = email or f"{role}@test.dev"
            u = db.query(User).filter_by(firebase_uid=f"uid-{role}").first()
            if u is None:
                u = User(
                    firebase_uid=f"uid-{role}",
                    email=target_email,
                    display_name=f"Test {role.title()}",
                    role=role,
                    locale="es",
                )
                db.add(u)
                db.commit()
                db.refresh(u)

        def _override():
            return CurrentUser(user=u, claims={"role": role, "uid": u.firebase_uid})

        app.dependency_overrides[get_current_user] = _override
        return u

    return _login
