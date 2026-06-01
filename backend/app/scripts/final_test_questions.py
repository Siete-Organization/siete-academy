"""Contenido Capa 3 — Prueba Final del curso (SDR Academy Siete).

Caso integrador: GestaLogix (SaaS B2B de trazabilidad farmacéutica para
distribuidores en MX/CO/PE).

Fuente: SDR_Academy_Siete_Documento_Maestro.md, líneas 12671-13503, v0.1 (2026-04-24).

Estructura del examen:
- 6 etapas con mezcla MCQ + tablas estructuradas + respuestas cortas.
- Video de defensa de 15 minutos (1 toma) con rúbrica de 15 dimensiones.

Shape de los datos:
- MCQ: preguntas auto-gradables (13 questions con choices/correct, compatible
  con `auto_grade_mcq`). Cubren P1.1, P1.2, P1.4, P2.2, P3.A.1, P3.B.1, P3.C,
  P3.D.1, P4.2, P5.1, P5.2, P6.1 — total 12 MCQ.
- SHORT_ANSWERS: 8 prompts de respuesta corta con rúbrica genérica /2.
- TABLES: 2 tablas estructuradas (filtros ICP + secuencia outbound).
- VIDEO_RUBRIC_15: rúbrica del video defense (15 dimensiones × 0-2 = /30).
- GENERIC_SHORT_RUBRIC: rúbrica genérica 0-2 para respuestas cortas.
- DIFFERENTIATOR_IDS: preguntas que pesan extra para distinción (75% acumulado).
"""

CASE_BRIEF: dict = {
    "title": "GestaLogix — SaaS B2B de trazabilidad farmacéutica (MX/CO/PE)",
    "summary": (
        "GestaLogix vende una plataforma de gestión logística y trazabilidad a "
        "distribuidores farmacéuticos medianos y grandes en México, Colombia y Perú. "
        "Fundada en 2022 por tres ingenieros del rubro farmacéutico. Serie A de USD 8M "
        "cerrada en marzo 2025. 40 empleados al cierre de 2025, plan de crecer a 70 en "
        "2026. Ticket promedio del cliente final: USD 35K-70K anuales."
    ),
    "platform": [
        "Trazabilidad de lotes (seriación, caducidad, retiros).",
        "Cadena de frío (sensores IoT + alertas automáticas).",
        "Control de inventario en tiempo real (múltiples bodegas).",
        "Cumplimiento regulatorio (COFEPRIS México, INVIMA Colombia, DIGEMID Perú).",
        "Reportería para auditorías (integración con ERP del cliente).",
    ],
    "market_context": (
        "Industria farmacéutica LATAM bajo presión regulatoria creciente desde 2023 "
        "(trazabilidad obligatoria + sanciones por incumplimiento). Distribuidores "
        "tradicionales dependen de sistemas legacy (SAP + Excel + workarounds manuales). "
        "El cumplimiento regulatorio es el driver #1 hoy. Competidores internacionales "
        "(TraceLink, Systech) son caros y tienen implementaciones de 12-18 meses. "
        "GestaLogix se posiciona como la alternativa regional, implementación 3-4 meses, "
        "40% más barata."
    ),
    "client_expectations": {
        "meetings_per_month": "10 calificadas/mes a partir del mes 2",
        "icp": "Distribuidores farmacéuticos con 50-500 empleados, operación en al menos 2 de los 3 países (MX/CO/PE)",
        "target_decision_maker": "VP de Operaciones, Director de Cadena de Suministro, o Gerente de Cumplimiento Regulatorio",
        "average_ticket": "USD 50K anuales por deal cerrado",
        "decision_timeline": "3-6 meses típico (ciclo B2B enterprise)",
    },
}


# ─────────────────────────────  MCQ AUTO-GRADABLES  ─────────────────────────────

MCQ: list[dict] = [
    {
        "id": "P1.1",
        "stage": 1,
        "topic": "Business Model Canvas — componente diferenciador",
        "type": "single",
        "prompt": (
            "¿Cuál de los 9 componentes del BMC de GestaLogix es más diferenciador "
            "competitivamente según el brief?"
        ),
        "choices": [
            {"id": "a", "text": "Key Partners (inversores y socios fundadores)."},
            {"id": "b", "text": "Customer Segments (distribuidores farmacéuticos medianos y grandes en MX/CO/PE)."},
            {"id": "c", "text": "Value Propositions (alternativa regional, implementación en 3-4 meses, 40% más barata que competidores internacionales — todo contra un driver regulatorio creciente)."},
            {"id": "d", "text": "Revenue Streams (tickets USD 35K-70K anuales)."},
        ],
        "correct": "c",
        "explanation": (
            "La propuesta de valor específica es lo que los separa del resto del mercado. "
            "La combinación regional + tiempo de implementación + precio + timing regulatorio "
            "es el diferenciador competitivo."
        ),
    },
    {
        "id": "P1.2",
        "stage": 1,
        "topic": "5 fuerzas de Porter — fuerza disruptiva a favor",
        "type": "single",
        "prompt": (
            "Aplicando las 5 fuerzas de Porter al mercado de GestaLogix, ¿cuál es hoy la "
            "fuerza más disruptiva a su favor?"
        ),
        "choices": [
            {"id": "a", "text": "Poder de negociación de los clientes (distribuidores farmacéuticos)."},
            {"id": "b", "text": "Amenaza de nuevos entrantes (otras startups regionales)."},
            {"id": "c", "text": "Amenaza de sustitutos (sistemas legacy + Excel)."},
            {"id": "d", "text": "Presión externa estructural (regulación + sanciones por incumplimiento) — que convierte al software de trazabilidad de \"nice-to-have\" a \"compliance obligatorio\", forzando a los distribuidores a actualizar sus sistemas."},
        ],
        "correct": "d",
        "explanation": (
            "La regulación actúa como driver externo que obliga a los distribuidores a moverse. "
            "Es la fuerza que convierte una conversación sobre \"optimización\" (opcional) en una "
            "sobre \"cumplimiento\" (no-opcional). Siete la va a apalancar en el gancho."
        ),
    },
    {
        "id": "P1.4",
        "stage": 1,
        "topic": "Dolor dominante del decisor (DIFERENCIADORA)",
        "differentiator": True,
        "type": "single",
        "prompt": (
            "El VP de Operaciones de un distribuidor farmacéutico de 300 empleados en México "
            "está hoy bajo la presión de COFEPRIS. ¿Cuál es su dolor dominante más probable "
            "respecto a trazabilidad, y qué hace que ese dolor sea accionable en una "
            "conversación con un SDR?"
        ),
        "choices": [
            {"id": "a", "text": "Dolor: \"quiero modernizar la empresa\". Accionable porque es una aspiración."},
            {"id": "b", "text": "Dolor: \"cada auditoría nos cuesta 3 semanas de un equipo de 4 personas y tuvimos una multa pequeña el año pasado — si se repite, la próxima multa sería grande\". Accionable porque es específico, cuantificable, con consecuencias concretas."},
            {"id": "c", "text": "Dolor: \"tengo curiosidad por la tecnología nueva\". Accionable porque el SDR puede hablar de features."},
            {"id": "d", "text": "Dolor: \"mi CEO me pidió un plan de digitalización para 2027\". Accionable porque tiene deadline."},
        ],
        "correct": "b",
        "explanation": (
            "Un dolor accionable para un SDR B2B es específico, cuantificable, con consecuencias "
            "concretas y presentes. Las otras son versiones genéricas (a, c) o demasiado futuras (d). "
            "El SDR con criterio reconoce que el dolor que abre conversaciones es el que el prospecto "
            "puede nombrar con detalle en el primer intercambio."
        ),
    },
    {
        "id": "P2.2",
        "stage": 2,
        "topic": "Expandir ICP a productos médicos no farmacéuticos",
        "type": "single",
        "prompt": (
            "El Team Lead te propone expandir el ICP a distribuidores de productos médicos "
            "(no farmacéuticos) — dispositivos, consumibles de hospital, etc. — \"porque también "
            "tienen trazabilidad\". ¿Qué hacés?"
        ),
        "choices": [
            {"id": "a", "text": "Acepto la expansión — más contactos = más reuniones."},
            {"id": "b", "text": "Rechazo la expansión totalmente — el cliente fue explícito: distribuidores farmacéuticos."},
            {"id": "c", "text": "Propongo correr un piloto de 2 semanas con 50-100 contactos de distribuidores de productos médicos, manteniendo 100% del foco en farmacéuticos, midiendo reply rate + meeting rate sobre reply + feedback del AE. Si rinde, se expande con criterio. Si no, se cierra el experimento."},
            {"id": "d", "text": "Acepto pero sin mezclar listas — armo campaña separada y veo qué pasa."},
        ],
        "correct": "c",
        "explanation": (
            "Aplicación directa de PDCA (M4 Sem 8): una variable nueva, muestra acotada, método de "
            "medición declarado. (a) acción sin método, (b) conservadurismo ciego, (d) parece "
            "razonable pero no declara método — termina en \"veamos qué sale\" sin datos para decidir."
        ),
    },
    {
        "id": "P3.A.1",
        "stage": 3,
        "topic": "Variante de acceso — Farmacéuticos del Sur (correo + teléfono verificados)",
        "type": "single",
        "prompt": (
            "Farmacéuticos del Sur (Colombia): 180 empleados, operación en Colombia y Perú. "
            "Apollo te devuelve al VP de Operaciones, Carlos Rojas, con email y teléfono "
            "verificados. Nunca fue contactado antes. ¿Qué variante de acceso aplica?"
        ),
        "choices": [
            {"id": "a", "text": "Variante 1 (correo + teléfono verificados del decisor)."},
            {"id": "b", "text": "Variante 2 (solo correo)."},
            {"id": "c", "text": "Variante 3 (sin contacto del decisor)."},
            {"id": "d", "text": "Variante 5 (recontacto)."},
        ],
        "correct": "a",
        "explanation": "Decisor con correo + teléfono verificados → variante 1 multicanal proactivo.",
    },
    {
        "id": "P3.B.1",
        "stage": 3,
        "topic": "Variante de acceso — Distribuidora Andina (sin decisor en Apollo)",
        "type": "single",
        "prompt": (
            "Distribuidora Andina (Perú): 400 empleados, operación en Perú y México. Apollo no "
            "tiene al decisor. Aparecen 3 Coordinadores de Operaciones y 1 Gerente de Cumplimiento "
            "Regulatorio con email verificado. Nunca contactada. ¿Qué variante aplica?"
        ),
        "choices": [
            {"id": "a", "text": "Variante 1."},
            {"id": "b", "text": "Variante 2."},
            {"id": "c", "text": "Variante 3 (sin contacto del decisor; uso referidores dentro de la empresa)."},
            {"id": "d", "text": "Variante 6 (artesanal wish list)."},
        ],
        "correct": "c",
        "explanation": (
            "Sin contacto del decisor + mandos medios verificados → variante 3 (referidores). "
            "El objetivo con ellos es pedir orientación, no vender."
        ),
    },
    {
        "id": "P3.C",
        "stage": 3,
        "topic": "Variante de acceso — Farma & Co (solo correo del decisor)",
        "type": "single",
        "prompt": (
            "Farma & Co (México): 220 empleados, operación en México y Colombia. Apollo tiene "
            "solo el correo del VP de Operaciones, Lucía Ramírez. No hay teléfono. Nunca contactada. "
            "¿Qué variante aplica?"
        ),
        "choices": [
            {"id": "a", "text": "Variante 1 (correo + teléfono)."},
            {"id": "b", "text": "Variante 2 (solo correo — email paciente, cadencia espaciada, espera respuesta con teléfono en firma)."},
            {"id": "c", "text": "Variante 3 (sin contacto del decisor)."},
            {"id": "d", "text": "Variante 4 (referidor ya dio el contacto)."},
        ],
        "correct": "b",
        "explanation": "Solo correo del decisor → variante 2 email paciente.",
    },
    {
        "id": "P3.D.1",
        "stage": 3,
        "topic": "Variante de acceso — MediTrack Perú (recontacto)",
        "type": "single",
        "prompt": (
            "MediTrack Perú: 85 empleados, operación en Perú. Hace 5 meses Siete la contactó. El "
            "decisor respondió a la tercera secuencia: \"Interesante pero es un mal momento, estamos "
            "con la integración de una empresa que acabamos de adquirir. Hablemos en Q1 del año que "
            "viene\". Estamos en noviembre — Q1 a 2 meses. Acaban de anunciar un nuevo centro de "
            "distribución en Lima. ¿Qué variante aplica?"
        ),
        "choices": [
            {"id": "a", "text": "Variante 1."},
            {"id": "b", "text": "Variante 4 (referidor dio el contacto)."},
            {"id": "c", "text": "Variante 5 (recontacto con ángulo nuevo tras ventana de enfriamiento)."},
            {"id": "d", "text": "Variante 6 (wish list)."},
        ],
        "correct": "c",
        "explanation": "Contacto previo + ventana de enfriamiento + señal fresca → variante 5.",
    },
    {
        "id": "P4.2",
        "stage": 4,
        "topic": "Regla de ramificación de la secuencia",
        "type": "single",
        "prompt": (
            "¿Cuál debe ser la regla de ramificación declarada para esta secuencia?"
        ),
        "choices": [
            {"id": "a", "text": "Si no responde en el paso 3, escalar a 2 llamadas consecutivas + WhatsApp."},
            {"id": "b", "text": "Si responde en cualquier paso → la secuencia automática se pausa y el SDR toma control manual; si no responde después del último paso → la cuenta se archiva con trigger de recontacto (~4-6 meses)."},
            {"id": "c", "text": "Si no responde en el paso 4, aumentar el volumen de envíos a la misma persona."},
            {"id": "d", "text": "Seguir mandando touches hasta que responda o bloquee."},
        ],
        "correct": "b",
        "explanation": (
            "Aplicación directa de M4 Sem 7 Bloque 4: toda secuencia necesita regla \"pausa al "
            "responder\" + trigger de archivo con recontacto. Las otras opciones rompen la lógica "
            "del sistema o caen en saturación."
        ),
    },
    {
        "id": "P5.1",
        "stage": 5,
        "topic": "Arquetipo Challenger Customer — Carlos Rojas",
        "type": "single",
        "prompt": (
            "Carlos Rojas (VP de Operaciones de Farmacéuticos del Sur) responde al séptimo día de "
            "la secuencia mencionando: que entiende la propuesta, que tienen un proveedor SAP ad-hoc "
            "hace 3 años que cumple mínimamente con INVIMA, que cualquier cambio implica 6 meses de "
            "paralización operativa que no pueden permitirse porque están por cerrar un contrato con "
            "una cadena grande, pero pide explícitamente \"un caso concreto donde hayan migrado un "
            "SAP existente sin frenar operaciones en una empresa de nuestro tamaño\". ¿Qué arquetipo "
            "del Challenger Customer es Carlos más probablemente?"
        ),
        "choices": [
            {"id": "a", "text": "Friend (dice sí a todo, amable, accesible)."},
            {"id": "b", "text": "Skeptic (cuestiona, pide pruebas, no se convence fácil, pero cuando se convence empuja internamente)."},
            {"id": "c", "text": "Blocker (dice \"no\" a cualquier cambio sin argumentar)."},
            {"id": "d", "text": "Climber (busca ascenso, apoya lo que lo haga verse bien)."},
        ],
        "correct": "b",
        "explanation": (
            "Skeptic puro: lee con atención, menciona dolores concretos, pide caso específico, deja "
            "abierto solo con datos. No es Friend (no acepta por cortesía), no es Blocker (no dice "
            "\"no\" — dice \"mostrame\"), no es Climber (no pide nada para su carrera). Los Skeptic "
            "son Mobilizers valiosos."
        ),
    },
    {
        "id": "P5.2",
        "stage": 5,
        "topic": "Objeción vs rechazo (DIFERENCIADORA)",
        "differentiator": True,
        "type": "single",
        "prompt": (
            "¿Es esta respuesta de Carlos un rechazo funcional o una objeción con información?"
        ),
        "choices": [
            {"id": "a", "text": "Rechazo funcional — Carlos fue claro en que no van a cambiar de plataforma, hay que respetar y archivar."},
            {"id": "b", "text": "Objeción con información: da razones concretas (tiempo, timing, proveedor actual, contrato grande pendiente) + pide activamente un caso específico de migración SAP → está diciendo \"mostrame y vemos\", no \"no me interesa\". Hay espacio para seguir."},
            {"id": "c", "text": "Rechazo disfrazado — la pregunta por el caso es amabilidad, pero la decisión ya está tomada."},
            {"id": "d", "text": "Objeción superficial — hay que insistir con un ángulo distinto."},
        ],
        "correct": "b",
        "explanation": (
            "Aplicación de M3 Sem 6: la clave es que Carlos pide un entregable específico. Si fuera "
            "rechazo, diría \"gracias, no\". Cuando el prospecto pide material concreto con parámetros "
            "específicos (migración SAP, tamaño similar, sin frenar operaciones), está explicitando "
            "la condición que tendría que cumplirse para avanzar. Es objeción con información dura."
        ),
    },
    {
        "id": "P6.1",
        "stage": 6,
        "topic": "Diagnóstico por descarte con cadena causal (DIFERENCIADORA)",
        "differentiator": True,
        "type": "single",
        "prompt": (
            "Métricas semanales (no cambiaste copy, ICP, cadencia ni herramientas; en Sem 3 research "
            "cargó 80 contactos sin pasar por ZeroBounce \"se ven bien a ojo\"):\n\n"
            "Métrica          | Sem 1 | Sem 2 | Sem 3 | Sem 4\n"
            "Bounce rate      | 2.4%  | 2.6%  | 4.8%  | 6.1%\n"
            "Reply rate       | 2.1%  | 2.0%  | 0.9%  | 0.4%\n"
            "Meeting/reply    | 26%   | 28%   | 27%   | 25%\n"
            "Show rate        | 72%   | 73%   | 71%   | 74%\n"
            "Precalif aprobada| 88%   | 89%   | 86%   | 90%\n\n"
            "¿Cuál es tu hipótesis principal y cuál es tu primera acción diagnóstica?"
        ),
        "choices": [
            {"id": "a", "text": "Fatiga de mensaje — A/B test de 3 variantes de asunto."},
            {"id": "b", "text": "ICP mal calibrado — revisar filtros de Apollo y ajustar industria/cargo."},
            {"id": "c", "text": "Cadena causal: batch de Sem 3 cargado sin validar → bounce rate subió (4.8% → 6.1%, por encima del umbral crítico 3-5%) → reputación de los dominios cayó → emails correctos caen a spam → reply rate se derrumba (2.0% → 0.4%). Métricas colaterales (meeting/reply, show, precalif) estables descartan ICP/copy. Primera acción: pausar + Postmaster + ZeroBounce retroactivo sobre los 80 contactos + activar dominio de reserva si reputación severamente dañada."},
            {"id": "d", "text": "Problema del copy — volver a la versión de Sem 1 que rindió mejor."},
        ],
        "correct": "c",
        "explanation": (
            "Integra múltiples bloques en un solo razonamiento: deliverability (M4 Sem 7), "
            "consecuencia sistémica de saltear validación (M4 Sem 8 Bloque 3), diagnóstico por "
            "descarte con métricas colaterales como filtro (M4 Sem 8 Bloque 6). El alumno que "
            "acierta conecta coincidencia temporal, identifica la cadena causal, descarta copy "
            "e ICP por métricas colaterales estables, y propone acciones ordenadas."
        ),
    },
]


# ─────────────────────────────  RESPUESTAS CORTAS  ─────────────────────────────

SHORT_ANSWERS: list[dict] = [
    {
        "id": "P1.3",
        "stage": 1,
        "topic": "JTBD dominante del VP de Operaciones",
        "prompt": (
            "Si GestaLogix no existiera, ¿qué estaría haciendo hoy un VP de Operaciones de un "
            "distribuidor farmacéutico mediano para cumplir con la regulación de trazabilidad? "
            "Describí el \"job to be done\" que GestaLogix está reemplazando. Máx. 80 palabras."
        ),
        "max_words": 80,
        "expected_answer": (
            "Combinación de (a) un sistema ERP legado como SAP con módulos de trazabilidad "
            "incompletos o mal configurados, (b) planillas Excel manuales para registrar lotes + "
            "cadena de frío, (c) un equipo de compliance haciendo reportería manual antes de cada "
            "auditoría, (d) contratación de consultores externos en momentos de crisis. El JTBD "
            "dominante es \"cumplir con la regulación sin frenar las operaciones ni contratar 3 "
            "consultores cada vez que hay una auditoría\". GestaLogix reemplaza esa combinación "
            "con una plataforma única."
        ),
        "rubric": (
            "2 puntos: nombra ≥2 alternativas (ERP legacy, Excel manual, equipo de compliance, "
            "consultores) + articula el JTBD real (\"cumplir sin frenar operaciones\"). "
            "1: nombra el JTBD pero sin alternativas claras. "
            "0: genérico (\"están con sistemas viejos\")."
        ),
        "max_points": 2,
    },
    {
        "id": "P3.A.2",
        "stage": 3,
        "topic": "Primer email a Carlos Rojas (variante 1, decisor con email y teléfono)",
        "prompt": (
            "Escribí el primer email que mandarías a Carlos Rojas, VP de Operaciones de "
            "Farmacéuticos del Sur. Máx. 90 palabras. Evalúa con el grid de 6 criterios de M3 "
            "Sem 5: foco en lector, gancho específico, longitud, CTA único, propuesta sin "
            "prometer, tono directo pero respetuoso."
        ),
        "max_words": 90,
        "expected_answer": (
            "Asunto: Farmacéuticos del Sur — trazabilidad bajo INVIMA + DIGEMID\n\n"
            "Hola Carlos, Vi que Farmacéuticos del Sur tiene operación tanto en Colombia como Perú. "
            "Para empresas con presencia en ambos, cumplir con INVIMA y DIGEMID en paralelo suele "
            "ser el principal dolor de cabeza del área de operaciones. ¿Cómo están manejando hoy "
            "la trazabilidad entre las dos operaciones? Si tiene sentido, puedo contarte cómo "
            "resolvimos esto con distribuidores de tamaño similar — 15 minutos, no más. "
            "Saludos, [SDR]"
        ),
        "rubric": (
            "2 puntos: gancho específico (presencia MX/CO), pregunta abierta sin presionar, "
            "longitud apropiada (~80 palabras), un solo CTA, foco en Carlos/Farmacéuticos del Sur, "
            "tono directo. 1: razonable pero falla en 1-2 criterios. 0: pecado capital (habla de "
            "Siete + sus 40 empleados + sus clientes) o copy genérico."
        ),
        "max_points": 2,
    },
    {
        "id": "P3.B.2",
        "stage": 3,
        "topic": "Primer email al referidor (variante 3, Gerente de Cumplimiento)",
        "prompt": (
            "Escribí el primer email al Gerente de Cumplimiento Regulatorio de Distribuidora "
            "Andina como referidor potencial. Máx. 80 palabras. Nombrá explícitamente cuál es tu "
            "objetivo (qué tipo de respuesta buscás de esta persona)."
        ),
        "max_words": 80,
        "expected_answer": (
            "Objetivo: pedir orientación, no vender. Tono consultivo.\n\n"
            "Hola Patricia, Por tu rol pensé que podrías orientarme. Estoy tratando de ubicar "
            "quién en Distribuidora Andina lidera las decisiones sobre sistemas de trazabilidad "
            "y cadena de frío. ¿Sería un tema que ve directamente el VP de Operaciones, o pasa "
            "antes por alguien más? Gracias por cualquier orientación. No quiero hacerte perder "
            "tiempo con algo que no vea tu área. [SDR]"
        ),
        "rubric": (
            "2 puntos: reconoce que es variante 3, pide orientación (no vende), tono consultivo, "
            "nombra rol específico del decisor que busca, cierra con respeto al tiempo del referidor. "
            "1: reconoce variante pero el email tiene tono de venta. 0: trata al mando medio como "
            "KDM; intenta agendar demo."
        ),
        "max_points": 2,
    },
    {
        "id": "P3.D.2",
        "stage": 3,
        "topic": "Email de recontacto (variante 5) — MediTrack Perú",
        "prompt": (
            "Escribí el primer email de recontacto a MediTrack Perú. Máx. 100 palabras. Debe "
            "referenciar la interacción anterior sin culpar al prospecto + usar la señal fresca "
            "(nuevo centro de distribución en Lima) como ángulo nuevo."
        ),
        "max_words": 100,
        "expected_answer": (
            "Asunto: MediTrack + nuevo centro en Lima\n\n"
            "Hola [Nombre], Volví a acordarme de esta conversación cuando vi el anuncio del nuevo "
            "centro de distribución en Lima. En junio dijiste que Q1 era un momento más lógico — "
            "entendible, la integración llevaba su tiempo. La expansión suma otra capa de "
            "trazabilidad: cadena de frío entre centros + sincronización regulatoria DIGEMID de "
            "la nueva locación. ¿Tiene sentido agendar 15 minutos en enero para ver si el timing "
            "ahora es mejor? Saludos, [SDR]"
        ),
        "rubric": (
            "2 puntos: referencia la interacción anterior sin reproche, usa la señal fresca (nuevo "
            "centro) como ángulo nuevo, respeta el timing declarado por el prospecto, CTA condicional. "
            "1: alguna falla (tono de reproche, gancho genérico, insistencia temprana). 0: no "
            "referencia la interacción anterior o repite el mensaje que ya se había mandado."
        ),
        "max_points": 2,
    },
    {
        "id": "P4.3",
        "stage": 4,
        "topic": "Verificación de deliverability antes de ejecutar masivamente",
        "prompt": (
            "Antes de empezar a ejecutar la secuencia masivamente en 200 empresas, ¿qué 3 cosas "
            "tenés que verificar en el equipo de infraestructura para no quemar tu dominio? "
            "Máx. 80 palabras."
        ),
        "max_words": 80,
        "expected_answer": (
            "1) Warmup de los dominios de envío: si son dominios nuevos, necesitan 2-4 semanas de "
            "warmup con volumen gradual antes de outreach masivo. "
            "2) Volumen por casilla/día: no superar 80-100 emails/casilla/día para no caer a spam. "
            "3) Validación de la lista: correr ZeroBounce/similar antes de cargar los 200 contactos "
            "para mantener bounce rate <3%. "
            "Bonus: SPF/DKIM/DMARC + dominio de reserva ya warmed up."
        ),
        "rubric": (
            "2 puntos: nombra los 3 (warmup + volumen/día + validación). "
            "1: nombra 2. 0: menos."
        ),
        "max_points": 2,
    },
    {
        "id": "P5.3",
        "stage": 5,
        "topic": "Respuesta a Carlos Skeptic con caso específico",
        "prompt": (
            "Escribí exactamente lo que le responderías a Carlos. Máx. 120 palabras. Tu "
            "respuesta debe (1) reconocer su contexto sin capitular, (2) responder a la pregunta "
            "específica que hizo con honestidad, (3) proponer un next step alineado al pedido."
        ),
        "max_words": 120,
        "expected_answer": (
            "Hola Carlos, Gracias por el contexto — especialmente lo del contrato con la cadena "
            "grande. Esa restricción cambia el cálculo. Tengo dos casos que calzan con tu pedido: "
            "uno de un distribuidor colombiano de tamaño similar que migró de SAP a nuestra "
            "plataforma en fases paralelas (ERP corriendo + trazabilidad superpuesta 4 meses hasta "
            "handover), sin ventana de paralización operativa. El otro es peruano, tamaño parecido, "
            "proceso más corto pero con menor complejidad de integración. Puedo mandarte el primero "
            "en 24h con datos concretos del proyecto (tiempo, módulos, handover) para que lo analices "
            "con tu equipo técnico. ¿Te sirve así o preferís ver los dos juntos? Saludos, [SDR]"
        ),
        "rubric": (
            "2 puntos: reconoce contexto específico (contrato + paralización), responde con precisión "
            "al pedido (caso con migración SAP paralela + datos concretos), no inventa cifras, "
            "ofrece next step acotado, cierra con pregunta que mantiene agencia del prospecto. "
            "1: aceptable pero con fricciones (reunión antes del caso, promesas cuantificadas sin "
            "sustento, no nombra la restricción de paralización). "
            "0: vende sin responder al pedido, ignora la información dada, capitula."
        ),
        "max_points": 2,
    },
    {
        "id": "P6.2",
        "stage": 6,
        "topic": "Escalación tras detectar caída de deliverability",
        "prompt": (
            "¿Qué escalás, a quién, y cuándo? Máx. 100 palabras."
        ),
        "max_words": 100,
        "expected_answer": (
            "El mismo día (no esperar 1 semana más), escalo a:\n"
            "● Team Lead: reporte por Slack/email: \"bounce rate subió a 6.1% y reply rate cayó 75%; "
            "probable problema de deliverability por batch no validado en Sem 3; pausé campaña hasta "
            "verificar Postmaster y correr ZeroBounce retroactivo\". Decisión urgente.\n"
            "● Equipo de research: como propuesta de política (no reproche): \"ningún batch entra "
            "a la lista sin pasar por ZeroBounce, aunque se vea bien a ojo\".\n"
            "● Outbound Specialist: verificar estado de dominios de reserva (warmup completo) "
            "para poder rotar si la reputación no se recupera en 1-2 semanas."
        ),
        "rubric": (
            "2 puntos: escala el mismo día, a 3 niveles (Team Lead + research + Outbound Specialist), "
            "con mensaje claro + datos + propuesta de política preventiva, sin reproche. "
            "1: escala pero incompleto (solo Team Lead, o sin propuesta preventiva, o con reproche). "
            "0: no escala o tarda en hacerlo; pide permiso para hacer cosas que tiene autonomía para hacer."
        ),
        "max_points": 2,
    },
    {
        "id": "P6.3",
        "stage": 6,
        "topic": "Hipótesis testeable de mejora continua (DIFERENCIADORA)",
        "differentiator": True,
        "prompt": (
            "En el 1:1 con tu Team Lead de la próxima semana, tenés que proponer una hipótesis "
            "testeable para evitar que este tipo de incidente vuelva a pasar. Formulala según PDCA. "
            "Máx. 100 palabras."
        ),
        "max_words": 100,
        "expected_answer": (
            "Hipótesis: si establecemos como regla dura \"ningún contacto entra al motor de "
            "secuencias sin pasar validación automatizada + revisión de bounce rate semanal\" + "
            "\"cualquier bounce rate semanal que supere 3% dispara pausa automática del SDR "
            "afectado\", el número de incidentes de deliverability críticos debería caer a ≤1 al "
            "semestre. Test: implementar la regla el próximo lunes. Medir durante 3 meses: número "
            "de eventos donde bounce rate >3% en una semana + tiempo medio de detección (objetivo: "
            "≤48h desde el inicio del síntoma). Magnitud esperada: -70% en incidentes críticos."
        ),
        "rubric": (
            "3 puntos: hipótesis formulada con \"si X → entonces Y\" + variable única (regla) + "
            "método de medición + magnitud esperada + timeline de evaluación. Todo explícito. "
            "2: razonable pero falla en 1 elemento (sin magnitud o sin método claro). "
            "1: vaga pero apuntada en la dirección correcta. "
            "0: plan de acción sin método (\"voy a tener más cuidado con los batches\")."
        ),
        "max_points": 3,
    },
]


# ─────────────────────────────  TABLAS ESTRUCTURADAS  ─────────────────────────────

TABLES: list[dict] = [
    {
        "id": "P2.1",
        "stage": 2,
        "topic": "Clasificación de filtros del ICP",
        "prompt": (
            "Completá la tabla con filtros operativos del ICP de GestaLogix. Marcá cada criterio "
            "como Duro (estructural), Señal (trigger de compra) o Negativo (descartar)."
        ),
        "rows": [
            {"id": "1", "label": "Distribuidor farmacéutico (industria)", "correct": "duro"},
            {"id": "2", "label": "50-500 empleados", "correct": "duro"},
            {"id": "3", "label": "Operación en al menos 2 de MX/CO/PE", "correct": "duro"},
            {"id": "4", "label": "Levantó ronda de inversión en los últimos 12 meses", "correct": "senal"},
            {"id": "5", "label": "Recibió una multa o sanción regulatoria reciente (COFEPRIS/INVIMA/DIGEMID)", "correct": "senal"},
            {"id": "6", "label": "Empresas que ya trabajan con TraceLink o Systech — descartar", "correct": "negativo"},
            {"id": "7", "label": "Expansión anunciada a un nuevo país o nueva bodega", "correct": "senal"},
            {"id": "8", "label": "Contrató Gerente de Cumplimiento Regulatorio en los últimos 6 meses", "correct": "senal"},
            {"id": "9", "label": "Empresa cuyo outbound ya pasó sin respuesta en los últimos 3 meses", "correct": "negativo"},
        ],
        "options": [
            {"id": "duro", "label": "Filtro duro (ICP estructural)"},
            {"id": "senal", "label": "Filtro de señal (trigger de compra)"},
            {"id": "negativo", "label": "Filtro negativo (descartar)"},
        ],
        "rubric": (
            "1 punto cada 3 respuestas correctas. Máx. 3 puntos (9 de 9). "
            "Umbral: 6 correctas para aprobar la pregunta."
        ),
        "max_points": 3,
    },
    {
        "id": "P4.1",
        "stage": 4,
        "topic": "Secuencia outbound de 6-7 touchpoints en 13-15 días",
        "prompt": (
            "Volvés a Farmacéuticos del Sur (variante 1). Después del primer email (Etapa 3), "
            "tenés que declarar toda la secuencia. Completá 6-7 touchpoints en 13-15 días. Para "
            "cada paso declará día, canal y propósito de esa acción (en 1 línea)."
        ),
        "expected_sequence": [
            {"paso": 1, "dia": 0, "canal": "email", "proposito": "Primer email con gancho específico (cumplimiento INVIMA + DIGEMID multi-país)"},
            {"paso": 2, "dia": 3, "canal": "email", "proposito": "Follow-up con nuevo ángulo: cliente similar cerrando cadena de frío"},
            {"paso": 3, "dia": 5, "canal": "telefono", "proposito": "Llamada corta referenciando los emails + permission-based opener"},
            {"paso": 4, "dia": 8, "canal": "email", "proposito": "Nuevo thread con pregunta distinta (no repetir) — por ej., cómo manejan auditorías actuales"},
            {"paso": 5, "dia": 11, "canal": "telefono", "proposito": "Segundo y último intento de llamada + despedida si no contesta"},
            {"paso": 6, "dia": 14, "canal": "email", "proposito": "Último email — cierra abierto (\"si esto cambia, quedo disponible\")"},
        ],
        "rubric": (
            "3 puntos: 6-7 touchpoints, 13-15 días, email → llamada → email → llamada coherente, "
            "ningún touch repetido idéntico, la llamada aparece después de al menos 1-2 emails. "
            "2: cumple la mayoría pero con errores menores (1 día de más/menos, touch repetido en forma). "
            "1: cadencia aceptable pero con errores de orden (WhatsApp como entrada, llamada el día 0). "
            "0: cadencia rota (3 touches en 2 días, 12 touches, o sin lógica)."
        ),
        "max_points": 3,
    },
]


# ─────────────────────────────  RÚBRICA DEL VIDEO  ─────────────────────────────

VIDEO_RUBRIC_15: dict = {
    "scale_per_dim": "0-2",
    "max_total": 30,
    "conversion": {
        "30": 100, "24": 80, "18": 60,
    },
    "critical_dimensions_for_distinction": [1, 2, 3, 4],
    "min_critical_for_distinction": "11/12 o 12/12",
    "dimensions": [
        {"id": 1, "label": "Identificación del problema", "critical": True,
         "scale": [
             {"score": 0, "descriptor": "No lo identifica o lo confunde."},
             {"score": 1, "descriptor": "Identifica parcialmente."},
             {"score": 2, "descriptor": "Identifica claro y correcto de entrada."},
         ]},
        {"id": 2, "label": "Uso de vocabulario específico del curso", "critical": True,
         "scale": [
             {"score": 0, "descriptor": "Habla en frases genéricas sin nombrar conceptos."},
             {"score": 1, "descriptor": "Usa 1-2 conceptos pero superficiales."},
             {"score": 2, "descriptor": "Nombra bloques específicos y conceptos con precisión (variantes de acceso, 6 canales, objeción vs rechazo, diagnóstico por descarte, PDCA, etc.)."},
         ]},
        {"id": 3, "label": "Jerarquización de causas", "critical": True,
         "scale": [
             {"score": 0, "descriptor": "No prioriza."},
             {"score": 1, "descriptor": "Prioriza en general pero sin justificar."},
             {"score": 2, "descriptor": "Justifica por qué una causa es más grave que otra con datos o lógica del funnel."},
         ]},
        {"id": 4, "label": "Integración entre módulos", "critical": True,
         "scale": [
             {"score": 0, "descriptor": "Defiende una decisión con un solo módulo."},
             {"score": 1, "descriptor": "Cruza 2 módulos."},
             {"score": 2, "descriptor": "Cruza 3-4 módulos en una misma decisión."},
         ]},
        {"id": 5, "label": "Presentación personal breve",
         "scale": [
             {"score": 0, "descriptor": "Ausente."},
             {"score": 1, "descriptor": "Larga o autorreferencial."},
             {"score": 2, "descriptor": "Corta, clara, enfocada."},
         ]},
        {"id": 6, "label": "Estructura del video",
         "scale": [
             {"score": 0, "descriptor": "Desordenada."},
             {"score": 1, "descriptor": "Cumple estructura pero con saltos."},
             {"score": 2, "descriptor": "Estructura clara, transiciones entre decisiones."},
         ]},
        {"id": 7, "label": "Decisión 1 — claridad del contexto",
         "scale": [
             {"score": 0, "descriptor": "Confuso."},
             {"score": 1, "descriptor": "Se entiende con esfuerzo."},
             {"score": 2, "descriptor": "Claro de entrada."},
         ]},
        {"id": 8, "label": "Decisión 1 — justificación",
         "scale": [
             {"score": 0, "descriptor": "Genérica."},
             {"score": 1, "descriptor": "Con algún concepto."},
             {"score": 2, "descriptor": "Con concepto + razón específica al caso."},
         ]},
        {"id": 9, "label": "Decisión 2 — claridad del contexto",
         "scale": [
             {"score": 0, "descriptor": "Confuso."},
             {"score": 1, "descriptor": "Se entiende con esfuerzo."},
             {"score": 2, "descriptor": "Claro de entrada."},
         ]},
        {"id": 10, "label": "Decisión 2 — justificación",
         "scale": [
             {"score": 0, "descriptor": "Genérica."},
             {"score": 1, "descriptor": "Con algún concepto."},
             {"score": 2, "descriptor": "Con concepto + razón específica al caso."},
         ]},
        {"id": 11, "label": "Decisión 3 — claridad del contexto",
         "scale": [
             {"score": 0, "descriptor": "Confuso."},
             {"score": 1, "descriptor": "Se entiende con esfuerzo."},
             {"score": 2, "descriptor": "Claro de entrada."},
         ]},
        {"id": 12, "label": "Decisión 3 — justificación",
         "scale": [
             {"score": 0, "descriptor": "Genérica."},
             {"score": 1, "descriptor": "Con algún concepto."},
             {"score": 2, "descriptor": "Con concepto + razón específica al caso."},
         ]},
        {"id": 13, "label": "Cierre — qué aprendiste",
         "scale": [
             {"score": 0, "descriptor": "Ausente o superficial."},
             {"score": 1, "descriptor": "Genérico (\"aprendí mucho\")."},
             {"score": 2, "descriptor": "Específico, conectado con decisiones concretas."},
         ]},
        {"id": 14, "label": "Cierre — qué harías distinto",
         "scale": [
             {"score": 0, "descriptor": "Ausente o \"nada, todo bien\"."},
             {"score": 1, "descriptor": "Cambios menores sin justificar."},
             {"score": 2, "descriptor": "Cambios específicos justificados con conceptos del curso."},
         ]},
        {"id": 15, "label": "Dominio verbal",
         "scale": [
             {"score": 0, "descriptor": "Lectura, muletillas constantes."},
             {"score": 1, "descriptor": "Acepta pero con pérdidas."},
             {"score": 2, "descriptor": "Habla con fluidez, responde a sí mismo con sentido."},
         ]},
    ],
}


# ─────────────────────────────  RÚBRICA GENÉRICA RESPUESTAS CORTAS  ─────────────

GENERIC_SHORT_RUBRIC: dict = {
    "scale": "0-2",
    "scoring": [
        {"score": 0, "descriptor": "No cumple lo pedido / fuera de tema / contradice lo enseñado / inventa datos no dados / es genérico copiable."},
        {"score": 1, "descriptor": "Cumple parcialmente. Identifica algún concepto correcto pero le falta especificidad al caso, o introduce un error notable, o usa la herramienta sin justificarla."},
        {"score": 2, "descriptor": "Cumple los 4 criterios: (a) específico al caso (no genérico), (b) usa vocabulario del curso correctamente, (c) decide algo concreto y trazable al diagnóstico, (d) respeta el límite de palabras pedido."},
    ],
    "by_type": {
        "emails": "Gancho específico (señal verificable, no genérica) + tono apropiado al destinatario (consultivo si referidor, propuesta si decisor, reconocimiento si recontacto) + un solo CTA + grid de 6 criterios + límite de palabras.",
        "tables": "2 = ≥80% correcto; 1 = 50-79%; 0 = <50%.",
        "diagnostics": "Identifica causa raíz (no síntoma) + estructura \"si X → entonces Y\" + variable única + método de medición + magnitud esperada + acción concreta priorizada.",
        "escalations": "Escala el mismo día + identifica a quién escalar (jerarquía + roles relevantes) + incluye propuesta preventiva, no solo reporte.",
    },
}


# ─────────────────────────────  PREGUNTAS DIFERENCIADORAS  ─────────────────────

DIFFERENTIATOR_IDS: list[str] = ["P1.4", "P5.2", "P6.1", "P6.3"]
"""IDs que pesan el doble en el cálculo de distinción. ≥75% acumulado en estas 4
preguntas es requisito para graduación con distinción (junto con curso ≥85%,
módulos ≥80%, prueba final ≥85%, video 11/12 o 12/12 en dimensiones críticas)."""


# ─────────────────────────────  PESOS Y UMBRALES  ──────────────────────────────

# Doc líneas 13487-13496: Nota Prueba Final = (Caso × 0.7) + (Video × 0.3)
WEIGHTS = {"case": 0.7, "video": 0.3}

# Doc línea 12726-12729
PASSING_SCORE = 60.0          # graduación básica
DISTINCTION_SCORE = 85.0      # graduación con distinción


def total_mcq_count() -> int:
    return len(MCQ)


def total_short_answers() -> int:
    return len(SHORT_ANSWERS)


def differentiator_questions() -> list[dict]:
    """Devuelve las 4 preguntas marcadas como diferenciadoras (MCQ + short answer)."""
    out: list[dict] = []
    for q in MCQ:
        if q.get("differentiator"):
            out.append(q)
    for q in SHORT_ANSWERS:
        if q.get("differentiator"):
            out.append(q)
    return out
