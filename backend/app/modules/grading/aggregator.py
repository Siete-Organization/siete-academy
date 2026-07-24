"""Agrega submissions + teacher reviews en una vista de resultados por cohorte.

Capa adelgazada — un único barrido a DB por cohorte, todo el cálculo en Python
para que sea fácil testear y razonar. Si el volumen sube (>50 alumnos × 8 sem),
se mueve a SQL.

Convención clave para Capa 2 / Capa 3:
- `submission.auto_score`         → componente auto-grado (MCQ del módulo · Caso del final).
- `teacher_review.score`          → componente video (rúbrica /6 o /30 convertida a %).
Si la submission tiene ambos disponibles, aplicamos la fórmula 70/30 del doc.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.assessments.models import Assessment, Submission, TeacherReview
from app.modules.courses.models import Module, ModuleTranslation
from app.modules.enrollment.models import Enrollment
from app.modules.grading import services as grading
from app.modules.users.models import User


@dataclass
class _SubmissionView:
    """Submission + review unidos (la review puede no existir)."""

    submission: Submission
    review: TeacherReview | None


@dataclass
class ModuleResult:
    module_id: int
    module_title: str | None
    order_index: int
    capa_1_scores: list[float | None] = field(default_factory=list)
    capa_1_avg: float | None = None
    capa_2_mcq: float | None = None
    capa_2_video: float | None = None
    capa_2_score: float | None = None


@dataclass
class FinalResult:
    case: float | None = None
    video: float | None = None
    score: float | None = None


@dataclass
class StudentResult:
    user_id: int
    name: str | None
    email: str
    modules: list[ModuleResult]
    final: FinalResult
    course_total: float | None
    status: str  # "distinction" | "basic" | "failing" | "in_progress"


@dataclass
class CohortResults:
    cohort_id: int
    modules: list[dict[str, Any]]  # [{id, title, order_index}]
    students: list[StudentResult]


def get_cohort_results(
    db: Session, *, cohort_id: int, course_id: int | None = None, locale: str = "es"
) -> CohortResults:
    """Devuelve una vista plana de resultados por alumno × módulo × capa para una cohorte.

    Si `course_id` es None, agrega sobre todos los módulos donde el alumno
    tiene assessments calificados (cohorte tiene 1 curso típicamente).
    """
    # 1. Alumnos inscritos en la cohorte
    enroll_rows = db.execute(
        select(Enrollment, User)
        .join(User, User.id == Enrollment.user_id)
        .where(Enrollment.cohort_id == cohort_id, User.role == "student")
        .order_by(User.display_name.asc())
    ).all()
    users = [u for _, u in enroll_rows]
    user_ids = [u.id for u in users]

    # 2. Módulos del curso (si filtramos por course_id) — orden estable
    mod_stmt = select(Module).order_by(Module.order_index.asc())
    if course_id is not None:
        mod_stmt = mod_stmt.where(Module.course_id == course_id)
    modules = db.execute(mod_stmt).scalars().all()
    module_ids = [m.id for m in modules]

    # 3. Traducciones de módulos en el locale pedido (con fallback a 'es')
    mod_titles = _fetch_module_titles(db, module_ids, locale)

    # 4. Assessments en esos módulos
    if module_ids:
        assessments = (
            db.query(Assessment).filter(Assessment.module_id.in_(module_ids)).all()
        )
    else:
        assessments = []
    final_assessments = (
        db.query(Assessment).filter(Assessment.type == "final_test").all()
    )
    assessments_all = assessments + final_assessments
    asmt_by_id = {a.id: a for a in assessments_all}

    # 5. Submissions de esos assessments para los alumnos de la cohorte
    sub_rows: list[tuple[Submission, TeacherReview | None]] = []
    if user_ids and asmt_by_id:
        sub_stmt = (
            select(Submission, TeacherReview)
            .outerjoin(TeacherReview, TeacherReview.submission_id == Submission.id)
            .where(
                Submission.user_id.in_(user_ids),
                Submission.assessment_id.in_(asmt_by_id.keys()),
            )
        )
        sub_rows = list(db.execute(sub_stmt).all())

    # Agrupar: subs[user_id][assessment_id] = [SubmissionView] (puede haber re-entregas)
    subs_by_user_asmt: dict[int, dict[int, list[_SubmissionView]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for s, r in sub_rows:
        subs_by_user_asmt[s.user_id][s.assessment_id].append(_SubmissionView(s, r))

    # 6. Construir resultado por alumno
    students: list[StudentResult] = []
    for u in users:
        students.append(
            _build_student_result(
                user=u,
                modules=modules,
                mod_titles=mod_titles,
                assessments_all=assessments_all,
                subs_by_asmt=subs_by_user_asmt.get(u.id, {}),
            )
        )

    return CohortResults(
        cohort_id=cohort_id,
        modules=[
            {
                "id": m.id,
                "title": mod_titles.get(m.id),
                "order_index": m.order_index,
            }
            for m in modules
        ],
        students=students,
    )


# ─────────────────────────────  Helpers  ─────────────────────────────


def _fetch_module_titles(
    db: Session, module_ids: list[int], locale: str
) -> dict[int, str]:
    """Devuelve {module_id: title} en el locale pedido, con fallback a 'es'."""
    if not module_ids:
        return {}
    rows = (
        db.query(ModuleTranslation)
        .filter(
            ModuleTranslation.module_id.in_(module_ids),
            ModuleTranslation.locale.in_([locale, "es"]),
        )
        .all()
    )
    by_module: dict[int, dict[str, str]] = defaultdict(dict)
    for t in rows:
        by_module[t.module_id][t.locale] = t.title
    return {
        mid: titles.get(locale) or titles.get("es") or next(iter(titles.values()))
        for mid, titles in by_module.items()
    }


def _latest_submission(views: list[_SubmissionView]) -> _SubmissionView | None:
    """Submission más reciente — capa 2 y final: la re-entrega reemplaza."""
    if not views:
        return None
    return max(views, key=lambda v: (v.submission.submitted_at, v.submission.id))


def _first_submission(views: list[_SubmissionView]) -> _SubmissionView | None:
    """Primera submission — capa 1: solo el primer intento cuenta para la nota.

    Los reintentos quedan como práctica (decisión 2026-07-24: sin esto, un
    alumno podía entregar en blanco, leer la revisión y re-entregar perfecto).
    """
    if not views:
        return None
    return min(views, key=lambda v: (v.submission.submitted_at, v.submission.id))


def _build_student_result(
    *,
    user: User,
    modules: list[Module],
    mod_titles: dict[int, str],
    assessments_all: list[Assessment],
    subs_by_asmt: dict[int, list[_SubmissionView]],
) -> StudentResult:
    # Indexar assessments por módulo y tier
    capa1_by_module: dict[int, list[Assessment]] = defaultdict(list)
    capa2_by_module: dict[int, Assessment | None] = {}
    final_assessment: Assessment | None = None

    for a in assessments_all:
        tier = grading.classify_tier(a)
        if tier == "capa_1":
            capa1_by_module[a.module_id].append(a)
        elif tier == "capa_2":
            capa2_by_module[a.module_id] = a
        elif tier == "capa_3":
            final_assessment = a

    # Orden estable de capa_1 dentro de cada módulo (por lesson order_index del assessment)
    for mid in capa1_by_module:
        capa1_by_module[mid].sort(key=lambda a: (a.lesson_id or 0, a.id))

    module_results: list[ModuleResult] = []
    for m in modules:
        mr = ModuleResult(
            module_id=m.id,
            module_title=mod_titles.get(m.id),
            order_index=m.order_index,
        )

        # Capa 1 — micro-pruebas (auto_score directo, cuenta el primer intento)
        for a in capa1_by_module.get(m.id, []):
            view = _first_submission(subs_by_asmt.get(a.id, []))
            mr.capa_1_scores.append(view.submission.auto_score if view else None)
        mr.capa_1_avg = grading.average(mr.capa_1_scores)

        # Capa 2 — prueba del módulo (MCQ + video)
        capa2 = capa2_by_module.get(m.id)
        if capa2 is not None:
            view = _latest_submission(subs_by_asmt.get(capa2.id, []))
            if view is not None:
                mr.capa_2_mcq = view.submission.auto_score
                mr.capa_2_video = view.review.score if view.review else None
                mr.capa_2_score = grading.module_test_score(mr.capa_2_mcq, mr.capa_2_video)

        module_results.append(mr)

    # Capa 3 — prueba final (caso híbrido por ítem + video con rúbrica /30)
    final = FinalResult()
    diff_pct: float | None = None
    vid_crit: bool | None = None
    if final_assessment is not None:
        view = _latest_submission(subs_by_asmt.get(final_assessment.id, []))
        if view is not None:
            details = view.review.details if view.review else None
            final.case = grading.final_case_score(
                final_assessment.config, view.submission.payload, details
            )
            final.video = grading.final_video_score(final_assessment.config, details)
            final.score = grading.final_test_score(final.case, final.video)
            # Inputs extra para distinción (doc líneas 1042-1043)
            diff_pct = grading.differentiator_score(
                final_assessment.config, view.submission.payload, details
            )
            vid_crit = grading.video_critical_ok(final_assessment.config, details)

    # Curso total — solo si tenemos las 3 capas
    micros_avg = grading.average(
        [mr.capa_1_avg for mr in module_results if mr.capa_1_avg is not None]
    )
    modules_avg = grading.average(
        [mr.capa_2_score for mr in module_results if mr.capa_2_score is not None]
    )
    course_total = grading.course_final_score(
        micros_avg=micros_avg,
        modules_avg=modules_avg,
        final_pct=final.score,
    )
    status = grading.graduation_status(
        course_final=course_total,
        per_module_scores=[mr.capa_2_score for mr in module_results],
        final_pct=final.score,
        differentiator_pct=diff_pct,
        video_critical_ok=vid_crit,
    )

    return StudentResult(
        user_id=user.id,
        name=user.display_name,
        email=user.email,
        modules=module_results,
        final=final,
        course_total=course_total,
        status=status,
    )
