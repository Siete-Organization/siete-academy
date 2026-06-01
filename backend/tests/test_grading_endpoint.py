"""Tests de integración del endpoint /grading/results.

Crea un escenario realista: 1 cohorte, 2 alumnos, 2 módulos con micro-pruebas (capa 1)
+ prueba módulo (capa 2), + 1 prueba final (capa 3). Verifica que la agregación,
las fórmulas y los umbrales se reflejan en el response.
"""
from __future__ import annotations

from datetime import date

import pytest

from app.modules.assessments.models import Assessment, Submission, TeacherReview
from app.modules.cohorts.models import Cohort
from app.modules.courses.models import (
    Course,
    Lesson,
    Module,
    ModuleTranslation,
)
from app.modules.enrollment.models import Enrollment
from app.modules.users.models import User


@pytest.fixture
def scenario(db):
    """Curso `sdr-academy-v1` con 2 módulos, 1 micro-prueba por módulo,
    1 prueba de módulo y 1 prueba final. 2 alumnos inscritos.
    """
    course = Course(slug="sdr-academy-v1")
    db.add(course)
    db.commit()
    db.refresh(course)

    # 4 módulos con 1 lesson cada uno (matchea la realidad del curso SDR)
    mods = []
    lessons = []
    for i in range(1, 5):
        m = Module(course_id=course.id, slug=f"m{i}", order_index=i)
        m.translations.append(ModuleTranslation(locale="es", title=f"Módulo {i}"))
        db.add(m)
        db.commit()
        db.refresh(m)
        mods.append(m)
        lesson = Lesson(module_id=m.id, order_index=0, kind="video")
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
        lessons.append(lesson)

    # Cohorte
    cohort = Cohort(
        name="Cohorte Test",
        locale="es",
        start_date=date(2026, 1, 1),
        end_date=date(2026, 3, 1),
        status="in_progress",
    )
    db.add(cohort)
    db.commit()
    db.refresh(cohort)

    # 2 alumnos: alice (alta perf), bob (mid)
    alice = User(
        firebase_uid="uid-alice", email="alice@test.dev", display_name="Alice",
        role="student", locale="es",
    )
    bob = User(
        firebase_uid="uid-bob", email="bob@test.dev", display_name="Bob",
        role="student", locale="es",
    )
    db.add_all([alice, bob])
    db.commit()
    db.refresh(alice)
    db.refresh(bob)
    db.add(Enrollment(user_id=alice.id, cohort_id=cohort.id, status="active"))
    db.add(Enrollment(user_id=bob.id, cohort_id=cohort.id, status="active"))
    db.commit()

    # Capa 1 — micro-prueba por módulo (asociada a lesson)
    capa1: list[Assessment] = []
    for m, lsn in zip(mods, lessons):
        a = Assessment(
            module_id=m.id, lesson_id=lsn.id, type="mcq",
            title=f"Micro {m.slug}", config={}, passing_score=70.0,
        )
        db.add(a)
        db.commit()
        db.refresh(a)
        capa1.append(a)

    # Capa 2 — prueba módulo por módulo
    capa2: list[Assessment] = []
    for m in mods:
        a = Assessment(
            module_id=m.id, lesson_id=None, type="capa_2",
            title=f"Prueba {m.slug}", config={}, passing_score=65.0,
        )
        db.add(a)
        db.commit()
        db.refresh(a)
        capa2.append(a)

    # Capa 3 — prueba final asignada al último módulo
    final_a = Assessment(
        module_id=mods[-1].id, lesson_id=None, type="final_test",
        title="Prueba Final", config={}, passing_score=60.0,
    )
    db.add(final_a)
    db.commit()
    db.refresh(final_a)

    return {
        "cohort": cohort,
        "course": course,
        "modules": mods,
        "alice": alice,
        "bob": bob,
        "capa1": capa1,
        "capa2": capa2,
        "final": final_a,
    }


def _submit(db, *, assessment_id, user_id, auto_score, review_score=None):
    s = Submission(
        assessment_id=assessment_id,
        user_id=user_id,
        payload={},
        auto_score=auto_score,
        status="auto_graded" if review_score is None else "reviewed",
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    if review_score is not None:
        tr = TeacherReview(
            submission_id=s.id, teacher_id=user_id, score=review_score,
            feedback="ok",
        )
        db.add(tr)
        db.commit()
    return s


# ────────────────────────────  Tests  ────────────────────────────


def test_admin_can_fetch_results(client, login_as, scenario):
    login_as("admin")
    r = client.get("/grading/results", params={"cohort_id": scenario["cohort"].id})
    assert r.status_code == 200
    body = r.json()
    assert body["cohort_id"] == scenario["cohort"].id
    # 4 módulos cargados, 2 alumnos
    assert len(body["modules"]) == 4
    assert len(body["students"]) == 2


def test_teacher_can_fetch_results(client, login_as, scenario):
    login_as("teacher")
    r = client.get("/grading/results", params={"cohort_id": scenario["cohort"].id})
    assert r.status_code == 200


def test_student_cannot_fetch_results(client, scenario):
    # client fixture default es student
    r = client.get("/grading/results", params={"cohort_id": scenario["cohort"].id})
    assert r.status_code == 403


def test_empty_cohort_returns_no_students(client, login_as, db):
    login_as("admin")
    empty = Cohort(
        name="Vacía", locale="es",
        start_date=date(2026, 1, 1), end_date=date(2026, 3, 1),
        status="draft",
    )
    db.add(empty)
    db.commit()
    db.refresh(empty)
    r = client.get("/grading/results", params={"cohort_id": empty.id})
    assert r.status_code == 200
    assert r.json()["students"] == []


def test_student_in_progress_when_no_submissions(client, login_as, scenario):
    login_as("admin")
    r = client.get("/grading/results", params={"cohort_id": scenario["cohort"].id})
    s = next(x for x in r.json()["students"] if x["email"] == "alice@test.dev")
    assert s["course_total"] is None
    assert s["status"] == "in_progress"
    for m in s["modules"]:
        assert m["capa_2_score"] is None
        assert m["capa_1_avg"] is None


def test_distinction_path(client, login_as, db, scenario):
    """Alice clava todo en ambos módulos + final → 'distinction'."""
    login_as("admin")
    alice = scenario["alice"]
    # Micro-pruebas: 90 en cada módulo
    for a in scenario["capa1"]:
        _submit(db, assessment_id=a.id, user_id=alice.id, auto_score=90.0)
    # Pruebas módulo: 90 MCQ + 90 video → 90% ≥ 80
    for a in scenario["capa2"]:
        _submit(db, assessment_id=a.id, user_id=alice.id, auto_score=90.0, review_score=90.0)
    # Prueba final: 90 caso + 90 video → 90% ≥ 85
    _submit(
        db, assessment_id=scenario["final"].id, user_id=alice.id,
        auto_score=90.0, review_score=90.0,
    )

    r = client.get("/grading/results", params={"cohort_id": scenario["cohort"].id})
    s = next(x for x in r.json()["students"] if x["email"] == "alice@test.dev")

    # Verificamos cada pieza
    for mr in s["modules"]:
        assert mr["capa_1_avg"] == 90.0
        assert mr["capa_2_score"] == 90.0
    assert s["final"]["score"] == 90.0
    # Curso = 90*0.20 + 90*0.50 + 90*0.30 = 90
    assert s["course_total"] == 90.0
    assert s["status"] == "distinction"


def test_basic_path(client, login_as, db, scenario):
    """Bob aprueba justo:
    - micros 75, módulos 72, final 65
    - curso = 75*0.20 + 72*0.50 + 65*0.30 = 15 + 36 + 19.5 = 70.5 ≥ 70 → basic.
    """
    login_as("admin")
    bob = scenario["bob"]
    for a in scenario["capa1"]:
        _submit(db, assessment_id=a.id, user_id=bob.id, auto_score=75.0)
    for a in scenario["capa2"]:
        _submit(db, assessment_id=a.id, user_id=bob.id, auto_score=72.0, review_score=72.0)
    _submit(
        db, assessment_id=scenario["final"].id, user_id=bob.id,
        auto_score=65.0, review_score=65.0,
    )

    r = client.get("/grading/results", params={"cohort_id": scenario["cohort"].id})
    s = next(x for x in r.json()["students"] if x["email"] == "bob@test.dev")
    assert s["course_total"] == 70.5
    assert s["status"] == "basic"


def test_capa2_only_mcq_no_review_is_none(client, login_as, db, scenario):
    """Si una capa_2 tiene solo MCQ (sin teacher review) → capa_2_score es None."""
    login_as("admin")
    alice = scenario["alice"]
    capa2 = scenario["capa2"][0]
    _submit(db, assessment_id=capa2.id, user_id=alice.id, auto_score=80.0)
    # No teacher review → no podemos calcular módulo (falta video)

    r = client.get("/grading/results", params={"cohort_id": scenario["cohort"].id})
    s = next(x for x in r.json()["students"] if x["email"] == "alice@test.dev")
    mr = s["modules"][0]
    assert mr["capa_2_mcq"] == 80.0
    assert mr["capa_2_video"] is None
    assert mr["capa_2_score"] is None


def test_module_order_stable(client, login_as, scenario):
    login_as("admin")
    r = client.get("/grading/results", params={"cohort_id": scenario["cohort"].id})
    modules = r.json()["modules"]
    assert [m["order_index"] for m in modules] == sorted([m["order_index"] for m in modules])
