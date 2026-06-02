"""Seed: Semana 2 del Módulo 1 (Rol del SDR, hitos, reunión calificada).

Cierra el Módulo 1.

Estrategia de contenido (Option C híbrida — replica el pattern de seed_w1):
- `MCQ_QUESTIONS` (4 preguntas Capa 1): transcripción literal del doc
  (Parte IV §Micro-pruebas Sem 2). Fiel.
- `LESSON_BODY_ES`: híbrido. Pregunta central + Bloques 1 y 2 transcriptos
  literal del doc (lines 3219-3316). Bloques 3-7 como resumen explícito
  con nota apuntando a la "Guía Semana 2 (PDF)" que vive como recurso
  descargable.
- `AVATAR_SCRIPT_ES` y `PRESENTATION_BLOCKS_ES`: borradores sintetizados
  en estilo del doc. Conceptos fieles pero la prosa exacta es invención
  nuestra — el doc no tiene estos artefactos. Reemplazar cuando se
  produzcan las versiones finales del pipeline HeyGen.
- `RESOURCES`: incluye `PLACEHOLDER_W2_GUIA` para el PDF descargable
  generado a partir de los Bloques 1-7 del doc.

Uso:
    cd backend && .venv/bin/python -m app.scripts.seed_w2
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
log = get_logger("seed_w2")


COURSE_SLUG = "sdr-academy-v1"
MODULE_SLUG = "m1-juego-y-jugador"


LESSON_BODY_ES = """**Pregunta central de la semana:** ¿Qué vende un SDR realmente y hasta dónde llega su responsabilidad?

Al terminar, vas a poder: ubicar al SDR dentro de una función comercial B2B completa, distinguir los 5 canales de generación de demanda y cuándo aplica cada uno, explicar qué es el outbound y cuándo tiene sentido, separar los hitos que vende el SDR de los que vende el AE, aplicar los 4 criterios de una "reunión calificada" a un caso concreto, y articular qué significa un buen handoff entre SDR y AE.

---

## Bloque 1 — La arquitectura de la función comercial B2B

En la Semana 1 viste que del otro lado hay un comité de 6-10 personas. Del tuyo también hay un equipo — aunque a veces no se ve así desde afuera. Entender **qué hace cada rol de tu lado** te evita cruzar líneas que queman deals.

La función comercial moderna B2B se organiza alrededor de **4 roles principales**, cada uno con un propósito específico:

**Marketing** — genera conciencia de marca y demanda entrante (inbound). Produce contenido, webinars, ads, SEO. Opera *antes del primer contacto comercial*. Métrica principal: MQLs entregados, costo por lead.

**SDR (Sales Development Representative)** — prospecta en frío, califica leads (de marketing o generados por él mismo), agenda reuniones. Opera *de MQL/prospecto a SQL/oportunidad*. Métrica principal: reuniones calificadas agendadas.

**AE (Account Executive)** — cierra deals. Toma la reunión calificada del SDR, hace demo/discovery, negocia y firma. Opera *de oportunidad a cliente*. Métrica principal: revenue cerrado, win rate.

**CSM (Customer Success Manager)** — maneja al cliente post-venta: onboarding, uso, renovación, expansión. Opera *de cliente a renovación/churn*. Métrica principal: retención, NPS, expansión.

**Por qué existen separados**

El libro fundacional del modelo SDR moderno es *Predictable Revenue* de Aaron Ross (2011). Ross, que implementó este modelo en Salesforce, argumenta que la separación prospector/closer es lo que permite escalar. La razón tiene que ver con economía de la atención: **prospectar en frío requiere un mindset y disciplina distintos a cerrar deals**. Mezclar ambas tareas en la misma persona genera que una de las dos se sacrifique.

Un AE que también prospecta: cuando tiene deals activos (que pagan las comisiones), deja de prospectar. Resultado: pipeline que entra en olas — mucho por 2 meses, nada por 3. La empresa no puede forecastear ni planificar headcount.

Un SDR dedicado: prospecta todo el día. Pipeline que entra estable. El AE se concentra en cerrar. Los números se vuelven predecibles.

**Implicación para vos**

No sos un "AE chico". No sos un "asistente de ventas". Sos un rol específico con métricas propias. El SDR bueno que entiende esto se concentra en **lo que su rol produce** y no intenta cerrar el deal (eso es del AE) ni hacer marketing de contenido (eso es de marketing).

*Fuentes: Ross & Tyler (2011). Predictable Revenue. Capítulos 1-3. · Bertuzzi (2016). The Sales Development Playbook. Definición de los 4 roles.*

---

## Bloque 2 — Los 5 canales de generación de demanda B2B

No todo lead entra por el mismo camino. Una empresa B2B típica usa **5 canales** (o combinaciones) para generar demanda. Cada uno tiene lógica, velocidad y costo propio.

**1. Inbound.** El prospecto viene a vos. Motivado por contenido (blog, SEO, webinars), anuncios (Google Ads, LinkedIn Ads), referencias orgánicas. Cuando llega, ya investigó — suele estar en consideración o evaluación. El rol del SDR acá es **calificar** (filtrar entre los que entraron pero no son ICP vs los que sí). Ventaja: menor fricción, mayor tasa de conversión. Desventaja: volumen limitado, caro de construir.

**2. Outbound.** Vos contactás al prospecto en frío. Típicamente en awareness — no te estaba buscando. El rol del SDR es **todo el ciclo** (prospección + calificación + agendamiento). Es lo que vas a hacer los próximos 6 meses. Ventaja: escalable, predecible, focalizable (elegís a quién le hablás). Desventaja: alta fricción, tasas de respuesta bajas (1-3% típico), exige volumen.

**3. Referidos.** Alguien dentro de la empresa (un cliente feliz, un empleado, un partner) te presenta al prospecto. Es el canal de **mayor tasa de conversión** — a veces 10x más que outbound — pero de volumen variable. No se puede "forzar".

**4. ABM (Account-Based Marketing).** En vez de prospectar muchas empresas genéricamente, elegís un grupo chico de cuentas muy estratégicas (típicamente 20-50) y trabajás campañas hiper-personalizadas sobre ellas. El SDR participa, pero con lógica artesanal (no masiva).

**5. Partnerships.** Otra empresa (integrador, proveedor complementario, canal de distribución) te trae leads calificados. Es el canal de mayor apalancamiento pero el más lento de construir.

**Por qué ninguno reemplaza al otro**

Cada canal tiene una **estructura de costo y velocidad distinta**. Inbound es barato por lead pero caro de construir. Outbound es caro por lead pero rápido de arrancar. Los referidos convierten 10x pero no se escalan. ABM genera deals grandes pero tarda meses. Partnerships apalanca pero depende de otros.

Una empresa B2B madura usa **3-5 canales en paralelo**. El SDR opera principalmente en outbound, pero entiende los otros porque muchas veces se cruzan en su trabajo (prospecto que originalmente vino por inbound y no respondió, ahora lo retoma el SDR; cuenta ABM que necesita aceleración outbound; etc.).

---

## Bloques 3 a 7 — Resumen para repaso

> Estos bloques están desarrollados en detalle en la **Guía Semana 2 (PDF descargable)** del material de apoyo. Acá queda el índice como repaso de los conceptos. El alumno debe consumir la guía completa antes de las micro-pruebas y la prueba del módulo.

**Bloque 3 — Qué es outbound específicamente (y cuándo NO aplica)**

Outbound B2B = proceso sistemático para identificar empresas ICP, contactarlas en frío por múltiples canales (email + llamada + LinkedIn + WhatsApp), y llevarlas a aceptar una reunión con el AE. Funciona cuando se cumplen 3 condiciones simultáneas: (1) ICP identificable y alcanzable, (2) ticket que justifica el costo del SDR, (3) ciclo de venta que soporta múltiples touchpoints. NO aplica para productos commodity de bajo ticket, ICP masivo indiferenciado, ni ventas que dependen 100% de demo visual. Benchmarks realistas (Bridge Group 2023): 15 reuniones calificadas/mes, conversión empresa→reunión 1-3%, ramp 3-4 meses hasta productividad plena.

**Bloque 4 — Venta por hitos: la cadena completa y qué vende el SDR**

Un deal B2B completo pasa por **6 hitos secuenciales**: (1) Reunión [SDR], (2) Asistencia + Precalificación [SDR], (3) Demo [AE], (4) Propuesta [AE], (5) Cierre [AE], (6) Renovación/Expansión [CSM]. El SDR vende **solo hitos 1 y 2** — no la demo, no la propuesta, no el cierre, no la renovación. Cruzar hitos (dar precio, hacer mini-demos por teléfono, ofrecer descuentos) arruina la venta del AE. Regla práctica: ante preguntas de producto/precio/concesión, redirigir al AE — "Excelente pregunta, [AE] tiene visibilidad completa; en la reunión lo discuten".

**Bloque 5 — Reunión calificada: los 4 criterios**

Una reunión es **calificada** si y solo si cumple los 4 criterios acumulativamente: (1) Empresa dentro del ICP (industria + tamaño + geografía + características relevantes), (2) Contacto es KDM o champion/referidor validado con llegada al decisor, (3) Asiste a la reunión el día agendado, (4) Pasa la precalificación mínima (existe el problema, no hay bloqueador absoluto, timing razonable). Si falta uno, no cuenta como calificada — y no debió generarse. La métrica del SDR es reuniones calificadas, no reuniones agendadas. Agendar 10 reuniones basura es peor que agendar 5 calificadas.

**Bloque 6 — El handoff al AE como momento sagrado**

El handoff es la transferencia formal del prospecto del SDR al AE. Información que pasa (en 1 página): empresa (nombre, industria, tamaño, señal usada), contacto (rol, responsabilidad, LinkedIn), contexto del outreach (qué ángulo funcionó), precalificación con framework Situación → Necesidad → Timing, advertencias (otros stakeholders, bloqueadores potenciales). NO pasa: especulaciones sin base, info irrelevante, chismes. Un handoff pobre quema deals que el AE podría haber cerrado — entra a ciegas a la reunión, pregunta cosas que el SDR ya validó, pierde la confianza del prospecto.

**Bloque 7 — Mindset del SDR: ejecutor con criterio**

El SDR es **ejecutor** (volumen, disciplina, consistencia es la variable #1 del rendimiento) Y **con criterio** (cada acción exige decisión: a quién contactar, cómo abrir, cómo redirigir cruces de hito, qué calificar). NO es operario (mandar 200 emails idénticos sin pensar), NO es cazador de comisiones (cualquier reunión vale), NO es asistente del AE (no es subordinado). El path típico de carrera: SDR → AE → Senior AE → Sales Manager → Director Comercial. Los fundamentos del módulo (anatomía B2B, hitos, calificación, handoff) sirven los próximos 10 años de carrera en ventas B2B.

---

**Fuentes principales del módulo:** Ross & Tyler (2011). Predictable Revenue. · Bertuzzi (2016). The Sales Development Playbook. · Blount (2015). Fanatical Prospecting. · Bridge Group (2023). SDR Metrics & Compensation Report. · Instantly (2026). Cold Email Benchmark Report."""


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
        "title": "Guía Semana 2 — Rol del SDR, hitos y reunión calificada (PDF descargable)",
        "url": "https://drive.google.com/file/d/PLACEHOLDER_W2_GUIA",
        "order_index": 0,
    },
    {
        "kind": "pdf",
        "title": "Handout — Rol del SDR e hitos (Semana 2)",
        "url": "https://drive.google.com/file/d/PLACEHOLDER_W2_HANDOUT",
        "order_index": 1,
    },
    {
        "kind": "link",
        "title": "Bridge Group — SDR Metrics & Compensation Report 2023",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W2_READING_SDR_METRICS",
        "order_index": 1,
    },
    {
        "kind": "link",
        "title": "Instantly — Cold Email Benchmark Report 2026",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W2_READING_COLD_EMAIL_BENCH",
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
