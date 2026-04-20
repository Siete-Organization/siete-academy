from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.modules.assessments.models import AIReview
from app.modules.auth.dependencies import CurrentUser, require_roles

router = APIRouter()


class AIReviewOut(BaseModel):
    id: int
    submission_id: int
    draft_feedback: str
    score_suggestion: float | None
    model_used: str

    class Config:
        from_attributes = True


@router.get("/submission/{submission_id}", response_model=AIReviewOut | None)
def for_submission(
    submission_id: int,
    _teacher: CurrentUser = Depends(require_roles("teacher", "admin")),
    db: Session = Depends(get_db),
) -> AIReview | None:
    return db.query(AIReview).filter_by(submission_id=submission_id).first()
