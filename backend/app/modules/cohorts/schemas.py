from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel


class CohortCreate(BaseModel):
    name: str
    locale: Literal["es", "en", "pt"] = "es"
    start_date: date
    end_date: date
    max_students: int = 20
    slack_invite_url: str | None = None


class CohortUpdate(BaseModel):
    name: str | None = None
    locale: Literal["es", "en", "pt"] | None = None
    start_date: date | None = None
    end_date: date | None = None
    status: str | None = None
    max_students: int | None = None
    slack_invite_url: str | None = None


class CohortOut(BaseModel):
    id: int
    name: str
    locale: str
    start_date: date
    end_date: date
    status: str
    max_students: int
    slack_invite_url: str | None = None

    class Config:
        from_attributes = True


class ModuleWindowCreate(BaseModel):
    module_id: int
    opens_at: datetime
    closes_at: datetime
    live_session_at: datetime | None = None


class ModuleWindowUpdate(BaseModel):
    opens_at: datetime | None = None
    closes_at: datetime | None = None
    live_session_at: datetime | None = None


class ModuleWindowOut(BaseModel):
    id: int
    cohort_id: int
    module_id: int
    opens_at: datetime
    closes_at: datetime
    live_session_at: datetime | None

    class Config:
        from_attributes = True
