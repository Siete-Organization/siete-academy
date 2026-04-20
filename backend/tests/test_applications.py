"""Tests for applications module.

Covers:
  * POST /applications wordcount validation (>=100 words per answer)
  * service review_application transitions + reviewer stamping
  * admin guard on review endpoint
"""

from datetime import datetime

import pytest

from app.modules.applications.models import Application
from app.modules.applications.schemas import ApplicationAnswer, ApplicationCreate
from app.modules.applications.services import create_application, review_application


def _long_answer(prefix: str = "word", n: int = 100) -> str:
    """Build a deterministic text with at least `n` words."""
    return " ".join(f"{prefix}{i}" for i in range(n))


class TestCreateApplicationService:
    def test_create_persists_answers_as_dict(self, db):
        data = ApplicationCreate(
            applicant_name="Ana Ejemplo",
            applicant_email="ana@example.com",
            applicant_phone=None,
            locale="es",
            answers=[
                ApplicationAnswer(question_id="why_sales", text=_long_answer("a")),
                ApplicationAnswer(question_id="achievement", text=_long_answer("b")),
                ApplicationAnswer(question_id="hours_per_week", text=_long_answer("c")),
            ],
            video_url="https://loom.com/x",
        )
        app_obj = create_application(db, data)
        assert app_obj.id is not None
        assert app_obj.status == "submitted"
        assert app_obj.answers == {
            "why_sales": _long_answer("a"),
            "achievement": _long_answer("b"),
            "hours_per_week": _long_answer("c"),
        }

    def test_word_count_validator_rejects_short_answer(self):
        with pytest.raises(ValueError, match="at least 100 words"):
            ApplicationAnswer(question_id="why_sales", text="too short")

    def test_word_count_validator_accepts_exactly_100(self):
        ans = ApplicationAnswer(question_id="x", text=_long_answer("w", 100))
        assert len(ans.text.split()) == 100


class TestReviewApplicationService:
    def test_review_sets_status_notes_reviewer_and_timestamp(self, db):
        from app.modules.users.models import User

        reviewer = User(
            firebase_uid="uid-reviewer",
            email="reviewer@test.dev",
            display_name="Rev",
            role="admin",
        )
        db.add(reviewer)
        db.commit()
        db.refresh(reviewer)

        app_obj = Application(
            applicant_name="Ana",
            applicant_email="ana@example.com",
            locale="es",
            answers={},
            status="submitted",
        )
        db.add(app_obj)
        db.commit()
        db.refresh(app_obj)

        updated = review_application(
            db,
            app_obj.id,
            status="approved",
            admin_notes="Great fit",
            reviewer_id=reviewer.id,
        )
        assert updated is not None
        assert updated.status == "approved"
        assert updated.admin_notes == "Great fit"
        assert updated.reviewed_by_id == reviewer.id
        assert isinstance(updated.reviewed_at, datetime)

    def test_review_returns_none_for_unknown_id(self, db):
        assert review_application(db, 999_999, status="rejected", admin_notes=None, reviewer_id=1) is None


class TestApplicationsEndpoint:
    def test_post_application_accepts_valid_body(self, client):
        body = {
            "applicant_name": "Luis",
            "applicant_email": "luis@example.com",
            "locale": "es",
            "video_url": "https://loom.com/x",
            "answers": [
                {"question_id": "why_sales", "text": _long_answer("a")},
                {"question_id": "achievement", "text": _long_answer("b")},
                {"question_id": "hours_per_week", "text": _long_answer("c")},
            ],
        }
        resp = client.post("/applications", json=body)
        assert resp.status_code == 201, resp.text
        data = resp.json()
        assert data["applicant_name"] == "Luis"
        assert data["status"] == "submitted"

    def test_post_application_rejects_short_answer(self, client):
        body = {
            "applicant_name": "Luis",
            "applicant_email": "luis@example.com",
            "locale": "es",
            "video_url": "https://loom.com/x",
            "answers": [
                {"question_id": "why_sales", "text": "too short"},
                {"question_id": "achievement", "text": _long_answer("b")},
                {"question_id": "hours_per_week", "text": _long_answer("c")},
            ],
        }
        resp = client.post("/applications", json=body)
        assert resp.status_code == 422
        detail = resp.json()["detail"]
        assert any("at least 100 words" in str(d.get("msg", "")) for d in detail)

    def test_review_endpoint_requires_admin(self, client, db, login_as):
        app_obj = Application(
            applicant_name="Ana",
            applicant_email="ana@example.com",
            locale="es",
            answers={},
            status="submitted",
        )
        db.add(app_obj)
        db.commit()
        db.refresh(app_obj)

        # Default client is a student — should be forbidden
        resp = client.post(
            f"/applications/{app_obj.id}/review",
            json={"status": "approved", "admin_notes": "ok"},
        )
        assert resp.status_code == 403

        # As admin — allowed
        login_as("admin")
        resp = client.post(
            f"/applications/{app_obj.id}/review",
            json={"status": "approved", "admin_notes": "ok"},
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["status"] == "approved"
