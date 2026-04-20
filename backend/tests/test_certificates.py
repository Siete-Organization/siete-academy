"""Tests for certificates service — eligibility + idempotent issuance."""

from datetime import date

from app.modules.certificates import services
from app.modules.certificates.models import Certificate
from app.modules.cohorts.models import Cohort
from app.modules.enrollment.models import Enrollment


def _seed_cohort(db) -> Cohort:
    c = Cohort(
        name="SDR 001",
        locale="es",
        start_date=date(2026, 5, 1),
        end_date=date(2026, 6, 30),
        status="in_progress",
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return c


class TestCertificateIssuance:
    def test_not_eligible_without_enrollment(self, db, default_student):
        cohort = _seed_cohort(db)
        assert services.issue_if_eligible(db, user_id=default_student.id, cohort_id=cohort.id) is None

    def test_not_eligible_below_100_pct(self, db, default_student):
        cohort = _seed_cohort(db)
        enr = Enrollment(user_id=default_student.id, cohort_id=cohort.id, progress_pct=80.0)
        db.add(enr)
        db.commit()
        assert services.issue_if_eligible(db, user_id=default_student.id, cohort_id=cohort.id) is None

    def test_issues_when_complete(self, db, default_student):
        cohort = _seed_cohort(db)
        enr = Enrollment(user_id=default_student.id, cohort_id=cohort.id, progress_pct=100.0)
        db.add(enr)
        db.commit()
        cert = services.issue_if_eligible(db, user_id=default_student.id, cohort_id=cohort.id)
        assert cert is not None
        assert len(cert.verification_code) >= 10
        assert cert.verification_code.isalnum()
        # Enrollment is marked completed
        db.refresh(enr)
        assert enr.status == "completed"
        assert enr.completed_at is not None

    def test_second_call_is_idempotent(self, db, default_student):
        cohort = _seed_cohort(db)
        enr = Enrollment(user_id=default_student.id, cohort_id=cohort.id, progress_pct=100.0)
        db.add(enr)
        db.commit()
        c1 = services.issue_if_eligible(db, user_id=default_student.id, cohort_id=cohort.id)
        c2 = services.issue_if_eligible(db, user_id=default_student.id, cohort_id=cohort.id)
        assert c1 is not None and c2 is not None
        assert c1.id == c2.id
        assert db.query(Certificate).count() == 1


class TestPublicVerification:
    def test_verify_public_endpoint(self, client, db, default_student):
        cohort = _seed_cohort(db)
        enr = Enrollment(user_id=default_student.id, cohort_id=cohort.id, progress_pct=100.0)
        db.add(enr)
        db.commit()
        cert = services.issue_if_eligible(db, user_id=default_student.id, cohort_id=cohort.id)
        assert cert is not None

        resp = client.get(f"/certificates/verify/{cert.verification_code}")
        assert resp.status_code == 200, resp.text
        body = resp.json()
        assert body["valid"] is True
        assert body["cohort_name"] == "SDR 001"

    def test_verify_unknown_code_404(self, client):
        assert client.get("/certificates/verify/NONEXISTENT").status_code == 404
