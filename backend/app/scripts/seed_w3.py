"""Seed: Semana 3 del Módulo 2 (Business Acumen: leer un negocio).

Apertura del Módulo 2 — "El otro lado". Contenido extraído de
SDR_Academy_Siete_Documento_Maestro.md (bloques 1-7 de Semana 3 + 4 micro-pruebas
MCQ Capa 1).

Crea el módulo `m2-el-otro-lado` (order_index=1) si no existe, y dentro la primera
lección (order_index=0) con la secuencia dinámica completa.

Uso:
    cd backend && .venv/bin/python -m app.scripts.seed_w3
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
log = get_logger("seed_w3")


COURSE_SLUG = "sdr-academy-v1"
MODULE_SLUG = "m2-el-otro-lado"


LESSON_BODY_ES = """Pregunta central de la semana: ¿Cómo se lee un negocio lo suficientemente bien para hablarle a su dueño como un par?

## Bloque 1 — Qué es business acumen y por qué separa al SDR mediocre del excelente
La brecha: dos SDRs con el mismo lead generan resultados 6× distintos (0.5% vs 3%) por lo que entienden del negocio del otro. Business acumen = leer cómo gana plata una empresa, qué la hace crecer, qué la frena. Es la variable individual que más mueve la carrera comercial B2B a 5 años.

## Bloque 2 — Business Model Canvas (Osterwalder)
9 componentes para leer cualquier empresa en 30 minutos: segmentos, propuesta de valor, canales, relación con cliente, fuentes de ingresos, recursos clave, actividades clave, alianzas clave, estructura de costos. Proceso: 10 min web + 10 min LinkedIn/News + 10 min pensando.

## Bloque 3 — Unit economics: LTV, CAC, payback
LTV (lifetime value) = ingreso promedio × meses de permanencia. CAC = costo total comercial / clientes nuevos. Payback = meses para recuperar CAC. Regla de oro SaaS B2B: LTV/CAC ≥ 3x (Skok). El SDR no calcula pero entiende el lenguaje del CFO. Benchmarks payback: PLG 6-9m, mid-market 12-18m, enterprise 18-24m.

## Bloque 4 — Las 5 fuerzas de Porter (industria)
Rivalidad entre competidores, amenaza de nuevos entrantes, amenaza de sustitutos, poder de compradores, poder de proveedores. Cuando todas son altas, industria dura (margen bajo). El gancho del cold email cambia según qué fuerza presiona más: retail compite por costo, banca tradicional se defiende de fintech, minería reduce costo por tonelada.

## Bloque 5 — Jobs to Be Done (Christensen)
La gente no compra productos, los contrata para hacer un trabajo. Un CFO no quiere reportes — quiere llegar tranquilo al board. 3 dimensiones del job: funcional (qué hace), emocional (cómo se siente al hacerlo), social (cómo se ve ante otros). Un SDR que integra las 3 dimensiones conecta con motivación real, no con el brochure.

## Bloque 6 — Mapeo dolor-solución
3 elementos: dolor específico del prospecto (no genérico) + impacto cuantificado + conexión con la oferta sin sobreprometer. Sin BMC + Porter + Jobs to Be Done previos, no hay mapeo — solo pitch disfrazado.

## Bloque 7 — El error #1 del SDR nuevo
Vender la solución sin haber entendido el problema. 3 filtros antes de cada outreach: (1) ¿identifiqué un dolor específico? (2) ¿los 2 primeros párrafos hablan del prospecto o de mí? (3) ¿la propuesta implícita es "esto PODRÍA aplicar" o "esto TE SIRVE"? Si alguno falla, rehacés.

**Fuentes:** Osterwalder & Pigneur (2010). Porter (1979). Christensen et al (2016). Skok SaaS Metrics 2.0. Bertuzzi (2016). Dixon & Adamson (2011)."""


AVATAR_SCRIPT_ES = """Arrancamos el Módulo 2. Si el Módulo 1 te enseñó cómo se compra en B2B, este módulo te enseña a leer el otro lado: la empresa que tenés enfrente y la persona que decide.

Esta semana, la pregunta central: ¿cómo se lee un negocio lo suficientemente bien para hablarle a su dueño como un par?

Para que te quede clara la apuesta: dos SDRs reciben el mismo lead — empresa de logística, 300 empleados, contacto con el COO. Uno escribe "trabajamos con empresas de logística ayudándoles a optimizar operaciones, ¿tenés 20 minutos?". Convierte al medio por ciento. Otro escribe "vi que abrieron centro en Arequipa el mes pasado; en logística que se expande a regiones lo que suele pesar es el calibrado de la demanda local — sobrestock y quiebre conviven hasta que el modelo se ajusta. ¿Les está pasando?". Convierte al tres por ciento. Seis veces más con la misma oferta.

La diferencia no es el copy. Es lo que el SDR entiende del negocio del otro.

En los siete bloques vas a ver: por qué business acumen separa al SDR mediocre del excelente, el Business Model Canvas para leer cualquier empresa en treinta minutos, unit economics para hablarle al CFO (LTV, CAC, payback), las cinco fuerzas de Porter para leer una industria, Jobs to Be Done para separar producto de problema, mapeo dolor-solución, y el error número uno del SDR nuevo: vender la solución sin entender el problema.

Vas a usar el anexo de industrias LATAM bastante. Tenelo cerca.

Al final, cuatro micro-pruebas que conectan los bloques en casos concretos. Arrancamos."""


PRESENTATION_BLOCKS_ES = [
    {
        "title": "La brecha: 0.5% vs 3%",
        "bullets": [
            "Mismo lead, misma oferta, 6× diferencia de conversión",
            "Variable que cambia: lo que el SDR entiende del negocio del otro",
            "Business acumen = activo conceptual transferible entre industrias",
            "Probable: la variable individual que más mueve la carrera a 5 años",
        ],
        "source": "Bridge Group 2023 + casos Siete",
    },
    {
        "title": "Business Model Canvas — 9 componentes",
        "bullets": [
            "Segmentos / Propuesta de valor / Canales",
            "Relación con cliente / Fuentes de ingresos",
            "Recursos / Actividades / Alianzas clave",
            "Estructura de costos",
            "Aplicable en 30 min (web + LinkedIn + pensar)",
        ],
        "source": "Osterwalder & Pigneur 2010, Business Model Generation",
    },
    {
        "title": "Unit economics — 3 métricas obsesivas",
        "bullets": [
            "LTV (ticket promedio × meses de permanencia)",
            "CAC (costo comercial / clientes nuevos)",
            "Payback (meses para recuperar CAC)",
            "Regla LTV/CAC ≥ 3x — gobierna casi todo B2B recurrente",
        ],
        "source": "Skok, SaaS Metrics 2.0",
    },
    {
        "title": "5 fuerzas de Porter — leer la industria",
        "bullets": [
            "Rivalidad entre competidores",
            "Amenaza de nuevos entrantes",
            "Amenaza de sustitutos",
            "Poder de negociación de compradores",
            "Poder de negociación de proveedores",
        ],
        "source": "Porter 1979/2008, Harvard Business Review",
    },
    {
        "title": "Jobs to Be Done — 3 dimensiones",
        "bullets": [
            "Funcional: qué tarea cumple",
            "Emocional: cómo se siente al hacerla",
            "Social: cómo se ve ante otros",
            "Un CFO no quiere reportes — quiere llegar tranquilo al board",
        ],
        "source": "Christensen et al 2016, Competing Against Luck",
    },
    {
        "title": "Mapeo dolor-solución — 3 piezas",
        "bullets": [
            "Dolor específico del prospecto (no genérico)",
            "Impacto cuantificado (porcentaje / dinero / tiempo)",
            "Conexión con oferta SIN sobreprometer",
            "Requiere BMC + Porter + JTBD previos",
        ],
        "source": "Bertuzzi 2016 + Christensen 2016",
    },
    {
        "title": "Error #1 del SDR nuevo",
        "bullets": [
            "Vender la solución sin entender el problema",
            "Filtro 1: ¿identifiqué dolor específico?",
            "Filtro 2: ¿hablo del prospecto o de mí en los 2 primeros párrafos?",
            "Filtro 3: ¿es 'PODRÍA aplicar' o 'TE SIRVE'?",
        ],
        "source": "Bertuzzi 2016 + Dixon & Adamson 2011",
    },
]


MCQ_QUESTIONS = [
    {
        "id": "q1",
        "block": 5,
        "type": "single",
        "prompt": (
            "ClarityHub (plataforma CRM) dice en su web: 'la plataforma de CRM más avanzada del "
            "mercado, con IA, automatización y dashboards en tiempo real'. Un SDR va a prospectar "
            "a Patricia, VP de Ventas de una fintech post-Serie B que está triplicando equipo "
            "comercial. Aplicando Jobs to Be Done, ¿cuál es la conexión MÁS EFECTIVA?"
        ),
        "choices": [
            {
                "id": "a",
                "text": (
                    "'ClarityHub te permite gestionar tu operación comercial con dashboards en "
                    "tiempo real.'"
                ),
            },
            {
                "id": "b",
                "text": "'ClarityHub potencia tu equipo de ventas con IA y automatización.'",
            },
            {
                "id": "c",
                "text": (
                    "'VPs de Ventas post-Serie B que triplican equipo comercial reportan "
                    "tranquilidad a la hora del board, porque pueden mostrar forecast preciso sin "
                    "pasar 2 días pre-reunión buscando números. ClarityHub les da esa visibilidad "
                    "de un día para otro.'"
                ),
            },
            {
                "id": "d",
                "text": "'ClarityHub es líder del mercado y trabaja con Google, Meta y Netflix.'",
            },
        ],
        "correct": ["c"],
        "explanation": (
            "Opción c aplica las 3 dimensiones del job: funcional (forecast preciso), emocional "
            "(tranquilidad pre-board) y social (mostrar números al board). Además ancla al "
            "contexto específico (post-Serie B + triplicación). Opciones a y b se quedan en lo "
            "funcional pelado. Opción d es name-dropping descontextualizado."
        ),
    },
    {
        "id": "q2",
        "block": 3,
        "type": "single",
        "prompt": (
            "Una startup SaaS B2B publica: 'crecemos al 15% mensual. Ticket promedio anual "
            "USD 3.600. Nos cuesta USD 8.500 adquirir un cliente. Permanencia promedio 18 "
            "meses.' ¿Qué observación tiene MÁS probabilidad de resonar con los founders?"
        ),
        "choices": [
            {"id": "a", "text": "'Crecer al 15% mensual es impresionante, felicidades.'"},
            {
                "id": "b",
                "text": (
                    "'Con LTV/CAC cerca de 1.6x (5.400 LTV / 8.500 CAC), están bajo la regla de "
                    "3x que los inversionistas miran. Probablemente el foco del año sea subir LTV "
                    "o bajar CAC.'"
                ),
            },
            {"id": "c", "text": "'El ticket de USD 3.600 es bajo para SaaS B2B, deberían subirlo.'"},
            {"id": "d", "text": "'Con 15% mensual de crecimiento, en 3 años van a ser unicornios.'"},
        ],
        "correct": ["b"],
        "explanation": (
            "LTV = USD 3.600/año × 1.5 años = USD 5.400. CAC = USD 8.500. LTV/CAC = 0.63 estricto "
            "o ~1.6x con margen bruto típico SaaS. Diagnóstico: bajo la regla 3x — ese es el dolor "
            "real de los founders, no la métrica pública del 15%. El SDR que entiende esto le "
            "habla del dolor de fondo. Opción a es cortesía sin valor. Opción c es opinión sin "
            "data. Opción d es proyección infundada."
        ),
    },
    {
        "id": "q3",
        "block": 4,
        "type": "multi",
        "prompt": (
            "Industria: retail físico de electrodomésticos en LATAM (Falabella, Ripley, Coppel). "
            "Marcá TODAS las fuerzas de Porter que están fuertemente PRESIONANDO a esta industria:"
        ),
        "choices": [
            {
                "id": "1",
                "text": (
                    "Rivalidad entre competidores existentes (pocas cadenas grandes compitiendo "
                    "feroz en precio)"
                ),
            },
            {
                "id": "2",
                "text": "Amenaza de nuevos entrantes (e-commerce: Mercado Libre, Amazon, D2C)",
            },
            {
                "id": "3",
                "text": (
                    "Amenaza de sustitutos (compra directa de marca, modelos de renta o "
                    "suscripción)"
                ),
            },
            {
                "id": "4",
                "text": (
                    "Poder de negociación de compradores (consumidor con acceso total a precios, "
                    "comparadores, reviews)"
                ),
            },
            {
                "id": "5",
                "text": (
                    "Poder de negociación de proveedores (Samsung, LG, Whirlpool presionando "
                    "costos)"
                ),
            },
        ],
        "correct": ["1", "2", "3", "4"],
        "explanation": (
            "Solo 1-4 presionan. La fuerza 5 está INVERTIDA: el retail tiene poder sobre los "
            "proveedores (negocia márgenes bajos, plazos de pago, exclusividades — los fabricantes "
            "dependen del retail físico para llegar al consumidor). Conclusión estratégica: retail "
            "físico está en industria muy dura, los dolores son defenderse del e-commerce y "
            "optimizar costo operativo."
        ),
    },
    {
        "id": "q4",
        "block": 7,
        "type": "single",
        "prompt": (
            "Cold email de un SDR de GrowthLab a Carolina (VP Marketing de un e-commerce de moda): "
            "'Asunto: Oportunidad de crecimiento. Hola Carolina, mi nombre es Diego de GrowthLab. "
            "Somos una plataforma de automatización de marketing B2B con +500 clientes en LATAM, "
            "incluyendo Alicorp y Falabella. Nuestra plataforma tiene +200 integraciones, AI "
            "nativa, y dashboards en tiempo real. Me encantaría mostrarte cómo podemos ayudar a "
            "[empresa] a escalar su marketing. ¿Tenés 30 min esta semana?' ¿Cuál es el error "
            "PRINCIPAL del email según el Bloque 7?"
        ),
        "choices": [
            {"id": "a", "text": "Es demasiado largo."},
            {
                "id": "b",
                "text": (
                    "Vende la solución sin entender el problema: cero referencia al contexto "
                    "específico de Carolina, a su empresa, a un dolor identificado. Es producto "
                    "genérico + CTA directo, sin mapeo dolor-solución."
                ),
            },
            {"id": "c", "text": "El asunto debería ser más específico."},
            {
                "id": "d",
                "text": (
                    "Menciona Alicorp y Falabella pero no son peer del e-commerce de moda."
                ),
            },
        ],
        "correct": ["b"],
        "explanation": (
            "Error #1 del SDR nuevo (Bloque 7). El email habla de la plataforma (200 integraciones, "
            "AI, dashboards) — dimensión funcional pura. Cero análisis del negocio de Carolina. "
            "Cero dolor específico. Pide 30 min sin construir relevancia. Opciones a, c y d son "
            "observaciones secundarias — el error estructural es el del Bloque 7: 'vender la "
            "solución sin entender el problema'."
        ),
    },
]


RESOURCES = [
    {
        "kind": "pdf",
        "title": "Handout — Business acumen (Semana 3)",
        "url": "https://drive.google.com/file/d/PLACEHOLDER_W3_HANDOUT",
        "order_index": 0,
    },
    {
        "kind": "link",
        "title": "Osterwalder — Business Model Canvas (PDF)",
        "url": "https://www.strategyzer.com/canvas/business-model-canvas",
        "order_index": 1,
    },
    {
        "kind": "link",
        "title": "Porter — The Five Competitive Forces That Shape Strategy (HBR)",
        "url": "https://hbr.org/2008/01/the-five-competitive-forces-that-shape-strategy",
        "order_index": 2,
    },
    {
        "kind": "link",
        "title": "Skok — SaaS Metrics 2.0 (LTV, CAC, payback)",
        "url": "https://www.forentrepreneurs.com/saas-metrics-2/",
        "order_index": 3,
    },
    {
        "kind": "link",
        "title": "Anexo — Landscape de industrias LATAM (10 industrias)",
        "url": "/docs/landscape-latam",
        "order_index": 4,
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
    return course


def _upsert_module(db, course: Course) -> Module:
    module = (
        db.query(Module)
        .filter_by(course_id=course.id, slug=MODULE_SLUG)
        .first()
    )
    if module:
        return module
    module = Module(course_id=course.id, slug=MODULE_SLUG, order_index=1)
    module.translations.append(
        ModuleTranslation(
            locale="es",
            title="Módulo 2 — El otro lado",
            summary="Cómo leer el negocio del prospecto y al comprador dentro de él.",
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
            duration_seconds=1500,
        )
        lesson.translations.append(
            LessonTranslation(
                locale="es",
                title="Semana 3 — Business acumen: leer un negocio",
                body=LESSON_BODY_ES,
            )
        )
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
        log.info("lesson.seeded", extra={"lesson_id": lesson.id})
    lesson.avatar_script = AVATAR_SCRIPT_ES
    lesson.presentation_blocks = PRESENTATION_BLOCKS_ES
    tr_es = next((t for t in lesson.translations if t.locale == "es"), None)
    if tr_es is not None:
        tr_es.body = LESSON_BODY_ES
        tr_es.title = "Semana 3 — Business acumen: leer un negocio"
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
            title="Micro-pruebas — Semana 3",
            config=config,
            passing_score=65.0,
        )
        db.add(a)
        db.commit()
        db.refresh(a)
        log.info("assessment.seeded", extra={"assessment_id": a.id})
        return a
    existing.title = "Micro-pruebas — Semana 3"
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
            "seed_w3.done",
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
