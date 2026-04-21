from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    translations: Mapped[list["CourseTranslation"]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )
    modules: Mapped[list["Module"]] = relationship(
        back_populates="course", cascade="all, delete-orphan", order_by="Module.order_index"
    )


class CourseTranslation(Base):
    __tablename__ = "course_translations"
    __table_args__ = (UniqueConstraint("course_id", "locale", name="uq_course_locale"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), index=True)
    locale: Mapped[str] = mapped_column(String(5))
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    course: Mapped[Course] = relationship(back_populates="translations")


class Module(Base):
    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), index=True)
    slug: Mapped[str] = mapped_column(String(100))
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    course: Mapped[Course] = relationship(back_populates="modules")
    translations: Mapped[list["ModuleTranslation"]] = relationship(
        back_populates="module", cascade="all, delete-orphan"
    )
    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="module", cascade="all, delete-orphan", order_by="Lesson.order_index"
    )
    resources: Mapped[list["ModuleResource"]] = relationship(
        back_populates="module", cascade="all, delete-orphan", order_by="ModuleResource.order_index"
    )


class ModuleTranslation(Base):
    __tablename__ = "module_translations"
    __table_args__ = (UniqueConstraint("module_id", "locale", name="uq_module_locale"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id", ondelete="CASCADE"), index=True)
    locale: Mapped[str] = mapped_column(String(5))
    title: Mapped[str] = mapped_column(String(200))
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    module: Mapped[Module] = relationship(back_populates="translations")


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(primary_key=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id", ondelete="CASCADE"), index=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    # "video" (YouTube iframe) | "reading" (manual / lectura inline, no descargable)
    kind: Mapped[str] = mapped_column(String(16), default="video")
    # YouTube unlisted video ID (ej: "dQw4w9WgXcQ"). El front embebe el iframe.
    youtube_id: Mapped[str | None] = mapped_column(String(20), nullable=True)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    module: Mapped[Module] = relationship(back_populates="lessons")
    translations: Mapped[list["LessonTranslation"]] = relationship(
        back_populates="lesson", cascade="all, delete-orphan"
    )


class LessonTranslation(Base):
    __tablename__ = "lesson_translations"
    __table_args__ = (UniqueConstraint("lesson_id", "locale", name="uq_lesson_locale"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id", ondelete="CASCADE"), index=True)
    locale: Mapped[str] = mapped_column(String(5))
    title: Mapped[str] = mapped_column(String(200))
    body: Mapped[str | None] = mapped_column(Text, nullable=True)

    lesson: Mapped[Lesson] = relationship(back_populates="translations")


class ModuleResource(Base):
    """Material complementario por módulo: PDFs, PPTs, videos, docs, links externos.

    Fase 0: basado en URL (Drive/Dropbox/YouTube/Loom).
    Fase 1+ podrá apuntar a uploads propios en /uploads/... servidos por StaticFiles.
    """

    __tablename__ = "module_resources"

    id: Mapped[int] = mapped_column(primary_key=True)
    module_id: Mapped[int] = mapped_column(
        ForeignKey("modules.id", ondelete="CASCADE"), index=True
    )
    # "pdf" | "ppt" | "video" | "doc" | "link"
    kind: Mapped[str] = mapped_column(String(16), default="link")
    title: Mapped[str] = mapped_column(String(200))
    url: Mapped[str] = mapped_column(String(600))
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    module: Mapped[Module] = relationship(back_populates="resources")
