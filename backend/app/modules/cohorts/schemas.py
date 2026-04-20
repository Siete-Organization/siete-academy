from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel


class CohortCreate(BaseModel):
    name: str
    locale: Literal["es", "en", "pt"] = "es"
    start_date: date
    end_date: date
    max_students: int = 20


class CohortOut(BaseModel):
    id: int
    name: str
    locale: str
    start_date: date
    end_date: date
    status: str
    max_students: int

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
