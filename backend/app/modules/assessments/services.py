from typing import Any

from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.modules.assessments.models import Assessment, Submission

log = get_logger("app.assessments")


def auto_grade_mcq(assessment: Assessment, payload: dict[str, Any]) -> float | None:
    """Calificación automática para MCQ. Retorna % o None si no aplica."""
    if assessment.type != "mcq":
        return None
    correct = assessment.config.get("correct_answers", {})
    if not correct:
        return None
    student_answers = payload.get("answers", {})
    if not student_answers:
        return 0.0
    hits = 0
    total = len(correct)
    for qid, right in correct.items():
        if str(student_answers.get(qid)) == str(right):
            hits += 1
    return round((hits / total) * 100, 2) if total else None


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
