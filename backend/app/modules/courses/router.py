from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.core.i18n import normalize_locale
from app.modules.auth.dependencies import CurrentUser, require_roles
from app.modules.courses import services
from app.modules.courses.models import Course, Lesson, Module, ModuleResource
from app.modules.courses.schemas import (
    CourseCreate,
    CourseOut,
    LessonAdminOut,
    LessonCreate,
    LessonOut,
    LessonUpdate,
    ModuleAdminOut,
    ModuleCreate,
    ModuleOut,
    ModuleUpdate,
    ResourceCreate,
    ResourceOut,
    ResourceUpdate,
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
        kind=body.kind,
    )
    return services.lesson_to_dict(le, "es")


# ──────────────── Admin editor ────────────────
# Editor de curso: vista completa con todas las traducciones + CRUD por módulo/lección.


@router.get("/{course_id}/admin", response_model=list[ModuleAdminOut])
def list_modules_admin(
    course_id: int,
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> list[dict]:
    if not db.get(Course, course_id):
        raise HTTPException(404, "Course not found")
    mods = (
        db.query(Module)
        .options(selectinload(Module.translations), selectinload(Module.lessons).selectinload(Lesson.translations))
        .filter(Module.course_id == course_id)
        .order_by(Module.order_index)
        .all()
    )
    return [services.module_admin_dict(m) for m in mods]


@router.patch("/modules/{module_id}", response_model=ModuleAdminOut)
def patch_module(
    module_id: int,
    body: ModuleUpdate,
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> dict:
    m = db.get(Module, module_id)
    if not m:
        raise HTTPException(404, "Module not found")
    services.update_module(
        db,
        m,
        order_index=body.order_index,
        translations=(
            [t.model_dump() for t in body.translations]
            if body.translations is not None
            else None
        ),
    )
    return services.module_admin_dict(m)


@router.patch("/lessons/{lesson_id}", response_model=LessonAdminOut)
def patch_lesson(
    lesson_id: int,
    body: LessonUpdate,
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> dict:
    le = db.get(Lesson, lesson_id)
    if not le:
        raise HTTPException(404, "Lesson not found")
    services.update_lesson(
        db,
        le,
        order_index=body.order_index,
        kind=body.kind,
        youtube_id=body.youtube_id,
        duration_seconds=body.duration_seconds,
        translations=(
            [t.model_dump() for t in body.translations]
            if body.translations is not None
            else None
        ),
    )
    return services.lesson_admin_dict(le)


@router.delete("/lessons/{lesson_id}", status_code=204)
def delete_lesson(
    lesson_id: int,
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> None:
    le = db.get(Lesson, lesson_id)
    if not le:
        raise HTTPException(404, "Lesson not found")
    services.delete_lesson(db, le)


# ──────────────── Module resources (PDF/PPT/video/doc/link) ────────────────


@router.get("/modules/{module_id}/resources", response_model=list[ResourceOut])
def list_resources(
    module_id: int,
    db: Session = Depends(get_db),
) -> list[ModuleResource]:
    if not db.get(Module, module_id):
        raise HTTPException(404, "Module not found")
    return (
        db.query(ModuleResource)
        .filter(ModuleResource.module_id == module_id)
        .order_by(ModuleResource.order_index)
        .all()
    )


@router.post(
    "/modules/{module_id}/resources",
    response_model=ResourceOut,
    status_code=201,
)
def create_resource(
    module_id: int,
    body: ResourceCreate,
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> ModuleResource:
    if not db.get(Module, module_id):
        raise HTTPException(404, "Module not found")
    r = ModuleResource(
        module_id=module_id,
        kind=body.kind,
        title=body.title,
        url=body.url,
        order_index=body.order_index,
    )
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


@router.patch("/resources/{resource_id}", response_model=ResourceOut)
def patch_resource(
    resource_id: int,
    body: ResourceUpdate,
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> ModuleResource:
    r = db.get(ModuleResource, resource_id)
    if not r:
        raise HTTPException(404, "Resource not found")
    if body.kind is not None:
        r.kind = body.kind
    if body.title is not None:
        r.title = body.title
    if body.url is not None:
        r.url = body.url
    if body.order_index is not None:
        r.order_index = body.order_index
    db.commit()
    db.refresh(r)
    return r


@router.delete("/resources/{resource_id}", status_code=204)
def delete_resource(
    resource_id: int,
    _admin: CurrentUser = Depends(require_roles("admin")),
    db: Session = Depends(get_db),
) -> None:
    r = db.get(ModuleResource, resource_id)
    if not r:
        raise HTTPException(404, "Resource not found")
    db.delete(r)
    db.commit()
