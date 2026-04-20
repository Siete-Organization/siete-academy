from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.logging import get_logger
from app.modules.ai_review.tasks import review_submission_task
from app.modules.assessments import services
from app.modules.assessments.models import Assessment, Submission, TeacherReview
from app.modules.assessments.schemas import (
    AssessmentCreate,
    AssessmentOut,
    ReviewCreate,
    ReviewOut,
    SubmissionCreate,
    SubmissionOut,
    SubmissionWithReview,
)
from app.modules.auth.dependencies import CurrentUser, get_current_user, require_roles

log = get_logger("app.assessments.router")
router = APIRouter()


@router.post("", response_model=AssessmentOut, status_code=201)
def create_assessment(
    body: AssessmentCreate,
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> Assessment:
    a = Assessment(**body.model_dump())
    db.add(a)
    db.commit()
    db.refresh(a)
    log.info(
        "assessment.created",
        extra={"assessment_id": a.id, "module_id": a.module_id, "type": a.type},
    )
    return a


@router.get("/module/{module_id}", response_model=list[AssessmentOut])
def list_by_module(module_id: int, db: Session = Depends(get_db)) -> list[Assessment]:
    return db.query(Assessment).filter(Assessment.module_id == module_id).all()


@router.post("/submissions", response_model=SubmissionOut, status_code=201)
def submit(
    body: SubmissionCreate,
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Submission:
    try:
        s = services.submit(
            db,
            assessment_id=body.assessment_id,
            user_id=current.user.id,
            payload=body.payload,
            file_url=body.file_url,
        )
    except ValueError as e:
        raise HTTPException(404, str(e)) from e

    # Kick off AI draft for teacher queue (no-op if Anthropic key not set)
    if s.status == "pending_review":
        try:
            review_submission_task.delay(s.id)
            log.info("ai.review_queued", extra={"submission_id": s.id})
        except Exception as e:
            log.warning(
                "ai.review_queue_failed",
                extra={"submission_id": s.id, "error": str(e)},
            )
    return s


@router.get("/submissions/pending", response_model=list[SubmissionOut])
def list_pending_reviews(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    _teacher: CurrentUser = Depends(require_roles("teacher", "admin")),
    db: Session = Depends(get_db),
) -> list[Submission]:
    return (
        db.query(Submission)
        .filter(Submission.status == "pending_review")
        .order_by(Submission.submitted_at.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.get("/submissions/me", response_model=list[SubmissionOut])
def my_submissions(
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> list[Submission]:
    return (
        db.query(Submission)
        .filter(Submission.user_id == current.user.id)
        .order_by(Submission.submitted_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.get("/submissions/me/with-reviews", response_model=list[SubmissionWithReview])
def my_submissions_with_reviews(
    current: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> list[dict]:
    """El alumno ve sus entregas junto con el feedback del profesor.

    Single round-trip: LEFT OUTER JOIN contra assessment + teacher_review.
    """
    stmt = (
        select(Submission, Assessment, TeacherReview)
        .outerjoin(Assessment, Assessment.id == Submission.assessment_id)
        .outerjoin(TeacherReview, TeacherReview.submission_id == Submission.id)
        .where(Submission.user_id == current.user.id)
        .order_by(Submission.submitted_at.desc())
        .offset(offset)
        .limit(limit)
    )
    return [
        {
            "submission": s,
            "assessment_title": a.title if a else "",
            "review": r,
        }
        for s, a, r in db.execute(stmt).all()
    ]


@router.post("/submissions/{submission_id}/review", response_model=ReviewOut, status_code=201)
def review_submission(
    submission_id: int,
    body: ReviewCreate,
    current: CurrentUser = Depends(require_roles("teacher", "admin")),
    db: Session = Depends(get_db),
) -> TeacherReview:
    s = db.get(Submission, submission_id)
    if not s:
        raise HTTPException(404, "Submission not found")
    existing = db.query(TeacherReview).filter_by(submission_id=submission_id).first()
    if existing:
        existing.score = body.score
        existing.feedback = body.feedback
        existing.attachment_url = body.attachment_url
        existing.teacher_id = current.user.id
        review = existing
        log.info(
            "teacher_review.updated",
            extra={
                "submission_id": submission_id,
                "teacher_id": current.user.id,
                "score": body.score,
                "has_attachment": bool(body.attachment_url),
            },
        )
    else:
        review = TeacherReview(
            submission_id=submission_id,
            teacher_id=current.user.id,
            score=body.score,
            feedback=body.feedback,
            attachment_url=body.attachment_url,
        )
        db.add(review)
        log.info(
            "teacher_review.created",
            extra={
                "submission_id": submission_id,
                "teacher_id": current.user.id,
                "score": body.score,
                "has_attachment": bool(body.attachment_url),
            },
        )
    s.status = "reviewed"
    db.commit()
    db.refresh(review)
    return review
