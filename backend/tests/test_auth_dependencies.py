"""Tests for auth dependency guards.

These hit live routers with the FastAPI dependency override machinery:
we don't validate the actual Firebase token — the override returns a CurrentUser
for each role under test. What's verified is the `require_roles` HTTP behaviour.
"""

import pytest

CASES = [
    # (role_under_test, expected_status_for_admin_route)
    ("student", 403),
    ("teacher", 403),
    ("recruiter", 403),
    ("admin", 200),
]


@pytest.mark.parametrize("role, expected", CASES)
def test_users_list_is_admin_only(client, login_as, role, expected):
    login_as(role)
    resp = client.get("/users")
    assert resp.status_code == expected, f"role={role}: {resp.text}"


def test_me_endpoint_returns_current_user(client):
    resp = client.get("/auth/me")
    assert resp.status_code == 200
    body = resp.json()
    assert body["email"] == "student@test.dev"
    assert body["role"] == "student"


def test_update_me_lets_student_change_own_profile(client):
    resp = client.patch("/users/me", json={"display_name": "Updated", "locale": "en"})
    assert resp.status_code == 200, resp.text
    assert resp.json()["display_name"] == "Updated"
    assert resp.json()["locale"] == "en"


def test_change_role_endpoint_requires_admin(client, db, login_as):
    from app.modules.users.models import User

    target = User(
        firebase_uid="uid-target",
        email="target@test.dev",
        display_name="Target",
        role="student",
        locale="es",
    )
    db.add(target)
    db.commit()
    db.refresh(target)

    # As student — forbidden
    resp = client.patch(f"/users/{target.id}/role", json={"role": "teacher"})
    assert resp.status_code == 403

    login_as("admin")
    resp = client.patch(f"/users/{target.id}/role", json={"role": "teacher"})
    assert resp.status_code == 200, resp.text
    assert resp.json()["role"] == "teacher"


def test_change_role_rejects_invalid_role(client, login_as, db):
    from app.modules.users.models import User

    target = User(
        firebase_uid="uid-target2",
        email="t2@test.dev",
        display_name="T",
        role="student",
        locale="es",
    )
    db.add(target)
    db.commit()
    db.refresh(target)

    login_as("admin")
    resp = client.patch(f"/users/{target.id}/role", json={"role": "superlord"})
    assert resp.status_code == 422
