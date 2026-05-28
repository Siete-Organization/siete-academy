from datetime import datetime
from typing import Literal

from pydantic import BaseModel

Stage = Literal[
    "e1_invited",
    "e1_active",
    "e2_active",
    "e3_t2_active",
    "e3_t1_active",
    "closed_camino_b",
    "declined",
]


class InviteCandidate(BaseModel):
    user_id: int
    country_deel_ok: bool = True
    notes: str | None = None


class CandidateOut(BaseModel):
    id: int
    user_id: int
    stage: Stage
    entered_stage_at: datetime
    monthly_usd: int | None
    country_deel_ok: bool
    assigned_manager_id: int | None
    notes: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StageTransition(BaseModel):
    to_stage: Stage
    reason: str | None = None
    monthly_usd: int | None = None  # se requiere al pasar a e2/e3_t2/e3_t1


class StageEventOut(BaseModel):
    id: int
    from_stage: str | None
    to_stage: str
    reason: str | None
    actor_id: int | None
    created_at: datetime

    class Config:
        from_attributes = True


class CandidateDetailOut(CandidateOut):
    events: list[StageEventOut] = []
