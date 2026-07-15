"""DELETE /applications/{id} — borrado admin de postulaciones."""

from __future__ import annotations

from app.modules.applications.models import Application


def _make_app(db, email: str = "borrable@test.dev") -> Application:
    app = Application(
        applicant_name="Para Borrar",
        applicant_email=email,
        linkedin_url="https://www.linkedin.com/in/borrable",
        country="Peru",
        locale="es",
        answers={},
        status="submitted",
    )
    db.add(app)
    db.commit()
    db.refresh(app)
    return app


def test_admin_deletes_application(client, db, login_as):
    app = _make_app(db)
    login_as("admin")
    r = client.delete(f"/applications/{app.id}")
    assert r.status_code == 204
    assert db.get(Application, app.id) is None


def test_delete_frees_email_for_reapply(client, db, login_as, monkeypatch):
    from app.modules.applications import router as apps_router

    class _Noop:
        def delay(self, *a, **k):
            return None

    monkeypatch.setattr(apps_router, "notify_submitted", _Noop())
    monkeypatch.setattr(apps_router, "score_application_task", _Noop())

    app = _make_app(db, email="reaplica@test.dev")
    login_as("admin")
    assert client.delete(f"/applications/{app.id}").status_code == 204

    payload = {
        "applicant_name": "Reaplica",
        "applicant_email": "reaplica@test.dev",
        "linkedin_url": "https://www.linkedin.com/in/reaplica",
        "country": "Peru",
        "locale": "es",
        "answers": [],
        "video_url": "https://loom.com/x",
    }
    r = client.post("/applications", json=payload)
    assert r.status_code == 201  # 201 (no 200 dedup): el email quedó libre


def test_delete_requires_admin(client, db, login_as):
    app = _make_app(db, email="protegida@test.dev")
    login_as("student")
    r = client.delete(f"/applications/{app.id}")
    assert r.status_code == 403
    assert db.get(Application, app.id) is not None


def test_delete_missing_returns_404(client, login_as):
    login_as("admin")
    assert client.delete("/applications/999999").status_code == 404
