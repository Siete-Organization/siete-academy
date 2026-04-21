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
        "kind": lesson.kind,
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


def module_admin_dict(module: Module) -> dict:
    """Vista admin del módulo — todas las traducciones + lecciones + recursos anidados."""
    return {
        "id": module.id,
        "course_id": module.course_id,
        "slug": module.slug,
        "order_index": module.order_index,
        "translations": [
            {"locale": t.locale, "title": t.title, "summary": t.summary}
            for t in sorted(module.translations, key=lambda x: x.locale)
        ],
        "lessons": [lesson_admin_dict(le) for le in sorted(module.lessons, key=lambda x: x.order_index)],
        "resources": [
            {
                "id": r.id,
                "module_id": r.module_id,
                "kind": r.kind,
                "title": r.title,
                "url": r.url,
                "order_index": r.order_index,
            }
            for r in sorted(module.resources, key=lambda x: x.order_index)
        ],
    }


def lesson_admin_dict(lesson: Lesson) -> dict:
    return {
        "id": lesson.id,
        "module_id": lesson.module_id,
        "order_index": lesson.order_index,
        "kind": lesson.kind,
        "youtube_id": lesson.youtube_id,
        "duration_seconds": lesson.duration_seconds,
        "translations": [
            {"locale": t.locale, "title": t.title, "body": t.body}
            for t in sorted(lesson.translations, key=lambda x: x.locale)
        ],
    }


def update_module(
    db: Session,
    module: Module,
    *,
    order_index: int | None,
    translations: list[dict] | None,
) -> Module:
    if order_index is not None:
        module.order_index = order_index
    if translations is not None:
        by_locale = {t.locale: t for t in module.translations}
        for item in translations:
            existing = by_locale.get(item["locale"])
            if existing:
                existing.title = item["title"]
                existing.summary = item.get("summary")
            else:
                module.translations.append(
                    ModuleTranslation(
                        locale=item["locale"],
                        title=item["title"],
                        summary=item.get("summary"),
                    )
                )
    db.commit()
    db.refresh(module)
    log.info("course.module_updated", extra={"module_id": module.id})
    return module


def update_lesson(
    db: Session,
    lesson: Lesson,
    *,
    order_index: int | None,
    kind: str | None,
    youtube_id: str | None,
    duration_seconds: int | None,
    translations: list[dict] | None,
) -> Lesson:
    if order_index is not None:
        lesson.order_index = order_index
    if kind is not None:
        lesson.kind = kind
    if youtube_id is not None:
        lesson.youtube_id = youtube_id or None
    if duration_seconds is not None:
        lesson.duration_seconds = duration_seconds
    if translations is not None:
        by_locale = {t.locale: t for t in lesson.translations}
        for item in translations:
            existing = by_locale.get(item["locale"])
            if existing:
                existing.title = item["title"]
                existing.body = item.get("body")
            else:
                lesson.translations.append(
                    LessonTranslation(
                        locale=item["locale"],
                        title=item["title"],
                        body=item.get("body"),
                    )
                )
    db.commit()
    db.refresh(lesson)
    log.info(
        "course.lesson_updated",
        extra={"lesson_id": lesson.id, "kind": lesson.kind},
    )
    return lesson


def delete_lesson(db: Session, lesson: Lesson) -> None:
    lid = lesson.id
    db.delete(lesson)
    db.commit()
    log.info("course.lesson_deleted", extra={"lesson_id": lid})


def create_lesson(
    db: Session,
    module_id: int,
    order_index: int,
    youtube_id: str | None,
    duration_seconds: int | None,
    translations: list[dict],
    kind: str = "video",
) -> Lesson:
    lesson = Lesson(
        module_id=module_id,
        order_index=order_index,
        kind=kind,
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
