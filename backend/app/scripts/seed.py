"""Rich seed for local demo.

Creates enough data so that an admin/teacher/student/recruiter can log in
(via dev bypass) and exercise every screen of the product. Idempotent — safe
to re-run. Reads-first so it only inserts missing rows.

Usage:
    cd backend && .venv/bin/python -m app.scripts.seed
    # or
    make seed
"""

from __future__ import annotations

from datetime import UTC, date, datetime, timedelta

from app.core.database import Base, SessionLocal, engine
from app.core.logging import configure_logging, get_logger
from app.modules.applications.models import Application
from app.modules.applications import models as _apps  # noqa: F401
from app.modules.assessments.models import AIReview, Assessment, Submission, TeacherReview
from app.modules.assessments import models as _assess  # noqa: F401
from app.modules.audit import models as _audit  # noqa: F401
from app.modules.certificates import models as _certs  # noqa: F401
from app.modules.cohorts.models import Cohort, ModuleWindow
from app.modules.cohorts import models as _cohorts  # noqa: F401
from app.modules.courses.models import (
    Course,
    CourseTranslation,
    Lesson,
    LessonTranslation,
    Module,
    ModuleTranslation,
)
from app.modules.courses import models as _courses  # noqa: F401
from app.modules.enrollment.models import Enrollment
from app.modules.enrollment import models as _enroll  # noqa: F401
from app.modules.live_sessions.models import LiveSession
from app.modules.live_sessions import models as _live  # noqa: F401
from app.modules.placement.models import PlacementCandidate, PlacementEvent
from app.modules.placement import models as _place  # noqa: F401
from app.modules.users.models import User
from app.modules.users import models as _users  # noqa: F401

configure_logging()
log = get_logger("seed")


def _ensure_schema() -> None:
    Base.metadata.create_all(engine)


def _upsert(db, model, *, lookup: dict, defaults: dict | None = None):
    instance = db.query(model).filter_by(**lookup).first()
    if instance:
        return instance, False
    data = {**lookup, **(defaults or {})}
    instance = model(**data)
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance, True


def seed_users(db) -> dict[str, User]:
    specs = [
        ("admin@siete.com", "Admin Siete", "admin", "seed-admin"),
        ("teacher@siete.com", "Mariana López", "teacher", "seed-teacher"),
        ("student@siete.com", "Luis Carrillo", "student", "seed-student"),
        ("recruiter@siete.com", "HR Cliente", "recruiter", "seed-recruiter"),
        ("camila@example.com", "Camila Reyes", "student", "seed-student-2"),
        ("diego@example.com", "Diego Pereira", "student", "seed-student-3"),
    ]
    created_users: list[User] = []
    for email, name, role, uid in specs:
        u, created = _upsert(
            db,
            User,
            lookup={"email": email},
            defaults={"firebase_uid": uid, "display_name": name, "role": role, "locale": "es"},
        )
        created_users.append(u)
        if created:
            log.info("seed.user", extra={"email": email, "role": role})
    by_email = {u.email: u for u in created_users}
    return {
        "admin": by_email["admin@siete.com"],
        "teacher": by_email["teacher@siete.com"],
        "student": by_email["student@siete.com"],
        "recruiter": by_email["recruiter@siete.com"],
        "camila": by_email["camila@example.com"],
        "diego": by_email["diego@example.com"],
    }


def seed_applications(db) -> None:
    if db.query(Application).count() > 0:
        return
    long_text = lambda p: " ".join(f"{p}{i}" for i in range(105))  # noqa: E731
    apps = [
        Application(
            applicant_name="Sofía Martínez",
            applicant_email="sofia.m@example.com",
            applicant_phone="+57 300 555 1212",
            locale="es",
            answers={
                "why_sales": long_text("a"),
                "achievement": long_text("b"),
                "hours_per_week": long_text("c"),
            },
            video_url="https://loom.com/share/demo-sofia",
            status="submitted",
        ),
        Application(
            applicant_name="Rodrigo Castro",
            applicant_email="rodrigo.c@example.com",
            locale="es",
            answers={
                "why_sales": long_text("x"),
                "achievement": long_text("y"),
                "hours_per_week": long_text("z"),
            },
            video_url="https://loom.com/share/demo-rodrigo",
            ai_score=78,
            ai_notes=(
                "Comunicación clara, motivación genuina. "
                "Banderas: dice 20h/sem pero trabaja full-time."
            ),
            status="under_review",
        ),
    ]
    for a in apps:
        db.add(a)
    db.commit()
    log.info("seed.applications", extra={"count": len(apps)})


def seed_course(db) -> dict[int, Module]:
    course, _ = _upsert(db, Course, lookup={"slug": "sdr-fundamentals"})
    if not course.translations:
        course.translations = [
            CourseTranslation(locale="es", title="Fundamentos SDR", description="Programa base de ocho semanas."),
            CourseTranslation(locale="en", title="SDR Fundamentals", description="Core eight-week program."),
            CourseTranslation(locale="pt", title="Fundamentos SDR", description="Programa base de oito semanas."),
        ]
        db.commit()

    modules_spec = [
        (
            0,
            "modelos-de-negocio",
            {"es": "Modelos de negocio", "en": "Business models", "pt": "Modelos de negócio"},
            {"es": "Cómo se gana dinero en B2B.", "en": "How money is made in B2B.", "pt": "Como se ganha dinheiro em B2B."},
        ),
        (
            1,
            "icp",
            {"es": "Ideal Customer Profile", "en": "Ideal Customer Profile", "pt": "Ideal Customer Profile"},
            {"es": "Del buyer persona al ICP utilitario.", "en": "From persona to practical ICP.", "pt": "Do persona ao ICP prático."},
        ),
        (
            2,
            "metodologia-sdr",
            {"es": "Metodología SDR", "en": "SDR methodology", "pt": "Metodologia SDR"},
            {"es": "Cadencias, discovery, qualification.", "en": "Cadences, discovery, qualification.", "pt": "Cadências, discovery, qualification."},
        ),
        (
            3,
            "herramientas-y-cold-calling",
            {"es": "Herramientas & Cold Calling", "en": "Tooling & Cold Calling", "pt": "Ferramentas & Cold Calling"},
            {"es": "Stack real + tu primera llamada en vivo.", "en": "Real stack + your first live call.", "pt": "Stack real + sua primeira ligação."},
        ),
    ]

    mods: dict[int, Module] = {}
    LESSON_VIDEOS = ["LXb3EKWsInQ", "pN-Z2kDpL6Q"]

    for order, slug, titles, summaries in modules_spec:
        m, created = _upsert(
            db,
            Module,
            lookup={"course_id": course.id, "slug": slug},
            defaults={"order_index": order},
        )
        if created or not m.translations:
            for loc, t in titles.items():
                m.translations.append(
                    ModuleTranslation(locale=loc, title=t, summary=summaries[loc])
                )
            db.commit()
        mods[order] = m

        if not m.lessons:
            for idx, yid in enumerate(LESSON_VIDEOS):
                le = Lesson(
                    module_id=m.id,
                    order_index=idx,
                    youtube_id=yid,
                    duration_seconds=600 + idx * 120,
                )
                le.translations.extend(
                    [
                        LessonTranslation(
                            locale="es",
                            title=f"Lección {idx + 1}: {titles['es']}",
                            body=f"Video guía de la lección {idx + 1}. Toma notas y haz los ejercicios al final.",
                        ),
                        LessonTranslation(
                            locale="en",
                            title=f"Lesson {idx + 1}: {titles['en']}",
                            body=f"Guide video for lesson {idx + 1}. Take notes and do the exercises.",
                        ),
                        LessonTranslation(
                            locale="pt",
                            title=f"Aula {idx + 1}: {titles['pt']}",
                            body=f"Vídeo guia da aula {idx + 1}. Tome notas e faça os exercícios.",
                        ),
                    ]
                )
                db.add(le)
            db.commit()
        if created:
            log.info("seed.module", extra={"slug": slug})

    return mods


def seed_assessments(db, mods: dict[int, Module]) -> dict[int, list[Assessment]]:
    out: dict[int, list[Assessment]] = {0: [], 1: [], 2: [], 3: []}
    specs = [
        (
            0, "mcq", "Quiz — Modelos de negocio",
            {
                "questions": [
                    {"id": "q1", "prompt": "¿Cuál es el principal driver de valor en un SaaS B2B?",
                     "options": {"a": "NPS", "b": "MRR recurrente", "c": "Tráfico web"}},
                    {"id": "q2", "prompt": "¿Qué significa ACV?",
                     "options": {"a": "Average Contract Value", "b": "Annual Customer Volume", "c": "Acquired Client Value"}},
                    {"id": "q3", "prompt": "¿Qué es un 'freemium motion'?",
                     "options": {"a": "Cobrar por usuario", "b": "Tier gratis con conversión a paga", "c": "Descuento anual"}},
                ],
                "correct_answers": {"q1": "b", "q2": "a", "q3": "b"},
            },
        ),
        (
            1, "written", "Entrega — Define un ICP para una PyME fintech",
            {"prompt": (
                "Nuestro cliente es una fintech B2B latinoamericana con ticket promedio $12k/año. "
                "Define en 200-300 palabras un ICP accionable: industria, tamaño, rol del buyer, "
                "señales de intent, exclusiones."
            )},
        ),
        (
            2, "prospection_db", "Entrega — Base de 50 prospects segmentados",
            {"instructions": (
                "Sube un CSV con 50 prospects que cumplan el ICP del módulo 1. Columnas: company, "
                "employees, industry, contact_name, title, linkedin_url, source_signal."
            )},
        ),
        (
            3, "cold_call_video", "Entrega — Graba un cold call role-play de 90 segundos",
            {
                "scenario": (
                    "El prospect es Head of Sales en una empresa SaaS Serie A (~50 empleados). "
                    "Acaban de levantar ronda. Objetivo: conseguir discovery de 20 min."
                ),
                "rubric": [
                    "Apertura clara y permiso",
                    "Pregunta de dolor específica",
                    "Manejo de objeción 'no tengo tiempo'",
                    "Cierre con CTA concreto",
                ],
            },
        ),
        (
            3, "team_exercise", "Ejercicio en equipo (sesión en vivo)",
            {
                "brief": (
                    "En grupos de 3, construyan una cadencia de 8 toques (email + LinkedIn + teléfono) "
                    "para el ICP definido en módulo 1."
                ),
                "deliverable": "Documento compartido con la cadencia.",
            },
        ),
    ]

    if db.query(Assessment).count() == 0:
        for order, type_, title, config in specs:
            a = Assessment(
                module_id=mods[order].id,
                type=type_, title=title, config=config, passing_score=70.0,
            )
            db.add(a)
            out[order].append(a)
        db.commit()
        log.info("seed.assessments", extra={"count": sum(len(v) for v in out.values())})
    else:
        for order, m in mods.items():
            out[order] = db.query(Assessment).filter_by(module_id=m.id).all()
    return out


def seed_cohort(db, mods: dict[int, Module]) -> Cohort:
    cohort, created = _upsert(
        db,
        Cohort,
        lookup={"name": "SDR 001 — Mayo 2026"},
        defaults={
            "locale": "es",
            "start_date": date(2026, 5, 1),
            "end_date": date(2026, 6, 30),
            "status": "in_progress",
            "max_students": 15,
        },
    )
    now = datetime.now(UTC).replace(tzinfo=None)
    window_specs = [
        (0, now - timedelta(days=3), now + timedelta(days=11), now + timedelta(days=10)),
        (1, now + timedelta(days=14), now + timedelta(days=28), now + timedelta(days=27)),
        (2, now + timedelta(days=28), now + timedelta(days=42), now + timedelta(days=41)),
        (3, now + timedelta(days=42), now + timedelta(days=56), now + timedelta(days=55)),
    ]
    for order, opens, closes, live_at in window_specs:
        _upsert(
            db,
            ModuleWindow,
            lookup={"cohort_id": cohort.id, "module_id": mods[order].id},
            defaults={"opens_at": opens, "closes_at": closes, "live_session_at": live_at},
        )
    if created:
        log.info("seed.cohort", extra={"cohort_name": cohort.name})
    return cohort


def seed_live_sessions(db, cohort: Cohort) -> None:
    windows = db.query(ModuleWindow).filter_by(cohort_id=cohort.id).all()
    for w in windows:
        _upsert(
            db,
            LiveSession,
            lookup={"module_window_id": w.id},
            defaults={
                "title": f"Sesión en vivo — Módulo {w.module_id}",
                "zoom_url": "https://us06web.zoom.us/j/88888888888?pwd=demo-siete-academy",
                "recording_url": None,
            },
        )
    log.info("seed.live_sessions", extra={"count": len(windows)})


def seed_enrollments(db, users: dict[str, User], cohort: Cohort) -> None:
    for role_key, progress in (("student", 40.0), ("camila", 75.0), ("diego", 100.0)):
        u = users[role_key]
        _upsert(
            db,
            Enrollment,
            lookup={"user_id": u.id, "cohort_id": cohort.id},
            defaults={
                "status": "active" if progress < 100 else "completed",
                "progress_pct": progress,
            },
        )
    log.info("seed.enrollments", extra={"count": 3})


def seed_submissions_and_reviews(
    db, users: dict[str, User], assessments: dict[int, list[Assessment]]
) -> None:
    if db.query(Submission).count() > 0:
        return
    mcq = assessments[0][0]
    written = assessments[1][0]

    s1 = Submission(
        assessment_id=mcq.id,
        user_id=users["student"].id,
        payload={"answers": {"q1": "b", "q2": "a", "q3": "b"}},
        status="auto_graded",
        auto_score=100.0,
    )
    s2 = Submission(
        assessment_id=written.id,
        user_id=users["camila"].id,
        payload={"text": (
            "ICP propuesto: Fintech B2B LatAm serie A con 50-200 empleados. Buyer: Head of Finance "
            "o CFO. Industria: retail digital, logística, salud privada. Señales: acaban de levantar "
            "ronda, están contratando finance ops. Excluye: empresas con más de 3 años sin "
            "crecimiento de head-count."
        )},
        status="reviewed",
    )
    s3 = Submission(
        assessment_id=written.id,
        user_id=users["diego"].id,
        payload={"text": "Pymes de 10-50 empleados. Venta por relación. Hablar con el dueño."},
        status="pending_review",
    )
    db.add_all([s1, s2, s3])
    db.commit()
    db.refresh(s2)
    db.refresh(s3)

    review = TeacherReview(
        submission_id=s2.id,
        teacher_id=users["teacher"].id,
        score=82.0,
        feedback=(
            "Muy buen nivel de especificidad. Dos mejoras:\n\n"
            "1. Las señales están bien pero son genéricas — piensa en cómo las detectas en la "
            "práctica (LinkedIn Sales Nav? Crunchbase? scraping?).\n\n"
            "2. La exclusión de '3 años sin crecimiento' es arbitraria. Justifícala o retírala."
        ),
        attachment_url="https://drive.google.com/file/d/demo-icp-review-notes/view",
    )
    db.add(review)

    ai = AIReview(
        submission_id=s3.id,
        draft_feedback=(
            "Diagnóstico: respuesta muy corta (25 palabras contra objetivo de 200-300). "
            "No define industrias, ni señales de intent, ni exclusiones. \"Venta por relación\" no "
            "es un ICP, es una táctica.\n\n"
            "Sugerencia al alumno:\n"
            "- Pedirle que reescriba con el framework del módulo (industria + tamaño + rol + señal).\n"
            "- Mostrarle el ejemplo de Camila como referencia.\n\n"
            "Score sugerido: 35/100 — no aprueba."
        ),
        score_suggestion=35.0,
        model_used="claude-opus-4-7",
    )
    db.add(ai)
    db.commit()
    log.info(
        "seed.submissions_and_reviews",
        extra={"submissions": 3, "reviews": 1, "ai_drafts": 1},
    )


def seed_placement(db, users: dict[str, User], cohort: Cohort) -> None:
    if db.query(PlacementCandidate).count() > 0:
        return
    specs = [
        (users["student"], "applying", "Terminando módulo 1. Sólido en modelos de negocio."),
        (users["camila"], "siete_interview", "Primera entrevista con equipo comercial agendada."),
        (users["diego"], "siete_test", "Pasó entrevista. Toma la prueba práctica el viernes."),
    ]
    for user, stage, summary in specs:
        c = PlacementCandidate(
            user_id=user.id,
            cohort_id=cohort.id,
            stage=stage,
            summary=summary,
            portfolio_url=f"https://linkedin.com/in/{user.email.split('@')[0]}",
        )
        db.add(c)
        db.flush()
        db.add(
            PlacementEvent(
                candidate_id=c.id,
                event_type="created",
                data={"cohort_id": cohort.id},
                actor_id=users["admin"].id,
            )
        )
        if stage != "applying":
            db.add(
                PlacementEvent(
                    candidate_id=c.id,
                    event_type="stage_changed",
                    data={"from": "applying", "to": stage},
                    actor_id=users["admin"].id,
                )
            )
    db.commit()
    log.info("seed.placement", extra={"count": len(specs)})


def seed_approved_grad(db, users: dict[str, User], cohort: Cohort) -> None:
    grad, _ = _upsert(
        db,
        User,
        lookup={"email": "valeria@example.com"},
        defaults={
            "firebase_uid": "seed-grad-valeria",
            "display_name": "Valeria Ortiz",
            "role": "student",
            "locale": "es",
        },
    )
    _upsert(
        db,
        Enrollment,
        lookup={"user_id": grad.id, "cohort_id": cohort.id},
        defaults={
            "status": "completed",
            "progress_pct": 100.0,
            "completed_at": datetime.now(UTC).replace(tzinfo=None),
        },
    )
    if db.query(PlacementCandidate).filter_by(user_id=grad.id).first():
        return
    c = PlacementCandidate(
        user_id=grad.id,
        cohort_id=cohort.id,
        stage="approved",
        summary=(
            "Graduada con distinción (92/100). Fuerte en discovery y manejo de objeciones. "
            "Background en BDR de SaaS 1 año."
        ),
        portfolio_url="https://linkedin.com/in/valeria-ortiz-demo",
    )
    db.add(c)
    db.flush()
    for event_type, data in [
        ("created", {"cohort_id": cohort.id}),
        ("stage_changed", {"from": "applying", "to": "siete_interview"}),
        ("stage_changed", {"from": "siete_interview", "to": "siete_test"}),
        ("stage_changed", {"from": "siete_test", "to": "approved"}),
    ]:
        db.add(
            PlacementEvent(
                candidate_id=c.id,
                event_type=event_type,
                data=data,
                actor_id=users["admin"].id,
            )
        )
    db.commit()
    log.info("seed.approved_grad", extra={"email": grad.email})


def seed_certificate(db, users: dict[str, User], cohort: Cohort) -> None:
    from app.modules.certificates.services import issue_if_eligible

    issue_if_eligible(db, user_id=users["diego"].id, cohort_id=cohort.id)


def run() -> None:
    _ensure_schema()
    db = SessionLocal()
    try:
        users = seed_users(db)
        seed_applications(db)
        mods = seed_course(db)
        assessments = seed_assessments(db, mods)
        cohort = seed_cohort(db, mods)
        seed_live_sessions(db, cohort)
        seed_enrollments(db, users, cohort)
        seed_submissions_and_reviews(db, users, assessments)
        seed_placement(db, users, cohort)
        seed_approved_grad(db, users, cohort)
        seed_certificate(db, users, cohort)
        log.info("seed.done")
    finally:
        db.close()


if __name__ == "__main__":
    run()
