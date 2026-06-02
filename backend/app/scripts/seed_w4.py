"""Seed: Semana 4 del Módulo 2 (Entender al comprador).

Cierre del Módulo 2. Contenido extraído de SDR_Academy_Siete_Documento_Maestro.md
(bloques 1-6 de Semana 4 + 4 micro-pruebas MCQ Capa 1).

Agrega la segunda lección al módulo `m2-el-otro-lado` (order_index=1) con la
secuencia dinámica completa.

Uso:
    cd backend && .venv/bin/python -m app.scripts.seed_w4
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
log = get_logger("seed_w4")


COURSE_SLUG = "sdr-academy-v1"
MODULE_SLUG = "m2-el-otro-lado"


LESSON_BODY_ES = """Pregunta central de la semana: ¿Quién está del otro lado del correo y qué le importa?

## Bloque 1 — ICP vs buyer persona: dos filtros distintos
ICP = la EMPRESA (industria + tamaño + geografía + características + señales + exclusiones). Buyer persona = la PERSONA dentro de esa empresa (rol + nivel de decisión + motivaciones + frenos + canales + tipo de mensaje). Son filtros acumulativos: primero ICP, después buyer persona. Saltar el segundo filtro genera "respuestas" que nunca convierten.

## Bloque 2 — Los 7 arquetipos del comité (Challenger Customer)
3 MOBILIZERS (los que mueven): Go-Getter (proactivo, empuja), Teacher (comparte conocimiento internamente), Skeptic (cuestiona, pero cuando se convence empuja fuerte). 4 TALKERS (hablan pero no mueven): Guide (info por auto-beneficio), Friend (amable sin peso), Climber (busca palanca de carrera), Blocker (opone cambio). Insight: Mobilizers son el 37% del comité pero generan el 100% del movimiento al "sí". Apuntar a Talkers es la trampa dulce del outbound.

## Bloque 3 — Psicología del decisor B2B
4 motores: avance de carrera, status interno, resultados medibles, evitar riesgo. 3 frenos: costo de cambio, miedo al error público, fatiga de proveedores. Sistema 1 (Kahneman) decide si seguir leyendo en <5 seg — si la primera línea no engancha emocional-intuitivamente, Sistema 2 nunca se activa. Por eso la primera línea importa más que el cuerpo.

## Bloque 4 — "No listo" vs "no fit": la distinción crítica
NO FIT: no califica como ICP/buyer persona — descarte definitivo. NO LISTO: califica pero no es el momento — pipeline futuro con trigger de recontacto. Tratar un "no fit" como "no listo" desperdicia 6-12 meses. Tratar un "no listo" como "no fit" pierde cuentas que cierran con el competidor. El SDR que distingue construye banco de pipeline futuro ordenado.

## Bloque 5 — Timing signals reales vs ruido
SEÑALES REALES (verificables, específicas, recientes): cambios de liderazgo <90d, contratación masiva, ronda de inversión (Serie B+), regulación nueva en <180d, M&A, lanzamiento de producto/línea, expansión geográfica. RUIDO: posts genéricos, premios de Employer Branding, reconocimientos sin contenido operativo, noticias >6 meses, movimientos del competidor. Regla: nunca escribas un email sin señal.

## Bloque 6 — Por qué entender al comprador mueve 1% → 3%
La diferencia entre top performer (3%) y promedio (1%) NO es producto ni herramientas — es qué tan profundo entiende el SDR al comprador. 30 emails al 3% > 50 emails al 1%. El anti-patrón del SDR nuevo: "más es más". La realidad: menos emails con más research = más conversión.

**Síntesis del Módulo 2:** no escribís a empresas, escribís a personas específicas dentro de empresas específicas. Entender ambas (negocio en Sem 3 + persona en Sem 4) separa outbound que convierte de outbound que se ignora.

**Fuentes:** Dixon, Adamson, Toman & Spenner (2015) The Challenger Customer. Dixon & Adamson (2011) The Challenger Sale. Miller-Heiman (1985+). Rackham (1988) SPIN Selling. Kahneman (2011). Bertuzzi (2016). Gartner 2020-2023. Bridge Group 2023."""


AVATAR_SCRIPT_ES = """Esta es la semana que cierra el Módulo 2. La semana anterior leíste el negocio. Esta semana leés a la persona dentro del negocio.

Pregunta central: ¿quién está del otro lado del correo y qué le importa?

Una idea contra-intuitiva para que la tengas en la cabeza: la persona más amable de tu lista de contactos probablemente no te va a hacer ganar el deal. Y la persona que cuestiona todo, que pide datos auditados, que pone trabas — esa es la que mueve cuando se convence.

El framework del Challenger Customer parte de eso. Dentro de cada comité de compra hay siete arquetipos. Solo tres mueven la decisión: el Go-Getter que empuja, el Teacher que evangeliza internamente, y el Skeptic que cuestiona con rigor. Los otros cuatro — Guide, Friend, Climber, Blocker — hablan, responden emails, agendan reuniones, pero no mueven la aguja. Apuntar a esos cuatro es la trampa dulce del outbound: parecen prospectos buenos porque son accesibles, pero el deal nunca avanza.

En los seis bloques de esta semana vas a ver: la distinción entre ICP (la empresa) y buyer persona (la persona dentro), los siete arquetipos del comité, la psicología del decisor B2B con motores y frenos, la diferencia crítica entre "no listo" y "no fit", las timing signals reales versus el ruido, y por qué entender al comprador mueve la conversión de uno a tres por ciento.

Una regla práctica para llevarte: nunca escribas un email sin señal verificable. Si después de quince minutos de research no encontraste nada, archivá con trigger o tratá la cuenta como artesanal. No mandes pitches genéricos.

Al final, cuatro micro-pruebas que cierran el Módulo 2. Después arranca el Módulo 3 — la conexión: escritura persuasiva y conversación en frío. Vamos."""


PRESENTATION_BLOCKS_ES = [
    {
        "title": "ICP vs Buyer Persona — dos filtros acumulativos",
        "bullets": [
            "ICP = la EMPRESA (industria + tamaño + geografía + exclusiones)",
            "Buyer persona = la PERSONA (rol + nivel de decisión + motivos + frenos)",
            "Filtro 1: ¿la empresa califica? Si no, descarte",
            "Filtro 2: ¿tengo acceso a buyer persona válido? Si no, archivo o referidor",
        ],
        "source": "Bertuzzi 2016 + Ross & Tyler 2011",
    },
    {
        "title": "7 arquetipos del comité (Challenger Customer)",
        "bullets": [
            "MOBILIZERS (37% del comité, 100% del movimiento al sí)",
            "Go-Getter: 'vamos por esto'",
            "Teacher: 'justo estuve leyendo algo'",
            "Skeptic: 'dame datos antes de avanzar'",
            "TALKERS (trampa dulce): Guide, Friend, Climber, Blocker",
        ],
        "source": "Dixon, Adamson, Toman & Spenner 2015",
    },
    {
        "title": "Psicología del decisor B2B — motores y frenos",
        "bullets": [
            "Motores: avance de carrera, status interno, resultados medibles, evitar riesgo",
            "Frenos: costo de cambio, miedo al error público, fatiga de proveedores",
            "Sistema 1 decide leer en <5 seg (Kahneman)",
            "Primera línea > cuerpo: si no engancha emocional, Sistema 2 no se activa",
        ],
        "source": "Kahneman 2011 + Dixon & Adamson 2011",
    },
    {
        "title": "No listo vs No fit — la distinción que construye pipeline",
        "bullets": [
            "NO FIT: no califica como ICP/buyer persona → descarte definitivo",
            "NO LISTO: califica pero no es el momento → archivo con trigger de recontacto",
            "Confundirlos cuesta: 6-12 meses perdidos o cuentas que cierran con el competidor",
            "Banco de pipeline futuro = cada trimestre se activan los recontactos que tocan",
        ],
        "source": "Bertuzzi 2016",
    },
    {
        "title": "Timing signals — reales vs ruido",
        "bullets": [
            "REALES: cambios de liderazgo <90d, contrataciones masivas, ronda Serie B+, regulación nueva, M&A, expansión geográfica",
            "RUIDO: posts motivacionales, premios Employer Branding, noticias >6m, movimientos del competidor",
            "Regla: nunca un email sin señal verificable",
            "Fuentes: LinkedIn empresa+decisor, Google News, Apollo/ZoomInfo intent",
        ],
        "source": "Bertuzzi 2016 + Gartner 2020-2023",
    },
    {
        "title": "Por qué entender al comprador mueve 1% → 3%",
        "bullets": [
            "Top performer (3%) vs promedio (1%): mismo producto, herramientas, tiempo/prospecto",
            "Diferencia: profundidad de entendimiento del comprador específico",
            "30 emails al 3% > 50 emails al 1%",
            "Anti-patrón del SDR nuevo: 'más es más'",
            "Realidad: menos emails con más research = más conversión",
        ],
        "source": "Bridge Group 2023 + Instantly 2026",
    },
    {
        "title": "Síntesis del Módulo 2",
        "bullets": [
            "Sem 3 te dio el lenguaje del negocio",
            "Sem 4 te dio el lenguaje del comprador dentro del negocio",
            "No escribís a empresas — escribís a personas específicas en empresas específicas",
            "Próximo módulo: M3 — La conexión (escritura persuasiva + conversación)",
        ],
        "source": "Cierre del módulo",
    },
]


MCQ_QUESTIONS = [
    {
        "id": "q1",
        "block": 1,
        "type": "single",
        "prompt": (
            "Tu ICP declarado es: 'empresas de servicios financieros LATAM, 200-800 empleados, "
            "con operación en 2+ países'. Tenés 4 leads en Apollo. ¿En cuál priorizar prospección "
            "considerando ICP + acceso a buyer persona válido?"
        ),
        "choices": [
            {
                "id": "a",
                "text": (
                    "FinTrust Perú — 450 empleados, SOLO Perú, contacto Carolina (VP Tecnología)"
                ),
            },
            {
                "id": "b",
                "text": (
                    "BancoRegión — 680 empleados, Perú+Colombia+Chile, contacto Martín "
                    "(Analista senior de Compliance que reporta al Director)"
                ),
            },
            {
                "id": "c",
                "text": (
                    "PagosPlus — 180 empleados, México+Colombia, contacto Diego (CFO)"
                ),
            },
            {
                "id": "d",
                "text": (
                    "Santander LATAM — 12.000 empleados, multi-country, contacto Lucía "
                    "(Gerenta de Innovación)"
                ),
            },
        ],
        "correct": ["b"],
        "explanation": (
            "BancoRegión cumple los 3 ejes del ICP (680 en rango 200-800, 3 países, sector). "
            "Martín es champion potencial con acceso al Director — vale invertir tiempo. "
            "FinTrust falla en geografía (solo Perú). PagosPlus (180) está bajo el rango. "
            "Santander (12K) es enterprise — requiere ABM, no outbound masivo. Lección: el ICP "
            "es el primer filtro. Un C-level en empresa fuera del ICP es tan descartable como "
            "un analista junior — y una empresa ICP con champion potencial puede ser mejor "
            "opción que una empresa fuera de ICP con KDM directo."
        ),
    },
    {
        "id": "q2",
        "block": 2,
        "type": "single",
        "prompt": (
            "Aplicando el framework Challenger Customer, ¿cuál de estas respuestas de un prospecto "
            "es señal de MOBILIZER genuino (no Talker)?"
        ),
        "choices": [
            {
                "id": "a",
                "text": (
                    "'Gracias por escribir, me parece interesante lo que plantean. Coincido en "
                    "que el tema es relevante. Quedo a disposición si algo se concreta.'"
                ),
            },
            {
                "id": "b",
                "text": (
                    "'Leí la propuesta. Tengo dudas sobre cómo se integraría con nuestro stack "
                    "actual y si los números son defensibles ante nuestro CFO. ¿Podés mandarme un "
                    "caso técnico detallado con métricas auditadas antes de avanzar?'"
                ),
            },
            {
                "id": "c",
                "text": (
                    "'Claro, encantado de conversar. Contame cuándo tengas disponibilidad y "
                    "coordinamos.'"
                ),
            },
            {
                "id": "d",
                "text": (
                    "'Sí me interesa, pero sería útil que compartas la propuesta con mi jefe "
                    "primero. Si a él le gusta, avanzamos. Mi email es X, el de él es Y.'"
                ),
            },
        ],
        "correct": ["b"],
        "explanation": (
            "Opción b es Skeptic (Mobilizer): cuestiona antes de aceptar, trae temas propios "
            "(CFO va a pedir números defensibles), propone siguiente paso con criterio. Los "
            "Skeptics terminan siendo los mejores champions porque cuando dicen sí es porque "
            "evaluaron. Opciones a y c son Friend — cortesía sin fricción, sin preguntas propias. "
            "Opción d es Guide — delega al jefe para eximirse de ser champion. Trampa dulce del "
            "outbound: confundir amabilidad y accesibilidad con buen prospecto."
        ),
    },
    {
        "id": "q3",
        "block": 4,
        "type": "match",
        "prompt": (
            "Clasificá cada respuesta de prospecto como NO FIT (descarte definitivo) o NO LISTO "
            "(archivo con fecha de recontacto):"
        ),
        "left": [
            {
                "id": "1",
                "text": (
                    "'Somos una empresa familiar sin fines de lucro, no compramos este tipo de "
                    "software.'"
                ),
            },
            {
                "id": "2",
                "text": (
                    "'Estamos en freeze de compras hasta que termine la transición del nuevo CEO. "
                    "A fines del próximo trimestre veamos temas nuevos.'"
                ),
            },
            {
                "id": "3",
                "text": (
                    "'No tenemos presupuesto este año ni el próximo. Nuestra prioridad es reducir "
                    "costos, no agregar proveedores.'"
                ),
            },
            {
                "id": "4",
                "text": (
                    "'Acabamos de firmar con otro proveedor un contrato de 3 años. Si quieren, "
                    "escríbanos más cerca del vencimiento.'"
                ),
            },
            {
                "id": "5",
                "text": "'Sáquenme de sus listas y no me vuelvan a escribir.'",
            },
            {
                "id": "6",
                "text": (
                    "'Interesante, pero primero necesitamos estabilizar el equipo comercial — "
                    "contratamos 5 AEs nuevos. Retomá en 3-4 meses.'"
                ),
            },
        ],
        "right": [
            {"id": "F", "text": "NO FIT (descarte definitivo)"},
            {"id": "L", "text": "NO LISTO (archivo con trigger de recontacto)"},
        ],
        "correct": {
            "1": "F",
            "2": "L",
            "3": "F",
            "4": "L",
            "5": "F",
            "6": "L",
        },
        "explanation": (
            "NO FIT (1, 3, 5): estructuralmente no van a comprar — ONG, sin presupuesto presente "
            "ni futuro + prioridad reducción de costos, o pidió no ser contactado (do not "
            "contact). NO LISTO (2, 4, 6): califican como ICP/buyer persona pero hay bloqueo "
            "temporal con timing concreto. Tricky el caso 3: un alumno puede leerlo como 'no "
            "listo' pero el prospecto dice 'NI este año NI el próximo + prioridad opuesta' — "
            "información estructural, no circunstancial."
        ),
    },
    {
        "id": "q4",
        "block": 5,
        "type": "multi",
        "prompt": (
            "Un SDR hace research sobre una empresa potencial y encuentra estos hallazgos. "
            "Marcá TODAS las SEÑALES REALES de timing (no marques los ruidos):"
        ),
        "choices": [
            {
                "id": "1",
                "text": (
                    "La empresa anunció en su sitio web el lanzamiento de operación en Brasil "
                    "para Q2 2026"
                ),
            },
            {
                "id": "2",
                "text": "El CEO compartió un post motivacional sobre liderazgo la semana pasada",
            },
            {
                "id": "3",
                "text": (
                    "La empresa publicó 18 ofertas de trabajo para área comercial en las últimas "
                    "3 semanas"
                ),
            },
            {"id": "4", "text": "El Director de Operaciones actualizó su foto de perfil en LinkedIn"},
            {
                "id": "5",
                "text": (
                    "Cerraron ronda Serie B por USD 28M con un fondo conocido hace 60 días"
                ),
            },
            {
                "id": "6",
                "text": (
                    "Un regulatorio de la industria anunció nueva normativa que entra en vigor "
                    "en 100 días"
                ),
            },
            {
                "id": "7",
                "text": "La empresa ganó el premio 'Best Employer Branding 2026' del país",
            },
            {
                "id": "8",
                "text": "El competidor directo de la empresa despidió a 200 personas",
            },
        ],
        "correct": ["1", "3", "5", "6"],
        "explanation": (
            "Señales reales = eventos verificables, específicos y recientes que correlacionan "
            "con probabilidad de compra. 1 (expansión geográfica con fecha), 3 (contratación "
            "masiva área comercial = pipeline debe escalar), 5 (Serie B = capital disponible), "
            "6 (regulación con fecha = compra urgente). Ruido: 2 (actividad social genérica), "
            "4 (irrelevante personal), 7 (clima interno, no momento de compra), 8 (afecta al "
            "competidor, no al prospecto). El SDR que confunde actividad visible con señal de "
            "compra escribe a empresas que no están en momento de compra."
        ),
    },
]


RESOURCES = [
    {
        "kind": "pdf",
        "title": "Guía Semana 4 — Entender al comprador (PDF descargable)",
        "url": "https://drive.google.com/file/d/PLACEHOLDER_W4_GUIA",
        "order_index": 0,
    },
    {
        "kind": "pdf",
        "title": "Handout — Entender al comprador (Semana 4)",
        "url": "https://drive.google.com/file/d/PLACEHOLDER_W4_HANDOUT",
        "order_index": 1,
    },
    {
        "kind": "link",
        "title": "Dixon et al — The Challenger Customer (libro de referencia)",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W4_READING_CHALLENGER_CUSTOMER",
        "order_index": 2,
    },
    {
        "kind": "link",
        "title": "Kahneman — Thinking, Fast and Slow (resumen práctico)",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W4_READING_KAHNEMAN_TWO_SYSTEMS",
        "order_index": 3,
    },
    {
        "kind": "doc",
        "title": "Plantilla — Clasificación NO FIT / NO LISTO (Bloque 4)",
        "url": "https://docs.google.com/spreadsheets/d/PLACEHOLDER_W4_PIPELINE",
        "order_index": 4,
    },
    {
        "kind": "link",
        "title": "Apollo + ZoomInfo — guía de intent signals e intent data",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W4_READING_INTENT_DATA",
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
                title="Semana 4 — Entender al comprador",
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
        tr_es.title = "Semana 4 — Entender al comprador"
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
            title="Micro-pruebas — Semana 4",
            config=config,
            passing_score=65.0,
        )
        db.add(a)
        db.commit()
        db.refresh(a)
        log.info("assessment.seeded", extra={"assessment_id": a.id})
        return a
    existing.title = "Micro-pruebas — Semana 4"
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
            "seed_w4.done",
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
