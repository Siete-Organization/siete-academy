from sqlalchemy.orm import Session

from app.core.i18n import pick_translation
from app.core.logging import get_logger
from app.modules.courses.models import (
    Course,
    CourseTranslation,
    Lesson,
    LessonTranslation,
    Module,
    ModuleTranslation,
)

log = get_logger("app.courses")


def course_to_dict(course: Course, locale: str) -> dict:
    translations = {t.locale: {"title": t.title, "description": t.description or ""} for t in course.translations}
    return {
        "id": course.id,
        "slug": course.slug,
        "title": pick_translation(translations, locale, "title"),
        "description": pick_translation(translations, locale, "description"),
    }


def module_to_dict(module: Module, locale: str) -> dict:
    translations = {t.locale: {"title": t.title, "summary": t.summary or ""} for t in module.translations}
    return {
        "id": module.id,
        "course_id": module.course_id,
        "slug": module.slug,
        "order_index": module.order_index,
        "title": pick_translation(translations, locale, "title"),
        "summary": pick_translation(translations, locale, "summary"),
    }


def lesson_to_dict(lesson: Lesson, locale: str) -> dict:
    translations = {t.locale: {"title": t.title, "body": t.body or ""} for t in lesson.translations}
    return {
        "id": lesson.id,
        "module_id": lesson.module_id,
        "order_index": lesson.order_index,
        "youtube_id": lesson.youtube_id,
        "duration_seconds": lesson.duration_seconds,
        "title": pick_translation(translations, locale, "title"),
        "body": pick_translation(translations, locale, "body"),
    }


def create_course(db: Session, slug: str, translations: list[dict]) -> Course:
    course = Course(slug=slug)
    for t in translations:
        course.translations.append(CourseTranslation(**t))
    db.add(course)
    db.commit()
    db.refresh(course)
    log.info(
        "course.created",
        extra={
            "course_id": course.id,
            "slug": slug,
            "locales": [t["locale"] for t in translations],
        },
    )
    return course


def create_module(
    db: Session, course_id: int, slug: str, order_index: int, translations: list[dict]
) -> Module:
    module = Module(course_id=course_id, slug=slug, order_index=order_index)
    for t in translations:
        module.translations.append(ModuleTranslation(**t))
    db.add(module)
    db.commit()
    db.refresh(module)
    log.info(
        "course.module_created",
        extra={
            "module_id": module.id,
            "course_id": course_id,
            "slug": slug,
            "order_index": order_index,
            "locales": [t["locale"] for t in translations],
        },
    )
    return module


def create_lesson(
    db: Session,
    module_id: int,
    order_index: int,
    youtube_id: str | None,
    duration_seconds: int | None,
    translations: list[dict],
) -> Lesson:
    lesson = Lesson(
        module_id=module_id,
        order_index=order_index,
        youtube_id=youtube_id,
        duration_seconds=duration_seconds,
    )
    for t in translations:
        lesson.translations.append(LessonTranslation(**t))
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    log.info(
        "course.lesson_created",
        extra={
            "lesson_id": lesson.id,
            "module_id": module_id,
            "order_index": order_index,
            "has_video": bool(youtube_id),
            "duration_seconds": duration_seconds,
            "locales": [t["locale"] for t in translations],
        },
    )
    return lesson
