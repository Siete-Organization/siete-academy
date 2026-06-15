"""Contenido Capa 2 — Prueba del Módulo 3 (La conexión).

Fuente: SDR_Academy_Siete_Documento_Maestro.md, Parte IV §Prueba del Módulo 3,
líneas 9023-9655, v0.1 (2026-04-22).

Estructura:
- MCQ: 16 preguntas (Sem 5 + Sem 6 del Módulo 3). 70% del peso de la prueba.
- VIDEO_CASES: 4 casos de banco para video narrado (1 asignado al azar). 30% del peso.
- VIDEO_RUBRIC: 3 criterios × 0-2 puntos → /6 → conversión a %.
"""

MCQ: list[dict] = [
    {
        "id": "M3.1",
        "topic": "Escalar el compromiso después de un primer \"sí\"",
        "section": "sem5",
        "type": "single",
        "prompt": (
            "Un SDR mandó un primer correo cuyo llamado a la acción era una pregunta de baja "
            "fricción: \"¿tiene sentido lo que planteo?\". El prospecto respondió: \"Sí, tiene "
            "sentido, es un tema que tenemos sobre la mesa.\"\n\n"
            "¿Cuál es la mejor forma de responder?"
        ),
        "choices": [
            {"id": "a", "text": "Aprovechar el interés y mandarle de inmediato un PDF con el producto, los casos de éxito y la propuesta comercial, para que llegue informado a una eventual reunión."},
            {"id": "b", "text": "Responder con una pregunta abierta amplia (\"¿Me cuentas todo el contexto del problema y cómo lo vienen manejando?\") y hacer el diagnóstico completo por correo antes de avanzar."},
            {"id": "c", "text": "Apoyarse en ese \"sí\" para escalar el compromiso de a poco: \"Buenísimo. ¿Te funciona 15 minutos el martes o el jueves para verlo en concreto?\" — una reunión corta es consistente con algo que el prospecto ya validó."},
            {"id": "d", "text": "Agradecer la respuesta y esperar una o dos semanas antes de proponer un paso concreto, para no presionar y dejar que el prospecto retome cuando quiera."},
        ],
        "correct": "c",
        "explanation": (
            "Tras un \"sí\" de baja fricción, el paso correcto es escalar el compromiso de a poco "
            "hacia una reunión corta y concreta (Sem 5). (a) abruma con un PDF y salta el ritmo; "
            "(b) convierte el correo en discovery; (d) deja enfriar un interés ya validado."
        ),
    },
    {
        "id": "M3.2",
        "topic": "Multi-select — violaciones del contrato asíncrono",
        "section": "sem6",
        "type": "multi",
        "prompt": (
            "Un SDR le manda estos mensajes a Carolina, CFO de una fintech que cerró Serie B, "
            "a lo largo de 3 minutos por WhatsApp:\n\n"
            "(1) Hola Carolina, ¿cómo estás?\n"
            "(2, 30 seg después) Soy Diego de DataFlow, te escribí por LinkedIn pero creo que no lo viste.\n"
            "(3, 1 min después) Felicitaciones por la Serie B 🎉 Te escribo porque tenemos una plataforma "
            "que ayuda a startups post-Serie B a reducir 60% el tiempo de cierre de mes. Trabajamos con "
            "[3 empresas desconocidas].\n"
            "(4, 30 seg después) ¿Tenemos 20 min esta semana? Te mando el caso de éxito por acá también.\n\n"
            "Marcá todas las violaciones del contrato asíncrono:"
        ),
        "choices": [
            {"id": "1", "text": "Manda 4 mensajes en menos de 2 minutos — rompe la lógica del goteo (1 mensaje, esperar respuesta)."},
            {"id": "2", "text": "El mensaje 3 tiene pitch completo + prueba social genérica en un solo envío."},
            {"id": "3", "text": "El mensaje 4 tiene 2 CTAs simultáneos (reunión + mandar caso)."},
            {"id": "4", "text": "Usa emojis (🎉) que están prohibidos en B2B."},
            {"id": "5", "text": "Debería haber llamado por teléfono primero en lugar de WhatsApp."},
            {"id": "6", "text": "\"Te escribí por LinkedIn pero creo que no lo viste\" es reproche implícito que destruye cualquier rapport posible."},
        ],
        "correct": ["1", "2", "3", "6"],
        "explanation": (
            "1, 2, 3 y 6 son violaciones reales. (4) Un emoji incidental no viola contrato B2B en LATAM. "
            "(5) No hay regla de \"teléfono primero\" — el problema del WhatsApp no es el canal sino el mal uso."
        ),
    },
    {
        "id": "M3.3",
        "topic": "Diagnóstico: objeción vs rechazo",
        "section": "sem6",
        "type": "single",
        "prompt": (
            "Durante una cold call, el prospecto dice:\n\n"
            "\"Mirá, estamos en medio de una reestructuración organizacional y no es el momento para "
            "evaluar proveedores nuevos. Estamos parando todas las decisiones de este tipo hasta tener claridad.\"\n\n"
            "¿Qué debería hacer el SDR?"
        ),
        "choices": [
            {"id": "a", "text": "Aceptar y cortar — la respuesta fue explícita."},
            {"id": "b", "text": "Responder \"¿cuándo creés que van a tener claridad?\" antes de cerrar, para poder archivar con fecha concreta de re-contacto."},
            {"id": "c", "text": "Insistir con un caso de éxito de otra empresa que también estaba en reestructuración."},
            {"id": "d", "text": "Ofrecer agendar una reunión \"informal, sin compromiso\" en 2 semanas."},
        ],
        "correct": "b",
        "explanation": (
            "Es objeción con timing, no rechazo. Preguntar cuándo esperan claridad te da una fecha de "
            "archivo concreta. El SDR con criterio diferencia objeciones con timing de rechazos definitivos "
            "(Sem 6 Bloque 4). (a) pierde pipeline futuro, (c) atropella, (d) viola el \"no\" temporal."
        ),
    },
    {
        "id": "M3.4",
        "topic": "Pareo KDM vs referidor",
        "section": "sem5",
        "type": "match",
        "prompt": (
            "Emparejá cada fragmento de mensaje con el destinatario correcto.\n\n"
            "1) \"Estoy tratando de ubicar a la persona que hoy lidera el tema de performance comercial "
            "en su empresa. ¿Te molesta si me indicás con quién tendría sentido conversar?\"\n"
            "2) \"Vi que contrataron 12 AEs nuevos este trimestre. Lo que vemos en ramp-ups así es que "
            "el pipeline se queda corto 3-4 meses. ¿Les está pasando algo de eso?\"\n"
            "3) \"Por tu rol creo que podrías orientarme. Estoy tratando de entender si en su empresa "
            "el tema de [área] lo manejan internamente o trabajan con alguien.\"\n"
            "4) \"El desafío más caro que vemos en empresas que triplican equipo en 6 meses es que los "
            "procesos comerciales no escalan al mismo ritmo. ¿Querés 20 min para verlo?\""
        ),
        "left": [
            {"id": "1", "text": "Mensaje 1 (ubicar persona)"},
            {"id": "2", "text": "Mensaje 2 (12 AEs nuevos)"},
            {"id": "3", "text": "Mensaje 3 (orientación)"},
            {"id": "4", "text": "Mensaje 4 (triplican equipo)"},
        ],
        "right": [
            {"id": "A", "text": "Mensaje al decisor (KDM): dolor + propuesta + CTA de reunión"},
            {"id": "B", "text": "Mensaje al referidor: pide orientación, no vende"},
        ],
        "correct": {"1": "B", "2": "A", "3": "B", "4": "A"},
        "explanation": (
            "Al referidor NUNCA se le pide reunión; se le pide orientación. Confundir los registros "
            "es el error número 1 del SDR novato (Sem 5 Bloque 6)."
        ),
    },
    {
        "id": "M3.5",
        "topic": "Diseño del gancho desde señal",
        "section": "sem5",
        "type": "single",
        "prompt": (
            "Tenés esta señal pública sobre una empresa que prospectás:\n\n"
            "\"Rappi anunció en LinkedIn la semana pasada la expansión de su operación de pagos "
            "(RappiPay) a 3 nuevos países en LATAM durante 2026.\"\n\n"
            "¿Cuál de los siguientes es el mejor gancho construido desde esa señal?"
        ),
        "choices": [
            {"id": "a", "text": "\"Hola Juan, vi que Rappi está creciendo mucho, felicitaciones. ¿Cómo están con esa expansión?\""},
            {"id": "b", "text": "\"Hola Juan, vi que RappiPay entra a 3 nuevos países en 2026. En expansión multi-país regulada como fintech, el cuello de botella que suele aparecer es la coordinación de compliance local — cada país con normativa propia. ¿Les está pasando algo así o ya tienen mapeado?\""},
            {"id": "c", "text": "\"Hola Juan, me encantaría presentarte nuestra plataforma de compliance que ayuda a fintechs en expansión. ¿Tenés 30 min esta semana?\""},
            {"id": "d", "text": "\"Hola Juan, te escribo porque sé que Rappi es una empresa innovadora y pensé que podríamos explorar oportunidades de sinergia.\""},
        ],
        "correct": "b",
        "explanation": (
            "Señal específica (RappiPay, 3 países, 2026) + hipótesis de consecuencia (compliance local) + "
            "pregunta abierta sin prometer. Cumple los 3 criterios del Bloque 5: especificidad, "
            "puente señal→consecuencia, pregunta sin promesa."
        ),
    },
    {
        "id": "M3.6",
        "topic": "Encadenada parte 1 — diagnóstico de precalificación",
        "section": "sem6",
        "type": "single",
        "prompt": (
            "Un SDR tiene una llamada de precalificación de 10 min agendada con un prospecto 2 días "
            "antes de la reunión con el AE. Leé cómo arrancó el SDR:\n\n"
            "SDR: \"Hola Pedro, gracias por tomar la llamada. Antes de la reunión quería hacerte unas "
            "preguntas rápidas para llegar preparados. ¿Te parece?\"\n"
            "Pedro: \"Dale, dale.\"\n"
            "SDR: \"Perfecto. Primera: ¿cuál es el presupuesto anual que tienen asignado para este tipo "
            "de soluciones? Segunda: ¿quién más participaría en la decisión si avanzáramos? Tercera: "
            "¿tienen un timeline específico de cuándo querrían implementar? Cuarta: ¿ya están evaluando "
            "otros proveedores? Quinta: ¿podés contarme más sobre sus procesos actuales?\"\n\n"
            "¿Qué está haciendo mal el SDR?"
        ),
        "choices": [
            {"id": "a", "text": "Debería haber preguntado primero sobre los procesos actuales (pregunta 5) antes de las otras."},
            {"id": "b", "text": "Está convirtiendo la precalificación en un interrogatorio BANT + ráfaga de 5 preguntas sin dejar respirar. La precalificación en outbound es filtro de mínimos, no interrogatorio de máximos."},
            {"id": "c", "text": "Debería haber pedido 20 min en lugar de 10 para una precalificación completa."},
            {"id": "d", "text": "No presentó quién es la empresa antes de hacer preguntas."},
        ],
        "correct": "b",
        "explanation": (
            "Doble falla: BANT en outbound (Sem 6 Bloque 5) + 5 preguntas seguidas sin espacio para "
            "procesar. El SDR convirtió precalificación en discovery."
        ),
    },
    {
        "id": "M3.7",
        "topic": "Uso correcto de LinkedIn en outbound",
        "section": "sem6",
        "type": "single",
        "prompt": (
            "Un SDR quiere usar LinkedIn para llegar a un decisor que todavía no respondió sus correos.\n\n"
            "¿Cuál es el uso de LinkedIn más alineado con lo que enseña el módulo?"
        ),
        "choices": [
            {"id": "a", "text": "Usarlo primero para investigar al decisor (qué publica, qué comenta, qué compartió hace poco) y, si hay material, hacer un micro-contacto genuino: un comentario real en una publicación suya o un mensaje corto que mencione algo específico que él planteó."},
            {"id": "b", "text": "Reenviarle por mensaje directo el mismo correo que no respondió, ahora por LinkedIn, para subir la probabilidad de que lo vea en otro canal."},
            {"id": "c", "text": "Conectar y, apenas acepte, mandarle el pitch completo con la propuesta y un link para agendar, aprovechando que LinkedIn funciona como canal de venta directa."},
            {"id": "d", "text": "Programar solicitudes de conexión automáticas a muchos perfiles del mismo cargo por día, para escalar el volumen de contactos sin invertir tanto tiempo en investigar."},
        ],
        "correct": "a",
        "explanation": (
            "LinkedIn en outbound es research + micro-contacto genuino, no un canal de venta directa "
            "ni de volumen (Sem 6). (b) repite el mismo mensaje fallido; (c) trata LinkedIn como pitch "
            "directo; (d) automatiza volumen sin investigación, lo que quema el perfil."
        ),
    },
    {
        "id": "M3.8",
        "topic": "Grid de 6 criterios — múltiples CTAs",
        "section": "sem5",
        "type": "single",
        "prompt": (
            "Leé este cold email:\n\n"
            "Asunto: 15 tiendas nuevas en Q1\n"
            "Hola Martina, vi que BIM abrió 15 tiendas nuevas en Perú y Ecuador este trimestre — "
            "crecimiento fuerte en plena expansión regional. En retail con expansión a ese ritmo, el "
            "cuello de botella más caro que vemos es la predicción de demanda por local: lo que funciona "
            "en San Isidro no funciona igual en Machala, y los primeros 6 meses post-apertura suelen "
            "tener sobrestock y subestock mezclados hasta que se calibra el modelo. En empresas "
            "similares ayudamos a reducir overstock en los primeros meses de expansión. ¿Querés que te "
            "cuente cómo lo hicimos en otro caso, o agendamos 20 min para verlo? También puedo "
            "mandarte el caso por escrito si preferís. Cualquier cosa me decís. Saludos, Ana.\n\n"
            "Aplicando el grid de 6 criterios de Sem 5, este email tiene un criterio rojo. ¿Cuál?"
        ),
        "choices": [
            {"id": "a", "text": "Especificidad del gancho — la señal (15 tiendas nuevas) es verificable y específica."},
            {"id": "b", "text": "Foco en el lector — todo el cuerpo habla de BIM y su contexto, no del remitente."},
            {"id": "c", "text": "Longitud — ~115 palabras, claramente por encima del umbral de 80."},
            {"id": "d", "text": "Un solo CTA — el email ofrece 3 caminos simultáneos (contar el caso, agendar 20 min, mandar el caso por escrito), lo que genera parálisis por exceso de opciones."},
            {"id": "e", "text": "Tono y registro — el tono es natural, directo, respetuoso."},
        ],
        "correct": "d",
        "explanation": (
            "Múltiples CTAs es el problema más grave (rojo). Tres opciones simultáneas paralizan al lector. "
            "Mejor ofrecer 1 y dejar que el prospecto pida lo que necesite. La longitud es amarilla, no roja."
        ),
    },
    {
        "id": "M3.9",
        "topic": "Labeling + tactical empathy",
        "section": "sem6",
        "type": "single",
        "prompt": (
            "Durante una cold call, el prospecto dice:\n\n"
            "\"Hace 8 meses probamos una plataforma parecida y fue un dolor de cabeza. Tardamos 4 "
            "meses en implementarla y al final no la usamos. Estoy bastante escéptico con este tipo de herramientas.\"\n\n"
            "¿Cuál de estas respuestas del SDR combina labeling con tactical empathy de forma más efectiva?"
        ),
        "choices": [
            {"id": "a", "text": "\"Entiendo. Te cuento que nosotros somos distintos — nuestra implementación es en 48 horas y tenemos un 95% de adopción.\""},
            {"id": "b", "text": "\"¿Escéptico...?\" [mirroring puro]"},
            {"id": "c", "text": "\"Parece que ese proyecto les dejó un mal sabor, y que hoy este tipo de herramientas parten con desventaja en tu mente. Totalmente entendible — no es fácil apostar de nuevo después de una experiencia así. ¿Qué fue lo peor de esa implementación?\""},
            {"id": "d", "text": "\"No te preocupes, te puedo mandar testimonios de nuestros clientes para que veas que somos diferentes.\""},
        ],
        "correct": "c",
        "explanation": (
            "Combina labeling (\"parece que ese proyecto les dejó un mal sabor\"), tactical empathy "
            "(\"no es fácil apostar de nuevo\") y pregunta abierta no-defensiva. (a) confronta y dispara "
            "defensa; (b) mirroring puro no aprovecha el momento; (d) ofrece prueba social genérica sin validar."
        ),
    },
    {
        "id": "M3.10",
        "topic": "Multi-select — señales reales vs ruido",
        "section": "sem5",
        "type": "multi",
        "prompt": (
            "Marcá todas las señales verificables y accionables para construir un gancho de cold email."
        ),
        "choices": [
            {"id": "1", "text": "La empresa acaba de cerrar una ronda Serie B por USD 35M."},
            {"id": "2", "text": "El CEO subió foto desayunando con su familia en Instagram."},
            {"id": "3", "text": "La empresa anunció apertura de 2 nuevas oficinas regionales en 2026."},
            {"id": "4", "text": "El VP de Operaciones cambió de \"Employee\" a \"Open to Work\" en su LinkedIn."},
            {"id": "5", "text": "La empresa ganó el reconocimiento \"Great Place to Work\"."},
            {"id": "6", "text": "Una regulación fintech nueva entra en vigor en 90 días afectando a la industria del prospecto."},
            {"id": "7", "text": "La empresa tuiteó un chiste sobre un partido de fútbol."},
            {"id": "8", "text": "Publicaron 20 ofertas de trabajo para data engineering en 3 semanas."},
        ],
        "correct": ["1", "3", "4", "6", "8"],
        "explanation": (
            "Señales accionables: 1 (financing), 3 (expansión), 4 (apertura del rol), 6 (regulación con timing), "
            "8 (contratación masiva). Ruido: 2 (social personal), 5 (reconocimiento sin implicación comercial), "
            "7 (no relacionado a negocio)."
        ),
    },
    {
        "id": "M3.11",
        "topic": "Permission-based opener bien ejecutado",
        "section": "sem6",
        "type": "single",
        "prompt": (
            "Un SDR arranca una cold call así:\n\n"
            "\"Hola Pedro, soy Lucía de DataSync. ¿Cómo estás?\" [Pedro: \"Bien, ¿qué tal?\"] \"Bien, "
            "gracias. Pedro, antes de avanzar — sé que te estoy llamando en frío y seguramente tenés "
            "50 cosas a la vez. ¿Me das 45 segundos para contarte por qué te llamo específicamente a "
            "vos? Si después querés colgar, sin drama.\"\n\n"
            "¿Qué hace bien esta apertura?"
        ),
        "choices": [
            {"id": "a", "text": "No es permission-based opener — pide mucho tiempo (45 segundos) y da muchas excusas."},
            {"id": "b", "text": "Combina: reconocimiento explícito de que es frío + pedido acotado de tiempo + permiso claro para salirse + foco anticipado en \"por qué a vos\" específicamente. Ejecuta las 5 partes del opener en formato comprimido."},
            {"id": "c", "text": "El problema es \"¿cómo estás?\" al inicio — eso es filler social que no aporta."},
            {"id": "d", "text": "Debería haber abierto con una frase impactante o una pregunta provocadora."},
        ],
        "correct": "b",
        "explanation": (
            "Reconocimiento honesto + pedido acotado + permiso claro para salir + promesa de especificidad. "
            "45 seg es específico y respetuoso, no excesivo. \"¿Cómo estás?\" en LATAM B2B es cortesía normal. "
            "Frases impactantes o preguntas provocadoras activan defensa, no curiosidad."
        ),
    },
    {
        "id": "M3.12",
        "topic": "Ordenamiento — anatomía de la cold call",
        "section": "sem6",
        "type": "match",
        "prompt": (
            "Asigná cada paso de la cold call bien ejecutada a su posición correcta (1-5):"
        ),
        "left": [
            {"id": "step_1", "text": "Paso 1 — primero"},
            {"id": "step_2", "text": "Paso 2"},
            {"id": "step_3", "text": "Paso 3"},
            {"id": "step_4", "text": "Paso 4"},
            {"id": "step_5", "text": "Paso 5 — último"},
        ],
        "right": [
            {"id": "permission", "text": "Permission-based opener (pedir permiso)"},
            {"id": "context", "text": "Contexto específico sobre el prospecto (señal observada)"},
            {"id": "reason", "text": "Razón concreta de por qué esto podría importar (hipótesis, no promesa)"},
            {"id": "question", "text": "Una pregunta abierta dirigida a obtener información"},
            {"id": "silence", "text": "Silencio (esperar respuesta del prospecto)"},
        ],
        "correct": {
            "step_1": "permission",
            "step_2": "context",
            "step_3": "reason",
            "step_4": "question",
            "step_5": "silence",
        },
        "explanation": (
            "Cada paso prepara el siguiente: el permiso genera espacio, el contexto justifica la interrupción, "
            "la razón introduce la hipótesis, la pregunta invita al prospecto a hablar, el silencio le da "
            "espacio para pensar (Sem 6 Bloque 2)."
        ),
    },
    {
        "id": "M3.13",
        "topic": "Integradora — mensaje al referidor con lógica asíncrona",
        "section": "sem5",
        "type": "single",
        "prompt": (
            "Un SDR quiere llegar al Gerente de Operaciones de una empresa pero no tiene su contacto. "
            "Identifica a Valeria, Coordinadora del mismo equipo, como posible referidor. Va a escribirle por LinkedIn.\n\n"
            "¿Cuál de estas aperturas de LinkedIn es la más apropiada?"
        ),
        "choices": [
            {"id": "a", "text": "\"Hola Valeria, trabajamos con empresas como la tuya ayudando a reducir costos operativos 30%. ¿Tenés 20 min para una llamada?\""},
            {"id": "b", "text": "\"Hola Valeria, me gustaría contactar al Gerente de Operaciones de tu empresa. Por tu rol pensé que podrías orientarme — ¿con quién tendría sentido conversar sobre temas de optimización de cadena de suministro?\""},
            {"id": "c", "text": "\"Hola Valeria, vi tu perfil y me pareció interesante. ¿Podrías presentarme al Gerente de Operaciones? Te adjunto mi propuesta.\""},
            {"id": "d", "text": "\"Hola Valeria, ¿tu empresa está evaluando proveedores para mejorar sus procesos operativos? Te puedo dar una cotización rápida.\""},
        ],
        "correct": "b",
        "explanation": (
            "Aplica dos principios integrados: mensaje a referidor, no al KDM (Sem 5 Bloque 6) + lógica "
            "asíncrona de LinkedIn (Sem 6 Bloque 6). (a) trata a Valeria como KDM, (c) es invasivo y "
            "asume llegada, (d) vende directamente como si Valeria fuera compradora."
        ),
    },
    {
        "id": "M3.14",
        "topic": "Evasión vs interés real",
        "section": "sem6",
        "type": "single",
        "prompt": (
            "Durante una cold call, después de la razón concreta, el prospecto dice:\n\n"
            "\"Mmm, interesante. ¿Me mandás info por mail así lo veo con más calma?\"\n\n"
            "¿Qué debería hacer el SDR?"
        ),
        "choices": [
            {"id": "a", "text": "Enviar el email inmediatamente después de colgar con información completa del producto."},
            {"id": "b", "text": "Responder \"perfecto, te mando\" y cortar — el prospecto mostró interés, lo mejor es respetar su ritmo."},
            {"id": "c", "text": "Pedir aclarar qué parte específica le interesa antes de cortar: \"Dale, te paso info. Antes de mandar, ¿qué parte específicamente te interesaría ver? Para no mandarte un PDF genérico.\""},
            {"id": "d", "text": "Insistir en agendar una reunión breve en lugar de mandar info."},
        ],
        "correct": "c",
        "explanation": (
            "\"Mandame info por mail\" es evasión cortés el 90% de las veces (Sem 6 Bloque 4). Pedir "
            "especificidad antes de mandar sirve como filtro: si hay interés real, el prospecto da una "
            "pista concreta; si era despedida, dice \"lo que me puedas mandar está bien\". Ya tenés diagnóstico."
        ),
    },
    {
        "id": "M3.15",
        "topic": "Corregir email con un solo cambio",
        "section": "sem5",
        "type": "single",
        "prompt": (
            "Leé este primer email:\n\n"
            "Asunto: Oportunidad para Corporación X\n"
            "Hola Mariana, Espero que este correo te encuentre bien. Mi nombre es Sebastián Torres y "
            "soy ejecutivo comercial en OptiGrowth. Somos una empresa con más de 8 años de experiencia "
            "ayudando a compañías como la tuya a optimizar sus procesos comerciales, aumentar su "
            "pipeline y mejorar sus tasas de conversión. Tenemos la suerte de trabajar con empresas "
            "como [Falabella, Cencosud, Banco de Crédito] que han visto resultados increíbles en los "
            "primeros 3 meses. Me encantaría que podamos conversar para explorar si lo que hacemos "
            "podría ayudarte a vos y a tu equipo. ¿Tendrías 30 min disponibles la próxima semana? "
            "También te puedo mandar casos de éxito si preferís verlo por escrito antes. Saludos cordiales, Sebastián.\n\n"
            "Si tuvieras que hacer un solo cambio para mejorar este email más que ningún otro, ¿cuál sería?"
        ),
        "choices": [
            {"id": "a", "text": "Reescribirlo desde la perspectiva de Corporación X: reemplazar toda la intro sobre OptiGrowth por una señal específica verificable de Mariana/Corporación X, y conectarla con un desafío hipotético."},
            {"id": "b", "text": "Sacar los emojis y las palabras superlativas (\"increíbles\", \"la suerte de\")."},
            {"id": "c", "text": "Bajar de 30 min a 15 min en el CTA principal."},
            {"id": "d", "text": "Cambiar el asunto a algo más específico."},
        ],
        "correct": "a",
        "explanation": (
            "El problema estructural es que todo el cuerpo habla del remitente (OptiGrowth). Reescribir "
            "desde Mariana cambia todo. Las otras correcciones son secundarias — no importan si el foco "
            "sigue en el remitente."
        ),
    },
    {
        "id": "M3.16",
        "topic": "Integradora final — los 3 errores más graves",
        "section": "sem6",
        "type": "multi",
        "prompt": (
            "Leé este mensaje que un SDR mandó por WhatsApp al CMO de una empresa:\n\n"
            "\"Hola Lucas, te escribe Pablo de MarketForge. Te contacto porque somos una plataforma "
            "que ayuda a CMOs de empresas B2B SaaS a optimizar sus campañas de demand gen. Trabajamos "
            "con empresas como TuyaMed, DataLeap y TechOnce. Para que podamos evaluar si tiene "
            "sentido avanzar, me gustaría saber: ¿cuál es tu presupuesto anual de marketing? ¿quién "
            "más participaría en la decisión? ¿tenés timeline definido? Te mando link a Calendly para "
            "agendar directamente. Espero tu respuesta hoy, gracias.\"\n\n"
            "Marcá los 3 errores más graves del mensaje:"
        ),
        "choices": [
            {"id": "1", "text": "El pecado capital: todo el mensaje habla del remitente y su plataforma, sin una sola referencia al negocio de Lucas."},
            {"id": "2", "text": "BANT en frío: pregunta presupuesto, autoridad y timing en un primer contacto."},
            {"id": "3", "text": "Viola el canal asíncrono: manda un pitch completo + preguntas BANT + link + deadline en un solo mensaje."},
            {"id": "4", "text": "Menciona empresas clientes sin datos de resultados."},
            {"id": "5", "text": "\"Espero tu respuesta hoy\" es una presión temporal que puede incomodar."},
            {"id": "6", "text": "No usa emojis para humanizar."},
        ],
        "correct": ["1", "2", "3"],
        "explanation": (
            "Los 3 errores estructurales que destruyen cualquier chance de conversación. (4) cierto pero "
            "menor frente a los otros 3, (5) menor también, (6) falso — los emojis no son requisito. "
            "Es la integradora final del MCQ que mide dominio de conceptos clave de ambas semanas."
        ),
    },
]


VIDEO_CASES: list[dict] = [
    {
        "id": "case_a",
        "title": "Copy de cold email mal escrito — ACME Consultores / Textiles del Sur",
        "scenario": (
            "ACME Consultores ofrece servicios de auditoría tributaria a empresas medianas en Perú. "
            "Su SDR, Roberto, está prospectando al CFO de Textiles del Sur (empresa de 280 empleados, "
            "cliente potencial ICP).\n\n"
            "Primer email de Roberto:\n\n"
            "Asunto: Servicios de auditoría tributaria — ACME Consultores\n"
            "Estimado Sr. Mendoza, Reciba un cordial saludo. Me permito presentarle a ACME Consultores, "
            "firma con más de 15 años de experiencia brindando servicios de auditoría tributaria, "
            "consultoría financiera y asesoría regulatoria a empresas medianas y grandes del Perú. "
            "Nuestro equipo está conformado por profesionales altamente capacitados, entre los que se "
            "encuentran ex-funcionarios de SUNAT y contadores públicos certificados con amplia "
            "trayectoria en el sector. Contamos con oficinas en Lima, Arequipa y Trujillo. Nos "
            "especializamos en identificar oportunidades de optimización tributaria y minimización de "
            "contingencias fiscales. Entre nuestros clientes se encuentran importantes empresas del "
            "sector textil, manufactura y retail. Sería un placer poder agendar una reunión con usted "
            "para presentarle con mayor detalle nuestros servicios y cómo podríamos apoyar a Textiles "
            "del Sur. Quedo a la espera de su amable respuesta. Cordialmente, Roberto Pérez — Ejecutivo "
            "Comercial Senior · ACME Consultores"
        ),
        "expected_key_point": (
            "Pecado capital (Sem 5 Bloque 4): todo el cuerpo habla de ACME/Roberto; ni una referencia "
            "a Textiles del Sur. Tono excesivamente formal, sin gancho específico, longitud inadecuada."
        ),
        "expected_concepts": [
            "pecado capital",
            "grid de 6 criterios (foco en lector = rojo)",
            "gancho desde señal verificable",
        ],
        "expected_decision": (
            "Reescritura específica: abrir con señal real sobre el sector textil en Perú (ej. normativa "
            "SUNAT reciente, cambios aduaneros, drawback) + conectarla con Textiles del Sur + reducir "
            "a <80 palabras + bajar tono a directo pero respetuoso."
        ),
    },
    {
        "id": "case_b",
        "title": "Cold call problemática — Paula / LogiFlow / Eduardo COO",
        "scenario": (
            "Una SDR, Paula, hace una cold call a Eduardo, COO de una empresa B2B de logística.\n\n"
            "Transcripción:\n\n"
            "Paula: Hola Eduardo, ¿te agarro en buen momento?\n"
            "Eduardo: Estoy complicado, ¿de qué se trata?\n"
            "Paula: Te cuento rapidísimo. Mi nombre es Paula y te llamo de LogiFlow. Somos una empresa "
            "que ayuda a compañías de logística como la tuya a optimizar sus procesos de gestión de "
            "flota usando IA y análisis predictivo. Trabajamos con clientes como DHL, FedEx y Maersk. "
            "La verdad hemos tenido resultados increíbles, con reducciones de costos operativos del 25% "
            "en promedio y mejoras de eficiencia del 40%. Por eso quería agendar una reunión para "
            "contarte cómo podríamos aplicar esto en tu empresa. ¿Tenés 30 minutos el jueves o el viernes?\n"
            "Eduardo: Mirá, la verdad mandame info por email y lo veo cuando tenga un rato.\n"
            "Paula: Dale, perfecto, te mando la info a tu mail corporativo ahora mismo con nuestro "
            "brochure completo y casos de éxito. Muchas gracias por tu tiempo, Eduardo. ¡Buen día!"
        ),
        "expected_key_point": (
            "Múltiples fallas jerarquizadas: apertura \"¿te agarro en buen momento?\" invita al corte; "
            "Paula habla 80% del tiempo (no respeta 70/30); prueba social desajustada (DHL/FedEx/Maersk "
            "para una empresa local). El error MÁS GRAVE: cuando Eduardo dice \"mandame info por email\", "
            "Paula acepta la evasión como si fuera interés (Sem 6 Bloque 4)."
        ),
        "expected_concepts": [
            "evasión vs interés real",
            "reconocer / reformular / reconducir",
            "anatomía de cold call (5 partes)",
            "regla del 70/30 de escucha activa",
        ],
        "expected_decision": (
            "Reescribe la respuesta: \"Dale, te paso info. Antes de mandar — ¿qué parte específicamente "
            "te interesaría ver? Para no mandarte un PDF genérico.\" + diagnóstico: si Eduardo da una "
            "pista concreta hay interés; si dice \"lo que puedas\" era despedida."
        ),
    },
    {
        "id": "case_c",
        "title": "WhatsApp mal manejado — Sofía / FinanzasPro / Juan Carlos CFO",
        "scenario": (
            "Sofía es SDR en FinanzasPro. Consiguió el número de Juan Carlos, CFO de una empresa "
            "mediana de construcción, a través de un contacto común que autorizó el mensaje. Así se "
            "desarrolla el intercambio por WhatsApp durante 3 días:\n\n"
            "Sofía (lunes 10:05 AM): Hola Juan Carlos, te escribe Sofía de FinanzasPro. María López me "
            "pasó tu contacto y me autorizó escribirte. Cómo andás?\n"
            "Sofía (lunes 10:07 AM): Te cuento por qué te escribo. Somos una plataforma que ayuda a "
            "CFOs de empresas medianas a cerrar sus balances 60% más rápido, con detección automática "
            "de errores y dashboards en tiempo real. Trabajamos con empresas de construcción, retail y "
            "fintech en LATAM. María mencionó que podría ser interesante para su empresa.\n"
            "Sofía (lunes 10:09 AM): ¿Tenés 20 minutos esta semana para que te muestre cómo funciona? "
            "Puedo mandarte un caso de éxito también si preferís verlo antes.\n"
            "Sofía (martes 9:00 AM): Hola Juan Carlos, no sé si pudiste ver mis mensajes de ayer. "
            "Cualquier duda quedo a la orden.\n"
            "Sofía (miércoles 2:30 PM): Hola Juan Carlos, sé que estás ocupado. Me encantaría saber si "
            "ya viste mi propuesta. ¿Podemos agendar?\n"
            "Juan Carlos (miércoles 4:15 PM): [bloquea el número]"
        ),
        "expected_key_point": (
            "Sofía violó el contrato asíncrono desde el primer intercambio (3 mensajes en 4 minutos el "
            "lunes) y empeoró con insistencia sin respuesta los días siguientes. Aunque tenía un número "
            "legítimamente obtenido, la ejecución destruyó la oportunidad. El bloqueo es la consecuencia "
            "natural cuando se rompen las reglas del canal."
        ),
        "expected_concepts": [
            "contrato asíncrono / lógica del goteo (Sem 6 Bloque 6)",
            "una pregunta por mensaje",
            "parálisis por múltiples CTAs",
            "insistencia sin respuesta = spam percibido",
        ],
        "expected_decision": (
            "Intercambio alternativo: lunes 10:05 un solo mensaje corto, referencia a María, una "
            "pregunta abierta específica sobre el cierre de mes. Esperar 2-3 días. Si no hay respuesta, "
            "un segundo mensaje breve con ángulo distinto en otro día/horario. Si no responde al "
            "segundo, archivar. Nunca más de 2 mensajes sin respuesta."
        ),
    },
    {
        "id": "case_d",
        "title": "Precalificación convertida en interrogatorio — Luis / TechSolve / Camila",
        "scenario": (
            "Luis es SDR en TechSolve. Tiene agendada una llamada de precalificación de 10 min con "
            "Camila, Directora de Marketing de una empresa B2B SaaS, 2 días antes de la reunión con el AE.\n\n"
            "Transcripción:\n\n"
            "Luis: Hola Camila, gracias por conectarte. Antes de la reunión con Nicolás del jueves, "
            "quería hacerte un par de preguntas para que él llegue preparado. ¿Está bien?\n"
            "Camila: Sí, dale.\n"
            "Luis: Perfecto. Primero: ¿cuál es el presupuesto anual que tienen asignado para tools de "
            "marketing automation?\n"
            "Camila: Ah... no te puedo dar un número exacto, depende del proyecto.\n"
            "Luis: Entiendo. ¿Quién toma la decisión final de compra de este tipo de herramientas en tu empresa?\n"
            "Camila: Bueno, yo propongo, después pasa por el CMO, y finalmente aprueba finanzas.\n"
            "Luis: Ok. ¿Tenés un timeline definido de cuándo estarían comprando o implementando una "
            "solución como la nuestra?\n"
            "Camila: No, la verdad ni siquiera sé si vamos a comprar algo. Estamos evaluando.\n"
            "Luis: Comprendo. Última: ¿están evaluando otros proveedores actualmente?\n"
            "Camila: Mirá, honestamente, recién estamos viendo qué opciones hay. Nicolás me contactó "
            "por LinkedIn, dijo que quería mostrarme la plataforma. Vine a escuchar. No sé si esto "
            "amerita una llamada.\n"
            "Luis: Ah... entiendo. Bueno, gracias por tu tiempo. Nos vemos el jueves."
        ),
        "expected_key_point": (
            "Luis convirtió la precalificación en un interrogatorio BANT (Budget, Authority, Need, Timing). "
            "El resultado es que Camila reconsideró si vale la pena la reunión con el AE. Luis perdió la "
            "reunión antes de empezar."
        ),
        "expected_concepts": [
            "BANT en outbound no aplica (Sem 6 Bloque 5)",
            "precalificación = filtro de mínimos, no discovery",
            "framework Situación → Necesidad → Timing",
        ],
        "expected_decision": (
            "Reescribe la precalificación: una pregunta única abierta de situación (\"Contame cómo "
            "están manejando hoy el tema de X\"). Dejar fluir la conversación. Los 3 mínimos (existe "
            "el problema, el contacto tiene llegada, no hay bloqueador absoluto) salen naturalmente "
            "en 10 min si sabés escuchar. No hace falta preguntar directamente por presupuesto ni timing."
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
                {"score": 2, "descriptor": "Usa vocabulario específico (pecado capital, grid de 6 criterios, S→N→T, reconocer/reformular/reconducir, etc.) correctamente aplicado al caso."},
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


# Pesos para nota final del módulo (Documento Maestro líneas 9625-9631)
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
