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
    kind: Literal["video", "reading"] = "video"
    youtube_id: str | None = None
    duration_seconds: int | None = None
    translations: list[LessonTranslationIn]


class LessonOut(BaseModel):
    id: int
    module_id: int
    order_index: int
    kind: str
    youtube_id: str | None
    duration_seconds: int | None
    title: str
    body: str | None


class LessonUpdate(BaseModel):
    order_index: int | None = None
    kind: Literal["video", "reading"] | None = None
    youtube_id: str | None = None
    duration_seconds: int | None = None
    translations: list[LessonTranslationIn] | None = None


class ModuleUpdate(BaseModel):
    order_index: int | None = None
    translations: list[ModuleTranslationIn] | None = None


class LessonAdminOut(BaseModel):
    """Editor view — todas las traducciones visibles."""

    id: int
    module_id: int
    order_index: int
    kind: str
    youtube_id: str | None
    duration_seconds: int | None
    translations: list[LessonTranslationIn]


ResourceKind = Literal["pdf", "ppt", "video", "doc", "link"]


class ResourceCreate(BaseModel):
    kind: ResourceKind
    title: str
    url: str
    order_index: int = 0


class ResourceUpdate(BaseModel):
    kind: ResourceKind | None = None
    title: str | None = None
    url: str | None = None
    order_index: int | None = None


class ResourceOut(BaseModel):
    id: int
    module_id: int
    kind: str
    title: str
    url: str
    order_index: int

    class Config:
        from_attributes = True


class ModuleAdminOut(BaseModel):
    id: int
    course_id: int
    slug: str
    order_index: int
    translations: list[ModuleTranslationIn]
    lessons: list[LessonAdminOut]
    resources: list[ResourceOut] = []
