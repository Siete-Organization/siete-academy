from datetime import datetime

from pydantic import BaseModel, Field


class EnrollmentCreate(BaseModel):
    user_id: int
    cohort_id: int


class EnrollmentOut(BaseModel):
    id: int
    user_id: int
    cohort_id: int
    cohort_name: str | None = None
    slack_invite_url: str | None = None
    status: str
    progress_pct: float
    enrolled_at: datetime
    completed_at: datetime | None

    class Config:
        from_attributes = True


class EnrollmentUpdate(BaseModel):
    cohort_id: int | None = None
    status: str | None = None


class EnrollmentAdminOut(BaseModel):
    """Enriquecida con datos del alumno para la vista admin de cohorte."""

    id: int
    user_id: int
    user_name: str | None
    user_email: str
    cohort_id: int
    status: str
    progress_pct: float
    enrolled_at: datetime
    completed_at: datetime | None


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
