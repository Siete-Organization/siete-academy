"""Integration tests for enrollment progress."""

from datetime import date

from app.modules.cohorts.models import Cohort
from app.modules.courses.models import Lesson, Module, ModuleTranslation
from app.modules.enrollment.models import Enrollment, LessonProgress
from app.modules.users.models import User


def _seed_basic(db, user: User) -> tuple[int, int]:
    """Create a cohort + module + lesson + enrollment. Return (enrollment_id, lesson_id)."""
    cohort = Cohort(
        name="SDR 001",
        locale="es",
        start_date=date(2026, 5, 1),
        end_date=date(2026, 6, 30),
        status="in_progress",
    )
    db.add(cohort)
    db.commit()
    db.refresh(cohort)

    from app.modules.courses.models import Course

    course = Course(slug="sdr")
    db.add(course)
    db.commit()
    db.refresh(course)

    mod = Module(course_id=course.id, slug="icp", order_index=0)
    db.add(mod)
    db.commit()
    db.refresh(mod)
    db.add(ModuleTranslation(module_id=mod.id, locale="es", title="ICP"))
    lesson = Lesson(module_id=mod.id, order_index=0, youtube_id="abc")
    db.add(lesson)
    db.commit()
    db.refresh(lesson)

    enr = Enrollment(user_id=user.id, cohort_id=cohort.id)
    db.add(enr)
    db.commit()
    db.refresh(enr)
    return enr.id, lesson.id


def test_post_progress_upserts_and_sets_completed_at(client, db):
    # client fixture already seeds a student user (id=1)
    student = db.query(User).filter_by(firebase_uid="uid-student").first()
    enr_id, lesson_id = _seed_basic(db, student)

    resp = client.post(
        f"/enrollment/{enr_id}/progress",
        json={"lesson_id": lesson_id, "watched_pct": 50, "completed": False},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["watched_pct"] == 50
    assert body["completed_at"] is None

    # Same lesson, mark completed — watched_pct should not go backward
    resp2 = client.post(
        f"/enrollment/{enr_id}/progress",
        json={"lesson_id": lesson_id, "watched_pct": 30, "completed": True},
    )
    body2 = resp2.json()
    assert body2["watched_pct"] == 50  # max-preserved
    assert body2["completed_at"] is not None
    # Only one progress row exists
    count = db.query(LessonProgress).filter_by(enrollment_id=enr_id, lesson_id=lesson_id).count()
    assert count == 1


def test_post_progress_forbidden_on_other_user_enrollment(client, db, login_as):
    # Create an enrollment for a different user
    other = User(
        firebase_uid="uid-other",
        email="other@test.dev",
        display_name="Other",
        role="student",
        locale="es",
    )
    db.add(other)
    db.commit()
    db.refresh(other)

    enr_id, lesson_id = _seed_basic(db, other)

    # Default client is the student with id=1 (not `other`)
    resp = client.post(
        f"/enrollment/{enr_id}/progress",
        json={"lesson_id": lesson_id, "watched_pct": 10, "completed": False},
    )
    assert resp.status_code == 403
