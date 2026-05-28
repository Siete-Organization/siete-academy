"""Tests para el path post-Academy (Parte IX)."""
import pytest

from app.modules.practica import services
from app.modules.practica.criteria import STAGE_DEFINITIONS, stage_definition
from app.modules.practica.models import PracticaCandidate, PracticaStageEvent
from app.modules.users.models import User


@pytest.fixture
def graduate(db) -> User:
    u = User(
        firebase_uid="uid-grad",
        email="grad@test.dev",
        display_name="Ana Graduada",
        role="student",
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


@pytest.fixture
def admin(db) -> User:
    u = User(
        firebase_uid="uid-admin-practica",
        email="admin-practica@test.dev",
        display_name="Admin",
        role="admin",
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


class TestInvite:
    def test_invite_creates_candidate_at_e1_invited(self, db, graduate, admin):
        c = services.invite(
            db,
            user_id=graduate.id,
            country_deel_ok=True,
            notes="Top of cohort",
            actor_id=admin.id,
        )
        assert c.stage == "e1_invited"
        assert c.country_deel_ok is True
        assert c.notes == "Top of cohort"
        assert c.monthly_usd is None

    def test_invite_logs_initial_event(self, db, graduate, admin):
        c = services.invite(
            db, user_id=graduate.id, country_deel_ok=True, notes=None, actor_id=admin.id
        )
        events = db.query(PracticaStageEvent).filter_by(candidate_id=c.id).all()
        assert len(events) == 1
        assert events[0].from_stage is None
        assert events[0].to_stage == "e1_invited"
        assert events[0].actor_id == admin.id

    def test_invite_twice_for_same_user_fails(self, db, graduate, admin):
        services.invite(
            db, user_id=graduate.id, country_deel_ok=True, notes=None, actor_id=admin.id
        )
        with pytest.raises(ValueError):
            services.invite(
                db,
                user_id=graduate.id,
                country_deel_ok=True,
                notes=None,
                actor_id=admin.id,
            )


class TestTransition:
    def test_e1_invited_to_e1_active(self, db, graduate, admin):
        c = services.invite(
            db, user_id=graduate.id, country_deel_ok=True, notes=None, actor_id=admin.id
        )
        c = services.transition(
            db, c, to_stage="e1_active", reason="aceptó", monthly_usd=None, actor_id=admin.id
        )
        assert c.stage == "e1_active"
        assert c.monthly_usd is None
        events = db.query(PracticaStageEvent).filter_by(candidate_id=c.id).all()
        assert len(events) == 2

    def test_e1_active_to_e2_requires_monthly_usd(self, db, graduate, admin):
        c = services.invite(
            db, user_id=graduate.id, country_deel_ok=True, notes=None, actor_id=admin.id
        )
        services.transition(
            db, c, to_stage="e1_active", reason=None, monthly_usd=None, actor_id=admin.id
        )
        with pytest.raises(services.TransitionError, match="monthly_usd"):
            services.transition(
                db, c, to_stage="e2_active", reason=None, monthly_usd=None, actor_id=admin.id
            )

    def test_e1_to_e2_with_monthly_usd_succeeds(self, db, graduate, admin):
        c = services.invite(
            db, user_id=graduate.id, country_deel_ok=True, notes=None, actor_id=admin.id
        )
        services.transition(
            db, c, to_stage="e1_active", reason=None, monthly_usd=None, actor_id=admin.id
        )
        c = services.transition(
            db, c, to_stage="e2_active", reason="aprobó E1", monthly_usd=400, actor_id=admin.id
        )
        assert c.stage == "e2_active"
        assert c.monthly_usd == 400

    def test_invalid_transition_skipping_stage_blocked(self, db, graduate, admin):
        c = services.invite(
            db, user_id=graduate.id, country_deel_ok=True, notes=None, actor_id=admin.id
        )
        with pytest.raises(services.TransitionError, match="not allowed"):
            services.transition(
                db, c, to_stage="e3_t2_active", reason=None, monthly_usd=900, actor_id=admin.id
            )

    def test_deel_ineligible_blocked_from_paid_stages(self, db, graduate, admin):
        c = services.invite(
            db, user_id=graduate.id, country_deel_ok=False, notes=None, actor_id=admin.id
        )
        services.transition(
            db, c, to_stage="e1_active", reason=None, monthly_usd=None, actor_id=admin.id
        )
        with pytest.raises(services.TransitionError, match="Deel"):
            services.transition(
                db, c, to_stage="e2_active", reason=None, monthly_usd=400, actor_id=admin.id
            )

    def test_closed_camino_b_is_terminal(self, db, graduate, admin):
        c = services.invite(
            db, user_id=graduate.id, country_deel_ok=True, notes=None, actor_id=admin.id
        )
        c = services.transition(
            db,
            c,
            to_stage="closed_camino_b",
            reason="declinó",
            monthly_usd=None,
            actor_id=admin.id,
        )
        with pytest.raises(services.TransitionError, match="not allowed"):
            services.transition(
                db, c, to_stage="e1_active", reason=None, monthly_usd=None, actor_id=admin.id
            )

    def test_t2_to_t1_within_e3_band_change(self, db, graduate, admin):
        c = services.invite(
            db, user_id=graduate.id, country_deel_ok=True, notes=None, actor_id=admin.id
        )
        for to, usd in [
            ("e1_active", None),
            ("e2_active", 400),
            ("e3_t2_active", 700),
            ("e3_t1_active", 1100),
        ]:
            c = services.transition(
                db, c, to_stage=to, reason=None, monthly_usd=usd, actor_id=admin.id
            )
        assert c.stage == "e3_t1_active"
        assert c.monthly_usd == 1100


class TestStageDefinitions:
    def test_all_model_stages_have_definition(self):
        keys = {s["key"] for s in STAGE_DEFINITIONS}
        for stage in (
            "e1_invited",
            "e1_active",
            "e2_active",
            "e3_t2_active",
            "e3_t1_active",
            "closed_camino_b",
            "declined",
        ):
            assert stage in keys, f"missing definition for {stage}"

    def test_paid_stages_show_compensation_band(self):
        for key in ("e2_active", "e3_t2_active", "e3_t1_active"):
            d = stage_definition(key)
            assert d is not None
            assert "USD" in d["compensation"]

    def test_stage_definition_unknown_returns_none(self):
        assert stage_definition("unknown_stage") is None


class TestEndpoints:
    def test_get_stages_is_public(self, client):
        r = client.get("/practica/stages")
        assert r.status_code == 200
        data = r.json()
        assert len(data["stages"]) == 7

    def test_me_returns_null_when_not_invited(self, client):
        r = client.get("/practica/me")
        assert r.status_code == 200
        assert r.json() is None

    def test_me_returns_candidate_when_invited(self, client, db, default_student, login_as):
        login_as("admin", email="admin-it@test.dev")

        # admin invites the default_student
        r = client.post(
            "/practica/candidates",
            json={"user_id": default_student.id, "country_deel_ok": True, "notes": "test"},
        )
        assert r.status_code == 201

        # switch back to student
        login_as("student")
        r = client.get("/practica/me")
        assert r.status_code == 200
        body = r.json()
        assert body["user_id"] == default_student.id
        assert body["stage"] == "e1_invited"

    def test_student_cannot_invite(self, client, default_student):
        r = client.post(
            "/practica/candidates",
            json={"user_id": default_student.id, "country_deel_ok": True},
        )
        # default client is student → require_roles("admin") fails
        assert r.status_code == 403

    def test_transition_invalid_returns_422(self, client, login_as, default_student):
        login_as("admin", email="admin-tr@test.dev")
        r = client.post(
            "/practica/candidates",
            json={"user_id": default_student.id, "country_deel_ok": True},
        )
        cid = r.json()["id"]
        r = client.post(
            f"/practica/candidates/{cid}/transition",
            json={"to_stage": "e3_t2_active", "monthly_usd": 700},
        )
        assert r.status_code == 422
