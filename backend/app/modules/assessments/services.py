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
    if assessment.type not in ("mcq", "capa_2"):
        return None

    questions = assessment.config.get("questions")
    student = payload.get("answers", {})

    if questions:
        total = len(questions)
        if total == 0:
            return None
        hits = 0
        for q in questions:
            qid = q.get("id")
            qtype = q.get("type", "single")
            correct = q.get("correct")
            given = student.get(qid)
            if _question_is_correct(qtype, correct, given):
                hits += 1
        return round((hits / total) * 100, 2)

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


def submit(
    db: Session, *, assessment_id: int, user_id: int, payload: dict, file_url: str | None
) -> Submission:
    assessment = db.get(Assessment, assessment_id)
    if assessment is None:
        log.warning("assessment.submit_not_found", extra={"assessment_id": assessment_id})
        raise ValueError("Assessment not found")

    auto = auto_grade_mcq(assessment, payload)
    status = "auto_graded" if auto is not None else "pending_review"

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
