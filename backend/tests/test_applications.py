"""Tests for applications module.

Covers:
  * POST /applications wordcount validation (>=100 words per answer)
  * service review_application transitions + reviewer stamping
  * admin guard on review endpoint
"""

from datetime import datetime, timedelta, timezone

from app.modules.applications.admission_questions_es import MCQ, OPEN_PROMPTS
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
            linkedin_url="https://www.linkedin.com/in/ana",
            country="Perú",
            locale="es",
            answers=[
                ApplicationAnswer(question_id="why_sales", text=_long_answer("a")),
                ApplicationAnswer(question_id="achievement", text=_long_answer("b")),
                ApplicationAnswer(question_id="hours_per_week", text=_long_answer("c")),
            ],
            video_url="https://loom.com/x",
        )
        app_obj, created = create_application(db, data)
        assert created is True
        assert app_obj.id is not None
        assert app_obj.status == "submitted"
        assert app_obj.answers == {
            "why_sales": _long_answer("a"),
            "achievement": _long_answer("b"),
            "hours_per_week": _long_answer("c"),
        }

    def test_timezone_aware_started_at_does_not_crash(self, db):
        """Regresión: el front manda started_at en ISO con 'Z' (tz-aware).

        El speed check restaba `datetime.utcnow()` (naive) − started_at (aware)
        → TypeError → 500 sin CORS → "Network Error" en el navegador. Solo le
        pasaba a quien pasaba los pisos (llega a la regla de velocidad).
        """
        data = ApplicationCreate(
            applicant_name="Aspirante Real",
            applicant_email="real@example.com",
            linkedin_url="https://www.linkedin.com/in/real",
            country="Perú",
            locale="es",
            answers=[
                ApplicationAnswer(
                    question_id=p["id"],
                    text=" ".join(["palabra"] * (p["min_words"] + 5)),
                )
                for p in OPEN_PROMPTS
            ],
            mcq_answers={q["id"]: q["correct"] for q in MCQ},
            # tz-aware, 70 min atrás — exactamente lo que envía el browser.
            started_at=datetime.now(timezone.utc) - timedelta(minutes=70),
            video_url="https://www.youtube.com/watch?v=x",
        )
        app_obj, created = create_application(db, data)
        assert created is True
        assert app_obj.auto_decision == "passed_stage_1"
        # started_at quedó normalizado a naive-UTC.
        assert app_obj.started_at.tzinfo is None

    def test_resubmit_same_email_returns_existing(self, db):
        def _build(name: str) -> ApplicationCreate:
            return ApplicationCreate(
                applicant_name=name,
                applicant_email="dup@example.com",
                linkedin_url="https://www.linkedin.com/in/dup",
                country="Perú",
                locale="es",
                answers=[
                    ApplicationAnswer(question_id="why_sales", text=_long_answer("a")),
                ],
                video_url="https://loom.com/x",
            )

        first, created_first = create_application(db, _build("Primera"))
        second, created_second = create_application(db, _build("Segunda vez"))

        assert created_first is True
        assert created_second is False
        # Idempotente: misma fila, conserva el primer envío.
        assert second.id == first.id
        assert second.applicant_name == "Primera"

    def test_short_answers_are_accepted(self):
        # No imponemos word-count: queremos que el aspirante pueda enviar
        # aunque escriba poco. El filtro lo hace el equipo en revisión.
        ans = ApplicationAnswer(question_id="why_sales", text="ok")
        assert ans.text == "ok"


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
            "linkedin_url": "https://www.linkedin.com/in/luis",
            "country": "Perú",
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

    def test_resubmit_same_email_returns_200_not_201(self, client):
        body = {
            "applicant_name": "Luis",
            "applicant_email": "dup-endpoint@example.com",
            "linkedin_url": "https://www.linkedin.com/in/luis",
            "country": "Perú",
            "locale": "es",
            "video_url": "https://loom.com/x",
            "answers": [{"question_id": "why_sales", "text": _long_answer("a")}],
        }
        first = client.post("/applications", json=body)
        assert first.status_code == 201, first.text
        # Reenvío del mismo email → 200 con la aplicación existente.
        again = client.post("/applications", json=body)
        assert again.status_code == 200, again.text
        assert again.json()["id"] == first.json()["id"]

    def test_post_application_rejects_missing_required_field(self, client):
        # linkedin_url y country son obligatorios en el schema actual.
        body = {
            "applicant_name": "Luis",
            "applicant_email": "luis@example.com",
            "country": "Perú",
            "locale": "es",
            "video_url": "https://loom.com/x",
            "answers": [
                {"question_id": "why_sales", "text": _long_answer("a")},
            ],
        }
        resp = client.post("/applications", json=body)
        assert resp.status_code == 422
        detail = resp.json()["detail"]
        assert any(d.get("loc", [])[-1:] == ["linkedin_url"] for d in detail)

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
