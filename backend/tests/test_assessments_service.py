"""Tests for assessments.services — grading + submission state transitions."""

import pytest

from app.modules.assessments.models import Assessment, Submission
from app.modules.assessments.services import auto_grade_mcq, submit
from app.modules.courses.models import Course, Module
from app.modules.users.models import User


def _build_mcq(**overrides) -> Assessment:
    """Pure-memory Assessment — no DB needed for grading tests."""
    base = dict(
        module_id=1,
        type="mcq",
        title="Quiz 1",
        config={"correct_answers": {"q1": "a", "q2": "b", "q3": "c"}},
        passing_score=70.0,
    )
    base.update(overrides)
    return Assessment(**base)


def _seed_module(db) -> int:
    c = Course(slug="sdr")
    db.add(c)
    db.commit()
    db.refresh(c)
    m = Module(course_id=c.id, slug="m1", order_index=0)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m.id


@pytest.fixture
def test_user(db) -> User:
    u = User(
        firebase_uid="uid-sub-user",
        email="sub@test.dev",
        display_name="Sub User",
        role="student",
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    return u


@pytest.fixture
def mcq_assessment_db(db):
    module_id = _seed_module(db)
    a = Assessment(
        module_id=module_id,
        type="mcq",
        title="Quiz 1",
        config={"correct_answers": {"q1": "a", "q2": "b", "q3": "c"}},
        passing_score=70.0,
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


@pytest.fixture
def written_assessment_db(db):
    module_id = _seed_module(db)
    a = Assessment(
        module_id=module_id,
        type="written",
        title="Write an email",
        config={"prompt": "Draft a cold email."},
        passing_score=70.0,
    )
    db.add(a)
    db.commit()
    db.refresh(a)
    return a


class TestAutoGradeMcq:
    """Pure-function grading — no DB."""

    def test_all_correct_returns_100(self):
        score = auto_grade_mcq(_build_mcq(), {"answers": {"q1": "a", "q2": "b", "q3": "c"}})
        assert score == 100.0

    def test_partial_correct_rounds_to_two_decimals(self):
        score = auto_grade_mcq(_build_mcq(), {"answers": {"q1": "a", "q2": "b", "q3": "z"}})
        assert score == 66.67

    def test_all_wrong_returns_zero(self):
        score = auto_grade_mcq(_build_mcq(), {"answers": {"q1": "x", "q2": "y", "q3": "z"}})
        assert score == 0.0

    def test_missing_answers_returns_zero(self):
        score = auto_grade_mcq(_build_mcq(), {"answers": {}})
        assert score == 0.0

    def test_empty_payload_returns_zero(self):
        score = auto_grade_mcq(_build_mcq(), {})
        assert score == 0.0

    def test_answers_coerced_to_string_for_comparison(self):
        # Student sends an int but config has string — still matches via string coercion
        assessment = _build_mcq(config={"correct_answers": {"q1": "2"}})
        score = auto_grade_mcq(assessment, {"answers": {"q1": 2}})
        assert score == 100.0

    def test_non_mcq_assessment_returns_none(self):
        a = _build_mcq(type="written", config={})
        assert auto_grade_mcq(a, {"text": "anything"}) is None

    def test_mcq_without_correct_answers_returns_none(self):
        a = _build_mcq(config={})
        assert auto_grade_mcq(a, {"answers": {"q1": "a"}}) is None


class TestAutoGradeMcqQuestionsShape:
    """Nuevo shape: config["questions"] con type single/multi/match."""

    def _cfg(self):
        return {
            "questions": [
                {"id": "q1", "type": "single", "correct": ["c"]},
                {"id": "q2", "type": "multi", "correct": ["2", "4", "7"]},
                {
                    "id": "q3",
                    "type": "match",
                    "correct": {"1": "A", "2": "B", "3": "C"},
                },
            ]
        }

    def test_all_correct(self):
        a = _build_mcq(config=self._cfg())
        score = auto_grade_mcq(
            a,
            {
                "answers": {
                    "q1": "c",
                    "q2": ["2", "4", "7"],
                    "q3": {"1": "A", "2": "B", "3": "C"},
                }
            },
        )
        assert score == 100.0

    def test_multi_partial_not_counted(self):
        """Multi-select requires the exact set — no partial credit per question."""
        a = _build_mcq(config=self._cfg())
        score = auto_grade_mcq(
            a,
            {
                "answers": {
                    "q1": "c",
                    "q2": ["2", "4"],  # missing 7
                    "q3": {"1": "A", "2": "B", "3": "C"},
                }
            },
        )
        # 2 of 3 correct = 66.67
        assert score == 66.67

    def test_match_extra_keys_fails(self):
        a = _build_mcq(config=self._cfg())
        score = auto_grade_mcq(
            a,
            {
                "answers": {
                    "q1": "c",
                    "q2": ["2", "4", "7"],
                    "q3": {"1": "A", "2": "B", "3": "C", "4": "Z"},
                }
            },
        )
        assert score == 66.67

    def test_missing_answer_for_a_question(self):
        a = _build_mcq(config=self._cfg())
        score = auto_grade_mcq(
            a,
            {"answers": {"q1": "c", "q2": ["2", "4", "7"]}},
        )
        assert score == 66.67


class TestSubmit:
    def test_mcq_submission_is_auto_graded(self, db, mcq_assessment_db, test_user):
        sub = submit(
            db,
            assessment_id=mcq_assessment_db.id,
            user_id=test_user.id,
            payload={"answers": {"q1": "a", "q2": "b", "q3": "c"}},
            file_url=None,
        )
        assert sub.status == "auto_graded"
        assert sub.auto_score == 100.0

    def test_written_submission_is_pending_review(self, db, written_assessment_db, test_user):
        sub = submit(
            db,
            assessment_id=written_assessment_db.id,
            user_id=test_user.id,
            payload={"text": "Hi there — quick question about your ICP…"},
            file_url=None,
        )
        assert sub.status == "pending_review"
        assert sub.auto_score is None

    def test_submit_persists_payload_and_file_url(self, db, written_assessment_db, test_user):
        sub = submit(
            db,
            assessment_id=written_assessment_db.id,
            user_id=test_user.id,
            payload={"text": "draft"},
            file_url="https://example.com/f.pdf",
        )
        reloaded = db.get(Submission, sub.id)
        assert reloaded is not None
        assert reloaded.payload == {"text": "draft"}
        assert reloaded.file_url == "https://example.com/f.pdf"

    def test_submit_raises_on_unknown_assessment(self, db, test_user):
        with pytest.raises(ValueError, match="Assessment not found"):
            submit(db, assessment_id=99999, user_id=test_user.id, payload={}, file_url=None)

    def test_capa2_submission_stays_pending_review_even_with_mcq(
        self, db, test_user
    ):
        """Capa_2 mezcla MCQ (auto-grade) + video (manual). El auto-grado del MCQ
        no debe sacar la entrega de la cola del teacher — el video tiene que ser
        revisado para que la fórmula 70/30 funcione.
        """
        module_id = _seed_module(db)
        a = Assessment(
            module_id=module_id,
            type="capa_2",
            title="Prueba M1",
            config={
                "questions": [{"id": "q1", "type": "single", "correct": ["a"]}],
            },
            passing_score=65.0,
        )
        db.add(a)
        db.commit()
        db.refresh(a)
        sub = submit(
            db,
            assessment_id=a.id,
            user_id=test_user.id,
            payload={"answers": {"q1": "a"}, "video_url": "https://loom.com/x"},
            file_url=None,
        )
        assert sub.status == "pending_review"
        # MCQ ya tiene puntaje calculado para que el teacher lo use
        assert sub.auto_score == 100.0

    def test_final_test_submission_stays_pending_review(self, db, test_user):
        """Igual que capa_2, la Prueba Final requiere review humano del video."""
        module_id = _seed_module(db)
        a = Assessment(
            module_id=module_id,
            type="final_test",
            title="Prueba Final",
            config={
                "questions": [{"id": "q1", "type": "single", "correct": ["b"]}],
            },
            passing_score=60.0,
        )
        db.add(a)
        db.commit()
        db.refresh(a)
        sub = submit(
            db,
            assessment_id=a.id,
            user_id=test_user.id,
            payload={"answers": {"q1": "b"}},
            file_url=None,
        )
        assert sub.status == "pending_review"
