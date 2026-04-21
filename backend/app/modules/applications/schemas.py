from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator

MIN_WORDS_PER_ANSWER = 100


class ApplicationAnswer(BaseModel):
    question_id: str
    text: str

    @field_validator("text")
    @classmethod
    def min_words(cls, v: str) -> str:
        if len(v.split()) < MIN_WORDS_PER_ANSWER:
            raise ValueError(
                f"Each open answer must have at least {MIN_WORDS_PER_ANSWER} words."
            )
        return v


class ApplicationCreate(BaseModel):
    applicant_name: str = Field(min_length=2, max_length=200)
    applicant_email: EmailStr
    applicant_phone: str | None = None
    linkedin_url: str = Field(min_length=8, max_length=500)
    country: str = Field(min_length=2, max_length=80)
    locale: Literal["es", "en", "pt"] = "es"
    answers: list[ApplicationAnswer]
    video_url: str | None = None  # URL de YouTube/Loom/Drive


class ApplicationListOut(BaseModel):
    """Lightweight row for admin list view — no full answers, no admin_notes."""

    id: int
    applicant_name: str
    applicant_email: EmailStr
    locale: str
    ai_score: int | None
    status: str
    created_at: datetime
    reviewed_at: datetime | None

    class Config:
        from_attributes = True


class ApplicationOut(BaseModel):
    id: int
    applicant_name: str
    applicant_email: EmailStr
    applicant_phone: str | None
    linkedin_url: str | None
    country: str | None
    locale: str
    answers: dict
    video_url: str | None
    ai_score: int | None
    ai_notes: str | None
    status: str
    admin_notes: str | None
    created_at: datetime
    reviewed_at: datetime | None

    class Config:
        from_attributes = True


class ApplicationReview(BaseModel):
    status: Literal["approved", "rejected", "under_review"]
    admin_notes: str | None = None
