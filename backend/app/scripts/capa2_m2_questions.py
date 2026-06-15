"""Contenido Capa 2 — Prueba del Módulo 2 (El otro lado).

Fuente: SDR_Academy_Siete_Documento_Maestro.md, Parte IV §Prueba del Módulo 2,
líneas 6451-7197, v0.1 (2026-04-22).

Estructura:
- MCQ: 16 preguntas (Sem 3 + Sem 4 del Módulo 2). 70% del peso de la prueba.
- VIDEO_CASES: 4 casos de banco para video narrado (1 asignado al azar). 30% del peso.
- VIDEO_RUBRIC: 3 criterios × 0-2 puntos → /6 → conversión a %.

Nota: el campo `correct` y `explanation` es solo para el grader/profesor; el
front pública (al alumno) recibe el shape sin ellos.
"""

MCQ: list[dict] = [
    {
        "id": "M2.1",
        "topic": "Aplicar Business Model Canvas",
        "section": "sem3",
        "type": "single",
        "prompt": (
            "TransLogic es un operador logístico que gestiona cadena de frío para alimentos y "
            "farmacéuticas en 4 países de LATAM (850 empleados). Tiene flota propia de camiones "
            "refrigerados y varios centros de almacenaje con temperatura controlada. Firma con sus "
            "clientes contratos anuales que le garantizan volumen.\n\n"
            "Aplicando el Business Model Canvas, ¿cuál es la fuente principal de ingresos de TransLogic?"
        ),
        "choices": [
            {"id": "a", "text": "El cobro a sus clientes por transportar y almacenar su mercadería, con un componente recurrente por los contratos de volumen que firma cada año."},
            {"id": "b", "text": "La flota de camiones refrigerados y los centros de almacenaje: son los activos que sostienen la operación, así que son lo que le genera ingresos."},
            {"id": "c", "text": "La operación diaria de coordinar rutas, choferes y cámaras frías: es lo que hace todos los días, y de ahí salen sus ingresos."},
            {"id": "d", "text": "Una comisión sobre las ventas que sus clientes de alimentos y farmacéuticas concretan gracias a la logística que les provee."},
        ],
        "correct": "a",
        "explanation": (
            "La fuente de ingresos es el cobro por transportar y almacenar mercadería, con componente "
            "recurrente por los contratos anuales de volumen. La flota y los centros son recursos clave "
            "(capex), no fuente de ingreso. La operación diaria son actividades clave. La comisión sobre "
            "ventas sería un modelo marketplace, que no es el caso."
        ),
    },
    {
        "id": "M2.2",
        "topic": "Unit economics aplicado",
        "section": "sem3",
        "type": "single",
        "prompt": (
            "Una empresa de SaaS B2B publicó estos números: ticket promedio anual de USD 5.400, "
            "costo de adquirir un cliente (CAC) de USD 7.200 y permanencia promedio del cliente de "
            "24 meses.\n\n"
            "¿Cuál es el diagnóstico correcto de su economía por cliente?"
        ),
        "choices": [
            {"id": "a", "text": "LTV = USD 5.400 (un año de ticket). LTV/CAC = 0,75; como es menor a 1, la empresa pierde dinero con cada cliente y es inviable."},
            {"id": "b", "text": "LTV = USD 5.400 × 2 años = USD 10.800. LTV/CAC = 1,5; como está por encima de 1, la economía por cliente es saludable y no hay foco de preocupación."},
            {"id": "c", "text": "LTV = USD 5.400 × 2 años = USD 10.800. LTV/CAC = 1,5: está muy por debajo de la regla de 3x, así que hay un problema de economía por cliente que probablemente preocupe a los dueños."},
            {"id": "d", "text": "Faltan datos para diagnosticar: sin conocer el margen y la tasa de recompra no se puede estimar el LTV de este negocio."},
        ],
        "correct": "c",
        "explanation": (
            "LTV = 5.400 × 2 años = 10.800; LTV/CAC = 10.800 / 7.200 = 1,5. La regla estándar de SaaS "
            "B2B es LTV/CAC ≥ 3, así que 1,5 está muy por debajo: hay un problema de economía por "
            "cliente. (a) no multiplica por permanencia y se queda en un año. (b) confunde \"por encima "
            "de 1\" con saludable, ignorando la regla de 3x. (d) hay info suficiente para el diagnóstico."
        ),
    },
    {
        "id": "M2.3",
        "topic": "5 fuerzas de Porter",
        "section": "sem3",
        "type": "single",
        "prompt": (
            "Industria: aseguradoras tradicionales de autos en LATAM (compañías establecidas desde "
            "hace décadas, no las nuevas aseguradoras digitales).\n\n"
            "¿Cuál de las 5 fuerzas de Porter está ejerciendo hoy la mayor presión disruptiva sobre esta industria?"
        ),
        "choices": [
            {"id": "a", "text": "La rivalidad entre las aseguradoras tradicionales: compiten fuerte entre sí por precio y cartera, y esa competencia interna es la mayor presión nueva del sector."},
            {"id": "b", "text": "La amenaza de nuevos entrantes: aseguradoras digitales y canales como los seguros embebidos en apps o en neobancos están redefiniendo cómo se distribuye y se contrata un seguro."},
            {"id": "c", "text": "El poder de negociación de los proveedores: las reaseguradoras internacionales fijan condiciones y son la fuerza que más aprieta el modelo tradicional hoy."},
            {"id": "d", "text": "El poder de negociación de los compradores: el cliente individual presiona los precios a la baja y eso es lo que está quebrando el modelo tradicional."},
        ],
        "correct": "b",
        "explanation": (
            "La mayor presión disruptiva viene de la amenaza de nuevos entrantes: aseguradoras "
            "digitales y canales como seguros embebidos en apps y neobancos están redefiniendo cómo "
            "se distribuye y contrata un seguro, comiendo el modelo tradicional agente → cliente → "
            "póliza anual. La rivalidad, los proveedores y el poder del comprador existen, pero no son "
            "las fuerzas que cambian el mapa hoy. Exige distinguir fuerza presente de fuerza disruptiva."
        ),
    },
    {
        "id": "M2.4",
        "topic": "Jobs to Be Done — dimensión emocional",
        "section": "sem3",
        "type": "single",
        "prompt": (
            "Una Gerenta de RRHH evalúa un software de onboarding para los nuevos empleados.\n\n"
            "¿Cuál de estas descripciones captura el job emocional de la Gerenta (cómo quiere "
            "sentirse), y no el funcional ni el social?"
        ),
        "choices": [
            {"id": "a", "text": "Quiere que el software recorte el tiempo de onboarding de 15 a 7 días, para que los nuevos empleados estén operativos más rápido."},
            {"id": "b", "text": "Quiere que la herramienta se integre con el sistema de RRHH que ya usa, sin tener que migrar datos ni rehacer procesos."},
            {"id": "c", "text": "Quiere que el área la vea como la persona que modernizó el onboarding y dejó una experiencia cuidada para cada nuevo ingreso."},
            {"id": "d", "text": "Quiere llegar tranquila a la reunión de directorio, sin la ansiedad de no saber si los nuevos empleados se están integrando bien, y poder desconectar sabiendo que el proceso está bajo control."},
        ],
        "correct": "d",
        "explanation": (
            "El job emocional es cómo quiere sentirse la persona mientras hace el trabajo. \"Llegar "
            "tranquila\", \"sin ansiedad\", \"poder desconectar\" son descriptores de estado interno. "
            "(a) y (b) son dimensión funcional. (c) es dimensión social (cómo la ve el área). Un SDR "
            "que escribe solo a la dimensión funcional pierde la mayor conexión: la emoción."
        ),
    },
    {
        "id": "M2.5",
        "topic": "ICP vs buyer persona",
        "section": "sem4",
        "type": "single",
        "prompt": (
            "Un SDR dice: \"Mi ICP es Gerentes de Marketing de fintechs en LATAM.\"\n\n"
            "¿Qué está haciendo mal?"
        ),
        "choices": [
            {"id": "a", "text": "Está mezclando dos filtros distintos: el ICP define la empresa (fintech en LATAM) y el buyer persona define a la persona (Gerente de Marketing); son criterios separados y acumulativos."},
            {"id": "b", "text": "Nada: así se define un ICP, combinando el tipo de empresa y el rol al que se le vende en una sola frase."},
            {"id": "c", "text": "Eligió mal el rol: para una fintech debería apuntar al CMO y no a un Gerente de Marketing, que no suele tener la decisión."},
            {"id": "d", "text": "Definió mal la geografía: \"LATAM\" es demasiado amplio para un ICP y debería bajar a países específicos."},
        ],
        "correct": "a",
        "explanation": (
            "ICP = empresa (industria, tamaño, geografía); buyer persona = persona (rol, decisión, "
            "motivaciones). Son dos filtros distintos y acumulativos. Confundirlos genera listas mal "
            "filtradas: se agenda con Gerentes de Marketing en empresas que no son ICP, o se "
            "prospectan fintechs sin saber qué rol buscar dentro."
        ),
    },
    {
        "id": "M2.6",
        "topic": "Identificar arquetipo Challenger Customer (Mobilizer/Skeptic)",
        "section": "sem4",
        "type": "single",
        "prompt": (
            "Un prospecto responde a un cold email del SDR:\n\n"
            "\"Interesante. Antes de programar una llamada: ¿pueden mostrarme 3 casos de uso con "
            "empresas de nuestro tamaño donde hayan medido el impacto específico en nuestra métrica "
            "principal (la tasa de cancelación de clientes)? Necesito datos reales antes de llevar "
            "esto a mi comité interno.\"\n\n"
            "¿Qué perfil de conducta representa esta persona?"
        ),
        "choices": [
            {"id": "a", "text": "El amistoso: responde con cordialidad y se muestra abierto a conversar sin poner trabas."},
            {"id": "b", "text": "El que negocia información: ofrece datos internos a cambio de algo que le interese conseguir."},
            {"id": "c", "text": "El escéptico: cuestiona y pide evidencia concreta antes de avanzar, y cuando se convence empuja fuerte la decisión hacia adentro."},
            {"id": "d", "text": "El que bloquea: pone condiciones para frenar el avance y mantener las cosas como están."},
        ],
        "correct": "c",
        "explanation": (
            "Señales del escéptico: cuestiona antes de avanzar, pide datos específicos (3 casos + "
            "métrica concreta), menciona comité interno (va a empujar si se convence) y tiene criterio "
            "propio. Es uno de los perfiles que impulsa la decisión. Muchos SDRs leen \"pide datos "
            "antes de avanzar\" como obstáculo; en realidad es la señal más clara de que impulsa."
        ),
    },
    {
        "id": "M2.7",
        "topic": "Frenos del decisor B2B",
        "section": "sem4",
        "type": "single",
        "prompt": (
            "Una CFO responde a una propuesta:\n\n"
            "\"La propuesta se ve bien, los números cierran. Pero cambiar de proveedor implica 3 meses "
            "de implementación, coordinar con IT, entrenar a 40 personas, y si algo sale mal me lo cargan "
            "a mí frente al directorio. Hoy tengo algo que funciona a medias; prefiero eso a arriesgar.\"\n\n"
            "¿Qué freno del decisor B2B domina esta respuesta?"
        ),
        "choices": [
            {"id": "a", "text": "Fatiga de proveedores: recibe tantas propuestas que su reacción por defecto es no enganchar con ninguna."},
            {"id": "b", "text": "Costo de cambio y miedo al error público combinados: el esfuerzo de migrar pesa, y sobre todo el riesgo de quedar expuesta ante el directorio si la apuesta falla."},
            {"id": "c", "text": "Falta de presupuesto: no tiene los recursos asignados para encarar el cambio este año."},
            {"id": "d", "text": "Desconocimiento del producto: todavía no entiende qué hace la solución ni cómo le serviría."},
        ],
        "correct": "b",
        "explanation": (
            "Dos frenos operando juntos: costo de cambio (\"3 meses, coordinar con IT, entrenar 40 "
            "personas\") y miedo al error público (\"me lo cargan a mí frente al directorio\"). La "
            "combinación es la que paraliza. Insistir con el ROI no sirve. Lo que podría desbloquear: "
            "un caso con plan de implementación explícito que minimice el riesgo percibido (ej. piloto de 30 días)."
        ),
    },
    {
        "id": "M2.8",
        "topic": "Timing signals reales vs ruido",
        "section": "sem4",
        "type": "multi",
        "prompt": (
            "Un SDR investiga una empresa potencial y encuentra estos hallazgos. "
            "Marcá todos los hallazgos que son señales reales de timing (no marques el ruido):"
        ),
        "choices": [
            {"id": "1", "text": "Contrató un nuevo CMO hace 40 días, traído de afuera (no una promoción interna)."},
            {"id": "2", "text": "El CEO subió una foto del equipo en un offsite corporativo."},
            {"id": "3", "text": "Publicó 30 ofertas de trabajo para ingeniería y ventas en las últimas 3 semanas."},
            {"id": "4", "text": "Ganó un premio de \"Mejor marca empleadora 2026\"."},
            {"id": "5", "text": "Anunció expansión de operaciones a Brasil y Colombia para el tercer trimestre de 2026."},
            {"id": "6", "text": "El Director de Tecnología publicó que \"este año es clave para modernizar nuestro stack\"."},
            {"id": "7", "text": "La competencia directa despidió a 150 personas."},
            {"id": "8", "text": "Cerró una ronda de inversión Serie D por USD 50M la semana pasada."},
        ],
        "correct": ["1", "3", "5", "6", "8"],
        "explanation": (
            "Señales operativas: 1 (nuevo CMO externo → ventana de ~90-100 días), 3 (30 ofertas → la "
            "maquinaria comercial escala), 5 (expansión multipaís → necesidades operativas), 6 "
            "(declaración explícita del Director de Tecnología), 8 (Serie D → capital + crecimiento). "
            "Ruido: 2 (social), 4 (clima interno), 7 (afecta al competidor, no al prospecto)."
        ),
    },
    {
        "id": "M2.9",
        "topic": "No listo vs no fit",
        "section": "sem4",
        "type": "single",
        "prompt": (
            "Un prospecto responde al cold email:\n\n"
            "\"Interesante la propuesta. Te voy a ser franco: el presupuesto de tecnología de todo el "
            "año ya está comprometido en otras prioridades. Pero yo armo el plan del próximo año entre "
            "septiembre y octubre, y el tema que planteas está en mi radar. ¿Puedes escribirme de "
            "nuevo a fines de agosto?\"\n\n"
            "¿Cómo clasificarías este caso?"
        ),
        "choices": [
            {"id": "a", "text": "No encaja: como no tiene presupuesto disponible, la empresa no califica y conviene descartarla."},
            {"id": "b", "text": "Frío: es una respuesta de cortesía para sacarse de encima al SDR sin comprometerse a nada."},
            {"id": "c", "text": "No listo, con un disparador concreto: el bloqueo de presupuesto es temporal y dejó una fecha (agosto, antes de armar el plan del año); se archiva con recontacto."},
            {"id": "d", "text": "Listo: como dijo que el tema está en su radar, conviene empujar la reunión cuanto antes."},
        ],
        "correct": "c",
        "explanation": (
            "Tres señales claras de \"no listo\" con disparador: (1) bloqueo temporal (presupuesto "
            "comprometido); (2) apertura genuina (\"está en mi radar\"); (3) disparador concreto "
            "(\"escribime a fines de agosto\"). \"No tiene presupuesto ahora\" ≠ \"no va a tener "
            "nunca\". El prospecto dio fecha específica, así que no es cortesía ni \"no encaja\"."
        ),
    },
    {
        "id": "M2.10",
        "topic": "Mapeo dolor-solución mal hecho",
        "section": "sem3",
        "type": "single",
        "prompt": (
            "Un SDR que vende una plataforma de gestión de ventas B2B le escribe a un VP de Ventas "
            "de una empresa de servicios financieros:\n\n"
            "\"Hola Ricardo, vi que tu empresa está creciendo. Nuestra plataforma ayuda a equipos de "
            "ventas como el tuyo a optimizar el pipeline y cerrar más negocios. Ayudamos a empresas "
            "similares a aumentar su conversión un 30%. ¿Tienes 20 minutos esta semana para ver cómo "
            "podemos ayudar a tu empresa?\"\n\n"
            "¿Cuál es el problema de fondo de este mapeo dolor-solución?"
        ),
        "choices": [
            {"id": "a", "text": "No hay mapeo: todo es genérico (\"crecer\", \"equipos como el tuyo\", \"empresas similares\"); no hay una señal específica de Ricardo ni un dolor de su contexto, solo producto y un pedido de reunión."},
            {"id": "b", "text": "Le falta citar la fuente del 30%: sin respaldo del dato, el prospecto no va a confiar en la cifra."},
            {"id": "c", "text": "El llamado a la acción es excesivo: pedir 20 minutos de entrada es demasiado y conviene proponer algo más liviano."},
            {"id": "d", "text": "El tono es demasiado informal para un VP de una empresa de servicios financieros: debería ser más formal."},
        ],
        "correct": "a",
        "explanation": (
            "Un mapeo bien hecho tiene dolor específico, impacto contextual y conexión con la oferta "
            "sin prometer. Este email tiene dolor genérico (\"crecer\"), impacto sin contexto (\"30%\") "
            "y conexión vaga (\"ayudar a tu empresa\"). Es producto con un CTA, no mapeo. Citar la "
            "fuente ayudaría, pero el problema es estructural, no de cita ni de tono."
        ),
    },
    {
        "id": "M2.11",
        "topic": "Error #1 del SDR nuevo",
        "section": "sem3",
        "type": "single",
        "prompt": (
            "Un SDR junior recibe este feedback de su manager:\n\n"
            "\"Tus cold emails explican bien lo que hace nuestro producto. Pero están convirtiendo al "
            "0,4%. El promedio del equipo es 1,8%.\"\n\n"
            "¿Cuál es el error más probable que está cometiendo el SDR?"
        ),
        "choices": [
            {"id": "a", "text": "Los emails son demasiado largos y el prospecto los abandona antes de llegar al pedido de reunión."},
            {"id": "b", "text": "No está haciendo suficiente volumen de envíos, y por eso la cantidad de respuestas que recibe es baja."},
            {"id": "c", "text": "El producto no tiene buen encaje con el mercado, y por eso ningún SDR del equipo logra convertir."},
            {"id": "d", "text": "Está vendiendo la solución sin haber entendido el problema: escribe desde el producto y no desde el dolor del prospecto."},
        ],
        "correct": "d",
        "explanation": (
            "\"Explican bien lo que hace nuestro producto\" es exactamente el síntoma del error #1 del "
            "SDR nuevo. La conversión baja (0,4% vs 1,8% del promedio) confirma que el problema no es "
            "ejecución sino enfoque. El feedback es sobre conversión, no volumen. El producto sí "
            "convierte con otros SDRs (1,8%), así que el problema es este SDR específico."
        ),
    },
    {
        "id": "M2.12",
        "topic": "Motivador del decisor",
        "section": "sem4",
        "type": "single",
        "prompt": (
            "Un VP de Ventas, ascendido hace 4 meses, responde a un cold email:\n\n"
            "\"Me interesa entender cómo otras empresas similares midieron el impacto después de "
            "implementar esto. Necesito poder presentar un caso concreto al CEO en mi primer review "
            "del próximo trimestre. Si hay métricas claras y un timeline realista, tiene chance.\"\n\n"
            "¿Cuál es el motor principal que mueve su decisión?"
        ),
        "choices": [
            {"id": "a", "text": "Conseguir resultados medibles como fin en sí mismo, más allá de lo que signifiquen para él."},
            {"id": "b", "text": "Avanzar en su carrera: recién ascendido, necesita un proyecto visible que demuestre impacto en su primer review ante el CEO."},
            {"id": "c", "text": "Evitar el riesgo: prefiere no moverse para no exponerse a un error en su nuevo cargo."},
            {"id": "d", "text": "Ganar posición interna: le importa sobre todo cómo lo perciben sus pares dentro de la empresa."},
        ],
        "correct": "b",
        "explanation": (
            "El VP dice literalmente \"mi primer review del próximo trimestre\": oportunidad de "
            "demostrar que el ascenso fue acertado. Proyecto exitoso = carrera asegurada; proyecto "
            "fallido = riesgo de salida. Los otros motores están presentes pero son secundarios. "
            "Implicación: mandarle un caso con métricas y timeline que él pueda usar en su review."
        ),
    },
    {
        "id": "M2.13",
        "topic": "Encadenada parte 1 — lectura integrada",
        "section": "sem3",
        "type": "single",
        "prompt": (
            "Empresa: AgroExport Argentina (exportadora de commodities agrícolas, 400 empleados, con "
            "expansión a Brasil anunciada para el cuarto trimestre de 2026). Contacto potencial: "
            "Camilo Díaz, Gerente de Logística, 3 años en el cargo. Un post reciente suyo: \"Este "
            "cuarto trimestre nos complica el volumen; las rutas actuales no escalan.\"\n\n"
            "¿Cuál es la hipótesis de dolor más probable para usar como gancho?"
        ),
        "choices": [
            {"id": "a", "text": "El crecimiento de la empresa está generando estrés y sobrecarga en el equipo de Camilo."},
            {"id": "b", "text": "El costo de exportar commodities agrícolas está subiendo por factores de mercado externos a la empresa."},
            {"id": "c", "text": "Con la expansión a Brasil anunciada y el comentario público de Camilo sobre rutas que no escalan, el dolor probable es rediseñar la operación logística para absorber volumen multipaís antes del cierre del año sin que se disparen los costos."},
            {"id": "d", "text": "Los empleados del área están sobrecargados de trabajo por el ritmo de la operación actual."},
        ],
        "correct": "c",
        "explanation": (
            "Combina dos señales específicas (expansión anunciada con fecha + queja pública del "
            "contacto) con un contexto operativo real (escalar logística multipaís es caro y "
            "complicado). Las otras opciones son generalidades o factores externos no accionables."
        ),
    },
    {
        "id": "M2.14",
        "topic": "Encadenada parte 2 — escritura del gancho",
        "section": "sem4",
        "type": "single",
        "prompt": (
            "Continúa el caso de la pregunta anterior (AgroExport Argentina + Camilo Díaz). "
            "El SDR quiere escribir el gancho del cold email para Camilo.\n\n"
            "¿Cuál de estos ganchos es el más efectivo?"
        ),
        "choices": [
            {"id": "a", "text": "\"Hola Camilo, vi tu comentario sobre rutas que no escalan y el anuncio de expansión a Brasil. En exportadoras que crecen a varios países, el costo más caro suele aparecer en los primeros meses, cuando las rutas armadas para el mercado original no rinden en el nuevo. ¿Les está pasando algo así o ya tienen cómo calibrarlo?\""},
            {"id": "b", "text": "\"Hola Camilo, vi que AgroExport está creciendo mucho. Nuestra plataforma optimiza la logística de punta a punta. ¿Tienes 20 minutos esta semana para que te cuente?\""},
            {"id": "c", "text": "\"Hola Camilo, tenemos 30 años de experiencia en logística internacional y trabajamos con grandes exportadoras globales. Me gustaría coordinar una llamada para presentarte lo que hacemos.\""},
            {"id": "d", "text": "\"Hola Camilo, el crecimiento de AgroExport es realmente impresionante y nos encantaría poder acompañarlos en este momento tan importante. ¿Conversamos esta semana?\""},
        ],
        "correct": "a",
        "explanation": (
            "Señal específica (post + expansión verificables) + conexión al dolor (\"el costo más caro "
            "en los primeros meses\") + no promete (ofrece una pregunta) + un solo CTA. (b) es "
            "genérico, (c) usa prueba social desajustada (grandes exportadoras globales vs AgroExport "
            "de 400 empleados), (d) es halago vacío. La encadenada P13→P14 prueba que el alumno "
            "traduce el dolor a un gancho bien estructurado."
        ),
    },
    {
        "id": "M2.15",
        "topic": "Mobilizer en el primer email",
        "section": "sem4",
        "type": "single",
        "prompt": (
            "Un SDR escribe el primer email a una empresa B2B prospecto. Dentro hay 4 contactos posibles:\n"
            "● Pablo (CEO): C-level, pero según su LinkedIn no suele responder correos en frío.\n"
            "● Mirta (Directora de Operaciones): publica seguido sobre operaciones y comparte "
            "artículos de su industria.\n"
            "● Juan (Gerente de Proyectos): LinkedIn con poca actividad, casi sin publicaciones.\n"
            "● Cecilia (VP de Finanzas): sus posts son sobre todo frases motivacionales y de buenas vibras.\n\n"
            "¿A quién conviene contactar primero para maximizar la chance de dar con alguien que "
            "impulse la decisión hacia adentro?"
        ),
        "choices": [
            {"id": "a", "text": "A Pablo: como CEO tiene el mayor peso en la decisión, así que es el mejor punto de entrada."},
            {"id": "b", "text": "A Juan: como Gerente de Proyectos es decisor operativo, así que es quien va a hacer avanzar el tema."},
            {"id": "c", "text": "A Cecilia: su actividad en LinkedIn la muestra accesible, y eso facilita conseguir la reunión."},
            {"id": "d", "text": "A Mirta: publica y comparte conocimiento de su industria, el patrón de conducta de quien divulga ideas y suele empujarlas internamente."},
        ],
        "correct": "d",
        "explanation": (
            "Publicar posts y compartir artículos de industria es la señal conductual más clara del "
            "que divulga (un perfil que impulsa la decisión hacia adentro). Jerarquía ≠ perfil de "
            "conducta; rol ≠ perfil de conducta. Los posts de \"buenas vibras\" son señal del "
            "amistoso (accesible, pero no impulsa)."
        ),
    },
    {
        "id": "M2.16",
        "topic": "Integradora final — sistema completo",
        "section": "sem4",
        "type": "single",
        "prompt": (
            "Una SDR con experiencia le explica a una colega que recién empieza:\n\n"
            "\"Lo que aprendí en estos años es que, antes de escribir un email, paso por tres filtros. "
            "El primero es el del negocio: ¿entiendo cómo gana dinero esta empresa, qué la hace crecer "
            "y qué la frena? Si no puedo responder eso en 30 segundos, todavía no estoy lista para "
            "escribir; no me alcanza con que LinkedIn diga 'es una fintech', necesito saber qué tipo "
            "de fintech, a quién le vende y cuál es su dolor de hoy. El segundo es el del comprador: la "
            "persona a la que le voy a escribir, ¿impulsa la decisión o solo conversa? Si no lo sé, "
            "busco señales antes, porque escribirle a alguien amable que nunca mueve nada me llena la "
            "agenda de reuniones que no cierran. El tercero es el del momento: ¿hay alguna señal "
            "concreta y reciente para construir un gancho específico? Si no la hay, la empresa no está "
            "lista para el email en frío hoy: la archivo con un disparador o investigo más a fondo si "
            "es una cuenta prioritaria.\"\n\n"
            "Una SDR junior quiere trabajar con estos tres filtros. ¿Cuál de estas decisiones los "
            "aplica correctamente?"
        ),
        "choices": [
            {"id": "a", "text": "Encontró una buena señal de timing (una ronda de inversión reciente), así que escribe de inmediato al primer contacto que aparece en su base de datos para no perder el momento."},
            {"id": "b", "text": "Antes de escribir, arma el modelo de negocio del prospecto, identifica si su contacto impulsa o solo conversa y busca una señal reciente; si falta cualquiera de los tres, no envía todavía."},
            {"id": "c", "text": "Como entiende bien el producto que vende, redacta un email claro que explica sus funciones y se lo manda a varios contactos de la empresa para cubrir todo el comité."},
            {"id": "d", "text": "Identifica por su cargo a la persona con más poder de decisión y le escribe enseguida, porque con el decisor correcto los otros dos filtros pasan a segundo plano."},
        ],
        "correct": "b",
        "explanation": (
            "Aplicar los tres filtros significa, antes de enviar: armar el modelo de negocio del "
            "prospecto (filtro del negocio), identificar si el contacto impulsa o solo conversa "
            "(filtro del comprador) y buscar una señal concreta y reciente (filtro del momento); si "
            "falta cualquiera, no se envía. (a) salta el filtro del negocio y del comprador. (c) es el "
            "error #1: escribe desde el producto. (d) confunde cargo con conducta y descarta dos filtros."
        ),
    },
]


VIDEO_CASES: list[dict] = [
    {
        "id": "case_a",
        "title": "Leer un negocio antes de la reunión",
        "scenario": (
            "Mercado Libre Argentina figura como cuenta ICP para un cliente que vende software de "
            "optimización de logística. Tu AE te pide armar un brief conceptual de 5 minutos antes de "
            "la reunión.\n\n"
            "Lo que debes producir en el video:\n"
            "1. El Business Model Canvas de Mercado Libre Argentina en sus 9 componentes (puedes "
            "enfocarte en el negocio de marketplace de e-commerce, no en Mercado Pago).\n"
            "2. Las 5 fuerzas de Porter aplicadas a la industria de e-commerce en LATAM, identificando "
            "las 2 fuerzas más disruptivas hoy.\n"
            "3. A partir de los dos análisis, el dolor estructural probable que el software de "
            "optimización logística podría atacar."
        ),
        "expected_key_point": (
            "Las 2 fuerzas más disruptivas son la rivalidad intensa (competencia con otros "
            "marketplaces globales) y el poder creciente del comprador (muchas alternativas + "
            "comparadores de precio), conectadas con un dolor logístico concreto: eficiencia de "
            "última milla y costo variable por envío."
        ),
        "expected_concepts": [
            "Business Model Canvas en los 9 componentes",
            "5 fuerzas de Porter — distinción de fuerzas dominantes",
            "mapeo dolor-solución estructural",
        ],
        "expected_decision": (
            "Mapear el dolor estructural a la eficiencia de última milla y el costo variable por "
            "envío, y proponer el ángulo del software de optimización logística sobre ese dolor como "
            "hipótesis a validar en la reunión con el AE. Un análisis 6/6 arma el Business Model "
            "Canvas completo y jerarquiza las fuerzas dominantes; uno débil describe el Canvas en "
            "general o aplica Porter sin priorizar fuerzas."
        ),
    },
    {
        "id": "case_b",
        "title": "Leer un comité de 6 personas",
        "scenario": (
            "Se muestran 6 respuestas de personas distintas de la misma empresa (extractos de emails "
            "o LinkedIn) y una descripción breve del rol de cada una:\n\n"
            "1) VP de Operaciones: \"Estoy cansado de proveedores que prometen y no cumplen. Si no "
            "tienes casos de estudio auditados con métricas claras, no sigo.\"\n"
            "2) Gerente de Proyectos: \"Qué interesante tu propuesta. Encantado de conversar. Dime "
            "cuándo te viene bien.\"\n"
            "3) Director Comercial: \"Leí el documento que me compartiste, me pareció excelente. Se lo "
            "pasé al comité ejecutivo para discutirlo en la próxima reunión; esto puede ser parte del "
            "plan del próximo trimestre.\"\n"
            "4) Analista senior: \"Te puedo dar información sobre cómo funciona esto internamente, pero "
            "necesito saber si vamos a poder incluir a mi equipo en el piloto. ¿Hablamos?\"\n"
            "5) Coordinador: \"Si esto me ayuda a ganar visibilidad ante el CEO, cuenta conmigo. "
            "Ayúdame a presentarlo con mi nombre en el brief.\"\n"
            "6) Director de Tecnología: \"No creo que sea el momento. Tenemos otras prioridades.\"\n\n"
            "Lo que debes producir:\n"
            "1. Identificar, para cada contacto, qué perfil de conducta representa (entre los que "
            "viste en la Semana 4).\n"
            "2. Separar quiénes impulsan la decisión, quiénes solo conversan y quién bloquea.\n"
            "3. Proponer una estrategia: con quién profundizar, a quién usar como referidor y con quién "
            "no gastar energía."
        ),
        "expected_key_point": (
            "Separar conducta de cargo. Perfiles: 1 = el escéptico (impulsa); 2 = el amistoso (solo "
            "conversa); 3 = el que divulga (impulsa); 4 = el que negocia información (solo conversa); "
            "5 = el que busca beneficio propio (solo conversa); 6 = el que bloquea. Impulsan: 1 y 3. "
            "Solo conversan: 2, 4, 5. Bloquea: 6."
        ),
        "expected_concepts": [
            "perfiles de conducta del comprador (Semana 4)",
            "quién impulsa la decisión vs quién solo conversa",
            "estrategia de mapeo de stakeholders",
        ],
        "expected_decision": (
            "Profundizar con #1 (el escéptico: darle los casos y métricas que pide) y con #3 (el que "
            "divulga: darle material para que evangelice internamente). Usar a #4 como fuente de "
            "información, no como aliado. No pelear con #6."
        ),
    },
    {
        "id": "case_c",
        "title": "Un mapeo dolor-solución genérico para reescribir",
        "scenario": (
            "Un SDR escribió este cold email:\n\n"
            "\"Hola Marina, vi que tu empresa está creciendo rápido. Nuestra plataforma ayuda a empresas "
            "B2B a mejorar su pipeline de ventas y alcanzar resultados increíbles. Trabajamos con clientes "
            "como Globant y Mercado Libre. ¿Tienes 20 minutos esta semana para ver si podemos ayudar?\"\n\n"
            "Contexto adicional que el SDR tiene, pero no usó:\n"
            "● Empresa de Marina: un neobanco regional que cerró una ronda de inversión grande hace "
            "pocos meses y anunció expansión a dos países nuevos.\n"
            "● Rol de Marina: VP de Growth.\n"
            "● Post reciente de Marina en LinkedIn: \"El desafío más caro de expandir a tres países a "
            "la vez: mantener el CAC estable mientras el canal local todavía no madura.\"\n\n"
            "Lo que debes producir en el video:\n"
            "1. Diagnosticar por qué el email escrito es un mapeo dolor-solución mal hecho.\n"
            "2. Reescribir el email aprovechando el contexto disponible y los principios de la Semana 3 "
            "y la Semana 4.\n"
            "3. Justificar cada cambio con el concepto del curso que lo fundamenta."
        ),
        "expected_key_point": (
            "El email es producto genérico sin señal específica: el SDR ignoró las tres señales "
            "disponibles (la ronda de inversión, la expansión a tres países y el post de Marina sobre "
            "el CAC), y usa una prueba social desajustada (empresas grandes que no son comparables). "
            "Es el error #1 del SDR nuevo + mapeo dolor-solución mal hecho."
        ),
        "expected_concepts": [
            "error #1 del SDR nuevo",
            "mapeo dolor-solución",
            "gancho específico",
            "prueba social ajustada al tamaño/contexto",
        ],
        "expected_decision": (
            "Reescribir con gancho específico (el post sobre el CAC en la expansión a tres países + el "
            "anuncio de expansión), dolor contextual (CAC distorsionado en mercados nuevos donde el "
            "canal local aún no madura), conexión sin prometer y un solo llamado a la acción. Nombra "
            "el error #1, el mapeo dolor-solución y el gancho específico."
        ),
    },
    {
        "id": "case_d",
        "title": "Clasificar 10 respuestas a cold emails",
        "scenario": (
            "Un SDR recibió 10 respuestas a cold emails esta semana. El ICP definido es: empresas B2B "
            "SaaS de LATAM, de 150 a 500 empleados. El producto que vende el SDR es una herramienta de "
            "automatización de marketing. Las 10 respuestas:\n\n"
            "1) SoftPlay Perú (120 empleados, SaaS B2C de gaming), CTO: \"Interesante, agendemos.\"\n"
            "2) GrowthLab Chile (300 empleados, SaaS B2B), VP de Marketing: \"Me interesa. Tengo "
            "reunión de directorio en 6 semanas; después de eso te retomo.\"\n"
            "3) DataFlow Colombia (400 empleados, SaaS B2B), CEO: \"Estamos en proceso de venta de la "
            "empresa a un fondo. La operación probablemente cierre en 4 meses.\"\n"
            "4) CloudRise Argentina (280 empleados, SaaS B2B), CMO: \"Ya firmamos contrato con un "
            "competidor directo de ustedes el mes pasado. 2 años de compromiso.\"\n"
            "5) PayStack LATAM (180 empleados, SaaS B2B), VP de Growth: \"Interesante, pero no es "
            "prioridad este año ni el que viene. Nuestra estrategia es consolidar lo que tenemos sin "
            "sumar herramientas.\"\n"
            "6) ConsultorQ Uruguay (400 empleados, SaaS B2B), CFO: \"Sáquenme de su lista, por favor, "
            "y no me contacten más.\"\n"
            "7) MetaEdu México (220 empleados, SaaS B2B de edtech), CMO: \"Tengo interés. Justo "
            "estamos evaluando herramientas, 3 opciones activas. ¿Puedes mandarme un deck?\"\n"
            "8) LogiSmart Perú (90 empleados, SaaS B2B de logística), COO: \"Me interesa, pero somos "
            "chicos. ¿Tienen descuento para empresas más pequeñas?\"\n"
            "9) HealthCore Chile (450 empleados, SaaS B2B de salud), Gerente de Marketing: \"Hablé con "
            "nuestra VP de Marketing, está interesada en conocer más. Te paso su contacto: maria@...\"\n"
            "10) PagosGlobal Brasil (650 empleados, SaaS B2B de pagos), CFO: \"Podríamos conversar, "
            "pero somos un equipo grande y con procesos propios.\"\n\n"
            "Lo que debes producir:\n"
            "1. Clasificar cada respuesta en una de: calificado / no listo / no encaja / no contactar.\n"
            "2. Para los \"no listo\": especificar una fecha o un disparador de recontacto.\n"
            "3. Identificar si el SDR está cometiendo algún error de segmentación."
        ),
        "expected_key_point": (
            "Clasificación esperada: 1 = no encaja (B2C y 120 < 150 del ICP); 2 = no listo "
            "(recontactar ~7 semanas, tras la reunión de directorio); 3 = no listo (recontactar 6-12 "
            "meses tras la venta, la nueva administración redefine prioridades); 4 = no listo "
            "(recontactar ~22 meses, antes del vencimiento del contrato); 5 = no listo con horizonte "
            "largo (~18 meses): el bloqueo es de prioridad y presupuesto, no del modelo; no es \"no "
            "encaja\" porque \"no encaja\" exige que nunca cierre; 6 = no contactar (marca "
            "permanente); 7 = calificado (calza ICP y está en evaluación activa); 8 = no encaja por "
            "tamaño (90 < 150); 9 = calificado (referido a un buyer persona válido, con contacto); "
            "10 = no encaja por tamaño (650 > 500). Patrón: varios casos fuera del ICP (1, 8, 10) → "
            "problema de segmentación aguas arriba."
        ),
        "expected_concepts": [
            "no listo (con disparador) vs no encaja estructural",
            "no contactar",
            "patrón de error de segmentación en filtros de prospección",
        ],
        "expected_decision": (
            "Avanzar con 7 y 9. Archivar 2, 3, 4 y 5 como \"no listo\" con disparador de fecha. "
            "Descartar 1, 8 y 10 (no encaja por tamaño/modelo) y respetar el \"no contactar\" de 6. "
            "Recomendar revisar los filtros de la base de prospección aguas arriba: varios casos "
            "fuera del ICP indican problema de segmentación, no de copy."
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
                {"score": 0, "descriptor": "Frases genéricas. No usa vocabulario del curso."},
                {"score": 1, "descriptor": "Usa algún concepto pero superficial o aplicado a medias."},
                {"score": 2, "descriptor": "Usa el vocabulario del curso (Business Model Canvas, 5 fuerzas de Porter, Jobs to Be Done, quién impulsa/solo conversa, el escéptico, no listo/no encaja, etc.) y lo conecta correctamente con el caso."},
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


# Pesos para nota final del módulo (Documento Maestro líneas 7170-7173)
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
