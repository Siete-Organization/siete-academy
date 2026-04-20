from typing import Literal

from pydantic import BaseModel

Locale = Literal["es", "en", "pt"]


class TranslationIn(BaseModel):
    locale: Locale
    title: str
    description: str | None = None


class CourseCreate(BaseModel):
    slug: str
    translations: list[TranslationIn]


class CourseOut(BaseModel):
    id: int
    slug: str
    title: str
    description: str | None


class ModuleTranslationIn(BaseModel):
    locale: Locale
    title: str
    summary: str | None = None


class ModuleCreate(BaseModel):
    slug: str
    order_index: int = 0
    translations: list[ModuleTranslationIn]


class ModuleOut(BaseModel):
    id: int
    course_id: int
    slug: str
    order_index: int
    title: str
    summary: str | None


class LessonTranslationIn(BaseModel):
    locale: Locale
    title: str
    body: str | None = None


class LessonCreate(BaseModel):
    order_index: int = 0
    youtube_id: str | None = None
    duration_seconds: int | None = None
    translations: list[LessonTranslationIn]


class LessonOut(BaseModel):
    id: int
    module_id: int
    order_index: int
    youtube_id: str | None
    duration_seconds: int | None
    title: str
    body: str | None
