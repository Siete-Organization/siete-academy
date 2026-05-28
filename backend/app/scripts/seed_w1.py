"""Seed: Semana 1 del Módulo 1 (Anatomía de la venta B2B).

Crea la primera lección con la secuencia dinámica completa:
Video → Avatar IA → Presentación → Material → Examen.

Contenido extraído de SDR_Academy_Siete_Documento_Maestro.md (bloques 1-6 de
Semana 1 + 4 micro-pruebas MCQ Capa 1).

Idempotente — re-ejecutable. Usa el curso `sdr-academy-v1` y el módulo
`m1-juego-y-jugador` (los crea si no existen).

Uso:
    cd backend && .venv/bin/python -m app.scripts.seed_w1
"""

from __future__ import annotations

from app.core.database import SessionLocal
from app.core.logging import configure_logging, get_logger
from app.modules.assessments.models import Assessment
from app.modules.assessments import models as _assess  # noqa: F401
from app.modules.audit import models as _audit  # noqa: F401
from app.modules.courses.models import (
    Course,
    CourseTranslation,
    Lesson,
    LessonTranslation,
    Module,
    ModuleResource,
    ModuleTranslation,
)
from app.modules.courses import models as _courses  # noqa: F401
from app.modules.users import models as _users  # noqa: F401

configure_logging()
log = get_logger("seed_w1")


COURSE_SLUG = "sdr-academy-v1"
MODULE_SLUG = "m1-juego-y-jugador"


LESSON_BODY_ES = """Pregunta central de la semana: ¿Cómo toman decisiones de compra las empresas y en qué se diferencia estructuralmente de una decisión personal?

## Bloque 1 — Por qué el B2B es estructuralmente distinto al B2C
Las 5 diferencias estructurales: 6-10 personas vs 1, ciclo de meses vs días, separación quien paga / quien usa, racionalidad aparente + emocionalidad real, ticket alto con consecuencias sostenidas.

## Bloque 2 — Cómo compra una empresa: racionalidad, política y comité
La paradoja del comprador B2B (Kahneman, Sistema 1 / Sistema 2). Avance de carrera, status interno, costos no visibles, miedo al error público, lealtades. El 77% de las decisiones B2B requiere consenso de al menos 3 personas (Gartner).

## Bloque 3 — Los buying cycles B2B: las 5 etapas
Awareness (acá entra el outbound) → Consideración (2-6 sem) → Evaluación (2-6 m, etapa más larga, 40-60% termina en no-decisión) → Decisión (2-8 sem) → Implementación (1-6 m).

## Bloque 4 — Los stakeholders de una decisión B2B
9 roles: Decisor económico, Decisor técnico (puede vetar), Usuario, Coach/champion, Influenciador, Bloqueador, Referidor, Compras, Legal. Cada uno con su motivación y su miedo. El mensaje del SDR le tiene que hablar a la motivación y tocarle el miedo del rol específico.

## Bloque 5 — El ciclo de vida del prospecto
Prospect → MQL → SQL → Opportunity → Customer → Renovación/Churn/Expansión. El SDR opera de Prospect a Opportunity. NO confundir con el lifecycle del cliente ya firmado (Onboarding → Use → Renew), que maneja Client Success.

## Bloque 6 — LOBs y la disociación quien paga / quien usa
En empresas grandes con líneas de negocio (LOBs) cada una puede tener presupuesto autónomo. Identificar temprano: quién usa, quién aprueba técnicamente, quién paga. Si solo contactás al usuario sin llegar al que paga, el deal se estanca.

**Fuentes:** Gartner (2020-2023). Kahneman (2011). Miller-Heiman (1985+). Ross & Tyler (2011). Bertuzzi (2016). Dixon et al (2015). Rackham (1988)."""


AVATAR_SCRIPT_ES = """Hola. Soy tu coach IA para esta primera semana del programa.

Antes de empezar, una pregunta para que la tengas en la cabeza todo este módulo: cuando una empresa compra algo, ¿quién decide realmente?

Si pensaste "la persona con el cargo más alto", esta semana vas a aprender que la respuesta es más complicada — y más interesante.

Del otro lado de tu email no hay una persona. Hay un sistema. Entre 6 y 10 personas, según Gartner, con intereses distintos, miedos distintos y agendas distintas. Algunas firman, otras vetan, otras te ignoran, y una sola — el coach interno — puede hacer que ganes o pierdas el deal.

En esta lección vamos a ver seis bloques. Primero, por qué comprar en B2B es estructuralmente diferente a comprar como persona. Después, la paradoja del comprador racional que en realidad decide por política interna. Después, las cinco etapas del buying cycle, los nueve roles del comité, el ciclo de vida del prospecto, y cómo se disocia quien paga de quien usa.

Al final hay cuatro micro-pruebas. No son para que te las saques de encima — son para que detectes dónde no quedó claro un concepto antes de avanzar a la Semana 2, que se construye sobre todo esto.

Una cosa más: cada concepto que vas a ver acá tiene fuente trazable. Si algo te parece dudoso, podés ir al libro o al estudio original. No te pedimos que confíes — te damos los fundamentos para que verifiques.

Arrancamos."""


PRESENTATION_BLOCKS_ES = [
    {
        "title": "Las 5 diferencias estructurales B2B vs B2C",
        "bullets": [
            "Cantidad: 6-10 personas vs 1",
            "Duración: meses/años vs horas/días",
            "Separación: quien paga ≠ quien usa",
            "Racionalidad aparente + emocionalidad real",
            "Ticket alto + aversión al error pública",
        ],
        "source": "Gartner B2B Buying Journey 2020-2023",
    },
    {
        "title": "La paradoja del comprador B2B",
        "bullets": [
            "Sistema 1 (intuitivo) decide; Sistema 2 (racional) justifica",
            "La matriz comparativa se arma para los demás, no para el decisor",
            "Factores invisibles: carrera, status interno, miedo al error público",
            "77% de decisiones B2B requieren consenso de ≥3 personas",
        ],
        "source": "Kahneman 2011, Gartner 2020+",
    },
    {
        "title": "Las 5 etapas del buying cycle",
        "bullets": [
            "1. Awareness (acá entra el outbound)",
            "2. Consideración — 2-6 semanas",
            "3. Evaluación — 2-6 meses (40-60% termina en no-decisión)",
            "4. Decisión — 2-8 semanas con negociación",
            "5. Implementación — 1-6 meses",
        ],
        "source": "Gartner + Bridge Group SDR Metrics",
    },
    {
        "title": "Los 9 roles del comité de compra",
        "bullets": [
            "Decisor económico (firma la PO)",
            "Decisor técnico (puede vetar)",
            "Usuario (uso diario)",
            "Coach/champion (te quiere hacer ganar)",
            "Influenciador / Bloqueador / Referidor",
            "Compras (negocia al final) / Legal (cláusulas)",
        ],
        "source": "Miller-Heiman, The New Strategic Selling 1985+",
    },
    {
        "title": "Lifecycle del prospecto (lo que mueve el SDR)",
        "bullets": [
            "Prospect → MQL → SQL → Opportunity → Customer",
            "El SDR opera Prospect → Opportunity",
            "Después del handoff, el SDR sale de la conversación",
            "NO confundir con onboarding (lifecycle del cliente ya firmado)",
        ],
        "source": "Predictable Revenue (Ross & Tyler 2011)",
    },
    {
        "title": "LOBs y disociación quien paga / quien usa",
        "bullets": [
            "Empresas grandes tienen líneas de negocio con presupuestos autónomos",
            "Identificar: quién usa, quién aprueba técnicamente, quién paga",
            "Solo usuario sin pagador → deal estancado",
            "Solo pagador sin champion interno → nadie empuja desde adentro",
        ],
        "source": "Miller-Heiman + Bertuzzi 2016",
    },
]


MCQ_QUESTIONS = [
    {
        "id": "q1",
        "block": 2,
        "type": "single",
        "prompt": (
            "Mauricio, VP Tech de empresa B2B (400 empleados), responde a tu propuesta: "
            "'la propuesta se ve bien. El problema es que nuestro proveedor actual lo trajo "
            "el CIO anterior hace 5 años y todavía tiene mucha llegada al directorio. Cambiar "
            "acá es básicamente tener una pelea interna que no me conviene justo ahora, con un "
            "board meeting en 6 semanas donde tengo otras prioridades que ganar. Quizás más "
            "adelante.' ¿Cuál es el factor principal que está frenando el deal?"
        ),
        "choices": [
            {"id": "a", "text": "Mauricio no le ve valor al producto."},
            {"id": "b", "text": "El precio es demasiado alto para la empresa."},
            {
                "id": "c",
                "text": (
                    "Política interna: cambiar de proveedor implica una pelea con el CIO anterior "
                    "(que aún tiene influencia) + Mauricio tiene otras prioridades políticas en juego."
                ),
            },
            {"id": "d", "text": "Mauricio no tiene autoridad para decidir."},
        ],
        "correct": ["c"],
        "explanation": (
            "Mauricio te lo dice explícito: la barrera no es técnica ni económica, es política. "
            "Calcula el costo político de pelear con el CIO anterior en un momento de otras "
            "batallas internas. La matriz de ROI no destraba esto. Un SDR con criterio pregunta: "
            "'¿Tendría sentido retomarlo en 8-10 semanas, después del board?'."
        ),
    },
    {
        "id": "q2",
        "block": 3,
        "type": "multi",
        "prompt": (
            "Marcá TODAS las respuestas de prospectos a un cold email que indican "
            "EVALUACIÓN ACTIVA (vs awareness, consideración temprana, post-decisión o bloqueado):"
        ),
        "choices": [
            {
                "id": "1",
                "text": (
                    "'Interesante. Nunca me senté a pensar si tenemos este problema. "
                    "Voy a consultar internamente.'"
                ),
            },
            {
                "id": "2",
                "text": (
                    "'Estamos evaluando 3 proveedores. ¿Podés mandarme deck y precios para "
                    "la comparación?'"
                ),
            },
            {
                "id": "3",
                "text": "'Ya firmamos con otro el mes pasado. Arrancamos la semana que viene.'",
            },
            {
                "id": "4",
                "text": (
                    "'Estamos armando RFP para Q2, ¿podés mandar info técnica para incluirte?'"
                ),
            },
            {"id": "5", "text": "'Sacame de tu lista por favor, no me escribas más.'"},
            {
                "id": "6",
                "text": "'Me interesa pero lo estamos mirando a futuro, no es prioridad este año.'",
            },
            {
                "id": "7",
                "text": (
                    "'Tenemos reunión interna próxima semana para ver si arrancamos proyecto. "
                    "¿Venís con demo el jueves?'"
                ),
            },
        ],
        "correct": ["2", "4", "7"],
        "explanation": (
            "Evaluación activa = shortlist armada + comparación formal (2), RFP en proceso (4), "
            "demo agendada para reunión de decisión (7). El resto está en awareness (1), "
            "post-decisión (3), bloqueo explícito (5) o consideración con timing largo (6)."
        ),
    },
    {
        "id": "q3",
        "block": 4,
        "type": "match",
        "prompt": (
            "Empresa B2B de 350 empleados evaluando software de marketing. "
            "Emparejá cada persona con su rol en el comité de compra:"
        ),
        "left": [
            {
                "id": "1",
                "text": (
                    "Laura, VP Marketing. Firma la PO final, presupuesto anual propio."
                ),
            },
            {
                "id": "2",
                "text": (
                    "Ramiro, Director IT. Evalúa integración con CRM y ERP, puede vetar."
                ),
            },
            {
                "id": "3",
                "text": (
                    "Florencia, Community Manager. Va a usarlo 6h/día con su equipo de 4."
                ),
            },
            {
                "id": "4",
                "text": (
                    "Carlos, Coordinador. Te pasó el contacto de Laura, empuja desde dentro hace 8 meses."
                ),
            },
            {
                "id": "5",
                "text": (
                    "Mónica, Directora de Compras. Entra al final para negociar precio y SLAs."
                ),
            },
        ],
        "right": [
            {"id": "A", "text": "Decisor económico"},
            {"id": "B", "text": "Decisor técnico (puede vetar)"},
            {"id": "C", "text": "Usuario"},
            {"id": "D", "text": "Coach / champion + referidor"},
            {"id": "E", "text": "Compras"},
        ],
        "correct": {"1": "A", "2": "B", "3": "C", "4": "D", "5": "E"},
        "explanation": (
            "Autoridad presupuestaria ≠ poder de veto técnico. Error de novato: asumir que el "
            "más senior es siempre el decisor económico — no es cierto en empresas con "
            "presupuestos descentralizados."
        ),
    },
    {
        "id": "q4",
        "block": 5,
        "type": "single",
        "prompt": (
            "Un SDR junior dice: 'Tenemos una empresa que está en la etapa de ONBOARDING. "
            "El SDR del trimestre pasado los pasó a esta etapa hace 2 meses.' "
            "¿Cuál es el problema con lo que dijo?"
        ),
        "choices": [
            {
                "id": "a",
                "text": "Está bien — onboarding es etapa correcta del lifecycle del prospecto.",
            },
            {
                "id": "b",
                "text": (
                    "Mezcla dos lifecycles distintos: 'onboarding' es parte del lifecycle del "
                    "cliente ya firmado (post-venta), no del lifecycle del prospecto. "
                    "El SDR mueve a Opportunity, no a Onboarding."
                ),
            },
            {"id": "c", "text": "El problema es que dice 'trimestre pasado' en vez de 'mes pasado'."},
            {"id": "d", "text": "El error es decir 'empresa' en vez de 'prospecto'."},
        ],
        "correct": ["b"],
        "explanation": (
            "Hay dos lifecycles que se confunden por nombres parecidos: "
            "Prospect→MQL→SQL→Opportunity→Customer (lo mueve el SDR) y "
            "Onboarding→Use→Renew (lo mueve Client Success post-firma). "
            "En empresas como Siete coexisten ambos — confundirlos genera reportes inservibles."
        ),
    },
]


RESOURCES = [
    {
        "kind": "pdf",
        "title": "Handout — Anatomía de la venta B2B (Semana 1)",
        "url": "https://drive.google.com/file/d/PLACEHOLDER_W1_HANDOUT",
        "order_index": 0,
    },
    {
        "kind": "link",
        "title": "Gartner — The B2B Buying Journey Report",
        "url": "https://www.gartner.com/en/sales/insights/b2b-buying-journey",
        "order_index": 1,
    },
    {
        "kind": "link",
        "title": "Anexo — Landscape de industrias B2B LATAM",
        "url": "/docs/landscape-latam",
        "order_index": 2,
    },
]


def _upsert_course(db) -> Course:
    course = db.query(Course).filter_by(slug=COURSE_SLUG).first()
    if course:
        return course
    course = Course(slug=COURSE_SLUG)
    course.translations.append(
        CourseTranslation(
            locale="es",
            title="SDR Academy Siete",
            description="Programa de 8 semanas en fundamentos de venta B2B outbound.",
        )
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    log.info("course.seeded", extra={"course_id": course.id, "slug": COURSE_SLUG})
    return course


def _upsert_module(db, course: Course) -> Module:
    module = (
        db.query(Module)
        .filter_by(course_id=course.id, slug=MODULE_SLUG)
        .first()
    )
    if module:
        return module
    module = Module(course_id=course.id, slug=MODULE_SLUG, order_index=0)
    module.translations.append(
        ModuleTranslation(
            locale="es",
            title="Módulo 1 — El juego y el jugador",
            summary="Cómo se compra en B2B y qué hace un SDR.",
        )
    )
    db.add(module)
    db.commit()
    db.refresh(module)
    log.info("module.seeded", extra={"module_id": module.id, "slug": MODULE_SLUG})
    return module


def _upsert_lesson(db, module: Module) -> Lesson:
    lesson = (
        db.query(Lesson)
        .filter_by(module_id=module.id, order_index=0)
        .first()
    )
    if lesson is None:
        lesson = Lesson(
            module_id=module.id,
            order_index=0,
            kind="video",
            youtube_id=None,
            duration_seconds=1200,
        )
        lesson.translations.append(
            LessonTranslation(
                locale="es",
                title="Semana 1 — Anatomía de la venta B2B",
                body=LESSON_BODY_ES,
            )
        )
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
        log.info("lesson.seeded", extra={"lesson_id": lesson.id})
    # Set the dynamic fields on every run so the seed stays the source of truth.
    lesson.avatar_script = AVATAR_SCRIPT_ES
    lesson.avatar_audio_url = lesson.avatar_audio_url or None
    lesson.presentation_url = lesson.presentation_url or None
    lesson.presentation_blocks = PRESENTATION_BLOCKS_ES
    # Refresh ES body in case the doc maestro evolved.
    tr_es = next((t for t in lesson.translations if t.locale == "es"), None)
    if tr_es is not None:
        tr_es.body = LESSON_BODY_ES
        tr_es.title = "Semana 1 — Anatomía de la venta B2B"
    db.commit()
    return lesson


def _upsert_resources(db, module: Module, lesson: Lesson) -> None:
    for spec in RESOURCES:
        existing = (
            db.query(ModuleResource)
            .filter_by(module_id=module.id, lesson_id=lesson.id, title=spec["title"])
            .first()
        )
        if existing:
            existing.kind = spec["kind"]
            existing.url = spec["url"]
            existing.order_index = spec["order_index"]
            continue
        db.add(
            ModuleResource(
                module_id=module.id,
                lesson_id=lesson.id,
                kind=spec["kind"],
                title=spec["title"],
                url=spec["url"],
                order_index=spec["order_index"],
            )
        )
    db.commit()
    log.info("resources.seeded", extra={"lesson_id": lesson.id, "count": len(RESOURCES)})


def _upsert_assessment(db, module: Module, lesson: Lesson) -> Assessment:
    config = {
        "rules": {
            "attempts": 1,
            "time_per_question_seconds": 120,
            "shuffle": True,
            "feedback_after_each": True,
        },
        "questions": MCQ_QUESTIONS,
    }
    existing = (
        db.query(Assessment)
        .filter_by(module_id=module.id, lesson_id=lesson.id, type="mcq")
        .first()
    )
    if existing is None:
        a = Assessment(
            module_id=module.id,
            lesson_id=lesson.id,
            type="mcq",
            title="Micro-pruebas — Semana 1",
            config=config,
            passing_score=65.0,
        )
        db.add(a)
        db.commit()
        db.refresh(a)
        log.info("assessment.seeded", extra={"assessment_id": a.id})
        return a
    existing.title = "Micro-pruebas — Semana 1"
    existing.config = config
    existing.passing_score = 65.0
    db.commit()
    return existing


def run() -> None:
    db = SessionLocal()
    try:
        course = _upsert_course(db)
        module = _upsert_module(db, course)
        lesson = _upsert_lesson(db, module)
        _upsert_resources(db, module, lesson)
        _upsert_assessment(db, module, lesson)
        log.info(
            "seed_w1.done",
            extra={
                "course_id": course.id,
                "module_id": module.id,
                "lesson_id": lesson.id,
            },
        )
    finally:
        db.close()


if __name__ == "__main__":
    run()
