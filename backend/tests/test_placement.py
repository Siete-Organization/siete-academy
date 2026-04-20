"""Tests for placement module — stage transitions + recruiter view."""

import pytest

from app.modules.placement import services
from app.modules.placement.models import PlacementCandidate, PlacementEvent
from app.modules.users.models import User


@pytest.fixture
def candidate(db, default_student):
    return services.create_or_get_candidate(
        db,
        user_id=default_student.id,
        cohort_id=None,
        summary="Exp prev en ventas B2C",
        portfolio_url=None,
        actor_id=default_student.id,
    )


class TestCandidateService:
    def test_create_is_idempotent(self, db, default_student):
        c1 = services.create_or_get_candidate(
            db, user_id=default_student.id, cohort_id=None,
            summary=None, portfolio_url=None, actor_id=None,
        )
        c2 = services.create_or_get_candidate(
            db, user_id=default_student.id, cohort_id=None,
            summary=None, portfolio_url=None, actor_id=None,
        )
        assert c1.id == c2.id

    def test_move_stage_records_event(self, db, candidate):
        updated = services.move_stage(
            db, candidate_id=candidate.id, stage="approved", note="pass!", actor_id=None
        )
        assert updated is not None
        assert updated.stage == "approved"
        events = db.query(PlacementEvent).filter_by(candidate_id=candidate.id).all()
        stage_changes = [e for e in events if e.event_type == "stage_changed"]
        assert len(stage_changes) == 1
        assert stage_changes[0].data["from"] == "applying"
        assert stage_changes[0].data["to"] == "approved"

    def test_move_stage_rejects_invalid(self, db, candidate):
        with pytest.raises(ValueError, match="Invalid stage"):
            services.move_stage(
                db, candidate_id=candidate.id, stage="dreaming", note=None, actor_id=None
            )

    def test_move_stage_same_stage_is_noop(self, db, candidate):
        services.move_stage(db, candidate_id=candidate.id, stage="applying", note=None, actor_id=None)
        events_after = (
            db.query(PlacementEvent)
            .filter_by(candidate_id=candidate.id, event_type="stage_changed")
            .count()
        )
        assert events_after == 0

    def test_add_note_appends_and_records_event(self, db, candidate):
        services.add_note(db, candidate_id=candidate.id, note="first note", actor_id=None)
        services.add_note(db, candidate_id=candidate.id, note="second note", actor_id=None)
        db.refresh(candidate)
        assert "first note" in candidate.notes
        assert "second note" in candidate.notes


class TestPlacementEndpoints:
    def test_create_candidate_requires_admin(self, client, db, login_as):
        resp = client.post("/placement/candidates", json={"user_id": 1})
        assert resp.status_code == 403  # default student

        login_as("admin")
        # Create a target user first
        target = User(firebase_uid="uid-target-p", email="target-p@test.dev", role="student")
        db.add(target)
        db.commit()
        db.refresh(target)
        resp = client.post("/placement/candidates", json={"user_id": target.id})
        assert resp.status_code == 201, resp.text
        assert resp.json()["stage"] == "applying"

    def test_stage_change_endpoint(self, client, db, login_as, default_student):
        login_as("admin")
        services.create_or_get_candidate(
            db, user_id=default_student.id, cohort_id=None,
            summary=None, portfolio_url=None, actor_id=None,
        )
        cand = db.query(PlacementCandidate).filter_by(user_id=default_student.id).first()
        resp = client.patch(
            f"/placement/candidates/{cand.id}/stage", json={"stage": "approved"}
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["stage"] == "approved"

    def test_recruiter_view_only_shows_approved_or_later(self, client, db, login_as, default_student):
        # Create two candidates with different stages
        login_as("admin")
        u2 = User(firebase_uid="uid-p2", email="p2@test.dev", role="student")
        db.add(u2)
        db.commit()
        db.refresh(u2)

        applying_cand = services.create_or_get_candidate(
            db, user_id=default_student.id, cohort_id=None,
            summary="hidden", portfolio_url=None, actor_id=None,
        )
        approved_cand = services.create_or_get_candidate(
            db, user_id=u2.id, cohort_id=None,
            summary="visible", portfolio_url=None, actor_id=None,
        )
        services.move_stage(db, candidate_id=approved_cand.id, stage="approved", note=None, actor_id=None)

        # Recruiter sees only the approved one
        login_as("recruiter")
        resp = client.get("/placement/recruiter/candidates")
        assert resp.status_code == 200
        ids = [c["id"] for c in resp.json()]
        assert approved_cand.id in ids
        assert applying_cand.id not in ids
