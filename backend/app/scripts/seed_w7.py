"""Seed: Semana 7 del Módulo 4 (La maquinaria del outbound).

Abre el Módulo 4 — "El sistema". Contenido extraído de
SDR_Academy_Siete_Documento_Maestro.md (bloques 1-8 de Semana 7 + 4 micro-pruebas
MCQ Capa 1).

Crea el módulo `m4-el-sistema` (order_index=3) si no existe, y dentro la primera
lección (order_index=0) con la secuencia dinámica completa.

Uso:
    cd backend && .venv/bin/python -m app.scripts.seed_w7
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
log = get_logger("seed_w7")


COURSE_SLUG = "sdr-academy-v1"
MODULE_SLUG = "m4-el-sistema"
LESSON_ORDER_INDEX = 0


LESSON_BODY_ES = """Pregunta central de la semana: ¿Cómo se combina gente, canales, tiempo e infraestructura para que esto funcione a escala?

**Dato crudo:** las secuencias multicanal superan a single-channel por un factor de 2x-3x en reply rate (Salesloft + Outreach State of Sales Engagement). Pero "usar todos los canales" no es la respuesta — la respuesta es saber por qué cada uno entra en el lugar que entra.

## Bloque 1 — Outbound como sistema de volumen, no como "escribirle a alguien"
Es alimentar un motor con listas, contactos y contenido. El SDR que trabaja como **sistema** escala; el que intenta ser artesanal a escala se quema. Esto no significa renunciar a personalización — significa entender que la personalización vive dentro del sistema, no contra él. Ross & Tyler (Predictable Revenue, 2011): outbound es replicable, no arte.

## Bloque 2 — Los 5 canales del outbound: qué hace único a cada uno
**Email:** canal base, escalable, asíncrono, trazable — punto de entrada por default. **Teléfono:** sincrónico, obliga a decisión, caro en tiempo. **LinkedIn:** research + micro-touch, no canal de alto volumen. **WhatsApp:** directo, personal, cercano; en LATAM B2B pesa; riesgo de bloqueo si se abusa. **Video:** diferenciador, consume mucho tiempo, alto retorno cuando es genuino.

## Bloque 3 — Multicanal vs single-channel: por qué funciona
Lift típico reportado: **2x-3x** vs canal único (Salesloft, Outreach, Outbound Kitchen 2025). Pero NO es "usar todos los canales para todos" — es elegir la combinación que tiene sentido para el contexto. El antipatrón clásico es saturar al prospecto con touches en 4 canales simultáneos.

## Bloque 4 — Secuencia y cadencia
**Secuencia:** conjunto ordenado de touches multicanal **con reglas de ramificación** según respuesta (o no respuesta). Sin reglas de ramificación, no es secuencia — es lista. **Cadencia:** timing entre touches. Ni tan pegado que incomode, ni tan separado que te olviden. Benchmark Instantly 2026: **4-7 touchpoints espaciados 2-4 días, ventana total 10-20 días**. Toda secuencia real declara: si el prospecto responde, la secuencia automática se pausa y el SDR toma control manual.

## Bloque 5 — Lógica del orden
**Email primero** — no impone presencia, establece nombre y contexto. **Llamada amplifica** — cuando entra, el prospecto ya vio el nombre y deja de ser interrupción al azar. **WhatsApp como empujón o precalificación**, no como entrada — en frío el prospecto lo lee como invasión de espacio personal. **LinkedIn corre en paralelo** como research + micro-touch, no como touchpoint dedicado de la secuencia principal.

## Bloque 6 — Variantes de acceso al decisor según información disponible
El SDR **no elige "la ruta 2"** — diagnostica qué información tiene y deriva la forma de acercamiento. Seis variantes:
- **V1 — Correo + teléfono del decisor verificados:** multicanal proactivo directo (email abre contexto, llamada amplifica, mensaje directo cierra).
- **V2 — Solo correo del decisor:** email paciente, más touches, cadencia espaciada.
- **V3 — Sin contacto del decisor:** vía referidores dentro de la empresa (champions potenciales — se les **pide orientación, no se les vende**). Esta es la variante más frecuente en la práctica.
- **V4 — Referidor me dio contacto del decisor:** retomo al decisor mencionando al referidor como ancla de credibilidad — ya no es frío absoluto.
- **V5 — Contacté antes sin éxito:** ventana de enfriamiento (3-6 meses típico) + ángulo nuevo. No repetir.
- **V6 — Wish list (alta prioridad):** aproximación artesanal con research profundo; el tiempo se justifica por valor potencial.

## Bloque 7 — Deliverability como concepto fundamental
Qué determina que un correo llegue al inbox: **reputación de dominio**, warm-up, volumen por casilla, qué es una "casilla quemada". Tratamiento conceptual — NO se pide configurar SPF/DKIM/DMARC. Pero el SDR tiene que entender por qué importa: cuando reply rate cae bruscamente sin cambios en copy/ICP/cadencia, la hipótesis más probable es deliverability. Diagnóstico antes que solución — **hasta que no se resuelva el canal, nada de lo demás importa**.

## Bloque 8 — Las herramientas como instrumentación del concepto
Apollo, ZoomInfo, Reply.io, Outreach, Salesloft, MailReach, Google Postmaster Tools — son ejemplos concretos de **categorías conceptuales**: base de datos de prospectos, motor de secuencias, warmup, monitoreo de deliverability. El concepto vive más allá de la herramienta. Si mañana Siete cambia de stack, el egresado transfiere el conocimiento en 1 semana aprendiendo la interfaz nueva. **La regla de carrera:** el alumno se va con el mapa conceptual, no con nombres de marcas.

**Síntesis:** outbound es una máquina con cinco piezas (canales) que se combinan en secuencias con reglas. Quien diseña la secuencia diagnostica primero qué información tiene del decisor y deriva la forma; no aplica una plantilla.

**Fuentes:** Ross & Tyler (2011). Bertuzzi (2016). Outbound Kitchen (2025). Instantly (2026). Salesloft / Outreach State of Sales Engagement. Cognism (2025-26). Google Postmaster Tools."""


AVATAR_SCRIPT_ES = """Semana 7. Abrimos el Módulo 4 — El sistema. La pregunta central: ¿cómo se combina gente, canales, tiempo e infraestructura para que esto funcione a escala?

Hasta acá viste cómo se escribe un email, cómo se conversa en frío, cómo se califica. Esta semana subís un nivel: no más mensajes sueltos, sino sistemas que producen mensajes. La diferencia entre un SDR que sostiene cien touches semanales y uno que se quema en treinta no está en la voluntad — está en la maquinaria.

Lo más importante de la semana es esto: outbound no es "escribirle a alguien". Es alimentar un motor con listas, contactos y contenido. El que trabaja como sistema, escala. El que intenta ser artesanal a escala, se quema.

Ocho bloques. Primero, por qué outbound es sistema y no artesanía. Segundo, los cinco canales — email, teléfono, LinkedIn, WhatsApp, video — y qué hace único a cada uno. Tercero, por qué multicanal supera a single-channel por dos o tres veces, según el estudio. Cuarto, qué es una secuencia de verdad — no una lista, una secuencia con reglas de ramificación. Quinto, la lógica del orden: por qué email entra primero, llamada amplifica, WhatsApp empuja, LinkedIn corre en paralelo. Sexto, el bloque más importante: las seis variantes de acceso al decisor según qué información tenés. No memorizás rutas — diagnosticás qué hay y derivás la forma. Séptimo, deliverability — la variable invisible que determina si tu trabajo sirve o no. Octavo, las herramientas como instrumentación del concepto: te vas con el mapa conceptual, no con nombres de marcas.

Una regla que te llevás ya: cuando reply rate cae bruscamente sin cambios en copy, ICP o cadencia, no toques el mensaje. Abrí Google Postmaster Tools y mirá deliverability. El canal es lo primero que se chequea.

Cuatro micro-pruebas al final. La primera te exige diagnosticar la variante de acceso correcta — el bloque seis es el que más vas a usar en el día a día. Vamos."""


PRESENTATION_BLOCKS_ES = [
    {
        "title": "Outbound como sistema — no como artesanía",
        "bullets": [
            "Alimentar un motor con listas, contactos y contenido",
            "Sistema escala. Artesanía a escala = burnout.",
            "Personalización vive DENTRO del sistema, no contra él",
            "Predictable Revenue (Ross & Tyler 2011): outbound replicable",
        ],
        "source": "Ross & Tyler 2011",
    },
    {
        "title": "Los 5 canales del outbound — qué hace único a cada uno",
        "bullets": [
            "Email: base, escalable, asíncrono, trazable — entrada por default",
            "Teléfono: sincrónico, obliga decisión, caro en tiempo",
            "LinkedIn: research + micro-touch, NO alto volumen",
            "WhatsApp: directo, personal — en LATAM pesa, riesgo bloqueo",
            "Video: diferenciador, costoso, alto retorno si es genuino",
        ],
        "source": "Bertuzzi 2016 + Operativa Siete",
    },
    {
        "title": "Multicanal vs single-channel — lift 2x-3x",
        "bullets": [
            "Salesloft / Outreach State of Sales: 2x-3x reply rate vs single",
            "Outbound Kitchen 2025: 232 empresas trackeadas, tendencia confirmada",
            "NO es 'todos los canales para todos'",
            "Antipatrón: saturación con touches simultáneos en 4 canales",
        ],
        "source": "Salesloft + Outreach + Outbound Kitchen 2025",
    },
    {
        "title": "Secuencia y cadencia",
        "bullets": [
            "Secuencia = touches ordenados CON reglas de ramificación",
            "Sin reglas = lista (no secuencia)",
            "Cadencia: 4-7 touchpoints, 2-4 días entre touches",
            "Ventana total: 10-20 días (Instantly 2026)",
            "Si responde → pausa automática, SDR toma control manual",
        ],
        "source": "Instantly 2026 + Bertuzzi 2016",
    },
    {
        "title": "Lógica del orden",
        "bullets": [
            "Email PRIMERO: no impone presencia, establece nombre y contexto",
            "Llamada AMPLIFICA: cuando entra, el prospecto ya vio el nombre",
            "WhatsApp = empujón/precalificación, NO entrada",
            "LinkedIn en paralelo (research + micro-touch)",
            "Llamar al día 1 con solo 1 email previo = contexto no aterriza",
        ],
        "source": "Bloque 5 + Predictable Revenue",
    },
    {
        "title": "6 variantes de acceso al decisor — diagnóstico, no plantilla",
        "bullets": [
            "V1: correo + teléfono → multicanal proactivo",
            "V2: solo correo → email paciente, cadencia espaciada",
            "V3: sin contacto → vía referidores (pedir orientación, NO vender)",
            "V4: referidor dio contacto → retomo con ancla de credibilidad",
            "V5: contacté antes sin éxito → ventana enfriamiento + ángulo nuevo",
            "V6: wish list → aproximación artesanal con research profundo",
        ],
        "source": "Predictable Revenue + propiedad Siete",
    },
    {
        "title": "Deliverability — la variable invisible",
        "bullets": [
            "Determina si el correo llega al inbox",
            "Variables: reputación dominio, warm-up, volumen por casilla, casilla quemada",
            "NO se pide configurar SPF/DKIM/DMARC — sí entender por qué importa",
            "Caída brusca de reply sin cambios = chequear deliverability PRIMERO",
            "Hasta que no se resuelva el canal, nada del mensaje importa",
        ],
        "source": "Google Postmaster Tools + MailReach",
    },
    {
        "title": "Herramientas = instrumentación del concepto",
        "bullets": [
            "Base de datos: Apollo, ZoomInfo, Crunchbase, Lusha",
            "Motor de secuencias: Reply.io, Outreach, Salesloft, Instantly, Smartlead",
            "Warmup: MailReach, Instantly Warmup, Smartlead Warmup",
            "Monitoreo deliverability: Google Postmaster, MXToolbox, GlockApps",
            "Cambiás de empresa, cambiás el stack — el concepto NO cambia",
        ],
        "source": "Bloque 8 + ecosistema outbound 2025-26",
    },
]


MCQ_QUESTIONS = [
    {
        "id": "q1",
        "block": 6,
        "type": "single",
        "prompt": (
            "Estás prospectando a Consultora Andina (empresa peruana de consultoría de "
            "transformación digital, 250 empleados). El decisor es la VP de Nuevos Negocios, "
            "Patricia Mendoza. Su email corporativo NO aparece en Apollo ni en la web; su "
            "teléfono tampoco. Apollo devuelve 4 coordinadores del área comercial (email "
            "verificado) y 2 gerentes de cuenta (uno con email y teléfono). Consultora Andina "
            "nunca fue contactada antes por Siete. ¿Qué variante de acceso al decisor "
            "corresponde?"
        ),
        "choices": [
            {
                "id": "a",
                "text": (
                    "V1 — multicanal proactivo directo a Patricia (email + llamada)."
                ),
            },
            {
                "id": "b",
                "text": "V2 — email paciente a Patricia con cadencia espaciada.",
            },
            {
                "id": "c",
                "text": (
                    "V3 — vía referidores dentro de la empresa, buscando champions en los "
                    "mandos medios."
                ),
            },
            {
                "id": "d",
                "text": (
                    "V5 — recontacto con ángulo nuevo después de ventana de enfriamiento."
                ),
            },
        ],
        "correct": ["c"],
        "explanation": (
            "El criterio de diagnóstico (Bloque 6) es explícito: si NO tenés contacto verificado "
            "del decisor y la empresa nunca fue contactada, la variante es V3 — acceso vía "
            "referidores. Los 4 coordinadores y 2 gerentes son candidatos a champions: les "
            "pedís orientación ('¿quién vería este tema en su organización?'), NO les vendés. "
            "Es la variante con la que más tiempo pasa un SDR típico y la que exige más "
            "criterio, porque el objetivo del mensaje es distinto (conseguir ruteo, no agendar "
            "reunión). (a/V1) requiere correo Y teléfono verificados del decisor. (b/V2) "
            "requiere al menos correo verificado del decisor. (d/V5) aplica solo cuando ya "
            "contactaste antes sin éxito. El error clásico del SDR novato es asumir que tiene "
            "que llegarle al decisor sí o sí desde el primer mensaje. V3 acepta que el camino "
            "es indirecto y no lo ve como segundo premio — en outbound B2B real, es el camino "
            "más frecuente."
        ),
    },
    {
        "id": "q2",
        "block": 5,
        "type": "multi",
        "prompt": (
            "Un SDR te pasa esta secuencia para revisar (KDM con email y teléfono verificados, "
            "variante V1): Paso 1 día 0 WhatsApp inicial / Paso 2 día 0 Email gancho / Paso 3 "
            "día 1 Llamada fría / Paso 4 día 1 LinkedIn conexión / Paso 5 día 2 Email follow-up "
            "/ Paso 6 día 3 Segunda llamada / Paso 7 día 4 WhatsApp empujón / Paso 8 día 5 "
            "Último email. Marcá TODOS los errores ESTRUCTURALES (no de calibración):"
        ),
        "choices": [
            {"id": "1", "text": "Arranca con WhatsApp en frío como primer touch."},
            {"id": "2", "text": "Usa email como segundo canal en vez de primero."},
            {"id": "3", "text": "8 touchpoints comprimidos en 5 días = saturación."},
            {
                "id": "4",
                "text": (
                    "Incluye LinkedIn como touchpoint en vez de tratarlo como canal paralelo."
                ),
            },
            {
                "id": "5",
                "text": (
                    "La llamada del día 1 aparece antes del follow-up por email — falta "
                    "acumulación de contexto escrito."
                ),
            },
            {"id": "6", "text": "Usa teléfono dos veces en la misma secuencia."},
            {
                "id": "7",
                "text": (
                    "No tiene ramificación declarada según respuesta del prospecto."
                ),
            },
        ],
        "correct": ["1", "3", "5", "7"],
        "explanation": (
            "Correctos 1, 3, 5, 7. (1) WhatsApp es empujón tras contacto previo, NO entrada — "
            "en frío se lee como invasión, riesgo alto de bloqueo. (3) Benchmark Instantly: 4-7 "
            "touchpoints / 2-4 días / ventana 10-20 días. Meter 8 en 5 días rompe la regla por "
            "factor 3x. (5) Lógica del orden es email → llamada: el email PRIMERO introduce "
            "contexto sin imponer presencia. Llamar al día 1 con solo un email previo (horas "
            "antes) no permite que el contexto aterrice. (7) Sin reglas de ramificación, no es "
            "secuencia — es lista. Toda secuencia real declara: si responde, pausa automática. "
            "NO son errores estructurales: (2) confunde causa — el error real es WhatsApp como "
            "entrada, no 'email segundo'. (4) detalle de calibración, no estructural. (6) "
            "teléfono dos veces es correcto — touch 3 y touch 7. El error no es la repetición "
            "sino la cadencia comprimida."
        ),
    },
    {
        "id": "q3",
        "block": 8,
        "type": "match",
        "prompt": (
            "Emparejá cada concepto con el grupo de herramientas que lo instrumentan. "
            "La pregunta evalúa si internalizaste el MAPA CONCEPTUAL — no nombres de marca:"
        ),
        "left": [
            {
                "id": "1",
                "text": "Base de datos de prospectos con filtros de ICP y señales",
            },
            {
                "id": "2",
                "text": "Motor de secuencias multicanal con reglas de ramificación",
            },
            {"id": "3", "text": "Monitoreo de deliverability y reputación de dominio"},
            {"id": "4", "text": "Warmup automatizado para dominios nuevos"},
        ],
        "right": [
            {"id": "A", "text": "MailReach, Instantly Warmup, Smartlead Warmup"},
            {"id": "B", "text": "Apollo, ZoomInfo, Crunchbase, Lusha"},
            {"id": "C", "text": "Google Postmaster Tools, MXToolbox, GlockApps"},
            {"id": "D", "text": "Reply.io, Outreach, Salesloft, Instantly, Smartlead"},
        ],
        "correct": {"1": "B", "2": "D", "3": "C", "4": "A"},
        "explanation": (
            "1 → B: Apollo, ZoomInfo, Crunchbase, Lusha son bases de datos de prospectos con "
            "filtros de ICP. 2 → D: Reply.io, Outreach, Salesloft, Instantly, Smartlead son "
            "motores de secuencias multicanal. 3 → C: Google Postmaster, MXToolbox, GlockApps "
            "MIDEN reputación y deliverability. 4 → A: MailReach, Instantly Warmup, Smartlead "
            "Warmup CONSTRUYEN reputación (warmup automatizado). Confundir 'monitoreo de "
            "deliverability' con 'warmup' es no entender la diferencia entre MEDIR (Postmaster) "
            "y CONSTRUIR (warmup). Confundir 'base de datos' con 'motor de secuencias' es no "
            "entender que Apollo NO manda emails — solo entrega contactos; y Reply.io NO tiene "
            "contactos — ejecuta secuencias sobre contactos que le cargás vos. Cuando entres a "
            "un trabajo nuevo con stack distinto (ZoomInfo + Outreach en vez de Apollo + "
            "Reply.io), los conceptos son idénticos — transferís el conocimiento en 1 semana."
        ),
    },
    {
        "id": "q4",
        "block": 7,
        "type": "single",
        "prompt": (
            "Sos SDR de Siete. Durante 8 semanas tu reply rate se mantuvo entre 2.0% y 2.3%. En "
            "las últimas 2 semanas, SIN cambios en el copy, SIN cambios en el ICP y SIN cambios "
            "en la cadencia, tu reply rate cayó a 0.4%. Tu Team Lead te pide hipótesis + primer "
            "paso del checklist. ¿Cuál es la respuesta correcta?"
        ),
        "choices": [
            {
                "id": "a",
                "text": (
                    "Hipótesis: fatiga de mensaje. Primer paso: rediseñar el asunto y probar 3 "
                    "variantes A/B."
                ),
            },
            {
                "id": "b",
                "text": (
                    "Hipótesis: ICP mal calibrado. Primer paso: revisar filtros de Apollo y "
                    "ajustar industria/cargo."
                ),
            },
            {
                "id": "c",
                "text": (
                    "Hipótesis: problema de deliverability — uno o más dominios se quemaron o "
                    "la reputación cayó. Primer paso: abrir Google Postmaster Tools y revisar "
                    "reputación de cada dominio activo."
                ),
            },
            {
                "id": "d",
                "text": (
                    "Hipótesis: lista contaminada con prospectos ya contactados. Primer paso: "
                    "pedir lista fresca al área de research."
                ),
            },
        ],
        "correct": ["c"],
        "explanation": (
            "La pregunta te da tres variables fijas (copy, ICP, cadencia) y una caída brusca "
            "(2.1% → 0.4% en 2 semanas = factor 5x). Cuando nada cambió en el mensaje ni en el "
            "receptor pero el reply rate cae así, la explicación más probable es que los "
            "mensajes NO están llegando al inbox — se caen a spam, a promociones o rebotan. El "
            "primer paso (Bloque 7) es Google Postmaster Tools: fuente más directa para ver si "
            "la reputación del dominio cayó. Los otros pasos del checklist (mail-tester, "
            "bounces, warmup de dominios de reserva) vienen DESPUÉS de esa primera lectura. "
            "(a) Fatiga de copy: el copy NO cambió. Si fuera fatiga, la caída sería gradual "
            "(semanas), no abrupta. Rediseñar copy antes de verificar deliverability es probar "
            "soluciones sobre un canal roto. (b) ICP: descartable por la misma lógica — no "
            "cambió. (d) Lista contaminada puede ser factor marginal, pero no explica caída de "
            "5x. Además, proponer solución antes que diagnóstico es el error clásico del SDR "
            "novato. Bloque 7: diagnóstico antes que solución. Hasta que no se resuelva el "
            "canal, nada de lo demás importa."
        ),
    },
]


RESOURCES = [
    {
        "kind": "pdf",
        "title": "Handout — La maquinaria del outbound (Semana 7)",
        "url": "https://drive.google.com/file/d/PLACEHOLDER_W7_HANDOUT",
        "order_index": 0,
    },
    {
        "kind": "doc",
        "title": "Plantilla — Diseño de secuencia multicanal con reglas de ramificación",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W7_SEQUENCE",
        "order_index": 1,
    },
    {
        "kind": "doc",
        "title": "Diagnóstico — Las 6 variantes de acceso al decisor (decision tree)",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W7_VARIANTS",
        "order_index": 2,
    },
    {
        "kind": "doc",
        "title": "Checklist — Diagnóstico de deliverability (orden de verificación)",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W7_DELIVERABILITY",
        "order_index": 3,
    },
    {
        "kind": "link",
        "title": "Outbound Kitchen — State of Outbound 2025 (232 empresas)",
        "url": "https://outboundkitchen.com/",
        "order_index": 4,
    },
    {
        "kind": "link",
        "title": "Google Postmaster Tools (documentación oficial)",
        "url": "https://postmaster.google.com/",
        "order_index": 5,
    },
    {
        "kind": "link",
        "title": "Instantly — Cold Email Benchmark Report 2026 (cadencias y touches)",
        "url": "https://instantly.ai/blog/cold-email-benchmarks",
        "order_index": 6,
    },
    {
        "kind": "link",
        "title": "Salesloft — State of Sales Engagement (multicanal lift)",
        "url": "https://salesloft.com/resources/",
        "order_index": 7,
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
    module = Module(course_id=course.id, slug=MODULE_SLUG, order_index=3)
    module.translations.append(
        ModuleTranslation(
            locale="es",
            title="Módulo 4 — El sistema",
            summary="La maquinaria del outbound y el mindset de mejora continua.",
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
            duration_seconds=1800,
        )
        lesson.translations.append(
            LessonTranslation(
                locale="es",
                title="Semana 7 — La maquinaria del outbound",
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
        tr_es.title = "Semana 7 — La maquinaria del outbound"
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
            title="Micro-pruebas — Semana 7",
            config=config,
            passing_score=65.0,
        )
        db.add(a)
        db.commit()
        db.refresh(a)
        log.info("assessment.seeded", extra={"assessment_id": a.id})
        return a
    existing.title = "Micro-pruebas — Semana 7"
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
            "seed_w7.done",
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
