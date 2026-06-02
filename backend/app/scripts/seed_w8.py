"""Seed: Semana 8 del Módulo 4 (Del proceso al mindset de mejora continua).

Cierra el Módulo 4 — "El sistema" y cierra el curso asincrónico. Contenido
extraído de SDR_Academy_Siete_Documento_Maestro.md (bloques 1-7 de Semana 8 +
4 micro-pruebas MCQ Capa 1).

Reutiliza el módulo `m4-el-sistema` (order_index=3, creado por seed_w7) y agrega
la segunda lección (order_index=1) con la secuencia dinámica completa.

Uso:
    cd backend && .venv/bin/python -m app.scripts.seed_w8
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
log = get_logger("seed_w8")


COURSE_SLUG = "sdr-academy-v1"
MODULE_SLUG = "m4-el-sistema"
LESSON_ORDER_INDEX = 1


LESSON_BODY_ES = """Pregunta central de la semana: ¿Cómo se ejecuta esto todos los días y cómo se sabe si está funcionando?

**Dato crudo:** una decisión de 30 minutos (saltar la limpieza de lista) cuesta 3 semanas de recuperación cuando el dominio se quema. Las etapas tempranas del proceso son infraestructura — romperlas contamina todo lo que venga después. Por eso el SDR senior invierte 30-40% del tiempo en preparación aunque "no se vea" en las métricas de reuniones.

## Bloque 1 — El proceso outbound end-to-end (10 etapas)
**ICP → listas → limpieza/validación → diseño de secuencia → ejecución diaria → gestión de respuestas → calificación → agendamiento → precalificación → handoff al AE.** El orden importa. Saltar un paso no rompe solo ese paso — rompe todo lo que viene después. Las primeras 3 etapas son infraestructura: invisibles en las métricas de reuniones, devastadoras cuando fallan.

## Bloque 2 — Armado de listas de calidad
Fuentes (Apollo, ZoomInfo, listas de eventos), filtros (industria, tamaño, geografía, señal de timing) y señales (ronda Series B+, expansión, contratación, M&A, regulación). Qué separa una lista buena de una basura. **"Cuantos más contactos, mejor" es falso** — una lista de 5.000 contactos con 30% de ruido produce menos reuniones que una de 1.500 limpios con señal verificable.

## Bloque 3 — Limpieza y validación: por qué NO es opcional
La cadena del daño cuando se salta esta etapa: bounces altos → reputación del dominio cae (Postmaster lo detecta) → proveedores clasifican como bulk sender → los **siguientes** emails (incluso a contactos validados) caen a spam → reply rate del sistema entero se hunde por semanas. **Una decisión de 30 minutos cuesta 3 semanas de recuperación.** Por eso esta etapa NO es opcional.

## Bloque 4 — Ejecución diaria
Bloques de tiempo, batching de actividades (todas las llamadas juntas, todos los emails juntos), gestión de múltiples cuentas en paralelo, cómo no perder el foco. Base teórica: **Teoría de constraints (Goldratt, 1984)** aplicada al cuello de botella humano — la atención del SDR es el recurso escaso, todo el sistema se diseña alrededor de protegerlo. El antipatrón: alternar entre activitis cada 5 minutos.

## Bloque 5 — Métricas del outbound: qué mide cada una + por qué NO se mide open rate
**Bounce rate** (salud de lista + reputación), **reply rate** (relevancia mensaje + deliverability), **meeting rate sobre reply** (calidad del flujo), **show rate** (calidad agendamiento), **precalificación aprobada** (calidad del filtro), **conversión empresa-a-reunión** (síntesis). Cuál es síntoma y cuál es causa. **NO se mide open rate** por 4 razones combinadas: (1) el pixel de tracking daña deliverability — los filtros anti-spam lo detectan; (2) Apple Mail Privacy Protection pre-abre en servidores → infla el dato artificialmente; (3) Outlook y Gmail con imágenes off subestiman; (4) reply rate + bounce rate son señales comportamentales/técnicas más duras que reemplazan al open rate.

## Bloque 6 — Diagnóstico por descarte
Cómo se encuentra la causa raíz de una métrica caída **recorriendo el funnel de arriba a abajo**, sin tocar variables al azar. **Principio:** un problema en el paso N se detecta por la métrica del paso N+1. El SDR aprende a hacer el recorrido — NO a memorizar "los 6 flujos canónicos". El SDR novato salta al mensaje o al ICP porque son las variables que cree controlar. El SDR bueno recorre el funnel en orden y **descarta con datos**, no con intuición. Las métricas colaterales son el filtro del descarte.

## Bloque 7 — Mindset de mejora continua: PDCA + Build-Measure-Learn
Cómo el SDR lee señales del día a día (objeciones recurrentes, respuestas reales, patrones) y las convierte en **hipótesis testeables**. Una hipótesis testeable cumple 3 condiciones: (1) formulación tipo "si X → entonces Y"; (2) variable única y acotada (NO cambias copy + cadencia + ICP al mismo tiempo); (3) método de medición declarado (ventana de tiempo + métrica + comparación antes/después). Base: **PDCA de Deming (1982)** + **Build-Measure-Learn de Ries (2011)**. El SDR novato salta a "cambiar algo" sin aislar qué; el SDR bueno aísla una variable y mide.

**Síntesis del curso:** lo que separa a un SDR bueno de uno promedio no es la herramienta, ni el cliente, ni el mercado — es la capacidad de leer señales del día a día y convertirlas en experimentos. Si te vas con plantillas, te vas con cero. Si te vas con criterio para diagnosticar y método para mejorar, te vas con todo.

**Fuentes:** Goldratt (1984). Deming (1982). Ries (2011). Bertuzzi (2016). Bridge Group (2023). Instantly (2026). Apple Mail Privacy Protection docs (2021+). Google Postmaster Tools."""


AVATAR_SCRIPT_ES = """Semana 8. Cierre del Módulo 4 y cierre del curso asincrónico. La pregunta central: ¿cómo se ejecuta esto todos los días y cómo se sabe si está funcionando?

Esta es la semana más intensa del curso. Te lo aviso con anticipación. Tenés ~7 horas entre contenido, ejercicios, micro-pruebas, cierre de la prueba final y la sesión en vivo. Apartá el tiempo.

Lo más importante de toda la semana: el SDR senior invierte treinta a cuarenta por ciento de su tiempo en preparación. En cosas que no se ven en las métricas de reuniones — armar listas, limpiarlas, planificar bloques de tiempo. El SDR junior recorta ahí "para ganar tiempo". Y termina con el dominio quemado y tres semanas de recuperación encima.

Siete bloques. Primero, el proceso outbound end-to-end: las diez etapas en orden, y qué se rompe si te salteás una. Segundo, armado de listas — por qué "cuantos más contactos mejor" es falso. Tercero, limpieza y validación — por qué no es opcional y qué cadena de daño dispara saltarla. Cuarto, ejecución diaria: bloques de tiempo, batching, teoría de constraints aplicada al cuello de botella humano. Quinto, las métricas del outbound — y por qué ya no se mide open rate. Sexto, diagnóstico por descarte: cómo se encuentra la causa raíz de una métrica caída sin tocar variables al azar. Séptimo, mindset de mejora continua: PDCA y Build-Measure-Learn — cómo se transforma una señal del día a día en hipótesis testeable.

Una regla que te llevás ya: cuando una métrica cae, un problema en el paso N se detecta por la métrica del paso N+1. Si el show rate cayó, no toques el mensaje. Andá a la etapa de agendamiento — confirmación de fecha, hora, canal, invitación de calendario, recordatorio. Las métricas colaterales que están estables son el filtro del descarte.

Cuatro micro-pruebas al final. La cuarta integra todo: te exige discriminar una hipótesis testeable de una intuición disfrazada. Es la pregunta que cierra el curso. Vamos."""


PRESENTATION_BLOCKS_ES = [
    {
        "title": "Proceso outbound end-to-end — 10 etapas",
        "bullets": [
            "ICP → listas → limpieza → diseño secuencia → ejecución",
            "→ gestión respuestas → calificación → agendamiento → precal → handoff",
            "El ORDEN importa — saltar un paso rompe lo que viene después",
            "Primeras 3 etapas = INFRAESTRUCTURA (invisibles, devastadoras si fallan)",
        ],
        "source": "Bertuzzi 2016 + Predictable Revenue",
    },
    {
        "title": "Armado de listas de calidad",
        "bullets": [
            "Fuentes: Apollo, ZoomInfo, listas de eventos",
            "Filtros: industria, tamaño, geografía, señal de timing",
            "Señales: Series B+, expansión, contratación, M&A, regulación",
            "'Más contactos = mejor' es FALSO",
            "5.000 con 30% ruido < 1.500 limpios con señal verificable",
        ],
        "source": "Bertuzzi 2016 + Outbound Kitchen 2025",
    },
    {
        "title": "Limpieza y validación — NO opcional",
        "bullets": [
            "Cadena del daño cuando se salta:",
            "Bounces altos → reputación cae (Postmaster) → bulk sender",
            "→ siguientes emails (incluso correctos) caen a spam",
            "→ reply rate del SISTEMA se hunde por semanas",
            "30 min ahorrados = 3 semanas de recuperación",
        ],
        "source": "Google Postmaster + experiencia operativa",
    },
    {
        "title": "Ejecución diaria — Teoría de constraints",
        "bullets": [
            "Bloques de tiempo + batching (llamadas juntas, emails juntos)",
            "Gestión de múltiples cuentas en paralelo",
            "Atención del SDR = recurso escaso (Goldratt 1984)",
            "Todo el sistema se diseña alrededor de protegerla",
            "Antipatrón: alternar activitis cada 5 min",
        ],
        "source": "Goldratt 1984, The Goal",
    },
    {
        "title": "Métricas — y por qué NO se mide open rate",
        "bullets": [
            "Bounce / reply / meeting-sobre-reply / show / precal aprobada / conversión",
            "Cuál es síntoma vs causa",
            "NO open rate por: pixel daña deliverability",
            "+ Apple MPP pre-abre en servidor (infla 50% del mercado)",
            "+ Outlook/Gmail-imgs-off subestima",
            "+ reply/bounce son señales más duras y confiables",
        ],
        "source": "Bridge Group + Apple MPP docs",
    },
    {
        "title": "Diagnóstico por descarte",
        "bullets": [
            "Recorré el funnel de ARRIBA a ABAJO — no toques variables al azar",
            "Principio: problema en paso N se detecta por métrica del paso N+1",
            "SDR novato: salta al mensaje o ICP (lo que cree controlar)",
            "SDR bueno: descarta con DATOS — métricas colaterales son el filtro",
            "Si show rate cayó: empezás en etapa 8, NO en el mensaje",
        ],
        "source": "Bloque 5 + método sistémico",
    },
    {
        "title": "Mindset de mejora continua — PDCA + B-M-L",
        "bullets": [
            "Hipótesis testeable — 3 condiciones:",
            "1. Formulación 'si X → entonces Y'",
            "2. Variable única y acotada (NO cambies 3 cosas a la vez)",
            "3. Método de medición declarado (ventana + métrica + antes/después)",
            "Deming 1982 (PDCA) + Ries 2011 (Build-Measure-Learn)",
            "Lectura de señal + experimento > 'cambiar algo'",
        ],
        "source": "Deming 1982 + Ries 2011",
    },
]


MCQ_QUESTIONS = [
    {
        "id": "q1",
        "block": 3,
        "type": "single",
        "prompt": (
            "Un SDR nuevo tiene que empezar a mandar una campaña el lunes. Le dan una lista de "
            "2.500 contactos de Apollo. Para ganar tiempo, decide SALTAR la etapa 3 (limpieza y "
            "validación) y empezar a enviar directamente. ¿Cuál es la consecuencia aguas abajo "
            "MÁS GRAVE?"
        ),
        "choices": [
            {
                "id": "a",
                "text": (
                    "El SDR va a necesitar responder más emails porque muchos van a rebotar y "
                    "volver con error. Ruido operativo los primeros días."
                ),
            },
            {
                "id": "b",
                "text": (
                    "Los prospectos con emails genéricos (info@, contacto@) pueden reenviar a "
                    "la persona equivocada, generando confusión sobre quién es el decisor."
                ),
            },
            {
                "id": "c",
                "text": (
                    "El bounce rate sube por encima del umbral crítico → reputación del dominio "
                    "cae → los emails SIGUIENTES (incluso los que iban a contactos validados) "
                    "caen a spam → reply rate del sistema completo se derrumba por semanas."
                ),
            },
            {
                "id": "d",
                "text": (
                    "Se pierde el 10-15% de los contactos porque eran emails no válidos, lo que "
                    "reduce la muestra efectiva pero no afecta el resto."
                ),
            },
        ],
        "correct": ["c"],
        "explanation": (
            "La etapa 3 (limpieza y validación) no se salta porque genera DAÑO AMPLIFICADO "
            "aguas abajo, no solo daño local. Cadena del daño: bounces altos → reputación cae "
            "(Postmaster) → proveedores clasifican como bulk sender → los SIGUIENTES emails "
            "(incluso los correctos) caen a spam → reply rate se hunde en todo el sistema. Una "
            "decisión de 30 minutos cuesta 3 semanas de recuperación. (a) ruido operativo es "
            "cierto pero menor — el problema no es responder más, es que el sistema entero se "
            "rompe. (b) emails genéricos existen pero NO son consecuencia de saltar validación "
            "— es un problema separado. (d) confunde PÉRDIDA LOCAL (esos contactos puntuales) "
            "con DAÑO SISTÉMICO (reputación). Regla general: en outbound, las etapas tempranas "
            "del proceso son INFRAESTRUCTURA. Romper infraestructura no afecta solo a lo que "
            "pasa ahora — contamina todo lo que venga hasta que se repara."
        ),
    },
    {
        "id": "q2",
        "block": 6,
        "type": "single",
        "prompt": (
            "Tabla semanal del SDR Mariana: Bounce rate estable ~2.1% / Reply rate estable "
            "~2.4% / Meeting rate sobre reply estable ~27% / Show rate cayó de 73-74% a 48% en "
            "Sem 4 / Precalificación aprobada estable ~88%. Mariana NO cambió su proceso. ¿Cuál "
            "es la PRIMERA ETAPA del proceso que debería revisar siguiendo diagnóstico por "
            "descarte?"
        ),
        "choices": [
            {
                "id": "a",
                "text": (
                    "Etapa 1 (ICP) — quizás está agendando gente fuera del perfil y por eso no "
                    "se presenta."
                ),
            },
            {
                "id": "b",
                "text": (
                    "Etapa 8 (Agendamiento) — donde se observa el síntoma; revisar cómo se "
                    "confirma la reunión (fecha, hora, canal, invitación de calendario, "
                    "recordatorio)."
                ),
            },
            {
                "id": "c",
                "text": (
                    "Etapa 4 (Diseño de secuencia) — probablemente el mensaje que llevó a la "
                    "reunión no explicó bien qué se iba a ver."
                ),
            },
            {
                "id": "d",
                "text": (
                    "Etapa 10 (Handoff al AE) — si el AE no recibe bien al prospecto, el "
                    "prospecto no vuelve."
                ),
            },
        ],
        "correct": ["b"],
        "explanation": (
            "Método de diagnóstico por descarte (Bloque 6): un problema en el paso N se detecta "
            "por la métrica del paso N+1. El show rate es la métrica de la etapa 8 "
            "(agendamiento) — el primer lugar donde buscar es la etapa 8 misma: ¿se está "
            "confirmando fecha + hora + canal + quién participa? ¿Los prospectos reciben "
            "invitación de calendario? ¿Hay recordatorio 24-48 h antes? (a) si el problema "
            "fuera ICP, OTRAS métricas aguas abajo también se habrían roto (meeting rate sobre "
            "reply, precal). Están estables → descartás ICP por métricas colaterales. (c) misma "
            "lógica — si el mensaje inflara expectativas, meeting-sobre-reply o precal se "
            "habrían movido. Estables → descartás. (d) handoff ocurre DESPUÉS del show rate, no "
            "antes — error de dirección del análisis. Lección: el SDR novato salta al mensaje o "
            "ICP porque son las variables que cree controlar. El SDR bueno RECORRE el funnel en "
            "orden y descarta con datos."
        ),
    },
    {
        "id": "q3",
        "block": 5,
        "type": "multi",
        "prompt": (
            "El Team Lead explica por qué el outbound B2B moderno YA NO mide open rate como "
            "métrica principal. Marcá TODAS las razones técnicamente correctas:"
        ),
        "choices": [
            {
                "id": "1",
                "text": (
                    "El pixel de tracking daña deliverability — los filtros anti-spam lo "
                    "detectan y clasifican el email como marketing."
                ),
            },
            {
                "id": "2",
                "text": (
                    "Apple Mail Privacy Protection pre-abre los emails en el servidor antes de "
                    "entregarlos → infla el open rate artificialmente."
                ),
            },
            {
                "id": "3",
                "text": (
                    "Los prospectos ya saben que hay tracking y directamente no abren emails de "
                    "desconocidos."
                ),
            },
            {
                "id": "4",
                "text": (
                    "Otros clientes (Outlook, Gmail con imágenes apagadas) devuelven open=false "
                    "aunque el prospecto lea el email — el dato se vuelve ruidoso."
                ),
            },
            {
                "id": "5",
                "text": (
                    "El reply rate y el bounce rate son datos comportamentales/técnicos más "
                    "duros y confiables que reemplazan al open rate como señal."
                ),
            },
            {
                "id": "6",
                "text": (
                    "El open rate siempre fue un dato manipulable (el prospecto podía abrir y "
                    "cerrar sin leer) y por eso nunca tuvo valor."
                ),
            },
        ],
        "correct": ["1", "2", "4", "5"],
        "explanation": (
            "Correctas 1, 2, 4, 5. (1) El pixel es una imagen invisible que canta cuando se "
            "abre — filtros anti-spam lo detectan y mandan el email a promociones/spam. El "
            "costo de medir open rate es que el email NI LLEGA al inbox. (2) Apple Mail Privacy "
            "Protection (activo desde 2021) pre-abre en servidores de Apple → 'open' automático "
            "sin que nadie haya leído. El dato queda inflado para el ~50% del mercado. (4) "
            "Outlook y Gmail con imágenes off NUNCA disparan el pixel aunque el prospecto lea. "
            "Combinación de 2+4 = ruido bidireccional (inflado por Apple, subestimado por "
            "Outlook/Gmail). (5) reply rate (dato comportamental duro — respondió) y bounce "
            "rate (dato técnico) son señales más confiables, no dependen de pixels ni de "
            "pre-apertura. NO correctas: (3) los prospectos pueden saber o no del tracking — el "
            "problema es ESTRUCTURAL (distorsión del dato + daño deliverability), no cultural. "
            "(6) el open rate sí tuvo valor entre ~2015-2020. La manipulación nunca fue el "
            "problema principal — el problema es la degradación técnica (Apple MPP + filtros) "
            "desde 2021. Razón de contexto, no de método."
        ),
    },
    {
        "id": "q4",
        "block": 7,
        "type": "single",
        "prompt": (
            "Un SDR identifica una señal en su día a día: 3 prospectos de retail respondieron "
            "que están con un proyecto grande de migración a Shopify y todo lo demás está "
            "pausado hasta Q4. El SDR quiere 'hacer algo con esto' para mejorar su tasa de "
            "respuesta en retail. ¿Cuál de las siguientes es una HIPÓTESIS TESTEABLE (no una "
            "intuición)?"
        ),
        "choices": [
            {
                "id": "a",
                "text": (
                    "Voy a cambiar el copy para empresas de retail — probablemente el mensaje "
                    "actual no les habla."
                ),
            },
            {
                "id": "b",
                "text": (
                    "El retail es un mercado difícil ahora; tengo que bajar mi expectativa de "
                    "reply rate para esa industria hasta fin de año."
                ),
            },
            {
                "id": "c",
                "text": (
                    "Si filtro empresas de retail que anunciaron migración a Shopify en los "
                    "últimos 60 días (señal pública detectable en LinkedIn y prensa) y las "
                    "archivo con trigger de recontacto en Q4, mi tasa efectiva de retail "
                    "debería subir porque dejo de insistir sobre empresas pausadas. Lo testeo 4 "
                    "semanas midiendo reply rate retail antes/después de aplicar el filtro."
                ),
            },
            {
                "id": "d",
                "text": (
                    "Voy a mandarle a estos 3 prospectos un caso de éxito de Shopify para que "
                    "vean que entiendo su momento."
                ),
            },
        ],
        "correct": ["c"],
        "explanation": (
            "Una hipótesis testeable cumple 3 condiciones (Bloque 7 — PDCA + Build-Measure"
            "-Learn): (1) formulación 'si X → entonces Y' (acá: 'si filtro empresas con señal "
            "de migración Shopify → reply rate retail sube'); (2) variable ÚNICA y acotada "
            "(filtrar por una señal específica — no cambia copy, ni cadencia, ni nada más); "
            "(3) método de medición declarado (4 semanas, comparando reply rate retail "
            "antes/después). Datos, no sensación. Además incluye el mecanismo lógico (estas "
            "empresas están pausadas, no no-fit), lo que permite decidir qué hacer si el test "
            "falla. (a) intuición — 'probablemente el mensaje no les habla' no define qué va a "
            "cambiar ni cómo lo va a medir. Cambiar copy sin método de medición no es PDCA. "
            "(b) es RESIGNACIÓN, no hipótesis — no propone acción ni test. (d) acción puntual "
            "sobre 3 prospectos específicos. No escala a regla general ni define cómo medir si "
            "funcionó. Trabajo artesanal sobre cuentas concretas, no hipótesis sobre el "
            "sistema. Lección: el SDR bueno lee una señal y la transforma en una hipótesis con "
            "variable única + método de medición. El SDR novato salta a 'cambiar algo' sin "
            "aislar qué."
        ),
    },
]


RESOURCES = [
    {
        "kind": "pdf",
        "title": "Guía Semana 8 — Proceso, métricas y mejora continua (PDF descargable)",
        "url": "https://drive.google.com/file/d/PLACEHOLDER_W8_GUIA",
        "order_index": 0,
    },
    {
        "kind": "pdf",
        "title": "Handout — Del proceso al mindset de mejora continua (Semana 8)",
        "url": "https://drive.google.com/file/d/PLACEHOLDER_W8_HANDOUT",
        "order_index": 1,
    },
    {
        "kind": "doc",
        "title": "Checklist — Proceso outbound end-to-end (10 etapas)",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W8_PROCESS",
        "order_index": 2,
    },
    {
        "kind": "doc",
        "title": "Plantilla — Diagnóstico por descarte (recorrido de funnel)",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W8_DIAGNOSIS",
        "order_index": 3,
    },
    {
        "kind": "doc",
        "title": "Plantilla — Formulación de hipótesis testeable (3 condiciones)",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W8_HYPOTHESIS",
        "order_index": 4,
    },
    {
        "kind": "doc",
        "title": "Tablero de métricas semanal — plantilla SDR (bounce/reply/meeting/show/precal)",
        "url": "https://docs.google.com/spreadsheets/d/PLACEHOLDER_W8_DASHBOARD",
        "order_index": 5,
    },
    {
        "kind": "link",
        "title": "Bridge Group — SDR Metrics Report 2023 (benchmarks por métrica)",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W8_READING_SDR_METRICS",
        "order_index": 6,
    },
    {
        "kind": "link",
        "title": "Apple — Mail Privacy Protection documentation (por qué no se mide open rate)",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W8_READING_APPLE_MPP",
        "order_index": 7,
    },
    {
        "kind": "link",
        "title": "Ries — Build-Measure-Learn (resumen The Lean Startup)",
        "url": "https://docs.google.com/document/d/PLACEHOLDER_W8_READING_LEAN_PRINCIPLES",
        "order_index": 8,
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
            duration_seconds=1500,
        )
        lesson.translations.append(
            LessonTranslation(
                locale="es",
                title="Semana 8 — Del proceso al mindset de mejora continua",
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
        tr_es.title = "Semana 8 — Del proceso al mindset de mejora continua"
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
            title="Micro-pruebas — Semana 8",
            config=config,
            passing_score=65.0,
        )
        db.add(a)
        db.commit()
        db.refresh(a)
        log.info("assessment.seeded", extra={"assessment_id": a.id})
        return a
    existing.title = "Micro-pruebas — Semana 8"
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
            "seed_w8.done",
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
