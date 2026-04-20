from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.core.i18n import normalize_locale
from app.modules.auth.dependencies import CurrentUser, require_roles
from app.modules.courses import services
from app.modules.courses.models import Course, Lesson, Module
from app.modules.courses.schemas import (
    CourseCreate,
    CourseOut,
    LessonCreate,
    LessonOut,
    ModuleCreate,
    ModuleOut,
)

router = APIRouter()


@router.get("", response_model=list[CourseOut])
def list_courses(
    locale: str = Query("es"),
    db: Session = Depends(get_db),
) -> list[dict]:
    loc = normalize_locale(locale)
    courses = db.query(Course).options(selectinload(Course.translations)).all()
    return [services.course_to_dict(c, loc) for c in courses]


@router.post("", response_model=CourseOut, status_code=201)
def create_course(
    body: CourseCreate,
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> dict:
    c = services.create_course(db, body.slug, [t.model_dump() for t in body.translations])
    return services.course_to_dict(c, "es")


@router.get("/{course_id}/modules", response_model=list[ModuleOut])
def list_modules(
    course_id: int,
    locale: str = Query("es"),
    db: Session = Depends(get_db),
) -> list[dict]:
    loc = normalize_locale(locale)
    mods = (
        db.query(Module)
        .options(selectinload(Module.translations))
        .filter(Module.course_id == course_id)
        .order_by(Module.order_index)
        .all()
    )
    return [services.module_to_dict(m, loc) for m in mods]


@router.post("/{course_id}/modules", response_model=ModuleOut, status_code=201)
def create_module(
    course_id: int,
    body: ModuleCreate,
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> dict:
    if not db.get(Course, course_id):
        raise HTTPException(404, "Course not found")
    m = services.create_module(
        db, course_id, body.slug, body.order_index, [t.model_dump() for t in body.translations]
    )
    return services.module_to_dict(m, "es")


@router.get("/modules/{module_id}/lessons", response_model=list[LessonOut])
def list_lessons(
    module_id: int,
    locale: str = Query("es"),
    db: Session = Depends(get_db),
) -> list[dict]:
    loc = normalize_locale(locale)
    lessons = (
        db.query(Lesson)
        .options(selectinload(Lesson.translations))
        .filter(Lesson.module_id == module_id)
        .order_by(Lesson.order_index)
        .all()
    )
    return [services.lesson_to_dict(le, loc) for le in lessons]


@router.post("/modules/{module_id}/lessons", response_model=LessonOut, status_code=201)
def create_lesson(
    module_id: int,
    body: LessonCreate,
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> dict:
    if not db.get(Module, module_id):
        raise HTTPException(404, "Module not found")
    le = services.create_lesson(
        db,
        module_id,
        body.order_index,
        body.youtube_id,
        body.duration_seconds,
        [t.model_dump() for t in body.translations],
    )
    return services.lesson_to_dict(le, "es")
