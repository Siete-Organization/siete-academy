"""Pydantic shapes para /grading/results.

Pensado para una sola llamada que poble una tabla densa Alumno × Módulo × Capa.
"""
from __future__ import annotations

from pydantic import BaseModel


class ModuleHeader(BaseModel):
    id: int
    title: str | None
    order_index: int


class ModuleResultOut(BaseModel):
    module_id: int
    module_title: str | None
    order_index: int
    capa_1_scores: list[float | None]
    capa_1_avg: float | None
    capa_2_mcq: float | None
    capa_2_video: float | None
    capa_2_score: float | None


class FinalResultOut(BaseModel):
    case: float | None
    video: float | None
    score: float | None


class StudentResultOut(BaseModel):
    user_id: int
    name: str | None
    email: str
    modules: list[ModuleResultOut]
    final: FinalResultOut
    course_total: float | None
    status: str


class CohortResultsOut(BaseModel):
    cohort_id: int
    modules: list[ModuleHeader]
    students: list[StudentResultOut]
