from datetime import datetime
from typing import Literal

from pydantic import BaseModel

Stage = Literal[
    "applying",
    "siete_interview",
    "siete_test",
    "approved",
    "presented",
    "placed",
    "rejected",
]


class CandidateCreate(BaseModel):
    user_id: int
    cohort_id: int | None = None
    summary: str | None = None
    portfolio_url: str | None = None


class CandidateUpdate(BaseModel):
    summary: str | None = None
    portfolio_url: str | None = None
    notes: str | None = None


class StageChange(BaseModel):
    stage: Stage
    note: str | None = None


class AssignAdmin(BaseModel):
    admin_id: int | None


class EventOut(BaseModel):
    id: int
    event_type: str
    data: dict
    actor_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True


class CandidateOut(BaseModel):
    id: int
    user_id: int
    cohort_id: int | None
    stage: str
    assigned_admin_id: int | None
    notes: str | None
    summary: str | None
    portfolio_url: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CandidateDetailOut(CandidateOut):
    # Enriquecido con datos del usuario y eventos para el detalle admin/recruiter
    user_name: str | None
    user_email: str | None
    events: list[EventOut]


class CandidateRecruiterOut(BaseModel):
    """Vista pública para el reclutador externo — solo candidatos aprobados."""

    id: int
    user_name: str | None
    user_email: str | None
    cohort_id: int | None
    stage: str
    summary: str | None
    portfolio_url: str | None
    approved_at: datetime | None
