"""Contenido Capa 2 — Prueba del Módulo 4 (El sistema).

Fuente: SDR_Academy_Siete_Documento_Maestro.md, Parte IV §Prueba del Módulo 4,
líneas 11519-12118, v0.1 (2026-04-24).

Estructura:
- MCQ: 16 preguntas (Sem 7 + Sem 8 del Módulo 4). 70% del peso de la prueba.
- VIDEO_CASES: 4 casos de banco para video narrado (1 asignado al azar). 30% del peso.
- VIDEO_RUBRIC: 3 criterios × 0-2 puntos → /6 → conversión a %.
"""

MCQ: list[dict] = [
    {
        "id": "M4.1",
        "topic": "Artesano vs sistema: cuándo aplica cada uno",
        "section": "sem7",
        "type": "single",
        "prompt": (
            "¿En cuál de los siguientes casos tiene sentido usar enfoque artesanal "
            "(research profundo, 4-6 h por cuenta) en vez de operar dentro del sistema?"
        ),
        "choices": [
            {"id": "a", "text": "Cuando el SDR quiere probar un copy nuevo antes de subirlo a la secuencia estándar."},
            {"id": "b", "text": "Cuando la cuenta es de muy alta prioridad (wish list del cliente, deal potencial de USD 500K+/año) o cuando el ICP es incierto en un mercado nuevo y hay que aprender artesanalmente antes de armar el sistema."},
            {"id": "c", "text": "Cuando el SDR se siente agotado de mandar emails en bulk y quiere un día \"distinto\" para no quemarse."},
            {"id": "d", "text": "Cuando el Team Lead pide más reuniones y el SDR cree que el enfoque personalizado va a convencer más."},
        ],
        "correct": "b",
        "explanation": (
            "Artesanal aplica ~5% del trabajo y se justifica solo en dos casos: wish list (deal grande "
            "que paga el research) o mercado nuevo donde el ICP se aprende cuenta por cuenta antes de "
            "sistematizar (Sem 7 Bloque 1). Las otras 3 opciones son racionalizaciones del SDR novato."
        ),
    },
    {
        "id": "M4.2",
        "topic": "Multi-select — errores estructurales en secuencia",
        "section": "sem7",
        "type": "multi",
        "prompt": (
            "Un SDR propone esta secuencia para un KDM con email y teléfono verificados:\n\n"
            "Paso 1 — Día 0 — WhatsApp — Mensaje presentándose\n"
            "Paso 2 — Día 1 — Email — Primer email con pitch\n"
            "Paso 3 — Día 1 — Teléfono — Llamada\n"
            "Paso 4 — Día 2 — Email — Follow-up\n"
            "Paso 5 — Día 3 — Teléfono — Segunda llamada\n"
            "Paso 6 — Día 4 — WhatsApp — Empujón\n"
            "Paso 7 — Día 5 — Email — Último email\n\n"
            "Marcá todos los errores estructurales de esta secuencia:"
        ),
        "choices": [
            {"id": "1", "text": "Arranca con WhatsApp en frío como primer touch — WhatsApp es empujón tras contacto previo, no entrada."},
            {"id": "2", "text": "7 touchpoints comprimidos en 5 días — cadencia demasiado pegada, rompe benchmark 4-7 touches espaciados 2-4 días, ventana total 10-20 días."},
            {"id": "3", "text": "La llamada del día 1 aparece antes del follow-up por email — la llamada entra sin contexto escrito acumulado."},
            {"id": "4", "text": "No declara regla de ramificación (qué pasa si el prospecto responde)."},
            {"id": "5", "text": "Usa teléfono dos veces en la secuencia — nunca debería llamarse dos veces al mismo prospecto."},
            {"id": "6", "text": "El último touch es un email, cuando debería ser siempre una llamada de despedida."},
        ],
        "correct": ["1", "2", "3", "4"],
        "explanation": (
            "1, 2, 3 y 4 son errores estructurales (Sem 7 Bloques 4 y 5). (5) falso: llamar dos veces "
            "es estándar — el problema no es el canal repetido sino la cadencia comprimida. "
            "(6) falso: no hay regla de cerrar con llamada — muchas secuencias cierran con email \"cierra abierto\"."
        ),
    },
    {
        "id": "M4.3",
        "topic": "Variante de acceso al decisor",
        "section": "sem7",
        "type": "single",
        "prompt": (
            "Prospectás a LogisTech Colombia, empresa de logística de 200 empleados. En Apollo confirmás:\n"
            "● El decisor (VP de Operaciones) tiene correo verificado pero no teléfono.\n"
            "● La empresa no fue contactada antes.\n\n"
            "¿Qué variante de acceso al decisor corresponde?"
        ),
        "choices": [
            {"id": "a", "text": "Variante 1 — multicanal proactivo (correo + teléfono + WhatsApp)."},
            {"id": "b", "text": "Variante 2 — email paciente con cadencia espaciada, esperando respuesta para migrar a multicanal."},
            {"id": "c", "text": "Variante 3 — vía referidores dentro de la empresa buscando champions."},
            {"id": "d", "text": "Variante 5 — recontacto con ángulo nuevo después de ventana de enfriamiento."},
        ],
        "correct": "b",
        "explanation": (
            "Tenés correo verificado del decisor pero no teléfono. Eso es variante 2 (Sem 7 Bloque 6): "
            "más touches por email (4-5), cadencia espaciada. Si el prospecto responde, aparece "
            "teléfono en la firma y podés migrar a multicanal. Descartás V1 (requiere teléfono), "
            "V3 (aplica sin contacto del decisor), V5 (aplica con contacto previo sin éxito)."
        ),
    },
    {
        "id": "M4.4",
        "topic": "Multicanal vs canal único — el lift 2-3x",
        "section": "sem7",
        "type": "single",
        "prompt": (
            "Estudios de la industria (Salesloft State of Sales, Outreach, consultoras outbound) muestran "
            "consistentemente que las secuencias multicanal (email + llamada + LinkedIn) generan 2x a 3x "
            "más engagement que las secuencias email-only.\n\n"
            "¿Cuál es la explicación conceptual de ese \"2-3x\"?"
        ),
        "choices": [
            {"id": "a", "text": "Las secuencias multicanal son más largas en tiempo total, así que hay más probabilidad de encontrar al prospecto en un buen momento."},
            {"id": "b", "text": "Cada canal alcanza a un subconjunto del ICP (gente que abre emails ≠ gente que atiende llamadas ≠ gente que usa LinkedIn activamente); al combinar 2-3 canales se amplía la cobertura del ICP."},
            {"id": "c", "text": "El algoritmo de Gmail y Outlook prioriza emails de dominios que también aparecen en LinkedIn, así que combinar canales mejora la deliverability."},
            {"id": "d", "text": "Multicanal genera más presión sobre el prospecto, lo que aumenta la tasa de respuesta por agotamiento."},
        ],
        "correct": "b",
        "explanation": (
            "Diversificación de cobertura (Sem 7 Bloque 3). 30-40% no abre emails, 40-50% no atiende "
            "llamadas, 30-50% no usa LinkedIn activamente. Combinar 2-3 canales diversifica los sesgos. "
            "(a) confunde correlación con causalidad, (c) es mito técnico, (d) violaría \"multicanal no es saturación\"."
        ),
    },
    {
        "id": "M4.5",
        "topic": "Pareo canal y cuándo funciona",
        "section": "sem7",
        "type": "match",
        "prompt": (
            "Emparejá cada canal con su perfil operativo:\n\n"
            "1) Email\n"
            "2) Teléfono\n"
            "3) LinkedIn\n"
            "4) WhatsApp\n"
            "5) Video personalizado"
        ),
        "left": [
            {"id": "1", "text": "Email"},
            {"id": "2", "text": "Teléfono"},
            {"id": "3", "text": "LinkedIn"},
            {"id": "4", "text": "WhatsApp"},
            {"id": "5", "text": "Video personalizado"},
        ],
        "right": [
            {"id": "A", "text": "Canal base del sistema. Alta escala, baja fricción, asíncrono. \"Los carbohidratos\" del outbound."},
            {"id": "B", "text": "Amplificador. Sincrónico. Después de emails, hace que el nombre sea familiar cuando suena el teléfono."},
            {"id": "C", "text": "Research + micro-touch. Mala idea tratarlo como \"otro canal de cold email\"."},
            {"id": "D", "text": "Empujón tras contacto previo. Tasa de respuesta alta en LATAM B2B cuando se usa bien, bloqueo alto si es frío."},
            {"id": "E", "text": "Artesanal. Tasas 2-3x superiores pero toma 5-10 min por envío. Se reserva para cuentas ABM o reactivaciones."},
        ],
        "correct": {"1": "A", "2": "B", "3": "C", "4": "D", "5": "E"},
        "explanation": (
            "Discriminación entre los 5 canales es la base conceptual de Sem 7 Bloque 5. Un alumno que "
            "confunde LinkedIn con WhatsApp o email con video no tiene calibrado el marco de función por canal."
        ),
    },
    {
        "id": "M4.6",
        "topic": "Multi-select — síntomas de casilla quemada",
        "section": "sem7",
        "type": "multi",
        "prompt": (
            "Un SDR sospecha que una de sus casillas de envío se quemó. Marcá todos los síntomas "
            "consistentes con una casilla quemada:"
        ),
        "choices": [
            {"id": "1", "text": "Bounce rate superior al 5% en las últimas 2 semanas."},
            {"id": "2", "text": "Score en mail-tester.com cayó a 4/10 desde 8/10 previos."},
            {"id": "3", "text": "Tasa de respuesta cayó drásticamente sin cambio de copy."},
            {"id": "4", "text": "Los emails llegan más lento de lo habitual — toman 30 minutos en llegar al destinatario."},
            {"id": "5", "text": "Google Postmaster Tools reporta reputación \"mala\" o \"baja\"."},
            {"id": "6", "text": "Los prospectos que responden dicen cosas como \"no me interesa\" más seguido que antes."},
        ],
        "correct": ["1", "2", "3", "5"],
        "explanation": (
            "1, 2, 3 y 5 son síntomas reales (Sem 7 Bloque 7). (4) falso: latencia de entrega es "
            "infraestructura, no deliverability — casilla quemada va a spam o no entrega, no entrega lento. "
            "(6) falso: \"no me interesa\" es señal de calidad del mensaje/ICP, no de deliverability."
        ),
    },
    {
        "id": "M4.7",
        "topic": "Herramientas como instrumentación del concepto",
        "section": "sem7",
        "type": "match",
        "prompt": (
            "Emparejá cada concepto con el grupo de herramientas que lo instrumenta:\n\n"
            "1) Base de datos de prospectos con filtros de ICP y señales\n"
            "2) Motor de secuencias multicanal con reglas de ramificación\n"
            "3) Warmup automatizado para dominios\n"
            "4) Monitoreo de deliverability y reputación"
        ),
        "left": [
            {"id": "1", "text": "Base de datos de prospectos"},
            {"id": "2", "text": "Motor de secuencias multicanal"},
            {"id": "3", "text": "Warmup automatizado"},
            {"id": "4", "text": "Monitoreo de deliverability"},
        ],
        "right": [
            {"id": "A", "text": "Reply.io, Outreach, Salesloft, Instantly, Smartlead"},
            {"id": "B", "text": "Google Postmaster Tools, MXToolbox, GlockApps"},
            {"id": "C", "text": "Apollo, ZoomInfo, Crunchbase, Lusha"},
            {"id": "D", "text": "MailReach, Instantly Warmup, Smartlead Warmup"},
        ],
        "correct": {"1": "C", "2": "A", "3": "D", "4": "B"},
        "explanation": (
            "Las herramientas se reemplazan, los conceptos se quedan (Sem 7 Bloque 8). Apollo no manda "
            "emails y Reply.io no tiene contactos. El alumno que confunde \"motor de secuencias\" con "
            "\"base de datos\" no entendió el marco."
        ),
    },
    {
        "id": "M4.8",
        "topic": "Saltear etapa del proceso — consecuencia sistémica",
        "section": "sem8",
        "type": "single",
        "prompt": (
            "Un SDR decide saltear la etapa 3 (limpieza y validación) para empezar a mandar la campaña antes.\n\n"
            "¿Cuál es la consecuencia más grave?"
        ),
        "choices": [
            {"id": "a", "text": "El SDR recibe muchos bounces en el inbox y genera ruido operativo los primeros días."},
            {"id": "b", "text": "Se pierde 10-15% de los contactos porque eran emails inválidos; reduce la muestra pero no afecta al resto."},
            {"id": "c", "text": "Bounce rate sube por encima del umbral → reputación del dominio cae → los próximos emails (incluso los correctos) van a spam → reply rate de todo el sistema se derrumba por semanas."},
            {"id": "d", "text": "El CRM queda contaminado con contactos inválidos y hay que limpiarlo después manualmente."},
        ],
        "correct": "c",
        "explanation": (
            "La etapa 3 genera daño amplificado aguas abajo, no solo daño local (Sem 8 Bloque 3). "
            "Un atajo de 30 min cuesta 3 semanas de recuperación porque rompe la infraestructura "
            "(reputación del dominio)."
        ),
    },
    {
        "id": "M4.9",
        "topic": "Armado de listas — los 3 filtros",
        "section": "sem8",
        "type": "match",
        "prompt": (
            "Un SDR está armando una lista para una campaña a fintechs en Chile. Clasificá cada criterio "
            "en filtros duros, filtros de señal o filtros negativos.\n\n"
            "1) Industria: fintech B2B / B2C\n"
            "2) Anunció Serie A/B en los últimos 90 días\n"
            "3) Empresa en Chile\n"
            "4) Empresas con las que el outbound ya pasó sin respuesta en los últimos 3 meses\n"
            "5) Cargo objetivo: VP Sales, Director Comercial\n"
            "6) Contrató 10+ personas en los últimos 90 días"
        ),
        "left": [
            {"id": "1", "text": "Industria: fintech B2B / B2C"},
            {"id": "2", "text": "Anunció Serie A/B en los últimos 90 días"},
            {"id": "3", "text": "Empresa en Chile"},
            {"id": "4", "text": "Empresas con outbound sin respuesta en los últimos 3 meses"},
            {"id": "5", "text": "Cargo objetivo: VP Sales, Director Comercial"},
            {"id": "6", "text": "Contrató 10+ personas en los últimos 90 días"},
        ],
        "right": [
            {"id": "A", "text": "Filtros duros (ICP estructural)"},
            {"id": "B", "text": "Filtros de señal (triggers de compra)"},
            {"id": "C", "text": "Filtros negativos (descartar)"},
        ],
        "correct": {"1": "A", "2": "B", "3": "A", "4": "C", "5": "A", "6": "B"},
        "explanation": (
            "Una lista buena combina los 3 tipos de filtro (Sem 8 Bloque 2). \"Cuantos más contactos, "
            "mejor\" es trampa — 500 con filtros bien aplicados rinde 10x que 5000 sin filtros."
        ),
    },
    {
        "id": "M4.10",
        "topic": "Ejecución diaria — bloques y cambio de contexto",
        "section": "sem8",
        "type": "single",
        "prompt": (
            "¿Cuál de las siguientes prácticas protege mejor la productividad del SDR según el principio "
            "de Goldratt (el SDR es el cuello de botella)?"
        ),
        "choices": [
            {"id": "a", "text": "Intercalar 15 min de emails + 15 min de llamadas + 15 min de CRM a lo largo del día para mantener variedad y no aburrirse."},
            {"id": "b", "text": "Hacer todos los llamados en un bloque sin interrupciones (60-90 min) en los horarios pico de contactabilidad, y batir las tareas de baja concentración (CRM, coordinaciones) en lotes específicos."},
            {"id": "c", "text": "Responder Slack y emails internos cada vez que llega una notificación, para no acumular pendientes al final del día."},
            {"id": "d", "text": "Dedicar toda la mañana solo a personalización artesanal de emails y toda la tarde solo a llamadas."},
        ],
        "correct": "b",
        "explanation": (
            "Bloques de alta concentración + batching de baja concentración (Sem 8 Bloque 4). Protege el "
            "foco del SDR (el cuello de botella). (a) error clásico del novato (40 cambios de contexto/día). "
            "(c) destruye foco. (d) ignora picos de contactabilidad (llamadas van en mañana + 14-15h)."
        ),
    },
    {
        "id": "M4.11",
        "topic": "Diagnóstico por descarte sobre un tablero de métricas",
        "section": "sem8",
        "type": "single",
        "prompt": (
            "Tablero semanal de la SDR Valeria. La Semana 4 muestra la anomalía:\n\n"
            "Métrica                    | Sem 1 | Sem 2 | Sem 3 | Sem 4\n"
            "Tasa de rebote             | 2.1%  | 2.2%  | 2.0%  | 2.1%\n"
            "Tasa de respuesta          | 2.4%  | 2.3%  | 2.5%  | 2.4%\n"
            "Reuniones sobre respuestas | 26%   | 27%   | 25%   | 9%\n"
            "Tasa de asistencia         | 73%   | 72%   | 74%   | 73%\n"
            "Precalificaciones aprobadas| 88%   | 90%   | 87%   | 89%\n\n"
            "Valeria no cambió el mensaje, ni el ICP, ni la cadencia, ni el volumen. Solo cayeron "
            "las reuniones sobre respuestas.\n\n"
            "Siguiendo el método de diagnóstico por descarte, ¿dónde está más probablemente la causa?"
        ),
        "choices": [
            {"id": "a", "text": "En el ICP (etapa 1): probablemente entraron prospectos que no encajan, y por eso responden, pero no agendan."},
            {"id": "b", "text": "En la entregabilidad (etapas 4-5): probablemente los correos están cayendo a spam y por eso se pierden reuniones."},
            {"id": "c", "text": "En la gestión de respuestas (etapa 7): llegan las mismas respuestas que antes, pero se están convirtiendo peor en reuniones agendadas."},
            {"id": "d", "text": "En la precalificación (etapa 9): probablemente se están filtrando de más los prospectos antes de la reunión."},
        ],
        "correct": "c",
        "explanation": (
            "Diagnóstico por descarte (Sem 8 Bloque 6): la métrica que cae es \"reuniones sobre "
            "respuestas\", que describe la etapa 7 (gestión de respuestas) — llegan las mismas "
            "respuestas pero se convierten peor en reuniones agendadas. Las métricas vecinas estables "
            "(rebote, respuesta, asistencia, precalificación) descartan ICP, entregabilidad y precalificación."
        ),
    },
    {
        "id": "M4.12",
        "topic": "Por qué NO se mide open rate",
        "section": "sem8",
        "type": "multi",
        "prompt": (
            "Marcá todas las razones reales por las que el outbound B2B moderno no mide open rate:"
        ),
        "choices": [
            {"id": "1", "text": "El pixel de tracking daña deliverability — los filtros anti-spam lo detectan y clasifican el email como marketing."},
            {"id": "2", "text": "Apple Mail Privacy Protection pre-abre los emails en el servidor → infla el open rate artificialmente."},
            {"id": "3", "text": "Los prospectos aprendieron a desactivar el tracking y ya no sirve medirlo."},
            {"id": "4", "text": "Otros clientes (Outlook, Gmail con imágenes off) devuelven open=false aunque el prospecto haya leído el email."},
            {"id": "5", "text": "El reply rate y el bounce rate son señales comportamentales/técnicas más duras y reemplazan al open rate."},
            {"id": "6", "text": "Los pixels fueron prohibidos por regulación de privacidad en la Unión Europea desde 2024."},
        ],
        "correct": ["1", "2", "4", "5"],
        "explanation": (
            "1, 2, 4 y 5 son reales (Sem 8 Bloque 5). (3) falso: la distorsión es estructural, no cultural. "
            "(6) falso: no hay regulación que prohíba pixels — es un mito de pasillo."
        ),
    },
    {
        "id": "M4.13",
        "topic": "Cargar más contactos de los que el sistema procesa",
        "section": "sem8",
        "type": "single",
        "prompt": (
            "Para \"ir más rápido\", un SDR carga en sus secuencias el doble de contactos de los que "
            "su infraestructura de correos y su tiempo pueden procesar en una semana.\n\n"
            "¿Qué ocurre, y qué métrica lo delata?"
        ),
        "choices": [
            {"id": "a", "text": "Cae la tasa de finalización de la secuencia: muchos contactos quedan a mitad de la cadencia y nunca completan sus toques; cargar de más no procesa más, sino peor."},
            {"id": "b", "text": "Sube la tasa de respuesta, porque tener más contactos activos a la vez aumenta la probabilidad de que alguno conteste en cada tanda de envíos."},
            {"id": "c", "text": "No pasa nada relevante mientras la infraestructura de correos aguante el volumen, ya que el tiempo del SDR no es una restricción real del sistema."},
            {"id": "d", "text": "Mejora la cobertura del ICP, porque cargar más contactos amplía la variedad de perfiles alcanzados y reparte mejor el esfuerzo de la campaña."},
        ],
        "correct": "a",
        "explanation": (
            "El SDR es el cuello de botella del sistema (Sem 8 Bloque 4). Cargar el doble de la "
            "capacidad real deja muchos contactos a mitad de la cadencia: cae la tasa de finalización "
            "de la secuencia. Cargar de más no procesa más, sino peor."
        ),
    },
    {
        "id": "M4.14",
        "topic": "PDCA — hipótesis testeable vs intuición",
        "section": "sem8",
        "type": "single",
        "prompt": (
            "¿Cuál de las siguientes es una hipótesis testeable según el ciclo PDCA / Build-Measure-Learn?"
        ),
        "choices": [
            {"id": "a", "text": "\"El mensaje que uso para industrias de retail no está funcionando; voy a cambiarlo esta semana.\""},
            {"id": "b", "text": "\"Tengo la intuición de que las llamadas a las 10 AM rinden más que a las 14h; voy a probar.\""},
            {"id": "c", "text": "\"Si cambio el asunto de 'Pregunta rápida' a '[Empresa], sobre su expansión regional', el reply rate sube ≥0.5 puntos. Test: 100 envíos con cada asunto en 2 semanas, comparar reply rate contra 100 envíos previos con el asunto viejo.\""},
            {"id": "d", "text": "\"Creo que el problema está en que los prospectos no confían; voy a empezar a mandar casos de éxito con los emails.\""},
        ],
        "correct": "c",
        "explanation": (
            "Cumple las 3 condiciones de hipótesis testeable (Sem 8 Bloque 7): formulación \"si X → "
            "entonces Y\", variable única (el asunto), método de medición declarado (100 vs 100, 2 "
            "semanas, reply rate). Las otras son intuiciones/acciones sin magnitud esperada, sin "
            "muestra declarada, ni cómo medir."
        ),
    },
    {
        "id": "M4.15",
        "topic": "Cadencia — timing entre touches",
        "section": "sem7",
        "type": "single",
        "prompt": (
            "Según Instantly 2026, la cadencia de secuencias outbound que mejor rinde es 4-7 touchpoints "
            "espaciados 2-4 días, ventana total 10-20 días hábiles, con 2-4 días entre touches.\n\n"
            "¿Cuál es la razón conceptual por la que secuencias de 10+ touchpoints en 30+ días rinden peor?"
        ),
        "choices": [
            {"id": "a", "text": "Los proveedores de email penalizan remitentes que usan secuencias largas."},
            {"id": "b", "text": "Los prospectos olvidan los touches iniciales y cada nuevo touch es como empezar de cero, perdiendo el efecto acumulativo del multicanal."},
            {"id": "c", "text": "Después del touch 5-6, los rendimientos marginales caen abruptamente — la gente que iba a responder ya respondió, y los touches adicionales solo generan fricción sin retorno."},
            {"id": "d", "text": "Las herramientas como Reply.io no soportan secuencias de más de 10 pasos."},
        ],
        "correct": "c",
        "explanation": (
            "Rendimientos marginales decrecientes (Sem 7 Bloque 4). 4-7 es el sweet spot: no tan pegado "
            "que incomode, no tan separado que te olviden. (a) falso técnicamente. (b) confunde causa: "
            "el problema de 30+ días no es \"empezar de cero\". (d) falso técnicamente."
        ),
    },
    {
        "id": "M4.16",
        "topic": "Integradora Sem 7 + Sem 8 (diferenciadora)",
        "section": "sem8",
        "type": "single",
        "prompt": (
            "Trabajás en una agencia de outbound. Un cliente nuevo (fintech LATAM, ICP: bancos tier 2 y "
            "cooperativas de crédito) tiene estos hechos:\n"
            "● 600 empresas en su lista total.\n"
            "● Su VP Sales dijo: \"nunca nadie hizo outbound a este segmento, lo primero que hacen los "
            "bancos con emails nuevos es bloquearlos.\"\n"
            "● El equipo de Siete debutó la semana pasada con 2 dominios nuevos. Mandaron 80 emails/casilla "
            "el primer día para arrancar rápido.\n"
            "● Resultado a los 7 días: bounce rate 6%, reply rate 0.3%, Postmaster muestra reputación "
            "\"baja\" para ambos dominios.\n\n"
            "¿Cuál fue el error estructural más grave del arranque?"
        ),
        "choices": [
            {"id": "a", "text": "El ICP es incorrecto — bancos no son fit para outbound frío."},
            {"id": "b", "text": "600 empresas son muy pocas para que el sistema funcione."},
            {"id": "c", "text": "Se salteó el warmup: dominios nuevos no pueden enviar volumen alto desde el día 1. Se necesitan 2-4 semanas de warmup con volumen gradual antes de outreach masivo."},
            {"id": "d", "text": "Debieron usar WhatsApp como canal principal para un segmento reacio al email."},
        ],
        "correct": "c",
        "explanation": (
            "Error estructural de deliverability (Sem 7 Bloque 7 + Sem 8 Bloque 3): dominios nuevos "
            "necesitan warmup de 2-4 semanas con volumen bajo y creciente. Arrancar con 80 emails/día "
            "desde el día 1 quema el dominio en 48h. La decisión no tiene nada que ver con ICP, tamaño "
            "de lista, ni canal; es infraestructura rota antes de empezar. Diferenciadora — pesa más "
            "para distinción."
        ),
    },
]


VIDEO_CASES: list[dict] = [
    {
        "id": "case_a",
        "title": "Secuencia mal diseñada (Sem 7) — Federico / Sandra fintech",
        "scenario": (
            "Federico, SDR de una agencia de outbound, prospecta a Sandra (Directora de RRHH de una "
            "empresa fintech argentina de 800 empleados). En Apollo tiene su email y teléfono verificados. "
            "Propuesta de secuencia:\n\n"
            "Paso 1 — Día 0 — WhatsApp — Mensaje presentándose y ofreciendo demo\n"
            "Paso 2 — Día 0 — Email — Pitch completo con 3 links a casos de éxito\n"
            "Paso 3 — Día 1 — Teléfono — Llamada fría\n"
            "Paso 4 — Día 1 — LinkedIn — Mensaje con pitch abreviado\n"
            "Paso 5 — Día 2 — Email — Follow-up\n"
            "Paso 6 — Día 3 — WhatsApp — Empujón con \"¿lo viste?\"\n"
            "Paso 7 — Día 4 — Teléfono — Segunda llamada\n"
            "Paso 8 — Día 5 — Email — \"Último intento\" — pidiendo respuesta sí/no"
        ),
        "expected_key_point": (
            "Múltiples errores jerarquizables: WhatsApp como canal de entrada en frío (es empujón, no "
            "entrada); 8 touchpoints en 5 días (rompe benchmark 4-7 touches en 10-20 días); llamada del "
            "día 1 antes del follow-up por email (rompe la lógica del orden); ausencia de regla de ramificación."
        ),
        "expected_concepts": [
            "cadencia + benchmark 4-7 touches espaciados 2-4 días",
            "WhatsApp como empujón, no entrada",
            "lógica del orden email → llamada → WhatsApp",
            "reglas de ramificación",
        ],
        "expected_decision": (
            "Secuencia corregida: 6-7 touchpoints en 13-15 días — email + email + llamada + email + "
            "email + WhatsApp + última llamada. Declarando regla de ramificación (si responde → pausa "
            "automática + SDR toma control manual)."
        ),
    },
    {
        "id": "case_b",
        "title": "Diagnóstico por descarte ante anomalía de métricas (Sem 8) — Lucía / 800 contactos nuevos",
        "scenario": (
            "Lucía es SDR en una agencia con 3 meses de operación en un cliente nuevo (tech LATAM). "
            "Lleva 4 semanas corriendo la misma campaña.\n\n"
            "Métrica          | Sem 1 | Sem 2 | Sem 3 | Sem 4\n"
            "Bounce rate      | 2.3%  | 2.5%  | 6.2%  | 5.8%\n"
            "Reply rate       | 2.5%  | 2.4%  | 0.9%  | 0.4%\n"
            "Meeting/reply    | 27%   | 26%   | 25%   | 28%\n"
            "Show rate        | 72%   | 74%   | 70%   | 73%\n"
            "Precalif aprobada| 88%   | 89%   | 86%   | 90%\n\n"
            "Lucía no cambió copy, ICP, cadencia ni volumen. Le pidieron a la agencia más contactos, y "
            "el equipo de research cargó 800 contactos nuevos al inicio de la Semana 3 \"para aumentar volumen\"."
        ),
        "expected_key_point": (
            "Caída de reply rate (2.4% → 0.4%) correlacionada con subida del bounce rate (2.5% → 6.2%) "
            "exactamente cuando cargaron 800 contactos nuevos. La lista se saltó la etapa 3 del proceso "
            "(limpieza y validación). Los bounces dispararon la reputación del dominio hacia abajo "
            "(Postmaster), y los emails correctos empezaron a caer a spam."
        ),
        "expected_concepts": [
            "proceso end-to-end, etapa 3 (limpieza y validación)",
            "cadena del daño de deliverability (bounces → reputación → spam → reply rate sistémico)",
            "diagnóstico por descarte: métricas aguas abajo estables descartan ICP/copy",
        ],
        "expected_decision": (
            "(a) Pausar la campaña inmediatamente. (b) Abrir Postmaster para ver reputación actual y "
            "tiempo de recuperación. (c) Correr validación sobre los 800 contactos nuevos "
            "(ZeroBounce/NeverBounce). (d) Si la reputación cayó mucho, activar dominio de reserva ya "
            "calentado. (e) Hablar con research: política firme de nunca cargar listas sin validar."
        ),
    },
    {
        "id": "case_c",
        "title": "Variante de acceso mal aplicada (Sem 7) — Bruno / Transportes del Norte",
        "scenario": (
            "Bruno es SDR en una agencia outbound que prospecta empresas de logística en México. El "
            "cliente le pidió abrir Transportes del Norte (600 empleados). En Apollo:\n"
            "● El decisor (VP de Operaciones) no aparece. No hay email ni teléfono.\n"
            "● Aparecen 5 contactos de mando medio con email verificado: 3 Coordinadores de Operaciones, "
            "1 Gerente de Ruta, 1 Analista Senior de Transporte.\n\n"
            "Bruno decide mandar el siguiente email a los 5:\n\n"
            "Asunto: Propuesta para Transportes del Norte\n"
            "Hola [Nombre], Te escribo porque trabajamos con empresas de logística optimizando la "
            "gestión de flotas con IA. Tenemos casos con empresas similares a Transportes del Norte "
            "con reducciones del 25% en costos operativos. Me encantaría agendar 30 minutos con tu "
            "equipo para presentarte la solución. ¿Podemos coordinar esta semana? Saludos, Bruno.\n\n"
            "Resultado a los 10 días: 0 respuestas."
        ),
        "expected_key_point": (
            "Bruno aplicó variante 1 (venta directa) a una situación de variante 3 (sin contacto del "
            "decisor) — Sem 7 Bloque 6. A mandos medios no se les vende; se les pide orientación. El "
            "email les pide agendar demo como si fueran decisores, dejándolos en un lugar incómodo "
            "(no pueden comprar, no pueden rutearlo bien porque el mensaje no lo pidió)."
        ),
        "expected_concepts": [
            "6 variantes de acceso al decisor",
            "variante 3 vs variante 1",
            "champion potencial vs KDM",
            "pedir orientación, no vender",
        ],
        "expected_decision": (
            "Reescribir con tono de orientación: \"Hola [Nombre], trato de ubicar quién lidera hoy el "
            "tema de operación de flota y optimización de rutas en Transportes del Norte. Por tu rol, "
            "pensé que podrías orientarme: ¿sería un tema que ve directamente el VP de Operaciones, o "
            "pasa por alguien antes? Gracias.\" Plan: 4 touchpoints por referidor × 5 referidores = 20 "
            "touchpoints distribuidos, no 5 pitches idénticos."
        ),
    },
    {
        "id": "case_d",
        "title": "Hipótesis testeable mal formulada (Sem 8) — Romina / 4 cambios simultáneos",
        "scenario": (
            "Romina es SDR senior y quiere mejorar su performance. Detectó que 5 prospectos de industria "
            "retail respondieron a su email diciendo: \"estamos con un proyecto grande de migración a "
            "Shopify y todo lo demás está pausado hasta Q4\".\n\n"
            "Plan que Romina le propuso a su Team Lead:\n\n"
            "\"Team Lead, Detecté que retail no está respondiendo bien. Creo que el mensaje no les habla. "
            "Mi plan: 1. Voy a cambiar el copy para empresas de retail — probablemente estoy siendo muy "
            "genérica. 2. Voy a mandar casos de éxito con empresas retail al segundo touch para mostrar "
            "que entendemos el sector. 3. Voy a acortar la secuencia de 6 a 4 touches porque siento que "
            "los perdemos por saturación. 4. Voy a agregar LinkedIn como canal adicional. Creo que con "
            "estos 4 cambios voy a subir el reply rate retail. Romina.\""
        ),
        "expected_key_point": (
            "Romina formuló un plan de acción sin método: 4 cambios simultáneos + sin variable aislada + "
            "sin método de medición + sin magnitud esperada (Sem 8 Bloque 7). Si al final del mes el reply "
            "rate cambia, no va a poder identificar cuál cambio fue el causante — no podrá replicar ni "
            "descartar. Además, la señal que detectó (migración Shopify + pausa hasta Q4) no es problema "
            "de copy — es una señal de compra negativa acotada en el tiempo."
        ),
        "expected_concepts": [
            "PDCA / Build-Measure-Learn",
            "hipótesis testeable = una variable aislada + método de medición declarado + magnitud esperada",
            "señal de compra negativa acotada en el tiempo",
            "intuición vs mindset de mejora continua",
        ],
        "expected_decision": (
            "Reescribir como hipótesis única testeable: \"Las empresas retail que anunciaron migración "
            "a Shopify en los últimos 60 días están estructuralmente no-listo (no no-fit). Si las filtro "
            "y archivo con trigger de recontacto en Q4, el reply rate retail efectivo sube. Test: 3 "
            "semanas, medir reply rate retail antes/después del filtro. Resultado esperado: +0.5 puntos.\""
        ),
    },
]


VIDEO_RUBRIC: dict = {
    "criteria": [
        {
            "key": "key_point",
            "label": "Identificación del punto clave",
            "scale": [
                {"score": 0, "descriptor": "No identifica o identifica mal."},
                {"score": 1, "descriptor": "Identifica pero parcial o dubitativo."},
                {"score": 2, "descriptor": "Identifica claro y correcto de entrada."},
            ],
        },
        {
            "key": "concepts",
            "label": "Justificación con conceptos del curso",
            "scale": [
                {"score": 0, "descriptor": "Frases genéricas (\"no me gusta\", \"está feo\"). No usa vocabulario del curso."},
                {"score": 1, "descriptor": "Usa algún concepto pero superficial o aplicado a medias."},
                {"score": 2, "descriptor": "Usa vocabulario específico (variantes de acceso, 5 canales, cadencia, deliverability, diagnóstico por descarte, PDCA, etc.) correctamente aplicado al caso."},
            ],
        },
        {
            "key": "decision",
            "label": "Decisión concreta y aterrizada",
            "scale": [
                {"score": 0, "descriptor": "No decide o decide desconectado del diagnóstico."},
                {"score": 1, "descriptor": "Decide razonable pero poco específico."},
                {"score": 2, "descriptor": "Decide específico, aterrizado al caso, trazable al diagnóstico."},
            ],
        },
    ],
    "score_conversion": {
        "6": 100,
        "5": 83,
        "4": 67,
        "3": 50,
        "2": 0,
        "1": 0,
        "0": 0,
    },
    "passing_video_score_pct": 67,
}


# Pesos para nota final del módulo (Documento Maestro líneas 12115-12118)
WEIGHTS = {"mcq": 0.7, "video": 0.3}
PASSING_SCORE = 65.0


def total_question_count() -> int:
    return len(MCQ)


def section_counts() -> dict[str, int]:
    out: dict[str, int] = {}
    for q in MCQ:
        sec = q.get("section", "unknown")
        out[sec] = out.get(sec, 0) + 1
    return out
