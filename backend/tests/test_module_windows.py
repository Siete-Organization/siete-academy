"""Tests for module-window management: patch dates + open/close now."""

from datetime import date, datetime, timedelta

import pytest

from app.modules.cohorts.models import Cohort, ModuleWindow
from app.modules.courses.models import Course, Module


@pytest.fixture
def cohort_and_window(db):
    c = Cohort(
        name="SDR 002",
        locale="es",
        start_date=date(2026, 6, 1),
        end_date=date(2026, 7, 31),
        status="open_applications",
    )
    db.add(c)
    course = Course(slug="sdr-test")
    db.add(course)
    db.commit()
    db.refresh(c)
    db.refresh(course)
    m = Module(course_id=course.id, slug="icp", order_index=0)
    db.add(m)
    db.commit()
    db.refresh(m)
    w = ModuleWindow(
        cohort_id=c.id,
        module_id=m.id,
        opens_at=datetime(2027, 1, 1),
        closes_at=datetime(2027, 1, 15),
    )
    db.add(w)
    db.commit()
    db.refresh(w)
    return c, w


class TestModuleWindowManagement:
    def test_patch_updates_dates_admin_allowed(self, client, db, login_as, cohort_and_window):
        _cohort, w = cohort_and_window
        login_as("admin")
        new_opens = "2026-09-01T10:00:00"
        resp = client.patch(
            f"/cohorts/{w.cohort_id}/windows/{w.id}",
            json={"opens_at": new_opens, "closes_at": "2026-09-15T23:59:00"},
        )
        assert resp.status_code == 200, resp.text
        body = resp.json()
        assert body["opens_at"].startswith("2026-09-01")

    def test_patch_forbidden_to_student(self, client, cohort_and_window):
        _cohort, w = cohort_and_window
        resp = client.patch(
            f"/cohorts/{w.cohort_id}/windows/{w.id}",
            json={"opens_at": "2026-09-01T10:00:00"},
        )
        assert resp.status_code == 403

    def test_teacher_can_open_and_close(self, client, db, login_as, cohort_and_window):
        _cohort, w = cohort_and_window
        login_as("teacher")

        # opens_at is in the far future → currently closed
        resp_open = client.post(f"/cohorts/{w.cohort_id}/windows/{w.id}/open")
        assert resp_open.status_code == 200, resp_open.text
        body = resp_open.json()
        assert datetime.fromisoformat(body["opens_at"]) < datetime.utcnow() + timedelta(minutes=1)

        resp_close = client.post(f"/cohorts/{w.cohort_id}/windows/{w.id}/close")
        assert resp_close.status_code == 200
        body = resp_close.json()
        assert datetime.fromisoformat(body["closes_at"]) <= datetime.utcnow() + timedelta(seconds=5)
