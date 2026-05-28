"""Seed: Semana 6 del Módulo 3 (Conversación, calificación y mensajería asíncrona).

Cierra el Módulo 3 — "La conexión". Contenido extraído de
SDR_Academy_Siete_Documento_Maestro.md (bloques 1-7 de Semana 6 + 4 micro-pruebas
MCQ Capa 1).

Reutiliza el módulo `m3-la-conexion` (order_index=2, creado por seed_w5) y agrega
la segunda lección (order_index=1) con la secuencia dinámica completa.

Uso:
    cd backend && .venv/bin/python -m app.scripts.seed_w6
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
log = get_logger("seed_w6")


COURSE_SLUG = "sdr-academy-v1"
MODULE_SLUG = "m3-la-conexion"
LESSON_ORDER_INDEX = 1


LESSON_BODY_ES = """Pregunta central de la semana: ¿Cómo converso en frío para generar interés real y distinguir al que califica del que no?

**Dato crudo:** la cold call promedio dura 82 segundos y el connect rate promedio es ~5% (Cognism 2025-26). El SDR que más habla en la apertura pierde — y la mayoría de los SDRs hablan demasiado.

## Bloque 1 — Por qué una cold call funciona cuando funciona
La sincronía. El canal sincrónico te da tres cosas que el asíncrono no puede: lectura de tono en tiempo real, resolución de objeciones inmediata, compromiso verbal del prospecto. No es "más eficiente" — es **cualitativamente distinto**. Si tu llamada termina sin ninguna de esas tres, podrías haber mandado un email y ahorrarte el tiempo.

## Bloque 2 — Anatomía de la apertura: permission-based opener
5 partes en este orden: **permiso** ("¿Te tomo 30 segundos?") + **contexto** (de dónde sale tu llamada) + **razón concreta** (gancho específico, no genérico) + **una pregunta abierta** + **silencio**. El SDR que más habla en la apertura, pierde. Braun (2020-26): el patrón pattern-interrupt funciona cuando el prospecto siente que controla el inicio.

## Bloque 3 — Escucha activa: el que más habla pierde, el que mejor pregunta gana
Cuatro técnicas de Voss (Never Split the Difference 2016): **mirroring** (espejo de las últimas 2-3 palabras como pregunta suave), **labeling** (etiquetar la emoción sin juzgar — "parece que…"), **tactical empathy** (validar la situación antes de pedir nada), **silencio estratégico** (4 segundos después de una pregunta importante, no rellenar). Mirroring devuelve palabras del prospecto sin interpretar; labeling nombra suavemente la emoción subyacente. Son distintas. Confundirlas es no entender Voss.

## Bloque 4 — Objeciones vs rechazos
Una **objeción** es información útil (revela fit, contexto, prioridad). Un **rechazo** es un cierre. Las objeciones universales: "no tengo tiempo", "no me interesa", "ya trabajamos con otro", "mándame info" — cada una tiene una verdad subyacente distinta. Protocolo: **reconocer → reformular → reconducir**. Nunca atropellar, nunca pelearse con el prospecto. "Estamos cómodos con nuestro proveedor" es objeción, no rechazo. "No vuelvas a llamar" es rechazo. Confundirlos quema pipeline que después no vuelve.

## Bloque 5 — Calificación en outbound: por qué NO aplica BANT
**BANT** (Budget / Authority / Need / Timing) supone una decisión ya tomada. El comprador frío no tiene presupuesto asignado, no se evaluó autoridad, la necesidad no está explícita, el timing no está definido. Preguntar BANT en frío es exigir al prospecto que haga el trabajo del SDR. El framework correcto en outbound es **Situación → Necesidad → Timing** (derivado de SPIN, Rackham 1988): qué hay hoy → qué duele de eso → si lo abordaran, cuándo. Tratalo como framework de pensamiento, no como guion a memorizar.

## Bloque 6 — Mensajería asíncrona: WhatsApp, LinkedIn y la lógica del goteo
En LATAM B2B WhatsApp pesa fuerte. Pero los canales asíncronos tienen un **contrato implícito** distinto: no hay expectativa de respuesta inmediata, el goteo se percibe como natural, el exceso se lee como spam. Lógica del goteo: **una pregunta por mensaje**, esperar la respuesta antes de mandar la siguiente. Si el prospecto responde corto, respondés corto — reflejá su registro. WhatsApp funciona cuando tenés el número legítimamente y no lo usás para contenido masivo. LinkedIn es canal de research y micro-touch, no de venta de alto volumen. Romper el contrato implícito = bloqueo en segundos.

## Bloque 7 — Vender la conversación, no el producto + precalificación
El CTA de un cold email/call no es "compra". Es **abrir una conversación**. Confundirlo es vender antes de calificar, y eso quema fit-checks que después no podés rehacer. La **precalificación pre-reunión** (10-15 min antes del meeting con el AE) es un **filtro de mínimos**, no un interrogatorio de máximos. Tres preguntas bien hechas valen más que diez mal hechas: situación → necesidad → timing condicional.

**Síntesis:** la cold call no es un performance — es una conversación honesta de 2 minutos donde el prospecto debe sentir que controla el ritmo. Si te quedaste con "qué decir cuando me dicen X", no entendiste la semana. Te tenés que quedar con cómo escuchar.

**Fuentes:** Rackham (1988). Voss & Raz (2016). Blount (2015, 2020). Bertuzzi (2016). Braun (2020-26). Cognism (2025-26)."""


AVATAR_SCRIPT_ES = """Semana 6, cierre del Módulo 3 — La conexión. La pregunta central: ¿cómo converso en frío para generar interés real y distinguir al que califica del que no?

Un dato incómodo antes de empezar: la cold call promedio dura ochenta y dos segundos. Connect rate, cinco por ciento. Los top performers llegan a diez, trece. La diferencia entre ese cinco y ese trece no está en lo que dicen — está en cómo escuchan.

Lo más importante de la semana: el SDR que más habla, pierde. Sin excepciones. La cold call no es tu turno de hablar; es tu turno de hacer una pregunta y callarte cuatro segundos.

Siete bloques. Primero, por qué la llamada existe — qué te da la sincronía que el email no te puede dar. Segundo, la apertura: permiso, contexto, razón, pregunta, silencio — en ese orden. Tercero, escucha activa con las cuatro técnicas de Chris Voss: mirroring, labeling, tactical empathy y silencio estratégico. Cuarto, la distinción crítica entre objeción y rechazo — confundirlas quema pipeline. Quinto, por qué BANT no aplica en outbound y qué framework sí: situación, necesidad, timing. Sexto, mensajería asíncrona — WhatsApp y LinkedIn — y la lógica del goteo: una pregunta por mensaje, esperás respuesta, después seguís. Séptimo, vendés la conversación, no el producto, y la precalificación es filtro de mínimos.

Una regla que te llevás ya: cuando alguien te dice "estamos cómodos con nuestro proveedor", eso no es rechazo. Es información. Es objeción. Reconocés, reformulás, reconducís — y preguntás qué tendría que pasar para que reconsideraran. Si te dan un escenario concreto, archivás con fecha. Si te dicen "nada", ahí sí cerrás educado.

Cuatro micro-pruebas al final. La cuarta integra todo con un caso de WhatsApp mal mandado. Vamos."""


PRESENTATION_BLOCKS_ES = [
    {
        "title": "Por qué la cold call: lo que la sincronía da",
        "bullets": [
            "Lectura de tono en tiempo real",
            "Resolución de objeciones en el momento",
            "Compromiso verbal del prospecto",
            "Si la llamada no te dio ninguna de las 3, era un email",
            "Cold call promedio: 82 seg. Connect rate: ~5%. Top: 10-13% (Cognism)",
        ],
        "source": "Blount 2015 + Cognism 2025-26",
    },
    {
        "title": "Anatomía de la apertura — permission-based opener",
        "bullets": [
            "1. Permiso ('¿te tomo 30 segundos?')",
            "2. Contexto (de dónde sale tu llamada)",
            "3. Razón concreta (gancho específico, no genérico)",
            "4. Una pregunta abierta",
            "5. Silencio (4 segundos, no rellenar)",
            "El SDR que más habla en la apertura, pierde",
        ],
        "source": "Braun 2020-26 + Blount 2015",
    },
    {
        "title": "Escucha activa — las 4 técnicas de Voss",
        "bullets": [
            "Mirroring: espejo de las últimas 2-3 palabras como pregunta suave",
            "Labeling: nombrar la emoción sin juzgar ('parece que…')",
            "Tactical empathy: validar situación antes de pedir nada",
            "Silencio estratégico: 4 seg después de pregunta importante",
            "Mirroring NO interpreta; labeling interpreta suavemente — son distintas",
        ],
        "source": "Voss & Raz 2016, Never Split the Difference",
    },
    {
        "title": "Objeciones vs rechazos — protocolo",
        "bullets": [
            "Objeción = información útil (fit, contexto, prioridad)",
            "Rechazo = cierre",
            "Universales: 'no tengo tiempo', 'no me interesa', 'ya trabajamos con otro', 'mandame info'",
            "Protocolo: reconocer → reformular → reconducir",
            "'Estamos cómodos con nuestro proveedor' = objeción, NO rechazo",
            "Nunca atropellar, nunca pelearse",
        ],
        "source": "Blount 2015 + Bertuzzi 2016",
    },
    {
        "title": "Calificación outbound — por qué BANT NO aplica",
        "bullets": [
            "BANT supone decisión ya tomada — el frío no la tiene",
            "Preguntar Budget/Authority/Timing duro = exigir al prospecto que haga tu trabajo",
            "Framework correcto: Situación → Necesidad → Timing",
            "S: qué hay hoy / N: qué duele de eso / T: si lo abordaran, cuándo",
            "Framework de pensamiento, NO guion a memorizar",
        ],
        "source": "Rackham 1988 (SPIN) + Bertuzzi 2016",
    },
    {
        "title": "Mensajería asíncrona — lógica del goteo",
        "bullets": [
            "Contrato implícito: sin expectativa de respuesta inmediata",
            "Una pregunta por mensaje. Esperás respuesta. Después seguís.",
            "Reflejá registro del prospecto (corto si corto)",
            "WhatsApp solo si tenés el número legítimamente",
            "LinkedIn = research + micro-touch, NO venta de alto volumen",
            "Romper el contrato = bloqueo en segundos",
        ],
        "source": "Blount 2020 Virtual Selling + Operativa LATAM",
    },
    {
        "title": "Vender la conversación + precalificación",
        "bullets": [
            "CTA = abrir conversación, NO 'compra'",
            "Confundirlo = vender antes de calificar = quema fit-check",
            "Precalificación: 10-15 min antes del meeting con AE",
            "Filtro de MÍNIMOS, NO interrogatorio de máximos",
            "3 preguntas bien > 10 mal: situación → necesidad → timing condicional",
        ],
        "source": "Bertuzzi 2016",
    },
]


MCQ_QUESTIONS = [
    {
        "id": "q1",
        "block": 4,
        "type": "single",
        "prompt": (
            "Un SDR acaba de terminar el permission-based opener y el contexto de su cold call. "
            "El prospecto responde: 'Mirá, el tema es que nosotros ya tenemos un proveedor con el "
            "que venimos trabajando hace 2 años. Estamos cómodos y por ahora no estamos pensando "
            "en cambiar.' ¿Qué debe hacer el SDR?"
        ),
        "choices": [
            {
                "id": "a",
                "text": (
                    "Aceptar el rechazo y cortar con amabilidad — el prospecto fue claro, "
                    "insistir daña la relación."
                ),
            },
            {
                "id": "b",
                "text": (
                    "Reformular y preguntar '¿qué tendría que pasar en tu empresa para que "
                    "consideraran revisar alternativas?' antes de cerrar."
                ),
            },
            {
                "id": "c",
                "text": (
                    "Responder que probablemente su proveedor actual no les está entregando "
                    "todo y pedir 20 min para mostrarle un comparativo."
                ),
            },
            {
                "id": "d",
                "text": (
                    "Enviar inmediatamente un caso de éxito con una empresa similar para probar "
                    "que sí vale la pena cambiar."
                ),
            },
        ],
        "correct": ["b"],
        "explanation": (
            "'Estamos cómodos con nuestro proveedor' es OBJECIÓN, no rechazo. Es información útil "
            "(hay proveedor, relación 2 años, 'cómodos' = satisfacción moderada, no entusiasmo). "
            "Protocolo reconocer/reformular/reconducir aplica. La pregunta '¿qué tendría que "
            "pasar?' es neutra y te da diagnóstico: si dan un escenario concreto, tenés trigger "
            "para archivar con fecha. Si dicen 'nada, estamos cerrados', ahí sí es rechazo y "
            "cerrás educado. (a) cierra prematuro un prospecto que en 6 meses puede estar listo. "
            "(c) atropella y genera defensa automática. (d) viola el contrato asíncrono y el "
            "material no pedido no se lee."
        ),
    },
    {
        "id": "q2",
        "block": 5,
        "type": "multi",
        "prompt": (
            "Un SDR tiene agendada una precalificación de 10-15 min con un Gerente de Marketing "
            "(empresa B2B 200 empleados, Serie B reciente), 2 días antes del meeting con el AE. "
            "Marcá TODAS las preguntas que NO deberías usar (porque pertenecen a BANT y rompen el "
            "formato outbound):"
        ),
        "choices": [
            {
                "id": "1",
                "text": "'¿Cómo están manejando hoy el tema de generación de leads B2B?'",
            },
            {
                "id": "2",
                "text": (
                    "'¿Cuál es el presupuesto anual que tienen asignado para prospección y "
                    "generación de demanda?'"
                ),
            },
            {
                "id": "3",
                "text": (
                    "'¿Hay algo de ese proceso que sientan que no les está rindiendo como "
                    "esperaban?'"
                ),
            },
            {
                "id": "4",
                "text": (
                    "'¿Quién más participaría de la evaluación si decidieran trabajar con un "
                    "proveedor externo?'"
                ),
            },
            {
                "id": "5",
                "text": (
                    "'Si decidieran abordar esto, ¿estarían viéndolo este trimestre o más para "
                    "el próximo año?'"
                ),
            },
            {
                "id": "6",
                "text": (
                    "'¿Cuándo van a tomar la decisión final? ¿Hay un timeline específico de "
                    "compra?'"
                ),
            },
            {
                "id": "7",
                "text": "'¿Qué están usando hoy o es algo que todavía no tienen armado?'",
            },
        ],
        "correct": ["2", "4", "6"],
        "explanation": (
            "Correctas 2, 4, 6. La 2 es BANT-Budget: asume decisión tomada al preguntar "
            "presupuesto en frío. La 4 es BANT-Authority disfrazada: mapear decisor antes de "
            "validar necesidad; la versión S es lateral ('¿este tipo de decisiones pasan por tu "
            "área?'). La 6 es BANT-Timing agresivo: '¿cuándo van a decidir?' asume decisión; la "
            "versión condicional es la 5. Las apropiadas: 1 (Situación pura), 3 (Necesidad sin "
            "presionar — se puede responder 'no, todo bien'), 5 (Timing condicional), 7 "
            "(Situación exploratoria)."
        ),
    },
    {
        "id": "q3",
        "block": 3,
        "type": "match",
        "prompt": (
            "Durante una cold call, el prospecto dice lo siguiente en distintos momentos. "
            "Emparejá cada respuesta del SDR con la técnica de escucha activa que está usando:"
        ),
        "left": [
            {
                "id": "1",
                "text": (
                    "(Prospecto: 'La verdad es que estamos en medio de un rediseño "
                    "organizacional.') → SDR: '¿Rediseño organizacional…?'"
                ),
            },
            {
                "id": "2",
                "text": (
                    "(Prospecto: 'Hace 6 meses probamos una herramienta parecida y fue un "
                    "desastre.') → SDR: 'Parece que quedó un mal sabor con ese tema.'"
                ),
            },
            {
                "id": "3",
                "text": (
                    "(Prospecto: 'Si te soy honesta, estoy tapada con 3 proyectos grandes.') → "
                    "SDR: 'Totalmente entiendo. Estar tapada con 3 proyectos simultáneos es "
                    "complicado — probablemente no es el momento ideal para sumar otro frente.'"
                ),
            },
            {
                "id": "4",
                "text": "(SDR, después de hacer una pregunta importante:) [silencio, 4 seg]",
            },
        ],
        "right": [
            {"id": "A", "text": "Mirroring (espejo)"},
            {"id": "B", "text": "Labeling (etiquetar emoción)"},
            {"id": "C", "text": "Tactical empathy (empatía táctica)"},
            {"id": "D", "text": "Silencio estratégico"},
        ],
        "correct": {"1": "A", "2": "B", "3": "C", "4": "D"},
        "explanation": (
            "1 → A: mirroring repite las últimas 2-3 palabras del prospecto como pregunta suave, "
            "sin interpretar. 2 → B: labeling nombra la emoción/estado ('parece que quedó un mal "
            "sabor') interpretando suavemente. 3 → C: tactical empathy valida la situación antes "
            "de pedir nada — reconocés y validás el estado. 4 → D: después de una pregunta "
            "importante, no rellenar — dejar que el prospecto procese. Confundir mirroring con "
            "labeling es no entender que mirroring devuelve palabras (no interpreta) y labeling "
            "nombra emoción (interpreta suave). Ambas son de Voss pero operan distinto."
        ),
    },
    {
        "id": "q4",
        "block": 6,
        "type": "single",
        "prompt": (
            "Un SDR le manda a Carolina (CFO de fintech con Serie B reciente) por WhatsApp: "
            "(msg 1) 'Hola Carolina, cómo estás?' (msg 2, 30 seg después) 'Soy Diego, te escribí "
            "por LinkedIn la semana pasada pero creo que no viste.' (msg 3, 1 min después) "
            "'Felicitaciones por la Serie B! Me encantaría contarte sobre una plataforma que "
            "ayuda a startups post-Serie B a consolidar reportes, reducir el cierre de mes 60% y "
            "detectar errores. Tenemos casos con [3 empresas desconocidas].' (msg 4, 30 seg "
            "después) '¿Tenés unos minutos esta semana? También te mando un PDF. ¿Martes o "
            "jueves?' ¿Cuál es el ERROR PRINCIPAL?"
        ),
        "choices": [
            {
                "id": "a",
                "text": (
                    "No consiguió el número de Carolina por un canal legítimo — no hay evidencia "
                    "de que se lo haya dado."
                ),
            },
            {
                "id": "b",
                "text": (
                    "Rompe la lógica del goteo: 4 mensajes en menos de 2 minutos con pitch "
                    "completo, múltiples CTAs y un PDF prometido. Violación directa del "
                    "contrato implícito del canal asíncrono."
                ),
            },
            {
                "id": "c",
                "text": (
                    "Usa emoji en un mensaje B2B, lo cual baja la credibilidad profesional."
                ),
            },
            {
                "id": "d",
                "text": (
                    "Menciona Serie B pero no tiene un gancho específico sobre el negocio de "
                    "Carolina — 'felicitaciones' es genérico."
                ),
            },
        ],
        "correct": ["b"],
        "explanation": (
            "Diego usó WhatsApp como si fuera una landing page — tiró todo el pitch de una, con "
            "múltiples CTAs y PDF prometido. Violó el contrato implícito del canal asíncrono "
            "(una pregunta por mensaje, esperar respuesta). El patrón '4 mensajes seguidos con "
            "pitch completo' es idéntico al patrón de spam masivo: Carolina probablemente "
            "bloquea el número en segundos. Una vez bloqueada, nunca más accedés; y si lo "
            "reporta, afecta tu número entero. (a) es problema serio pero incluso con número "
            "legítimo el patrón b destruiría la conversación. (c) detalle de forma, no "
            "estructural — un emoji no bloquea canal. (d) cierto, pero mejorar el gancho no "
            "arregla los 4 mensajes seguidos. Si hubiera mandado UN solo mensaje corto y "
            "esperado 2-3 días, había chance. El exceso, no el contenido, lo mató."
        ),
    },
]


RESOURCES = [
    {
        "kind": "pdf",
        "title": "Handout — Conversación, calificación y mensajería asíncrona (Semana 6)",
        "url": "https://drive.google.com/file/d/PLACEHOLDER_W6_HANDOUT",
        "order_index": 0,
    },
    {
        "kind": "doc",
        "title": "Plantilla — Permission-based opener (5 partes)",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W6_OPENER",
        "order_index": 1,
    },
    {
        "kind": "doc",
        "title": "Plantilla — Protocolo reconocer/reformular/reconducir (objeciones universales)",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W6_OBJ_PROTOCOL",
        "order_index": 2,
    },
    {
        "kind": "doc",
        "title": "Plantilla — Guion de precalificación (Situación → Necesidad → Timing)",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W6_SNT",
        "order_index": 3,
    },
    {
        "kind": "link",
        "title": "Voss — Never Split the Difference (resumen mirroring/labeling/tactical empathy)",
        "url": "https://www.blackswanltd.com/the-edge/topics/negotiation-tactics",
        "order_index": 4,
    },
    {
        "kind": "link",
        "title": "Cognism — State of Cold Calling 2025/26 (benchmarks)",
        "url": "https://www.cognism.com/cold-calling-statistics",
        "order_index": 5,
    },
    {
        "kind": "link",
        "title": "Josh Braun — Permission-based openers y pattern interrupts",
        "url": "https://joshbraun.substack.com/",
        "order_index": 6,
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
        .filter_by(module_id=module.id, order_index=LESSON_ORDER_INDEX)
        .first()
    )
    if lesson is None:
        lesson = Lesson(
            module_id=module.id,
            order_index=LESSON_ORDER_INDEX,
            kind="video",
            youtube_id=None,
            duration_seconds=1500,
        )
        lesson.translations.append(
            LessonTranslation(
                locale="es",
                title="Semana 6 — Conversación, calificación y mensajería asíncrona",
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
        tr_es.title = "Semana 6 — Conversación, calificación y mensajería asíncrona"
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
            title="Micro-pruebas — Semana 6",
            config=config,
            passing_score=65.0,
        )
        db.add(a)
        db.commit()
        db.refresh(a)
        log.info("assessment.seeded", extra={"assessment_id": a.id})
        return a
    existing.title = "Micro-pruebas — Semana 6"
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
            "seed_w6.done",
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
