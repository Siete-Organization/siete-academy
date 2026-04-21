from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field

AssessmentType = Literal["mcq", "written", "prospection_db", "cold_call_video", "team_exercise"]


class AssessmentCreate(BaseModel):
    module_id: int
    type: AssessmentType
    title: str
    config: dict[str, Any] = Field(default_factory=dict)
    passing_score: float = 70.0


class AssessmentUpdate(BaseModel):
    type: AssessmentType | None = None
    title: str | None = None
    config: dict[str, Any] | None = None
    passing_score: float | None = None


class AssessmentOut(BaseModel):
    id: int
    module_id: int
    type: str
    title: str
    config: dict
    passing_score: float

    class Config:
        from_attributes = True


class SubmissionCreate(BaseModel):
    assessment_id: int
    payload: dict[str, Any] = Field(default_factory=dict)
    file_url: str | None = None


class SubmissionOut(BaseModel):
    id: int
    assessment_id: int
    user_id: int
    payload: dict
    file_url: str | None
    status: str
    auto_score: float | None
    submitted_at: datetime

    class Config:
        from_attributes = True


class ReviewCreate(BaseModel):
    score: float = Field(ge=0, le=100)
    feedback: str = Field(min_length=1)
    attachment_url: str | None = None


class ReviewOut(BaseModel):
    id: int
    submission_id: int
    teacher_id: int
    score: float
    feedback: str
    attachment_url: str | None = None
    approved_at: datetime

    class Config:
        from_attributes = True


class SubmissionWithReview(BaseModel):
    """Vista del alumno — su entrega + feedback del profesor si ya fue calificada."""

    submission: SubmissionOut
    assessment_title: str
    review: ReviewOut | None
