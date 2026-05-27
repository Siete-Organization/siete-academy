"""Seed: Semana 5 del Módulo 3 (Escritura persuasiva en frío).

Apertura del Módulo 3 — "La conexión". Contenido extraído de
SDR_Academy_Siete_Documento_Maestro.md (bloques 1-8 de Semana 5 + 4 micro-pruebas
MCQ Capa 1).

Crea el módulo `m3-la-conexion` (order_index=2) si no existe, y dentro la primera
lección (order_index=0) con la secuencia dinámica completa.

Uso:
    cd backend && .venv/bin/python -m app.scripts.seed_w5
"""

from __future__ import annotations

from app.core.database import Base, SessionLocal, engine
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
log = get_logger("seed_w5")


COURSE_SLUG = "sdr-academy-v1"
MODULE_SLUG = "m3-la-conexion"


LESSON_BODY_ES = """Pregunta central de la semana: ¿Cómo escribo un mensaje que alguien que no me conoce decida leer y responder?

**Dato crudo:** el 58% de las respuestas en cold email llegan al primer email (Instantly 2026). Si tu primer email no funciona, más de la mitad del funnel se rompe desde el arranque.

## Bloque 1 — Los 7 principios de persuasión de Cialdini aplicados a cold email
Reciprocidad (dar antes de pedir), Compromiso & consistencia (CTAs pequeños primero), Prueba social (relevante, no de tamaño), Autoridad (observación específica > títulos), Simpatía (tono humano), Escasez (real, no artificial), Unidad (misma tribu). No son técnicas de venta — son cómo funciona la mente del lector.

## Bloque 2 — Escribir para alguien que no te quiere leer
3-7 segundos para decidir si sigue leyendo. 4 reglas: brevedad (<80 palabras), claridad (1 idea), especificidad (hechos, no vaguedades), 1 solo CTA. Recortá, no resumas (Heath & Heath 2007: "si tenés 3 prioridades, no tenés prioridades").

## Bloque 3 — Anatomía del mensaje outbound: 4 partes
**Asunto** (3-7 palabras, específico, sin palabras-trigger). **Apertura** (2 líneas sobre el lector, no sobre vos). **Gancho** ("porque vos [situación] probablemente [consecuencia]"). **CTA** (pregunta pequeña o acción concreta con opción acotada).

## Bloque 4 — El pecado capital: hablar del remitente
Regla "tachar-y-contar": tachá todas las menciones a vos/tu empresa. Si queda casi nada → tu email era autopresentación con CTA. Carnegie (1936) sigue vigente: "hablale de él mismo y te escuchará por horas".

## Bloque 5 — Construcción de ganchos desde señales reales
Sin gancho: 0.5-1% conversión. Con gancho bien construido: 2-4% (Bridge Group). Fórmula: [señal específica verificable] + [consecuencia o desafío típico en esa situación] = gancho. Sin prometer solución. 15 min de research antes de cada email — si no hay señal, no escribís.

## Bloque 6 — Dos conversaciones distintas: al decisor (KDM) y al referidor
Al KDM: objetivo abrir conversación sobre su desafío, tono directo, CTA = reunión o validación. Al referidor: NO se le vende, pide orientación sobre quién decide, tono humilde, CTA = que indique a la persona correcta. Confundirlos destruye el outbound.

## Bloque 7 — Tono y registro en LATAM B2B
Bibliografía anglosajona no aplica tal cual. Más formalidad que el estándar US, 1 línea de cortesía OK, humor genuino humaniza, longitud ~85-90 palabras = ~75-80 en inglés. Pronombre: "tú" es default seguro en lista mixta LATAM. Evitar: corporativo extremo, vendedor de pilas, técnico puro.

## Bloque 8 — Grid de 6 criterios para evaluar copy
Especificidad del gancho / Foco en el lector / Longitud / Un solo CTA / Tono y registro / Asunto. Cada uno verde/amarillo/rojo. Regla de decisión: **cualquier rojo no se envía** — rehacer antes. Amarillos se mejoran si hay tiempo, no bloquean.

**Síntesis:** no te llevás plantillas para copiar. Te llevás criterio para evaluar cualquier copy que te muestren y para reaccionar cuando lo que ayer funcionaba hoy deja de funcionar.

**Fuentes:** Cialdini (2021, 2016). Heath & Heath (2007). Carnegie (1936). Bertuzzi (2016). Instantly (2026). Bridge Group (2023). Iyengar & Lepper (2000)."""


AVATAR_SCRIPT_ES = """Arrancamos el Módulo 3 — La conexión. Esta semana, la pregunta central: ¿cómo escribo un mensaje que alguien que no me conoce decida leer y responder?

Antes del contenido, un dato incómodo: el cincuenta y ocho por ciento de las respuestas en cold email llegan al primer email. Si tu primero no funciona, más de la mitad del funnel se rompe desde el arranque. No hay follow-up que arregle eso.

Lo más importante de la semana es esto: no vas a aprender la plantilla que funciona. Vas a aprender por qué el cold email funciona cuando funciona.

Tenés tres a siete segundos. No treinta. No "cuando tenga tiempo". Tres a siete segundos. En esos segundos, tu email tiene que hacer una sola cosa — que el lector piense "esto parece específico para mí, vale los treinta segundos de leer bien".

Los ocho bloques de la semana: los siete principios de persuasión de Cialdini aplicados a cold email; las cuatro reglas de escribir para alguien que no te quiere leer; las cuatro partes del mensaje outbound; el pecado capital del SDR nuevo, que es hablar del remitente; cómo construir ganchos desde señales reales; la diferencia entre escribirle al decisor y al referidor; tono y registro específicos para LATAM; y un grid de seis criterios para evaluar cualquier copy sin depender de "me gusta o no me gusta".

Una regla práctica para llevarte ya: la regla del tachar-y-contar. Antes de mandar un email, tachá todas las menciones a vos, a tu empresa, a tu producto. Mirá lo que queda. Si queda casi nada — tu email era autopresentación disfrazada de cold email. No se corrige editando; se reescribe desde el lector.

Al final, cuatro micro-pruebas. La cuarta integra todo con el grid de evaluación. Vamos."""


PRESENTATION_BLOCKS_ES = [
    {
        "title": "Los 7 principios de Cialdini en cold email",
        "bullets": [
            "Reciprocidad — dar antes de pedir (observación útil, no 'llamada gratis')",
            "Compromiso — CTA pequeño primero, no '30 min' de entrada",
            "Prueba social — relevante por segmento, no por tamaño",
            "Autoridad — observación específica > títulos",
            "Simpatía — tono humano, no plantilla corporativa",
            "Escasez — real (regulación, fecha), no artificial",
            "Unidad — misma tribu del lector, no corporación gringa",
        ],
        "source": "Cialdini 2021, Influence",
    },
    {
        "title": "Las 4 reglas de escritura en frío",
        "bullets": [
            "Brevedad: <80 palabras (Instantly 2026)",
            "Claridad: 1 idea por mensaje",
            "Especificidad: hechos verificables, no vaguedades",
            "1 solo CTA (parálisis por exceso, Iyengar & Lepper 2000)",
            "Recortá, no resumas",
        ],
        "source": "Instantly 2026 + Heath & Heath 2007",
    },
    {
        "title": "Anatomía del mensaje — 4 partes",
        "bullets": [
            "Asunto: 3-7 palabras, específico, sin palabras-trigger",
            "Apertura: 2 líneas sobre el LECTOR, no sobre vos",
            "Gancho: [señal] + [consecuencia o desafío típico], sin prometer",
            "CTA: pregunta pequeña o acción concreta con opción acotada",
        ],
        "source": "Bertuzzi 2016 + Braun Bad-Ass B2B Growth",
    },
    {
        "title": "El pecado capital + regla del tachar-y-contar",
        "bullets": [
            "Pecado: hablar del remitente en vez del prospecto",
            "Test: tachá menciones a vos/tu empresa, mirá lo que queda",
            "Si queda nada → no se edita, se REESCRIBE desde el lector",
            "Carnegie 1936: 'hablale de él mismo y te escuchará por horas'",
        ],
        "source": "Carnegie 1936 + Bloque 4",
    },
    {
        "title": "Construir ganchos desde señales reales",
        "bullets": [
            "Sin gancho: 0.5-1%. Con gancho específico: 2-4%",
            "Señal = hecho verificable, específico, reciente",
            "Buenas: expansión, contratación masiva, ronda Series B+, regulación, M&A",
            "Malas: 'está creciendo', halagos genéricos, proyecciones",
            "15 min de research antes de cada email — si no hay señal, no escribís",
        ],
        "source": "Bloque 5 + Bridge Group SDR Metrics",
    },
    {
        "title": "Decisor (KDM) vs Referidor — 2 mensajes distintos",
        "bullets": [
            "AL KDM: abrir conversación sobre su desafío. Tono directo. CTA = reunión.",
            "AL REFERIDOR: NO vender. Pedir orientación. Tono humilde. CTA = indicar a la persona correcta.",
            "Confundirlos = 0.2% en vez de 1% de conversión",
        ],
        "source": "Bertuzzi 2016",
    },
    {
        "title": "Tono y registro LATAM B2B",
        "bullets": [
            "Bibliografía anglosajona NO aplica tal cual",
            "1 grado más formal que el estándar US",
            "1 línea de cortesía OK ('quedo atento')",
            "Humor genuino diferencia; humor forzado quema",
            "'tú' = default seguro en lista mixta",
        ],
        "source": "Operativa Siete + ajuste cultural",
    },
    {
        "title": "Grid de 6 criterios — evaluación objetiva",
        "bullets": [
            "1. Especificidad del gancho",
            "2. Foco en el lector (no remitente)",
            "3. Longitud (<80 palabras)",
            "4. Un solo CTA",
            "5. Tono y registro",
            "6. Asunto",
            "Regla: cualquier ROJO no se envía. Amarillos no bloquean.",
        ],
        "source": "Síntesis + Heath & Heath 2007",
    },
]


MCQ_QUESTIONS = [
    {
        "id": "q1",
        "block": 4,
        "type": "single",
        "prompt": (
            "Cold email a Lava Fresh (lavandería industrial de 30 empleados): 'Estimado Sr. Ramírez, "
            "mi nombre es Pablo Rodríguez y soy ejecutivo comercial senior en SoluTech. Somos una "
            "empresa con más de 15 años ayudando a compañías como la suya a optimizar sus procesos "
            "comerciales. Trabajamos con Walmart, Falabella y Cencosud automatizando prospección "
            "outbound con un approach que combina IA y SDRs especializados. Me encantaría coordinar "
            "una reunión de 45 minutos para presentarle nuestra propuesta. Quedo atento.' "
            "¿Cuál es el problema MÁS GRAVE de este copy?"
        ),
        "choices": [
            {
                "id": "a",
                "text": "El CTA pide 45 minutos, demasiado tiempo para un cold email.",
            },
            {
                "id": "b",
                "text": (
                    "Menciona Walmart, Falabella y Cencosud — empresas gigantes — cuando Lava "
                    "Fresh es lavandería industrial de 30 empleados. Activa distancia, no prueba "
                    "social."
                ),
            },
            {
                "id": "c",
                "text": (
                    "Todo el copy habla del remitente (SoluTech, sus 15 años, sus clientes) y no "
                    "hay una sola referencia al lector ni a su contexto. Pecado capital."
                ),
            },
            {
                "id": "d",
                "text": "El asunto 'Propuesta de servicios para Lava Fresh' es genérico.",
            },
        ],
        "correct": ["c"],
        "explanation": (
            "Los 4 problemas son reales, pero el pecado capital INVALIDA el resto. Si corregís a, "
            "b o d sin corregir c, el email sigue sin funcionar. Si corregís c (reescribir desde "
            "la perspectiva del lector con un gancho específico sobre Lava Fresh), podría "
            "funcionar incluso manteniendo algunos otros errores. Esta pregunta exige jerarquizar, "
            "no identificar."
        ),
    },
    {
        "id": "q2",
        "block": 2,
        "type": "multi",
        "prompt": (
            "Cold email a evaluar: 'Asunto: 15 tiendas nuevas en el último trimestre. Hola Diego, "
            "vi que abrieron 15 tiendas nuevas este trimestre en Perú y Ecuador. En expansión "
            "regional a ese ritmo, el cuello de botella más caro que vemos es la predicción de "
            "demanda por local — lo que funciona en San Isidro no funciona en Machala. En empresas "
            "similares ayudamos a reducir overstock y mejorar márgenes en los primeros 6 meses de "
            "expansión. ¿Querés que te cuente cómo lo hicimos con [empresa]? También podemos "
            "agendar 30 min si preferís verlo en detalle. O mandame tu WhatsApp y te paso un caso "
            "escrito. Como referencia, nuestros clientes incluyen empresas top del retail. "
            "Saludos, Ana.' Marcá TODOS los problemas de forma que tiene:"
        ),
        "choices": [
            {"id": "1", "text": "La longitud supera las 80 palabras recomendadas (~110)"},
            {
                "id": "2",
                "text": (
                    "Tiene más de un CTA (ofrece 3 opciones: contar el caso, agendar 30 min, "
                    "mandar WhatsApp)"
                ),
            },
            {"id": "3", "text": "La apertura habla del remitente en vez del lector"},
            {
                "id": "4",
                "text": (
                    "El cierre 'nuestros clientes incluyen empresas top del retail' es prueba "
                    "social genérica que debilita el copy"
                ),
            },
            {"id": "5", "text": "El asunto es demasiado largo"},
            {"id": "6", "text": "No menciona ninguna señal específica del prospecto"},
        ],
        "correct": ["1", "2", "4"],
        "explanation": (
            "Correcto 1, 2, 4. La 1: ~110 palabras > 80 (zona amarilla). La 2: 3 CTAs activan "
            "parálisis (Iyengar & Lepper 2000). La 4: prueba social sin especificidad activa "
            "sospecha (Cialdini 2021). NO son correctas: 3 (la apertura habla del LECTOR desde "
            "la primera línea — 'vi que abrieron 15 tiendas'); 5 (8 palabras, dentro del rango "
            "3-7 con margen por alta especificidad); 6 (la señal 15 tiendas en Perú y Ecuador es "
            "exactamente lo que el Bloque 5 define como gancho bueno)."
        ),
    },
    {
        "id": "q3",
        "block": 5,
        "type": "match",
        "prompt": (
            "Emparejá cada apertura de cold email con su clasificación correcta según los "
            "principios del módulo:"
        ),
        "left": [
            {
                "id": "1",
                "text": "'Hola Diego, vi que Globant abrió oficina en Bogotá el mes pasado...'",
            },
            {
                "id": "2",
                "text": (
                    "'Estimado Sr. Ramírez, mi nombre es Pablo y soy ejecutivo en SoluTech...'"
                ),
            },
            {
                "id": "3",
                "text": (
                    "'Hola Carlos, tu empresa está creciendo rápido y pensé que te interesaría...'"
                ),
            },
            {
                "id": "4",
                "text": (
                    "'Hola Ana, estoy tratando de ubicar a la persona que lidera el área de "
                    "operaciones. ¿Te molesta si me indicás con quién tendría sentido conversar?'"
                ),
            },
        ],
        "right": [
            {"id": "A", "text": "Pecado capital: foco en remitente"},
            {"id": "B", "text": "Gancho genérico (señal no verificable)"},
            {"id": "C", "text": "Mensaje a referidor (pide orientación, no vende)"},
            {"id": "D", "text": "Gancho específico (señal verificable)"},
        ],
        "correct": {"1": "D", "2": "A", "3": "B", "4": "C"},
        "explanation": (
            "1 → D: 'Globant abrió oficina en Bogotá el mes pasado' es señal verificable, "
            "específica y reciente. 2 → A: empieza 'mi nombre es X y soy Y en Z' — pecado "
            "capital. 3 → B: 'creciendo rápido' aplica a cualquier empresa, no es verificable. "
            "4 → C: tono humilde, pide orientación, no asume que es el decisor. Confundir D con "
            "B es el error central que no internaliza la diferencia entre señal verificable y "
            "afirmación genérica."
        ),
    },
    {
        "id": "q4",
        "block": 8,
        "type": "single",
        "prompt": (
            "Aplicá el grid de 6 criterios a este email: 'Asunto: ¿Expansión a Colombia = pipeline "
            "local? Hola Juan, vi que Ualá anunció la apertura de operación en Colombia para Q3 "
            "2026. En expansión regional vemos que el cuello de botella más caro suele ser armar "
            "pipeline local antes de que el ramp-up de SDRs nuevos esté listo — quedan 4-6 meses "
            "con el equipo original corriendo doble. ¿Les está pasando algo así, o ya tienen el "
            "plan de transición cubierto? Quedo atento. Martina'. ¿Cuál veredicto es correcto?"
        ),
        "choices": [
            {"id": "a", "text": "6 verdes — copy modelo, se envía tal cual."},
            {
                "id": "b",
                "text": "5 verdes + 1 amarillo en LONGITUD — se envía, el amarillo es aceptable.",
            },
            {
                "id": "c",
                "text": "5 verdes + 1 amarillo en ASUNTO — se envía, el amarillo es aceptable.",
            },
            {
                "id": "d",
                "text": (
                    "4 verdes + 2 amarillos — se envía pero se recomienda mejorar antes de la "
                    "próxima ronda."
                ),
            },
            {"id": "e", "text": "1 rojo — no se envía, hay que rehacerlo."},
        ],
        "correct": ["c"],
        "explanation": (
            "Gancho (Ualá + Colombia + Q3 2026): verde. Foco en lector (todo el cuerpo habla del "
            "prospecto): verde. Longitud (~70 palabras < 80): verde. Un solo CTA (pregunta "
            "sí/no): verde. Tono (natural, sin corporativismo): verde. Asunto ('¿Expansión a "
            "Colombia = pipeline local?' es específico y corto pero el '=' lee como social media "
            "más que email profesional): AMARILLO. Veredicto: enviable con ajuste menor del "
            "asunto. Regla: cualquier rojo bloquea; solo amarillos no."
        ),
    },
]


RESOURCES = [
    {
        "kind": "pdf",
        "title": "Handout — Escritura persuasiva en frío (Semana 5)",
        "url": "https://drive.google.com/file/d/PLACEHOLDER_W5_HANDOUT",
        "order_index": 0,
    },
    {
        "kind": "link",
        "title": "Cialdini — Los 7 principios de persuasión (resumen)",
        "url": "https://www.influenceatwork.com/principles-of-persuasion/",
        "order_index": 1,
    },
    {
        "kind": "link",
        "title": "Instantly — Cold Email Benchmark Report 2026",
        "url": "https://instantly.ai/blog/cold-email-benchmarks",
        "order_index": 2,
    },
    {
        "kind": "link",
        "title": "Bad-Ass B2B Growth (Josh Braun) — newsletter de referencia",
        "url": "https://joshbraun.substack.com/",
        "order_index": 3,
    },
    {
        "kind": "doc",
        "title": "Plantilla — Grid de 6 criterios para evaluar copy",
        "url": "https://docs.google.com/spreadsheets/d/PLACEHOLDER_W5_GRID",
        "order_index": 4,
    },
    {
        "kind": "doc",
        "title": "Plantilla — Estructura de cold email outbound (4 partes)",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W5_TEMPLATE",
        "order_index": 5,
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
    module = Module(course_id=course.id, slug=MODULE_SLUG, order_index=2)
    module.translations.append(
        ModuleTranslation(
            locale="es",
            title="Módulo 3 — La conexión",
            summary="Escritura persuasiva en frío y conversación con el prospecto.",
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
                title="Semana 5 — Escritura persuasiva en frío",
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
        tr_es.title = "Semana 5 — Escritura persuasiva en frío"
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
            title="Micro-pruebas — Semana 5",
            config=config,
            passing_score=65.0,
        )
        db.add(a)
        db.commit()
        db.refresh(a)
        log.info("assessment.seeded", extra={"assessment_id": a.id})
        return a
    existing.title = "Micro-pruebas — Semana 5"
    existing.config = config
    existing.passing_score = 65.0
    db.commit()
    return existing


def run() -> None:
    Base.metadata.create_all(engine)
    db = SessionLocal()
    try:
        course = _upsert_course(db)
        module = _upsert_module(db, course)
        lesson = _upsert_lesson(db, module)
        _upsert_resources(db, module, lesson)
        _upsert_assessment(db, module, lesson)
        log.info(
            "seed_w5.done",
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
