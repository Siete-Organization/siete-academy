"""Seed: Semana 3 del Módulo 2 (Business Acumen: leer un negocio).

Apertura del Módulo 2 — "El otro lado".

Estrategia de contenido (Option C híbrida — replica el pattern de seed_w1):
- `MCQ_QUESTIONS` (4 preguntas Capa 1): transcripción literal del doc.
- `LESSON_BODY_ES`: híbrido. Pregunta central + Bloques 1 y 2 transcriptos
  literal del doc (lines 5228-5332). Bloques 3-7 como resumen explícito
  con nota apuntando a la "Guía Semana 3 (PDF)" como recurso descargable.
- `AVATAR_SCRIPT_ES` y `PRESENTATION_BLOCKS_ES`: borradores sintetizados.
- `RESOURCES`: incluye `PLACEHOLDER_W3_GUIA`.

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


LESSON_BODY_ES = """**Pregunta central de la semana:** ¿Cómo se lee un negocio lo suficientemente bien para hablarle a su dueño como un par?

Al terminar, vas a poder: analizar un negocio desconocido en 30 minutos y describir cómo gana plata, qué lo hace crecer y qué lo frena; leer una industria e identificar sus fuerzas dominantes; conectar un dolor específico del prospecto con una solución específica del cliente al que representás.

---

## Bloque 1 — Qué es business acumen y por qué separa al SDR mediocre del excelente

En el Módulo 1 aprendiste **cómo compra** una empresa B2B. Ahora toca aprender a **leer la empresa que tenés enfrente**.

**La brecha real**

Dos SDRs reciben el mismo lead: una empresa de logística de 300 empleados en Perú. Contactan al COO. Ambos escriben un email. Las respuestas son distintas.

**SDR-1** escribe: "Hola Javier, vi que tu empresa está creciendo. Trabajamos con empresas de logística ayudándoles a optimizar sus operaciones. ¿Tenés 20 minutos esta semana para ver si podemos ayudar?"

**SDR-2** escribe: "Hola Javier, vi que abrieron centro logístico en Arequipa el mes pasado. En logística que se expande a regiones, lo que suele pesar fuerte en el primer año es el calibrado de la demanda local — hasta que el modelo se ajusta, conviven sobrestock y quiebre en los distintos puntos. ¿Les está pasando algo así o ya tienen métricas estables por local?"

**SDR-1** convierte al 0.5%. **SDR-2** al 3%. No cambió el producto, no cambió la empresa objetivo. Cambió **lo que el SDR entiende del negocio del otro**.

Eso es business acumen: la capacidad de **leer cómo funciona un negocio** lo suficiente como para identificar qué lo preocupa hoy. No es saber "sobre logística" en abstracto — es saber cómo gana plata una empresa de logística, qué la hace crecer, qué la frena, y cómo eso se traduce en dolores que alguien tiene que resolver.

**Por qué el 80% de SDRs nunca lo construyen**

Construir business acumen requiere **leer afuera del script de ventas**. Leer informes de industria, analizar los números públicos de empresas, entender cómo funcionan ciclos, costos, márgenes. La mayoría de los SDRs no lo hace porque:

- No sienten que es "su trabajo" (creen que es trabajo del AE o del product marketing).
- Les parece intimidante meterse con finanzas, economía, estrategia.
- No lo ven premiado en incentivos de corto plazo.

El resultado es un SDR "profesional" que hace volumen pero nunca diferencia. Cuando cambia de industria o de producto, **arranca desde cero** — porque no construyó nada transferible.

El SDR que invierte en business acumen convierte mejor, crece más rápido a AE, y cuando cambia de empresa lleva un activo conceptual que no se deprecia. Es, probablemente, **la variable individual que más mueve la carrera comercial B2B a 5 años**.

*Fuentes: Bridge Group (2023). Sales Development Metrics & Compensation Research Report. · Dixon & Adamson (2011). The Challenger Sale. El perfil "Challenger" es el que más convierte — su característica principal es teaching basado en entender el negocio del comprador.*

---

## Bloque 2 — Anatomía de un negocio: Business Model Canvas

Necesitás un framework para leer cualquier empresa rápido. El estándar de la industria es el **Business Model Canvas** (Osterwalder & Pigneur, 2010). 9 componentes. 30 minutos para aplicarlo a una empresa que no conocés.

**Los 9 componentes**

1. **Segmentos de clientes.** ¿A quién le vende? Edad / tamaño / industria / geografía. Una misma empresa puede tener varios segmentos (ej: un banco vende a retail y a corporate).
2. **Propuesta de valor.** ¿Qué problema resuelve o qué necesidad cubre? No la versión del marketing — la versión real (Jobs to Be Done).
3. **Canales.** ¿Cómo entrega el producto/servicio? Tiendas físicas, online, app, distribuidores, fuerza de ventas directa.
4. **Relación con el cliente.** ¿Cómo se vincula? Autoservicio, atención personalizada, comunidad, self-service.
5. **Fuentes de ingresos.** ¿Cómo cobra? Venta única, suscripción, comisión, licencia, uso (pay-per-use), publicidad, freemium.
6. **Recursos clave.** ¿Qué necesita para operar? Físicos (fábricas, tiendas), intelectuales (patentes, marca), humanos (talento), financieros (capital).
7. **Actividades clave.** ¿Qué hace todos los días? Producción, distribución, marketing, soporte.
8. **Alianzas clave.** ¿Con quién se asocia? Proveedores, partners estratégicos, joint ventures.
9. **Estructura de costos.** ¿Dónde se le va la plata? Costos fijos (rent, salarios) vs variables (materia prima, pagos por transacción). Economías de escala o scope.

**Cómo usarlo en 30 minutos**

Para leer una empresa nueva:

1. **10 min en su sitio web:** sección "Quiénes somos", "Productos", "Clientes". Completá segmentos + propuesta de valor + canales.
2. **10 min en LinkedIn + Google News:** tamaño, contrataciones recientes, noticias. Completá recursos clave + actividades + alianzas.
3. **10 min pensando:** con la información, ¿cómo gana plata? ¿Dónde están sus costos mayores? ¿Qué economía de escala o scope puede estar buscando? Completá ingresos + costos.

Al terminar, tenés un **modelo mental** de la empresa. No perfecto, pero **suficiente para hablarle al COO como par en un primer email**.

*Fuentes: Osterwalder & Pigneur (2010). Business Model Generation. Wiley. · Blank & Dorf (2012). The Startup Owner's Manual.*

---

## Bloques 3 a 7 — Resumen para repaso

> Estos bloques están desarrollados en detalle en la **Guía Semana 3 (PDF descargable)** del material de apoyo. Acá queda el índice como repaso. El alumno debe consumir la guía completa antes de las micro-pruebas y la prueba del módulo.

**Bloque 3 — Unit economics básico: LTV, CAC, payback**

Las 3 métricas que cualquier empresa B2B mira obsesivamente. **LTV** (Lifetime Value): cuánto dinero genera un cliente promedio durante toda su relación (ticket × permanencia, ajustado por margen). **CAC** (Customer Acquisition Cost): costo total de adquirir un cliente nuevo (marketing + comercial / nuevos clientes). **Payback**: meses para recuperar el CAC. Regla estándar SaaS B2B (Skok, *SaaS Metrics 2.0*): **LTV/CAC ≥ 3x**. Si LTV/CAC < 1, la empresa pierde plata con cada cliente. El SDR no calcula unit economics pero entiende el lenguaje del CFO. Benchmarks payback: PLG 6-9m, mid-market 12-18m, enterprise 18-24m.

**Bloque 4 — Leer una industria: las 5 fuerzas de Porter**

Cualquier industria está definida por la intensidad de 5 fuerzas (Porter, 1979): (1) Rivalidad entre competidores existentes, (2) Amenaza de nuevos entrantes, (3) Amenaza de sustitutos, (4) Poder de negociación de compradores, (5) Poder de negociación de proveedores. Cuando son altas, industria dura (margen bajo); cuando son bajas, atractiva. El gancho del cold email cambia según qué fuerza presiona más: retail LATAM (rivalidad intensa, margen bajo) → "optimizar inventario por local"; banca tradicional (sustitutos fintech alta) → "acelerar onboarding digital"; minería (poder comprador alto, precios commodity) → "reducir costo por tonelada".

**Bloque 5 — Jobs to Be Done (Christensen): entender la oferta del cliente**

La gente no compra productos — contrata productos para hacer un trabajo. Un CFO no quiere reportes, quiere llegar tranquilo al board meeting. 3 dimensiones del job: (1) **Funcional** (¿qué tarea concreta debe cumplir?), (2) **Emocional** (¿cómo quiere sentirse mientras la hace?), (3) **Social** (¿cómo quiere verse ante otros?). En B2B las tres importan. Un SDR que solo vende funcional ("reducimos 17 horas") pierde las otras dos. Un SDR que integra las 3 conecta con motivación real.

**Bloque 6 — Mapeo dolor-solución**

Con BMC + Porter + JTBD, podés construir un mapeo dolor-solución bien hecho: (1) **Dolor específico** del prospecto (no genérico — "en [situación específica], la dinámica que genera dolor es Y"), (2) **Impacto cuantificado** (cuánto cuesta no resolverlo), (3) **Conexión con oferta sin prometer**. Sin los 3 bloques anteriores hechos, no hay mapeo — solo pitch disfrazado.

**Bloque 7 — El error #1 del SDR nuevo**

Vender la solución sin haber entendido el problema. Es el síntoma del que tiene cold emails que "explican bien lo que hace el producto" pero convierten al 0.4% vs el benchmark del equipo de 1.8%. 3 filtros antes de cada outreach: (1) ¿Identifiqué un dolor específico del prospecto? (2) ¿Los 2 primeros párrafos hablan del prospecto o de mí? (3) ¿La propuesta implícita es "esto PODRÍA aplicar" o "esto TE SIRVE"? Si alguno falla, rehacés.

---

**Fuentes principales del módulo:** Osterwalder & Pigneur (2010). Business Model Generation. · Porter (1979). HBR. · Christensen et al (2016). Competing Against Luck. · Skok. SaaS Metrics 2.0. · Bertuzzi (2016). The Sales Development Playbook. · Dixon & Adamson (2011). The Challenger Sale."""


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
        "title": "Guía Semana 3 — Business Acumen (PDF descargable)",
        "url": "https://drive.google.com/file/d/PLACEHOLDER_W3_GUIA",
        "order_index": 0,
    },
    {
        "kind": "pdf",
        "title": "Handout — Business acumen (Semana 3)",
        "url": "https://drive.google.com/file/d/PLACEHOLDER_W3_HANDOUT",
        "order_index": 1,
    },
    {
        "kind": "link",
        "title": "Osterwalder — Business Model Canvas (PDF)",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W3_READING_BIZ_MODEL_CANVAS",
        "order_index": 2,
    },
    {
        "kind": "link",
        "title": "Porter — The Five Competitive Forces That Shape Strategy (HBR)",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W3_READING_PORTER_5_FORCES",
        "order_index": 3,
    },
    {
        "kind": "link",
        "title": "Skok — SaaS Metrics 2.0 (LTV, CAC, payback)",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W3_READING_SAAS_METRICS",
        "order_index": 4,
    },
    {
        "kind": "link",
        "title": "Anexo — Landscape de industrias LATAM (10 industrias)",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W3_LANDSCAPE_LATAM",
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
