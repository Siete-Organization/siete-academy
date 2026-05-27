"""Seed: Semana 2 del Módulo 1 (Rol del SDR, hitos, reunión calificada).

Cierra el Módulo 1. Contenido extraído de SDR_Academy_Siete_Documento_Maestro.md
(bloques 1-7 de Semana 2 + 4 micro-pruebas MCQ Capa 1).

Crea la segunda lección del módulo `m1-juego-y-jugador` (order_index=1) con la
secuencia dinámica completa.

Uso:
    cd backend && .venv/bin/python -m app.scripts.seed_w2
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
log = get_logger("seed_w2")


COURSE_SLUG = "sdr-academy-v1"
MODULE_SLUG = "m1-juego-y-jugador"


LESSON_BODY_ES = """Pregunta central de la semana: ¿Qué vende un SDR realmente y hasta dónde llega su responsabilidad?

## Bloque 1 — La arquitectura de la función comercial B2B
4 roles principales: Marketing (genera demanda, métrica MQLs), SDR (prospecta + agenda, métrica reuniones calificadas), AE (cierra deals, métrica revenue), CSM (retiene, métrica net retention). La separación SDR/AE permite escalar (Predictable Revenue, Ross 2011): mezclar prospect + close hace que el pipeline entre en olas.

## Bloque 2 — Los 5 canales de generación de demanda B2B
Inbound (vienen a vos), Outbound (vos contactás en frío), Referidos (10× conversión pero no escalan), ABM (cuentas estratégicas 20-50, hiper-personalizado), Partnerships (apalanca pero lento). El SDR opera principalmente en outbound pero entiende los otros porque se cruzan.

## Bloque 3 — Qué es outbound (y cuándo NO aplica)
Definición: identificar empresas ICP + contactar en frío por múltiples canales + agendar reunión con AE. Funciona si: ICP identificable + ticket que justifica costo + ciclo que soporta el modelo. NO aplica: commodity de bajo ticket, ICP masivo indiferenciado, ventas que dependen 100% de demo visual. Benchmarks realistas: 15 reuniones calificadas/mes, conversión empresa→reunión 1-3%, ramp 3-4 meses.

## Bloque 4 — Venta por hitos: la cadena completa
6 hitos secuenciales: (1) Reunión [SDR], (2) Asistencia + Precalificación [SDR], (3) Demo [AE], (4) Propuesta [AE], (5) Cierre [AE], (6) Renovación [CSM]. El SDR vende SOLO hitos 1 y 2. Cruzar hitos (dar precio, hacer demo, ofrecer descuento) arruina la venta del AE. Regla: redirigir hacia la reunión, no cortar al prospecto.

## Bloque 5 — Reunión calificada: los 4 criterios
Acumulativos: (1) Empresa dentro del ICP (industria + tamaño + geografía + características), (2) Contacto es KDM o champion validado, (3) Asiste a la reunión, (4) Pasa precalificación mínima (problema existe + no hay bloqueador absoluto + timing razonable). Si falta uno, NO califica — la reunión no debió generarse. Métrica del SDR: reuniones calificadas, no agendadas.

## Bloque 6 — El handoff al AE como momento sagrado
Información que pasa: empresa + contacto + señal + contexto del outreach + precalificación (situación/necesidad/timing) + advertencias. NO pasa: especulaciones sin base, info irrelevante, chismes. Cabe en 1 página. Un handoff pobre quema deals que el AE podría haber cerrado.

## Bloque 7 — Mindset del SDR: ejecutor con criterio
El SDR es ejecutor (volumen, disciplina) Y con criterio (cada acción es decisión). NO es: operario, cazador de comisiones, asistente del AE. El path típico: SDR → AE → Senior AE → Sales Manager → Director. Los fundamentos del módulo sirven los próximos 10 años de carrera B2B.

**Fuentes:** Ross & Tyler (2011) Predictable Revenue. Bertuzzi (2016) Sales Development Playbook. Blount (2015) Fanatical Prospecting. Bridge Group (2023). Instantly (2026)."""


AVATAR_SCRIPT_ES = """Bienvenido a la semana 2 del Módulo 1. Esta semana cerramos el módulo.

La pregunta central: ¿qué vende un SDR realmente y hasta dónde llega su responsabilidad?

La respuesta corta: un SDR vende dos cosas, no seis. La reunión y la asistencia precalificada. Punto. Todo lo demás lo vende el AE.

Suena obvio, pero es donde más se rompe el rol. Un SDR con ganas — y con miedo a "perder el deal" — cruza hitos que no le corresponden. Da precio, hace mini-demos por teléfono, ofrece descuentos. Cada vez que hace eso, le quema margen al AE, distorsiona expectativas del prospecto, y a mediano plazo pierde credibilidad interna.

En los siete bloques de esta semana vas a ver: la arquitectura completa de la función comercial B2B, los cinco canales de generación de demanda, qué es outbound específicamente y cuándo no aplica, la cadena de seis hitos del deal, los cuatro criterios de una reunión calificada, el handoff al AE como momento sagrado, y el mindset que separa al SDR bueno del promedio.

Una idea importante para llevarte: agendar diez reuniones basura es peor que agendar cinco calificadas. La métrica que importa no es volumen bruto — es reuniones que cumplen los cuatro criterios. Si no lo cumplen, no las cuentes como ganadas. Eso te protege a vos, al AE, y al cliente.

Al final cuatro micro-pruebas. Si pasás esta semana con criterio, cerrás el Módulo 1 listo para arrancar el Módulo 2: leer el negocio del otro lado."""


PRESENTATION_BLOCKS_ES = [
    {
        "title": "Arquitectura de la función comercial B2B",
        "bullets": [
            "Marketing → MQLs (antes del contacto comercial)",
            "SDR → Reuniones calificadas (prospect → opportunity)",
            "AE → Revenue cerrado (opportunity → customer)",
            "CSM → Net retention (customer → renew/expansion)",
        ],
        "source": "Ross & Tyler 2011, Predictable Revenue",
    },
    {
        "title": "5 canales de demanda B2B",
        "bullets": [
            "Inbound — viene a vos (ya investigó)",
            "Outbound — vos contactás en frío",
            "Referidos — 10× conversión, sin escala",
            "ABM — 20-50 cuentas, hiper-personalizado",
            "Partnerships — apalanca pero lento",
        ],
        "source": "Bertuzzi 2016, Sales Development Playbook",
    },
    {
        "title": "Cuándo outbound funciona",
        "bullets": [
            "ICP identificable y alcanzable",
            "Ticket justifica el costo del SDR",
            "Ciclo soporta múltiples touchpoints",
            "Benchmark: 15 reuniones calificadas/mes, conversión 1-3%, ramp 3-4 meses",
        ],
        "source": "Bridge Group 2023 + Instantly 2026",
    },
    {
        "title": "Los 6 hitos del deal — quién vende qué",
        "bullets": [
            "1. Reunión → SDR",
            "2. Asistencia + Precalificación → SDR",
            "3. Demo → AE",
            "4. Propuesta → AE",
            "5. Cierre → AE",
            "6. Renovación → CSM",
        ],
        "source": "Operativa Siete + Bertuzzi 2016",
    },
    {
        "title": "Reunión calificada — 4 criterios acumulativos",
        "bullets": [
            "ICP (industria + tamaño + geografía + características)",
            "KDM o champion validado con llegada real",
            "Asiste (no manda reemplazo sin perfil)",
            "Pasa precalificación: existe el problema, sin bloqueador, timing razonable",
        ],
        "source": "Operativa Siete + Bertuzzi 2016 (qualified opportunity)",
    },
    {
        "title": "Handoff sagrado — qué pasa al AE",
        "bullets": [
            "Empresa: nombre, industria, tamaño, señal usada",
            "Contacto: rol, responsabilidad, LinkedIn",
            "Contexto del outreach: qué ángulo funcionó",
            "Precalificación: Situación + Necesidad + Timing",
            "Advertencias: bloqueadores, otros stakeholders",
        ],
        "source": "Bertuzzi 2016",
    },
    {
        "title": "Mindset — ejecutor con criterio",
        "bullets": [
            "Ejecutor: volumen, disciplina, consistencia (variable #1)",
            "Con criterio: cada acción exige decisión",
            "Entiende el negocio (M2 entero) y al comprador",
            "NO es operario, NO es cazador de comisiones, NO es asistente del AE",
        ],
        "source": "Bloque 7 — síntesis del módulo",
    },
]


MCQ_QUESTIONS = [
    {
        "id": "q1",
        "block": 4,
        "type": "single",
        "prompt": (
            "Una SDR está en una cold call con Pedro, Director de Operaciones. Pedro dice: "
            "'Me interesa el tema. ¿Cuánto cuesta esto? Solo para tener un rango aproximado "
            "antes de meter al AE.' ¿Cuál es la mejor respuesta de la SDR?"
        ),
        "choices": [
            {
                "id": "a",
                "text": (
                    "'Nuestra licencia cuesta entre USD 1.200 y USD 3.500/mes según volumen. "
                    "Si querés, te paso la tabla de precios por email.'"
                ),
            },
            {
                "id": "b",
                "text": (
                    "'Depende de varios factores de tu caso que Florencia (la AE) va a querer "
                    "entender mejor. La reunión es corta — ahí cuadran ese detalle. "
                    "¿El martes 10am o jueves 3pm?'"
                ),
            },
            {
                "id": "c",
                "text": "'Prefiero no darte un rango porque no tengo autoridad para eso.'",
            },
            {
                "id": "d",
                "text": (
                    "'Nuestro mejor cliente pagó USD 2.000/mes, así que asumí que vos estarías "
                    "en un rango similar.'"
                ),
            },
        ],
        "correct": ["b"],
        "explanation": (
            "El SDR vende 2 hitos (reunión + asistencia/precalificación). Dar precio es hito 4 "
            "(propuesta), del AE. La opción b redirige sin cortar: reconoce el pedido, explica por "
            "qué la AE resuelve esto, y cierra el hito que el SDR sí vende con 2 opciones concretas. "
            "Opción a cruza el hito 4. Opción c es defensiva ('no tengo autoridad' suena a "
            "jerarquía baja). Opción d ancla un precio basado en nada."
        ),
    },
    {
        "id": "q2",
        "block": 5,
        "type": "multi",
        "prompt": (
            "Un SDR reporta 4 reuniones agendadas. Marcá TODAS las que CALIFICAN "
            "(cumplen los 4 criterios: ICP + KDM/champion + asiste + pasa precalificación):"
        ),
        "choices": [
            {
                "id": "A",
                "text": (
                    "Textil Andina (400 empleados, ICP). Gerente de Producción dice: "
                    "'la decisión va por Dirección Comercial, pero yo puedo traer el tema.'"
                ),
            },
            {
                "id": "B",
                "text": (
                    "Frutas del Pacífico (180 empleados, ICP). CEO en precalificación: "
                    "'estamos en pleno proceso de venta de la empresa, cierra en 60 días.'"
                ),
            },
            {
                "id": "C",
                "text": (
                    "SoftBank LATAM (1200 empleados, ICP dice 50-300). VP Ventas llegó, "
                    "interés, conversación fluida."
                ),
            },
            {
                "id": "D",
                "text": (
                    "Café del Centro (25 cafés, ICP). CEO llega, confirma problema de gestión "
                    "de inventario, no hay bloqueadores, timing razonable."
                ),
            },
        ],
        "correct": ["D"],
        "explanation": (
            "Solo D cumple los 4 criterios. A: falla criterio 2 (KDM) — el Gerente de Producción "
            "no decide y el champion no está validado. B: falla criterio 4 (precalificación) — "
            "bloqueador absoluto (empresa en venta). C: falla criterio 1 (ICP) — fuera del rango "
            "de tamaño. Error de novato: contar como calificada toda reunión que ocurra."
        ),
    },
    {
        "id": "q3",
        "block": 6,
        "type": "single",
        "prompt": (
            "Un SDR entrega este handoff: 'Empresa: GreenTech Solutions (SaaS, 450 empleados). "
            "Contacto: Daniela López, VP RRHH, 3 años en cargo. Señal: anunciaron en LinkedIn la "
            "contratación de 60 ingenieros en Q3. Outreach: 2 emails, respondió el 2do. El gancho "
            "fue \"en ramp-ups así el cuello suele ser onboarding\". Precalificación: situación "
            "(onboarding manual y disperso), necesidad (productividad en 2m vs 4m), timing "
            "(presupuesto asignado Q próximo). Advertencia: Director de Ingeniería (Rafael Sosa) "
            "evalúa propuestas antes de firma, no participa de la primera reunión. Agenda: "
            "(1) validar contexto, (2) involucrar a Rafael, (3) mostrar caso similar.' "
            "¿Cuál es el problema principal del handoff?"
        ),
        "choices": [
            {
                "id": "a",
                "text": "Es demasiado largo — los handoffs deben caber en 3-4 líneas.",
            },
            {
                "id": "b",
                "text": (
                    "No tiene problemas significativos. Contiene todo lo que necesita el AE: "
                    "contexto, contacto, señal, precalificación completa, advertencia sobre otro "
                    "stakeholder, agenda sugerida."
                ),
            },
            {
                "id": "c",
                "text": "Falta información sobre la personalidad de Daniela.",
            },
            {
                "id": "d",
                "text": (
                    "Falta información de precios — debería incluir presupuesto estimado para "
                    "que el AE llegue preparado."
                ),
            },
        ],
        "correct": ["b"],
        "explanation": (
            "Es un handoff bien hecho. Cumple los criterios del Bloque 6: empresa, contacto, "
            "señal, contexto del outreach, precalificación (Situación + Necesidad + Timing), "
            "advertencia estratégica (Rafael Sosa con poder de veto) y agenda. Los handoffs no "
            "son 4 líneas — son lo que se necesite. Incluir 'presupuesto estimado' sería cruzar "
            "el hito 4 (propuesta)."
        ),
    },
    {
        "id": "q4",
        "block": 7,
        "type": "single",
        "prompt": (
            "Un SDR junior recibe del manager: 'Tu objetivo es agendar 8 reuniones esta semana. "
            "Bono de USD 50 por cada reunión que el AE acepte.' ¿Cuál es la actitud correcta?"
        ),
        "choices": [
            {
                "id": "a",
                "text": (
                    "Focalizarse exclusivamente en cerrar el número (8 reuniones) sin importar "
                    "con quién ni cómo. El incentivo es claro."
                ),
            },
            {
                "id": "b",
                "text": (
                    "Agendar 8 con cualquiera que diga 'sí' — al final el AE filtra en la reunión "
                    "si no sirve."
                ),
            },
            {
                "id": "c",
                "text": (
                    "Focalizarse en 8 reuniones que sean CALIFICADAS (4 criterios). Mejor 5 "
                    "calificadas que 10 sin filtro — las no-calificadas queman credibilidad y el "
                    "incentivo real del rol es calidad sostenida, no volumen bruto del primer mes."
                ),
            },
            {
                "id": "d",
                "text": (
                    "Ignorar el pedido del manager y focalizarse solo en 'aprender el oficio' — "
                    "los números distraen del aprendizaje."
                ),
            },
        ],
        "correct": ["c"],
        "explanation": (
            "Mindset del Bloque 7: ejecutor + con criterio. Opción a es 'cazador de comisiones', "
            "explícitamente lo que el SDR NO es. Opción b delega el filtro al AE — el error que "
            "el concepto de 'reunión calificada' existe para prevenir. Opción d es opuesta: "
            "ignorar la disciplina de volumen es torre de marfil. Un buen reporte: 'esta semana "
            "agendé 5 calificadas, descarté 6 que no cumplían criterios.'"
        ),
    },
]


RESOURCES = [
    {
        "kind": "pdf",
        "title": "Handout — Rol del SDR e hitos (Semana 2)",
        "url": "https://drive.google.com/file/d/PLACEHOLDER_W2_HANDOUT",
        "order_index": 0,
    },
    {
        "kind": "link",
        "title": "Bridge Group — SDR Metrics & Compensation Report 2023",
        "url": "https://bridgegroupinc.com/sdr-metrics-report",
        "order_index": 1,
    },
    {
        "kind": "link",
        "title": "Instantly — Cold Email Benchmark Report 2026",
        "url": "https://instantly.ai/blog/cold-email-benchmarks",
        "order_index": 2,
    },
    {
        "kind": "doc",
        "title": "Plantilla — Handoff SDR → AE (Bloque 6)",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W2_HANDOFF",
        "order_index": 3,
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
    return module


def _upsert_lesson(db, module: Module) -> Lesson:
    lesson = (
        db.query(Lesson)
        .filter_by(module_id=module.id, order_index=1)
        .first()
    )
    if lesson is None:
        lesson = Lesson(
            module_id=module.id,
            order_index=1,
            kind="video",
            youtube_id=None,
            duration_seconds=1500,
        )
        lesson.translations.append(
            LessonTranslation(
                locale="es",
                title="Semana 2 — El rol del SDR, hitos y reunión calificada",
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
        tr_es.title = "Semana 2 — El rol del SDR, hitos y reunión calificada"
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
            title="Micro-pruebas — Semana 2",
            config=config,
            passing_score=65.0,
        )
        db.add(a)
        db.commit()
        db.refresh(a)
        log.info("assessment.seeded", extra={"assessment_id": a.id})
        return a
    existing.title = "Micro-pruebas — Semana 2"
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
            "seed_w2.done",
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
