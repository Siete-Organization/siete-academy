from typing import Any

from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.modules.assessments.models import Assessment, Submission

log = get_logger("app.assessments")


def auto_grade_mcq(assessment: Assessment, payload: dict[str, Any]) -> float | None:
    """Calificación automática para MCQ.

    Soporta dos shapes de config:
    1. Legacy: ``{"correct_answers": {qid: choice_id}}`` — single-choice only.
    2. Nuevo: ``{"questions": [{id, type: "single"|"multi"|"match", correct: ...}]}``
       donde ``correct`` es lista (single/multi) o dict {leftId: rightId} (match).

    En ambos casos la submission del alumno viene en ``payload["answers"]``:
    single → ``{qid: "c"}``, multi → ``{qid: ["b","c"]}``, match → ``{qid: {"1":"A","2":"B"}}``.
    """
    if assessment.type not in ("mcq", "capa_2", "final_test"):
        return None

    questions = assessment.config.get("questions")
    student = payload.get("answers", {})

    if questions:
        earned, total = sum_mcq_points(questions, student)
        if total == 0:
            return None
        return round((earned / total) * 100, 2)

    # Legacy single-choice fallback
    correct_legacy = assessment.config.get("correct_answers", {})
    if not correct_legacy:
        return None
    if not student:
        return 0.0
    hits = 0
    total = len(correct_legacy)
    for qid, right in correct_legacy.items():
        if str(student.get(qid)) == str(right):
            hits += 1
    return round((hits / total) * 100, 2) if total else None


def count_mcq_correct(questions: list[dict], answers: dict[str, Any]) -> int:
    """Cuenta cuántas preguntas (shape `questions`) están correctas. Usado por el
    auto-grado y por el grading híbrido del caso final (Capa 3)."""
    hits = 0
    for q in questions:
        if _question_is_correct(
            q.get("type", "single"), q.get("correct"), answers.get(q.get("id"))
        ):
            hits += 1
    return hits


def sum_mcq_points(questions: list[dict], answers: dict[str, Any]) -> tuple[float, float]:
    """Devuelve (puntos obtenidos, puntos totales) ponderando cada pregunta por su
    campo ``points`` (default 1). Permite puntaje ponderado — p.ej. el caso de la
    Prueba Final, con ítems de 2 y 3 puntos (/42). Con ``points`` ausente equivale
    a contar aciertos (capa_2 y mcq puro no cambian)."""
    earned = 0.0
    total = 0.0
    for q in questions:
        pts = float(q.get("points", 1) or 1)
        total += pts
        if _question_is_correct(
            q.get("type", "single"), q.get("correct"), answers.get(q.get("id"))
        ):
            earned += pts
    return earned, total


def _question_is_correct(qtype: str, correct: Any, given: Any) -> bool:
    if given is None:
        return False
    if qtype == "single":
        if isinstance(correct, list):
            return len(correct) == 1 and str(given) == str(correct[0])
        return str(given) == str(correct)
    if qtype == "multi":
        if not isinstance(correct, list) or not isinstance(given, list):
            return False
        return sorted(map(str, correct)) == sorted(map(str, given))
    if qtype == "match":
        if not isinstance(correct, dict) or not isinstance(given, dict):
            return False
        if set(correct.keys()) != set(given.keys()):
            return False
        return all(str(correct[k]) == str(given[k]) for k in correct)
    return False


# Claves que revelan la respuesta correcta o la rúbrica de corrección. NUNCA
# deben llegar al alumno en los endpoints student-facing (capa_2 / final_test).
_STRIP_TOP = ("short_rubric", "video_rubric", "differentiator_ids", "correct_answers")
_STRIP_QUESTION = ("correct", "explanation", "differentiator")
_STRIP_SHORT = ("expected_answer", "rubric")
_STRIP_TABLE = ("expected_sequence", "rubric")


def public_config(config: dict[str, Any]) -> dict[str, Any]:
    """Copia del config sin claves de respuesta ni rúbricas.

    El alumno necesita enunciados, opciones y el brief — nunca las respuestas
    correctas ni las rúbricas. El grading vive server-side (``auto_grade_mcq`` +
    review del profesor), que lee el config crudo de la DB, así que quitar estas
    claves de la respuesta HTTP no afecta la nota.

    Se aplica a TODOS los endpoints student-facing, incluidas las micropruebas
    (capa_1): su corrección vive server-side y la revisión post-entrega viaja
    en la respuesta del POST (``build_mcq_review``).
    """
    if not config:
        return {}
    clean = {k: v for k, v in config.items() if k not in _STRIP_TOP}

    questions = clean.get("questions")
    if isinstance(questions, list):
        clean["questions"] = [
            {k: v for k, v in q.items() if k not in _STRIP_QUESTION}
            for q in questions
            if isinstance(q, dict)
        ]

    short_answers = clean.get("short_answers")
    if isinstance(short_answers, list):
        clean["short_answers"] = [
            {k: v for k, v in sa.items() if k not in _STRIP_SHORT}
            for sa in short_answers
            if isinstance(sa, dict)
        ]

    tables = clean.get("tables")
    if isinstance(tables, list):
        clean["tables"] = [_public_table(t) for t in tables if isinstance(t, dict)]

    return clean


def _public_table(table: dict[str, Any]) -> dict[str, Any]:
    clean = {k: v for k, v in table.items() if k not in _STRIP_TABLE}
    rows = clean.get("rows")
    if isinstance(rows, list):
        # Las tablas de clasificación llevan la respuesta correcta por fila.
        clean["rows"] = [
            {k: v for k, v in row.items() if k != "correct"}
            for row in rows
            if isinstance(row, dict)
        ]
    return clean


def build_mcq_review(assessment: Assessment, payload: dict) -> list[dict[str, Any]] | None:
    """Corrección pregunta a pregunta para la respuesta del POST de entrega.

    Solo micropruebas (type ``mcq``): el alumno recibe su revisión DESPUÉS de
    entregar, en vez de tener las respuestas correctas en el config pre-entrega
    (que era el leak de capa 1). Capa_2/final no devuelven revisión: quedan
    en manos del profesor.
    """
    if assessment.type != "mcq":
        return None
    questions = (assessment.config or {}).get("questions")
    if not isinstance(questions, list):
        return None
    answers = payload.get("answers", {}) or {}
    review: list[dict[str, Any]] = []
    for q in questions:
        if not isinstance(q, dict):
            continue
        qid = q.get("id")
        review.append(
            {
                "id": qid,
                "is_correct": _question_is_correct(
                    q.get("type", "single"), q.get("correct"), answers.get(qid)
                ),
                "correct": q.get("correct"),
                "explanation": q.get("explanation"),
            }
        )
    return review


def submit(
    db: Session, *, assessment_id: int, user_id: int, payload: dict, file_url: str | None
) -> Submission:
    assessment = db.get(Assessment, assessment_id)
    if assessment is None:
        log.warning("assessment.submit_not_found", extra={"assessment_id": assessment_id})
        raise ValueError("Assessment not found")

    auto = auto_grade_mcq(assessment, payload)
    # Capa_2 y final_test SIEMPRE requieren review humano del video, incluso si
    # el MCQ ya autocorrigió. Solo mcq puro va directo a auto_graded.
    requires_review = assessment.type in ("capa_2", "final_test")
    if auto is not None and not requires_review:
        status = "auto_graded"
    else:
        status = "pending_review"

    s = Submission(
        assessment_id=assessment_id,
        user_id=user_id,
        payload=payload,
        file_url=file_url,
        auto_score=auto,
        status=status,
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    log.info(
        "submission.created",
        extra={
            "submission_id": s.id,
            "assessment_id": assessment_id,
            "assessment_type": assessment.type,
            "status": status,
            "auto_score": auto,
        },
    )
    return s
