"""Tests para C.2 — notificación Slack al subir video de capa_2 / final_test."""
from __future__ import annotations

from unittest.mock import patch

import pytest

from app.modules.assessments.models import Assessment
from app.modules.courses.models import Course, Module, ModuleTranslation
from app.modules.notifications import services as notif_services


@pytest.fixture
def module_m1(db) -> Module:
    course = Course(slug="sdr-academy-v1")
    db.add(course)
    db.commit()
    db.refresh(course)
    m = Module(course_id=course.id, slug="m1-x", order_index=1)
    m.translations.append(ModuleTranslation(locale="es", title="M1"))
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


@pytest.fixture
def capa2_assessment(db, module_m1) -> Assessment:
    a = Assessment(
        module_id=module_m1.id,
        type="capa_2",
        title="Prueba M1",
        config={"questions": [{"id": "q1", "type": "single", "correct": ["a"]}]},
        passing_score=65.0,
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


@pytest.fixture
def final_assessment(db, module_m1) -> Assessment:
    a = Assessment(
        module_id=module_m1.id,
        type="final_test",
        title="Prueba Final",
        config={"questions": [{"id": "q1", "type": "single", "correct": ["b"]}]},
        passing_score=60.0,
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


# ──────────────────────────  Service-level tests  ──────────────────────────


class TestSendSlackVideoNotify:
    def test_stubbed_when_url_not_set(self, monkeypatch, caplog):
        """Sin SLACK_VIDEO_NOTIFY_URL, loguea y no falla."""
        from app.core.config import get_settings

        get_settings.cache_clear()
        monkeypatch.delenv("SLACK_VIDEO_NOTIFY_URL", raising=False)

        with caplog.at_level("INFO"):
            notif_services.send_slack_video_notify(
                student_name="Alice",
                student_email="alice@test.dev",
                module_label="Módulo 1",
                video_url="https://loom.com/x",
                assessment_title="Prueba M1",
            )
        get_settings.cache_clear()
        # Sin URL configurada, debe haber logueado el stub
        assert any("slack_video.stubbed" in r.message for r in caplog.records)

    def test_posts_to_webhook_when_url_set(self, monkeypatch):
        """Con URL configurada, hace POST con el payload formateado."""
        from app.core.config import get_settings

        monkeypatch.setenv("SLACK_VIDEO_NOTIFY_URL", "https://hooks.slack.com/X")
        get_settings.cache_clear()

        calls: list[dict] = []

        def fake_post(url, json, timeout):  # noqa: ARG001
            calls.append({"url": url, "json": json})

            class R:
                def raise_for_status(self):
                    return None

            return R()

        with patch("httpx.post", side_effect=fake_post):
            notif_services.send_slack_video_notify(
                student_name="Alice",
                student_email="alice@test.dev",
                module_label="Módulo 1",
                video_url="https://loom.com/x",
                assessment_title="Prueba M1",
            )

        get_settings.cache_clear()

        assert len(calls) == 1
        assert calls[0]["url"] == "https://hooks.slack.com/X"
        text = calls[0]["json"]["text"]
        assert "Alice" in text
        assert "Módulo 1" in text
        assert "Prueba M1" in text
        assert "https://loom.com/x" in text

    def test_failure_does_not_raise(self, monkeypatch, caplog):
        """Si el POST falla, no debe propagar la excepción (alumno no debe ver 5xx)."""
        from app.core.config import get_settings

        monkeypatch.setenv("SLACK_VIDEO_NOTIFY_URL", "https://hooks.slack.com/X")
        get_settings.cache_clear()

        def boom(*args, **kwargs):  # noqa: ARG001
            raise RuntimeError("network down")

        with patch("httpx.post", side_effect=boom), caplog.at_level("WARNING"):
            notif_services.send_slack_video_notify(
                student_name="Alice",
                student_email="alice@test.dev",
                module_label="Módulo 1",
                video_url="https://loom.com/x",
                assessment_title="Prueba M1",
            )

        get_settings.cache_clear()
        assert any("slack_video.failed" in r.message for r in caplog.records)


# ─────────────────────────  Submit endpoint integration  ─────────────────────


class TestSubmitTriggersSlackNotify:
    def test_capa2_submission_with_file_url_triggers_notify(
        self, client, capa2_assessment, default_student
    ):
        with patch(
            "app.modules.assessments.router.send_slack_video_notify_task"
        ) as mock_task:
            r = client.post(
                "/assessments/submissions",
                json={
                    "assessment_id": capa2_assessment.id,
                    "payload": {"answers": {"q1": "a"}},
                    "file_url": "https://loom.com/case-a",
                },
            )
        assert r.status_code == 201
        mock_task.delay.assert_called_once()
        kwargs = mock_task.delay.call_args.kwargs
        assert kwargs["student_email"] == default_student.email
        assert kwargs["module_label"] == "Módulo 1"
        assert kwargs["video_url"] == "https://loom.com/case-a"

    def test_capa2_submission_without_file_url_does_not_notify(
        self, client, capa2_assessment
    ):
        with patch(
            "app.modules.assessments.router.send_slack_video_notify_task"
        ) as mock_task:
            r = client.post(
                "/assessments/submissions",
                json={
                    "assessment_id": capa2_assessment.id,
                    "payload": {"answers": {"q1": "a"}},
                },
            )
        assert r.status_code == 201
        mock_task.delay.assert_not_called()

    def test_capa2_with_video_url_in_payload_triggers_notify(
        self, client, capa2_assessment
    ):
        """También dispara si el front mete video_url en payload en lugar de file_url."""
        with patch(
            "app.modules.assessments.router.send_slack_video_notify_task"
        ) as mock_task:
            r = client.post(
                "/assessments/submissions",
                json={
                    "assessment_id": capa2_assessment.id,
                    "payload": {
                        "answers": {"q1": "a"},
                        "video_url": "https://youtu.be/abc",
                    },
                },
            )
        assert r.status_code == 201
        mock_task.delay.assert_called_once()
        assert (
            mock_task.delay.call_args.kwargs["video_url"] == "https://youtu.be/abc"
        )

    def test_final_test_submission_uses_prueba_final_label(
        self, client, final_assessment
    ):
        with patch(
            "app.modules.assessments.router.send_slack_video_notify_task"
        ) as mock_task:
            r = client.post(
                "/assessments/submissions",
                json={
                    "assessment_id": final_assessment.id,
                    "payload": {"answers": {"q1": "b"}},
                    "file_url": "https://loom.com/final-defense",
                },
            )
        assert r.status_code == 201
        mock_task.delay.assert_called_once()
        assert mock_task.delay.call_args.kwargs["module_label"] == "Prueba Final"

    def test_mcq_submission_does_not_notify(self, client, db, module_m1):
        """Las micro-pruebas (type=mcq) no deben disparar Slack — son auto-graded sin video."""
        a = Assessment(
            module_id=module_m1.id,
            type="mcq",
            title="Micro w1",
            config={"questions": [{"id": "q1", "type": "single", "correct": ["a"]}]},
            passing_score=70.0,
        )
        db.add(a)
        db.commit()
        db.refresh(a)

        with patch(
            "app.modules.assessments.router.send_slack_video_notify_task"
        ) as mock_task:
            r = client.post(
                "/assessments/submissions",
                json={
                    "assessment_id": a.id,
                    "payload": {"answers": {"q1": "a"}},
                    "file_url": "https://loom.com/x",  # incluso con file_url
                },
            )
        assert r.status_code == 201
        mock_task.delay.assert_not_called()

    def test_slack_failure_does_not_break_submission(
        self, client, capa2_assessment
    ):
        """Si .delay() lanza, la submission igual debe completarse."""
        with patch(
            "app.modules.assessments.router.send_slack_video_notify_task"
        ) as mock_task:
            mock_task.delay.side_effect = RuntimeError("broker down")
            r = client.post(
                "/assessments/submissions",
                json={
                    "assessment_id": capa2_assessment.id,
                    "payload": {"answers": {"q1": "a"}},
                    "file_url": "https://loom.com/x",
                },
            )
        # Submission persistida igual
        assert r.status_code == 201
        assert r.json()["status"] == "pending_review"
