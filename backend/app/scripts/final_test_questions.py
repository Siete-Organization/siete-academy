"""Contenido Capa 3 — Prueba Final del curso (SDR Academy Siete).

Caso integrador: GestaLogix (SaaS B2B de trazabilidad farmacéutica para
distribuidores en MX/CO/PE).

Fuente de verdad: guiones_videos/v2/guiones_corregidos_NICO/LIMPIO_PRUEBAS_FINAL.md
(v1, 2026-06-13). NICO rediseñó el caso a **16 MCQ de respuesta única 100%
autocorregibles** (antes: híbrido con respuestas cortas + tablas manuales).

Estructura del examen:
- Caso escrito: 16 ítems MCQ, puntaje **ponderado /42** (6 ítems × 2 pts + 10 ítems
  × 3 pts). Se autocalifica entero (no requiere corrección manual). Pesa 70%.
- Video de defensa (~8 min, 1 toma) con rúbrica de 15 dimensiones (/30). Pesa 30%.

Shape de los datos:
- MCQ: lista de preguntas con ``points`` (2 o 3) y ``correct`` (compatible con
  ``sum_mcq_points`` / ``auto_grade_mcq``). Las 4 diferenciadoras llevan
  ``differentiator: True``.
- SHORT_ANSWERS / TABLES: vacías (el rediseño de NICO no tiene componentes manuales;
  se conservan los símbolos por compatibilidad con el seeder y el grading).
- VIDEO_RUBRIC_15: rúbrica del video (15 dimensiones × 0-2 = /30; 6 críticas).
- DIFFERENTIATOR_IDS: preguntas que cuentan para distinción (≥75% = ≥9/12).
"""

CASE_BRIEF: dict = {
    "title": "GestaLogix — SaaS B2B de trazabilidad farmacéutica (MX/CO/PE)",
    "summary": (
        "GestaLogix es una empresa SaaS B2B que vende una plataforma de gestión "
        "logística y trazabilidad a distribuidores farmacéuticos medianos y grandes en "
        "México, Colombia y Perú. Fundada en 2022 por tres profesionales de la industria "
        "farmacéutica. Serie A de USD 8M cerrada en marzo de 2025 (un fondo de Ciudad de "
        "México y dos family offices peruanos). 40 empleados al cierre de 2025; plan de "
        "crecer a 70 durante 2026. Ticket promedio del cliente final: USD 35K-70K anuales."
    ),
    "platform": [
        "Trazabilidad de lotes (seriación, caducidad, retiros).",
        "Cadena de frío (sensores y alertas automáticas).",
        "Control de inventario en tiempo real (múltiples bodegas).",
        "Cumplimiento regulatorio (COFEPRIS en México, INVIMA en Colombia, DIGEMID en Perú).",
        "Reportería para auditorías (integración con el ERP del cliente).",
    ],
    "market_context": (
        "La industria farmacéutica de la región está bajo presión regulatoria creciente "
        "sobre trazabilidad y cumplimiento, con sanciones por incumplimiento. Los "
        "distribuidores tradicionales dependen de sistemas heredados (ERP más planillas más "
        "procesos manuales). El cumplimiento regulatorio es el principal motor de la "
        "conversación actual. Los competidores internacionales (TraceLink, Systech) son "
        "caros y tienen implementaciones de 12-18 meses; GestaLogix se posiciona como la "
        "alternativa regional: implementación en 3-4 meses y alrededor de 40% más económica."
    ),
    "client_expectations": {
        "meetings_per_month": "10 reuniones calificadas/mes a partir del mes 2",
        "icp": "Distribuidores farmacéuticos con 50-500 empleados, con operación en al menos 2 de los 3 países (MX/CO/PE)",
        "target_decision_maker": "VP de Operaciones, Director de Cadena de Suministro o Gerente de Cumplimiento Regulatorio",
        "average_ticket": "USD 50K anuales por negocio cerrado",
        "decision_timeline": "3-6 meses (ciclo de compra B2B enterprise)",
    },
}


# ─────────────────────────────  MCQ AUTO-GRADABLES (/42)  ────────────────────────
# 6 ítems de 2 puntos (1.1, 1.3, 2.2, 3.A.1, 3.B.1, 6.2) + 10 ítems de 3 puntos
# (1.4, 2.1, 3.A.2, 3.B.2, 4.1, 4.3, 5.2, 5.3, 6.1, 6.3) = 42 puntos.

MCQ: list[dict] = [
    {
        "id": "P1.1",
        "stage": 1,
        "topic": "Business Model Canvas — componente más diferenciador",
        "type": "single",
        "points": 2,
        "prompt": (
            "Lees el modelo de negocio de GestaLogix con el Business Model Canvas. ¿Cuál de "
            "sus componentes es el más diferenciador competitivamente, según el brief?"
        ),
        "choices": [
            {"id": "a", "text": "Las alianzas clave: el respaldo de la Serie A (un fondo mexicano y dos family offices peruanos) es lo que les da espalda para diferenciarse."},
            {"id": "b", "text": "Los recursos clave: el equipo fundador con experiencia en la industria farmacéutica regional es el activo que los separa del resto."},
            {"id": "c", "text": "La propuesta de valor: alternativa regional, implementación en 3-4 meses y alrededor de 40% más económica que los competidores internacionales, sobre un motor de cumplimiento creciente."},
            {"id": "d", "text": "Las fuentes de ingresos: el modelo de suscripción anual de USD 35K-70K por cliente es lo que sostiene la diferencia."},
        ],
        "correct": "c",
        "explanation": (
            "La propuesta de valor (regional + 3-4 meses + 40% más barata, sobre un motor "
            "regulatorio creciente) es lo que los separa del resto del mercado."
        ),
    },
    {
        "id": "P1.3",
        "stage": 1,
        "topic": "Jobs to Be Done — el trabajo que GestaLogix reemplaza",
        "type": "single",
        "points": 2,
        "prompt": (
            "Si GestaLogix no existiera, ¿qué estaría haciendo hoy el área de operaciones de "
            "un distribuidor farmacéutico mediano para cumplir con la trazabilidad? Es decir, "
            "¿cuál es el trabajo por resolver (Jobs to Be Done) que GestaLogix reemplaza?"
        ),
        "choices": [
            {"id": "a", "text": "Contrata consultores externos antes de cada auditoría para que le armen la reportería a tiempo."},
            {"id": "b", "text": "Sostiene a mano una mezcla de ERP heredado, planillas para lotes y cadena de frío, y reportería manual antes de cada auditoría; el trabajo de fondo es cumplir con la regulación sin frenar las operaciones."},
            {"id": "c", "text": "Busca reducir el gasto en tecnología y consolidar a sus proveedores de software en un solo contrato anual."},
            {"id": "d", "text": "Arma un plan de transformación digital a varios años porque se lo pidió la dirección general."},
        ],
        "correct": "b",
        "explanation": (
            "El JTBD dominante es \"cumplir con la regulación sin frenar las operaciones\". "
            "Hoy se resuelve a mano (ERP heredado + planillas + reportería manual). Las otras "
            "son piezas parciales o desvían el foco."
        ),
    },
    {
        "id": "P1.4",
        "stage": 1,
        "topic": "Dolor dominante accionable del decisor (DIFERENCIADORA)",
        "differentiator": True,
        "type": "single",
        "points": 3,
        "prompt": (
            "El VP de Operaciones de un distribuidor farmacéutico de 300 empleados en México "
            "está bajo la presión de COFEPRIS. ¿Cuál es su dolor dominante más accionable en "
            "una primera conversación con un SDR?"
        ),
        "choices": [
            {"id": "a", "text": "Le preocupa el costo anual de las licencias de su ERP heredado y le gustaría renegociarlo con el proveedor."},
            {"id": "b", "text": "La dirección le fijó como objetivo del año reducir la cantidad de proveedores de tecnología de la empresa."},
            {"id": "c", "text": "La integración del sistema actual le da problemas, aunque ese tema en la práctica lo lleva el área de tecnología y no la suya."},
            {"id": "d", "text": "Cada auditoría le consume semanas de un equipo chico y ya tuvo una sanción menor el año pasado; si se repite, la próxima sería grave."},
        ],
        "correct": "d",
        "explanation": (
            "Un dolor accionable es específico, cuantificable, con consecuencia presente y propio "
            "del rol. (a) es de compras, (b) es ajeno al dolor operativo, (c) lo lleva otra área."
        ),
    },
    {
        "id": "P2.1",
        "stage": 2,
        "topic": "Clasificación de criterios del ICP (duro / señal / negativo)",
        "type": "single",
        "points": 3,
        "prompt": (
            "Estos son los 9 criterios candidatos para el ICP de GestaLogix:\n\n"
            "1) Distribuidor farmacéutico (industria)\n"
            "2) Entre 50 y 500 empleados\n"
            "3) Operación en al menos 2 de México, Colombia o Perú\n"
            "4) Anunció recientemente la apertura de una nueva bodega o centro de distribución\n"
            "5) Recibió una sanción regulatoria reciente (COFEPRIS, INVIMA o DIGEMID)\n"
            "6) Ya trabaja con TraceLink o Systech (competencia directa)\n"
            "7) Contrató un Gerente de Cumplimiento Regulatorio en los últimos 6 meses\n"
            "8) Levantó una ronda de inversión en los últimos 12 meses\n"
            "9) Ya es cliente actual de GestaLogix\n\n"
            "¿Cuál de las siguientes opciones clasifica correctamente los 9 criterios como Duro "
            "(estructural, define quién entra), Señal (disparador de compra) o Negativo (descartar)?"
        ),
        "choices": [
            {"id": "a", "text": "Duros: 1, 2, 3 · Señales: 4, 5, 7, 8 · Negativos: 6, 9."},
            {"id": "b", "text": "Duros: 1, 2, 3, 8 · Señales: 4, 5, 7 · Negativos: 6, 9."},
            {"id": "c", "text": "Duros: 1, 2, 3 · Señales: 4, 5, 6, 7, 8 · Negativos: 9."},
            {"id": "d", "text": "Duros: 1, 2 · Señales: 3, 4, 5, 7, 8 · Negativos: 6, 9."},
        ],
        "correct": "a",
        "explanation": (
            "Duros = estructura (industria, tamaño, geografía). Señales = disparadores (bodega, "
            "sanción, contratación de cumplimiento, ronda). Negativos = competencia directa (6) y "
            "cliente actual (9). (b) sube la ronda a duro; (c) clasifica la competencia como señal; "
            "(d) baja la geografía a señal."
        ),
    },
    {
        "id": "P2.2",
        "stage": 2,
        "topic": "Expandir el ICP a productos médicos no farmacéuticos",
        "type": "single",
        "points": 2,
        "prompt": (
            "Tu líder de equipo te propone expandir el ICP a distribuidores de productos médicos "
            "no farmacéuticos (dispositivos, consumibles de hospital) \"porque también manejan "
            "trazabilidad\". ¿Qué haces?"
        ),
        "choices": [
            {"id": "a", "text": "Acepto la expansión: con más contactos disponibles llego antes a la meta de reuniones del mes."},
            {"id": "b", "text": "Propongo un piloto acotado: 50-100 contactos del segmento nuevo durante 2 semanas, con el foco principal intacto y un método de medición declarado (tasa de respuesta y reuniones sobre respuestas); si rinde, se expande; si no, se cierra."},
            {"id": "c", "text": "Rechazo la expansión de plano: el cliente pidió distribuidores farmacéuticos y no hay nada que discutir al respecto."},
            {"id": "d", "text": "Acepto y armo una campaña aparte para ese segmento, y voy viendo con el tiempo qué resultados deja la cosa."},
        ],
        "correct": "b",
        "explanation": (
            "Aplicación directa de PDCA: una variable nueva, muestra acotada, método de medición "
            "declarado. (a) acción sin método, (c) conservadurismo ciego, (d) parece razonable pero "
            "no declara método — termina en \"veamos qué sale\" sin datos para decidir."
        ),
    },
    {
        "id": "P3.A.1",
        "stage": 3,
        "topic": "Variante de acceso — Farmacéutica Velmar (correo + teléfono verificados)",
        "type": "single",
        "points": 2,
        "prompt": (
            "Farmacéutica Velmar (Colombia): 180 empleados, operación en Colombia y Perú. Tu base "
            "te devuelve al VP de Operaciones, Carlos Rojas, con correo y teléfono verificados. "
            "Nunca fue contactada. ¿Qué variante de acceso aplica?"
        ),
        "choices": [
            {"id": "a", "text": "Variante 1 — correo y teléfono verificados del decisor: acercamiento multicanal directo."},
            {"id": "b", "text": "Variante 2 — solo correo del decisor: correo paciente con cadencia espaciada."},
            {"id": "c", "text": "Variante 3 — sin contacto del decisor: acceso vía referidores internos."},
            {"id": "d", "text": "Variante 5 — recontacto con ángulo nuevo tras una ventana de enfriamiento."},
        ],
        "correct": "a",
        "explanation": "Decisor con correo + teléfono verificados → variante 1, multicanal proactivo.",
    },
    {
        "id": "P3.A.2",
        "stage": 3,
        "topic": "Mejor primer mensaje para el decisor (Carlos Rojas)",
        "type": "single",
        "points": 3,
        "prompt": (
            "Eliges el primer correo para Carlos Rojas, VP de Operaciones de Velmar. ¿Cuál es el "
            "mejor de los cuatro?"
        ),
        "choices": [
            {"id": "a", "text": "Hola Carlos. Te escribo para presentarte GestaLogix, la plataforma regional de trazabilidad y cadena de frío: seriación de lotes, alertas automáticas y reportería para auditorías, todo en una sola herramienta. Trabajamos con varios distribuidores de la región. ¿Agendamos 30 minutos para mostrártela?"},
            {"id": "b", "text": "Hola Carlos. Quería ver si te interesa conocer una solución de trazabilidad y cadena de frío para tu operación. Tenemos muy buenas referencias y creo que podría encajar con lo que necesitan. ¿Tienes un espacio para conversar pronto?"},
            {"id": "c", "text": "Hola Carlos. Vi que Velmar opera tanto en Colombia como en Perú. Para distribuidores con presencia en los dos países, sostener INVIMA y DIGEMID en paralelo suele recaer sobre el área de operaciones. ¿Cómo están manejando hoy la trazabilidad entre ambas operaciones? Si tiene sentido, te comparto en 15 minutos cómo lo resolvieron operaciones de tamaño similar."},
            {"id": "d", "text": "Hola Carlos. Creo que podemos ayudar a Velmar a reducir bastante el tiempo de sus auditorías y los costos de cumplimiento. ¿Cuándo te viene bien una demostración para que lo veas en detalle y con números?"},
        ],
        "correct": "c",
        "explanation": (
            "Foco en el lector + gancho específico (operación MX/CO) + pregunta abierta + CTA de "
            "bajo compromiso. (a) es pecado capital sutil (habla del producto), (b) gancho genérico, "
            "(d) promete mejora difusa y pide demostración de entrada."
        ),
    },
    {
        "id": "P3.B.1",
        "stage": 3,
        "topic": "Variante de acceso — Distribuidora Andix (sin contacto del decisor)",
        "type": "single",
        "points": 2,
        "prompt": (
            "Distribuidora Andix (Perú): 400 empleados, operación en Perú y México. Tu base no tiene "
            "contacto verificado del decisor: solo un patrón de correo inferido del VP de Operaciones "
            "marcado como baja confianza. Sí aparecen, con correo verificado, tres Coordinadores de "
            "Operaciones y un Gerente de Cumplimiento Regulatorio, Mariela Fuentes. Nunca fue "
            "contactada. ¿Qué variante de acceso aplica?"
        ),
        "choices": [
            {"id": "a", "text": "Variante 1 — el patrón de correo inferido y el teléfono de la central alcanzan para un acercamiento multicanal directo al decisor."},
            {"id": "b", "text": "Variante 2 — con el patrón de correo inferido del decisor basta para una secuencia de correo paciente a su casilla."},
            {"id": "c", "text": "Variante 5 — recontacto con ángulo nuevo, porque ya hay rastros de contacto previo en la base."},
            {"id": "d", "text": "Variante 3 — al no haber contacto verificado del decisor, el acceso es vía referidores internos: los mandos medios con correo verificado son candidatos a orientarte."},
        ],
        "correct": "d",
        "explanation": (
            "Sin contacto verificado del decisor + mandos medios verificados → variante 3 "
            "(referidores). El objetivo con ellos es pedir orientación, no vender. Un patrón inferido "
            "de baja confianza no habilita variante 1 ni 2; no hubo contacto previo (descarta 5)."
        ),
    },
    {
        "id": "P3.B.2",
        "stage": 3,
        "topic": "Mejor mensaje para la referidora (Mariela Fuentes)",
        "type": "single",
        "points": 3,
        "prompt": (
            "Tu objetivo con Mariela no es venderle: es que te oriente hacia quién decide sobre "
            "trazabilidad. ¿Cuál es el mejor mensaje?"
        ),
        "choices": [
            {"id": "a", "text": "Hola Mariela. Por tu rol pensé que podrías orientarme. Estoy tratando de ubicar quién en Distribuidora Andix lidera las decisiones sobre sistemas de trazabilidad y cadena de frío: ¿es algo que ve directamente el VP de Operaciones o pasa antes por otra área? Cualquier pista me ayuda. No quiero hacerte perder tiempo con algo que no toque a tu equipo."},
            {"id": "b", "text": "Hola Mariela. Por tu rol pensé que podrías orientarme. Trabajamos con GestaLogix, una plataforma de trazabilidad regional que cumple con DIGEMID y COFEPRIS, se implementa en pocos meses y suele ahorrar bastante en auditorías. ¿Quién sería la persona indicada para verlo, y te sumo en copia cuando lo presente?"},
            {"id": "c", "text": "Hola Mariela. Vi tu perfil y creo que el área de cumplimiento es clave en esto. ¿Tienes 20 minutos esta semana para que te muestre cómo GestaLogix puede ayudar a Distribuidora Andix con la trazabilidad? Llevo una breve demostración."},
            {"id": "d", "text": "Hola Mariela. Estoy contactando empresas del sector para presentar una solución que podría interesarles. ¿Me podrías ayudar a avanzar internamente con esto cuando tengas un momento? Quedo atento."},
        ],
        "correct": "a",
        "explanation": (
            "Pide orientación sin vender, nombra el rol que busca y respeta su tiempo. (b) desliza el "
            "pitch de venta, (c) la trata como decisora e intenta agendar demostración, (d) es tan "
            "vago que no permite rutear."
        ),
    },
    {
        "id": "P4.1",
        "stage": 4,
        "topic": "Errores estructurales de una secuencia propuesta",
        "type": "single",
        "points": 3,
        "prompt": (
            "Vuelves a Farmacéutica Velmar (variante 1). Un compañero te pasa esta secuencia para "
            "revisar antes de cargarla:\n\n"
            "Paso 1 — Día 0 — Teléfono — Llamada en frío de apertura\n"
            "Paso 2 — Día 0 — Correo — Primer correo con el gancho\n"
            "Paso 3 — Día 2 — Correo — Reenvío del mismo correo \"por si no llegó\"\n"
            "Paso 4 — Día 4 — WhatsApp — Mensaje al número personal del decisor\n"
            "Paso 5 — Día 7 — Correo — Seguimiento con un ángulo nuevo\n"
            "Paso 6 — Día 10 — Teléfono — Segunda llamada\n"
            "Paso 7 — Día 13 — Correo — Cierre abierto\n\n"
            "¿Cuál de estas opciones identifica correctamente los errores estructurales de la secuencia?"
        ),
        "choices": [
            {"id": "a", "text": "La llamada va antes del primer correo; el reenvío del mismo correo; usar el teléfono dos veces; y meter WhatsApp al número personal del decisor."},
            {"id": "b", "text": "La llamada va antes del primer correo; el reenvío del mismo correo; WhatsApp al número personal; y que la secuencia se reparta en una ventana demasiado corta."},
            {"id": "c", "text": "La llamada va antes del primer correo; el reenvío del mismo correo; WhatsApp al número personal como toque de cadencia; y que no declara ninguna regla de qué hacer si el prospecto responde."},
            {"id": "d", "text": "El reenvío del mismo correo; y meter WhatsApp al número personal del decisor."},
        ],
        "correct": "c",
        "explanation": (
            "Errores: llamada antes del contexto escrito, reenvío idéntico, WhatsApp al número "
            "personal, y ausencia de regla de ramificación. (a) marca de más \"teléfono dos veces\" "
            "(es correcto), (b) inventa \"ventana demasiado corta\" (13 días está bien), (d) es incompleta."
        ),
    },
    {
        "id": "P4.3",
        "stage": 4,
        "topic": "Verificaciones de entregabilidad antes de ejecutar a escala",
        "type": "single",
        "points": 3,
        "prompt": (
            "Antes de ejecutar esta secuencia sobre toda la lista, ¿cuál de estas opciones lista las "
            "tres verificaciones correctas con el equipo de infraestructura para no quemar tu dominio?"
        ),
        "choices": [
            {"id": "a", "text": "El calentamiento de los dominios; la validación de la lista; y activar el píxel de seguimiento de aperturas para priorizar a quien abre."},
            {"id": "b", "text": "El calentamiento de los dominios; subir el volumen diario por casilla para terminar antes; y la validación de la lista."},
            {"id": "c", "text": "El volumen por casilla al día; cargar la plantilla con imágenes y enlaces para verse más profesional; y la validación de la lista."},
            {"id": "d", "text": "El calentamiento de los dominios de envío; el volumen por casilla al día; y la validación de la lista para mantener baja la tasa de rebote."},
        ],
        "correct": "d",
        "explanation": (
            "Calentamiento + volumen por casilla + validación de lista. Los distractores meten "
            "anti-patrones: píxel de apertura (a) y plantilla recargada de imágenes (c) dañan la "
            "entregabilidad; subir el volumen (b) contradice el tope por casilla."
        ),
    },
    {
        "id": "P5.2",
        "stage": 5,
        "topic": "Objeción con información vs rechazo (DIFERENCIADORA)",
        "differentiator": True,
        "type": "single",
        "points": 3,
        "prompt": (
            "Al séptimo día de la secuencia de Velmar, Carlos Rojas (VP de Operaciones) responde:\n\n"
            "\"Hola, gracias por tu seguimiento. Leí tus dos correos y entiendo la propuesta, pero "
            "acá hay varias complicaciones. Ya tenemos un proveedor que nos armó una integración a "
            "medida con nuestro ERP hace tres años; no es perfecta, pero cumple lo mínimo con INVIMA. "
            "Además, cualquier cambio de plataforma implica meses de paralización operativa que hoy "
            "no podemos permitirnos: estamos por cerrar un contrato con una cadena grande y no hay "
            "margen para disrupciones. Si tienen un caso concreto donde hayan migrado un ERP existente "
            "sin frenar operaciones en una empresa de nuestro tamaño, me interesa verlo. Pero si es "
            "rehacer la plataforma desde cero, lo dejamos para el año que viene. Saludos, Carlos.\"\n\n"
            "¿Cómo lees la respuesta de Carlos?"
        ),
        "choices": [
            {"id": "a", "text": "Es un rechazo funcional: dejó claro que no van a cambiar de plataforma, así que corresponde respetar y archivar la cuenta."},
            {"id": "b", "text": "Es un rechazo disfrazado: pide un caso por cortesía, pero ya tiene proveedor y el contrato grande le da la excusa perfecta para no avanzar."},
            {"id": "c", "text": "Es una objeción con información: da razones concretas y pide un caso específico de migración sin frenar operaciones, o sea, explicita la condición que tendría que cumplirse para avanzar."},
            {"id": "d", "text": "Es una objeción superficial: no dio una razón de fondo, así que corresponde volver a insistir con otro ángulo hasta que ceda."},
        ],
        "correct": "c",
        "explanation": (
            "Carlos pide un entregable específico (caso de migración sin frenar operaciones, tamaño "
            "similar): explicita la condición para avanzar. Es objeción con información dura, no rechazo "
            "(no dice \"gracias, no\") ni objeción superficial (sí dio razones de fondo)."
        ),
    },
    {
        "id": "P5.3",
        "stage": 5,
        "topic": "Mejor respuesta a Carlos (objeción con información)",
        "type": "single",
        "points": 3,
        "prompt": "¿Cuál es la mejor respuesta para mandarle a Carlos?",
        "choices": [
            {"id": "a", "text": "Hola Carlos, gracias por el contexto; lo del contrato grande cambia el cálculo. Tengo el caso de un distribuidor de tamaño parecido que migró su ERP en fases paralelas, sin ventana de paralización, y otro más corto con menos integración. Te mando el primero con los datos del proyecto para que lo revises con tu equipo técnico. ¿Te sirve así o prefieres ver los dos?"},
            {"id": "b", "text": "Hola Carlos, entiendo que es un mal momento. Si no es prioridad ahora, lo dejamos para más adelante y te vuelvo a escribir el año que viene cuando tengan más espacio. Quedo atento a cualquier cosa que necesites mientras tanto. Gracias por tu tiempo."},
            {"id": "c", "text": "Hola Carlos, justo tengo un caso que calza con lo que pides, pero antes me gustaría mostrarte la plataforma en una demostración de 30 minutos para que veas cómo funciona la migración. ¿Coordinamos esta semana y después te paso el caso?"},
            {"id": "d", "text": "Hola Carlos, claro: te mando un caso donde migramos un ERP igual al tuyo en exactamente 6 semanas, sin un solo día de parada y con 100% de cumplimiento desde el primer mes. ¿Cuándo lo revisamos juntos?"},
        ],
        "correct": "a",
        "explanation": (
            "Reconoce el contexto sin capitular, responde al pedido exacto (caso de migración paralela) "
            "y mantiene la agencia del prospecto. (b) capitula y cierra, (c) antepone la demostración al "
            "pedido, (d) inventa cifras exactas (6 semanas, 100%) — viola \"proponer sin prometer\"."
        ),
    },
    {
        "id": "P6.1",
        "stage": 6,
        "topic": "Diagnóstico por descarte con cadena causal (DIFERENCIADORA)",
        "differentiator": True,
        "type": "single",
        "points": 3,
        "prompt": (
            "Pasaron 4 semanas ejecutando. Métricas semanales:\n\n"
            "Métrica                     | Sem 1 | Sem 2 | Sem 3 | Sem 4\n"
            "Tasa de rebote              | 2.3%  | 2.4%  | 2.2%  | 2.5%\n"
            "Tasa de respuesta           | 3.1%  | 3.0%  | 3.3%  | 3.2%\n"
            "Reuniones sobre respuestas  | 24%   | 25%   | 26%   | 25%\n"
            "Tasa de asistencia          | 71%   | 73%   | 72%   | 72%\n"
            "Precalificaciones aprobadas | 84%   | 86%   | 85%   | 38%\n\n"
            "Contexto: no cambiaste el mensaje, ni el ICP declarado, ni la cadencia, ni las "
            "herramientas. En la Semana 3, el equipo de investigación —presionado por la meta de "
            "reuniones— sumó 90 contactos nuevos de \"empresas con trazabilidad\"; al revisarlos por "
            "encima, ves que varios son distribuidores de productos médicos no farmacéuticos y algunas "
            "farmacéuticas por debajo de 50 empleados. Ese lote entró sin el piloto acotado que habías "
            "propuesto en la Etapa 2.\n\n"
            "¿Cuál es tu hipótesis principal y cuál es tu primera acción diagnóstica?"
        ),
        "choices": [
            {"id": "a", "text": "Es fatiga de mensaje: el gancho se gastó después de cuatro semanas. Primera acción: una prueba A/B con variantes del asunto y del cuerpo."},
            {"id": "b", "text": "La lista se contaminó con prospectos fuera del ICP: responden por afinidad temática pero no pasan la precalificación. Las demás métricas están estables, lo que descarta canal, mensaje, gestión y agendamiento; la caída aislada de la precalificación apunta a quién entra a la lista. Primera acción: separar las métricas del lote nuevo y medir qué porción cae fuera del ICP."},
            {"id": "c", "text": "Es entregabilidad: los dominios se quemaron y los correos caen a spam. Primera acción: pausar la campaña y revisar la reputación de cada dominio."},
            {"id": "d", "text": "Es agendamiento: las reuniones se están confirmando mal. Primera acción: revisar las invitaciones de calendario y los recordatorios."},
        ],
        "correct": "b",
        "explanation": (
            "La única métrica que cae es la precalificación, justo tras cargar un lote fuera de ICP "
            "sin piloto (coincidencia temporal). Las métricas vecinas estables descartan entregabilidad "
            "(rebote ok), mensaje/canal (respuesta ok) y agendamiento (asistencia ok). El caso cierra en "
            "bucle con la decisión de la Etapa 2."
        ),
    },
    {
        "id": "P6.2",
        "stage": 6,
        "topic": "Acción de escalación",
        "type": "single",
        "points": 2,
        "prompt": "Confirmada la hipótesis, ¿qué escalas y cómo?",
        "choices": [
            {"id": "a", "text": "Espero a la reunión semanal con mi líder para no alarmar con un dato que quizás se acomoda solo en los próximos días."},
            {"id": "b", "text": "Le escribo al equipo de investigación marcando que el lote que cargaron arruinó mis métricas y pido que no vuelvan a hacerlo."},
            {"id": "c", "text": "Le pido permiso a mi líder para pausar la incorporación del lote nuevo antes de tocar nada, porque no quiero excederme en mis atribuciones."},
            {"id": "d", "text": "El mismo día reporto a mi líder con el dato (la precalificación cayó a 38% por probable contaminación del lote de la Semana 3, ya separé las métricas) y le propongo al equipo de investigación, como política y no como reproche, que ningún lote entre a la lista sin pasar el chequeo de los filtros duros del ICP."},
        ],
        "correct": "d",
        "explanation": (
            "Escala el mismo día, con el dato y separando métricas, y propone una política preventiva "
            "sin reproche. (a) tarda, (b) es reproche, (c) pide permiso para algo que es su atribución."
        ),
    },
    {
        "id": "P6.3",
        "stage": 6,
        "topic": "Hipótesis testeable para prevenir el incidente (DIFERENCIADORA)",
        "differentiator": True,
        "type": "single",
        "points": 3,
        "prompt": (
            "En tu próximo 1:1 propones una hipótesis para que esto no se repita. ¿Cuál está bien "
            "formulada?"
        ),
        "choices": [
            {"id": "a", "text": "Si ajustamos los filtros del ICP y, de paso, reescribimos el gancho del mensaje para las empresas nuevas, la precalificación debería recuperarse y la conversión general también debería mejorar en las próximas semanas."},
            {"id": "b", "text": "Si ningún contacto entra al motor sin pasar el chequeo de los filtros duros del ICP y revisamos la tasa de precalificación cada semana con pausa automática si baja del 70%, los incidentes de contaminación deberían caer a uno o menos por trimestre; lo medimos durante 3 meses contra el histórico."},
            {"id": "c", "text": "Si exigimos que cada lote pase el chequeo de los filtros duros del ICP antes de entrar al motor, vamos a tener bastantes menos prospectos fuera de perfil de ahora en adelante y la precalificación debería ir mejorando de forma sostenida."},
            {"id": "d", "text": "Si establecemos el chequeo de los filtros duros del ICP como regla fija del equipo, la precalificación debería volver a su nivel normal en algún momento y eso nos va a dar más reuniones de calidad."},
        ],
        "correct": "b",
        "explanation": (
            "Cumple las condiciones de hipótesis testeable: variable única (chequeo de filtros), método "
            "y umbral declarados (precalif semanal, pausa <70%), magnitud esperada (≤1 incidente/trimestre) "
            "y ventana de medición (3 meses vs histórico). (a) mezcla 2 variables; (c) y (d) no declaran "
            "método ni magnitud."
        ),
    },
]


# ─────────────────────────────  COMPONENTES MANUALES (vacíos)  ───────────────────
# El rediseño de NICO (v1, 2026-06-13) convirtió todo el caso a MCQ autocorregible.
# Se conservan vacíos por compatibilidad con el seeder y el motor de grading.

SHORT_ANSWERS: list[dict] = []
TABLES: list[dict] = []
GENERIC_SHORT_RUBRIC: dict = {}


# ─────────────────────────────  RÚBRICA DEL VIDEO (/30)  ─────────────────────────

VIDEO_RUBRIC_15: dict = {
    "scale_per_dim": "0-2",
    "max_total": 30,
    "conversion": {"30": 100, "24": 80, "18": 60},
    "critical_dimensions_for_distinction": [1, 2, 3, 4, 5, 6],
    "min_critical_points": 11,
    "min_critical_for_distinction": "11/12 o 12/12",
    "defense_decisions": [
        "El mensaje a la referidora de Distribuidora Andix (Etapa 3, Situación B).",
        "La respuesta a Carlos Rojas (Etapa 5).",
        "El diagnóstico de la caída de métricas (Etapa 6: hipótesis y propuesta de prevención).",
    ],
    "dimensions": [
        {"id": 1, "label": "Identificación del problema", "critical": True,
         "scale": [
             {"score": 0, "descriptor": "No lo identifica o lo confunde."},
             {"score": 1, "descriptor": "Lo identifica de forma parcial."},
             {"score": 2, "descriptor": "Claro y correcto de entrada."},
         ]},
        {"id": 2, "label": "Vocabulario del curso", "critical": True,
         "scale": [
             {"score": 0, "descriptor": "Frases genéricas, sin nombrar conceptos."},
             {"score": 1, "descriptor": "Usa uno o dos conceptos, superficiales."},
             {"score": 2, "descriptor": "Nombra conceptos con precisión (variantes de acceso, objeción frente a rechazo, diagnóstico por descarte, hipótesis testeable, ICP, entre otros)."},
         ]},
        {"id": 3, "label": "Jerarquización de causas", "critical": True,
         "scale": [
             {"score": 0, "descriptor": "No prioriza."},
             {"score": 1, "descriptor": "Prioriza en general, sin justificar."},
             {"score": 2, "descriptor": "Justifica por qué una causa pesa más que otra con datos o lógica del embudo."},
         ]},
        {"id": 4, "label": "Integración entre partes del curso", "critical": True,
         "scale": [
             {"score": 0, "descriptor": "Defiende una decisión apoyándose en una sola parte del curso."},
             {"score": 1, "descriptor": "Cruza dos partes."},
             {"score": 2, "descriptor": "Cruza tres o más partes en una misma decisión."},
         ]},
        {"id": 5, "label": "Justificación de la respuesta a Carlos", "critical": True,
         "scale": [
             {"score": 0, "descriptor": "Genérica."},
             {"score": 1, "descriptor": "Con algún concepto."},
             {"score": 2, "descriptor": "Con concepto más razón específica al caso (objeción con información, pedido concreto, respuesta al pedido sin capitular)."},
         ]},
        {"id": 6, "label": "Justificación del diagnóstico de métricas", "critical": True,
         "scale": [
             {"score": 0, "descriptor": "Genérica."},
             {"score": 1, "descriptor": "Con algún concepto."},
             {"score": 2, "descriptor": "Con concepto más razón específica (descarte por métricas vecinas, causa aguas arriba, hipótesis con método)."},
         ]},
        {"id": 7, "label": "Presentación personal breve",
         "scale": [
             {"score": 0, "descriptor": "Ausente."},
             {"score": 1, "descriptor": "Larga o autorreferencial."},
             {"score": 2, "descriptor": "Corta, clara, enfocada."},
         ]},
        {"id": 8, "label": "Estructura del video",
         "scale": [
             {"score": 0, "descriptor": "Desordenada."},
             {"score": 1, "descriptor": "Cumple la estructura con saltos."},
             {"score": 2, "descriptor": "Estructura clara, con transiciones."},
         ]},
        {"id": 9, "label": "Decisión 1 (referidora) — claridad del contexto",
         "scale": [
             {"score": 0, "descriptor": "Confuso."},
             {"score": 1, "descriptor": "Se entiende con esfuerzo."},
             {"score": 2, "descriptor": "Claro de entrada."},
         ]},
        {"id": 10, "label": "Decisión 1 (referidora) — justificación",
         "scale": [
             {"score": 0, "descriptor": "Genérica."},
             {"score": 1, "descriptor": "Con algún concepto."},
             {"score": 2, "descriptor": "Concepto más razón específica (variante 3, pedir orientación sin vender)."},
         ]},
        {"id": 11, "label": "Decisión 2 y 3 — claridad del contexto",
         "scale": [
             {"score": 0, "descriptor": "Confuso."},
             {"score": 1, "descriptor": "Se entiende con esfuerzo."},
             {"score": 2, "descriptor": "Claro de entrada."},
         ]},
        {"id": 12, "label": "Cierre — qué aprendiste",
         "scale": [
             {"score": 0, "descriptor": "Ausente o superficial."},
             {"score": 1, "descriptor": "Genérico."},
             {"score": 2, "descriptor": "Específico, conectado con decisiones concretas."},
         ]},
        {"id": 13, "label": "Cierre — qué harías distinto",
         "scale": [
             {"score": 0, "descriptor": "Ausente o \"nada\"."},
             {"score": 1, "descriptor": "Cambios menores sin justificar."},
             {"score": 2, "descriptor": "Cambios específicos justificados con conceptos del curso."},
         ]},
        {"id": 14, "label": "Dominio verbal",
         "scale": [
             {"score": 0, "descriptor": "Lectura, muletillas constantes."},
             {"score": 1, "descriptor": "Aceptable, con pérdidas."},
             {"score": 2, "descriptor": "Fluido, responde con sentido."},
         ]},
        {"id": 15, "label": "Honestidad del razonamiento",
         "scale": [
             {"score": 0, "descriptor": "Inventa certezas o resultados."},
             {"score": 1, "descriptor": "Mezcla criterio con suposiciones sin marcarlas."},
             {"score": 2, "descriptor": "Defiende el criterio sin afirmar que acertó; reconoce lo que no sabe."},
         ]},
    ],
}


# ─────────────────────────────  PREGUNTAS DIFERENCIADORAS  ─────────────────────

DIFFERENTIATOR_IDS: list[str] = ["P1.4", "P5.2", "P6.1", "P6.3"]
"""Las 4 diferenciadoras (todas MCQ de 3 puntos = 12 pts). Para distinción se exige
≥75% acumulado = ≥9/12 (junto con curso ≥85%, módulos ≥80%, prueba final ≥85% y el
video ≥11/12 en sus 6 dimensiones críticas)."""


# ─────────────────────────────  PESOS Y UMBRALES  ──────────────────────────────

# Nota Prueba Final = (Caso% × 0.7) + (Video% × 0.3). Caso = puntos ÷ 42 × 100.
WEIGHTS = {"case": 0.7, "video": 0.3}

PASSING_SCORE = 60.0          # graduación básica
DISTINCTION_SCORE = 85.0      # graduación con distinción


def total_mcq_count() -> int:
    return len(MCQ)


def total_case_points() -> int:
    """Puntaje máximo del caso (suma de ``points``). Debe dar 42."""
    return sum(int(q.get("points", 1)) for q in MCQ)


def total_short_answers() -> int:
    return len(SHORT_ANSWERS)


def differentiator_questions() -> list[dict]:
    """Devuelve las preguntas marcadas como diferenciadoras (todas MCQ en el rediseño)."""
    out: list[dict] = []
    for q in MCQ:
        if q.get("differentiator"):
            out.append(q)
    for q in SHORT_ANSWERS:
        if q.get("differentiator"):
            out.append(q)
    return out
