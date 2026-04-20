from datetime import datetime

from pydantic import BaseModel, Field


class EnrollmentCreate(BaseModel):
    user_id: int
    cohort_id: int


class EnrollmentOut(BaseModel):
    id: int
    user_id: int
    cohort_id: int
    status: str
    progress_pct: float
    enrolled_at: datetime
    completed_at: datetime | None

    class Config:
        from_attributes = True


class LessonProgressUpdate(BaseModel):
    lesson_id: int
    watched_pct: float = Field(ge=0, le=100)
    completed: bool = False


class LessonProgressOut(BaseModel):
    id: int
    enrollment_id: int
    lesson_id: int
    watched_pct: float
    completed_at: datetime | None
    last_seen_at: datetime

    class Config:
        from_attributes = True
