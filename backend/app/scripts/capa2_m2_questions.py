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
            "Recibís datos sobre una empresa B2B: TransLogic, operador logístico que "
            "gestiona cadena de frío para alimentos en 4 países LATAM. 850 empleados. "
            "Modelo: cobran por servicio transportado + almacenaje. Sus clientes son "
            "empresas de alimentos, farmacéuticas y laboratorios que necesitan "
            "trazabilidad y temperatura controlada.\n\n"
            "Aplicando BMC, ¿cuál de las siguientes es la fuente principal de ingresos de TransLogic?"
        ),
        "choices": [
            {"id": "a", "text": "Venta de la flota de camiones refrigerados."},
            {"id": "b", "text": "Comisión sobre las ventas de las empresas clientes."},
            {"id": "c", "text": "Cobro por servicio de transporte + almacenaje (modelo transaccional + recurrente)."},
            {"id": "d", "text": "Venta de software de trazabilidad."},
        ],
        "correct": "c",
        "explanation": (
            "El enunciado lo dice explícitamente — \"cobran por servicio transportado + almacenaje\". "
            "Modelo operativo logístico B2B típico: ingresos transaccionales con componente recurrente. "
            "La flota es recurso clave (capex), no fuente de ingreso. La comisión sobre ventas sería marketplace. "
            "El software no se menciona."
        ),
    },
    {
        "id": "M2.2",
        "topic": "Unit economics aplicado",
        "section": "sem3",
        "type": "single",
        "prompt": (
            "Una empresa SaaS B2B tiene estos números:\n"
            "● Ticket promedio anual: USD 5.400\n"
            "● CAC: USD 7.200\n"
            "● Permanencia promedio del cliente: 24 meses\n"
            "● Margen bruto: 75%\n\n"
            "¿Cuál es el diagnóstico correcto de unit economics?"
        ),
        "choices": [
            {"id": "a", "text": "LTV = USD 5.400. LTV/CAC = 0.75 (bajo). Empresa insostenible."},
            {"id": "b", "text": "LTV contribución (con margen 75%) = USD 5.400 × 2 años × 0.75 = USD 8.100. LTV/CAC = 1.13. Por debajo de la regla de 3x. Hay problema de unit economics que probablemente explique frustración del CFO del prospecto."},
            {"id": "c", "text": "LTV = USD 5.400 × 2 años = USD 10.800. LTV/CAC = 1.5. Saludable."},
            {"id": "d", "text": "No hay suficiente información para calcular."},
        ],
        "correct": "b",
        "explanation": (
            "Cálculo correcto de LTV contribución incluye el margen bruto. "
            "LTV revenue: 5.400 × 2 = 10.800. LTV contribución (×0.75) = 8.100. "
            "LTV/CAC = 8.100 / 7.200 = 1.13. La regla estándar de SaaS B2B es LTV/CAC ≥ 3 — "
            "este negocio está estructuralmente insostenible a largo plazo. "
            "(a) no multiplica por permanencia. (c) no aplica margen. (d) hay toda la info necesaria."
        ),
    },
    {
        "id": "M2.3",
        "topic": "5 fuerzas de Porter",
        "section": "sem3",
        "type": "single",
        "prompt": (
            "Industria: aseguradoras tradicionales de autos en LATAM (no InsurTech nuevas, "
            "aseguradoras establecidas de décadas).\n\n"
            "¿Cuál de las 5 fuerzas está ejerciendo mayor presión disruptiva sobre esta industria en 2026?"
        ),
        "choices": [
            {"id": "a", "text": "Rivalidad entre competidores existentes — las aseguradoras tradicionales compiten feroz entre sí."},
            {"id": "b", "text": "Amenaza de sustitutos + amenaza de nuevos entrantes (InsurTech, seguros embebidos en apps como Rappi, neobancos con productos de seguros integrados). Ambas fuerzas están redefiniendo qué es \"un seguro\" y cómo se distribuye."},
            {"id": "c", "text": "Poder de negociación de los proveedores (reaseguradoras internacionales)."},
            {"id": "d", "text": "Poder de negociación de compradores — el cliente individual no tiene poder ante aseguradoras grandes."},
        ],
        "correct": "b",
        "explanation": (
            "El cambio estructural más grande en seguros LATAM 2024-2026 combina dos fuerzas: "
            "nuevos entrantes (InsurTech licenciadas, brazos digitales de banca, neobancos) + "
            "sustitutos (seguros embebidos dentro de la compra misma). Están comiendo el modelo "
            "tradicional agente → cliente → póliza anual. Las otras fuerzas existen pero no son "
            "las que cambian el mapa hoy. Exige distinguir entre fuerza presente y fuerza disruptiva."
        ),
    },
    {
        "id": "M2.4",
        "topic": "Jobs to Be Done — dimensión emocional",
        "section": "sem3",
        "type": "single",
        "prompt": (
            "Una Gerenta de RRHH compra un software de onboarding. Lee sobre distintas "
            "dimensiones del \"job\" (trabajo que contrata al producto para hacer).\n\n"
            "¿Cuál de las siguientes descripciones representa el job emocional de la Gerenta?"
        ),
        "choices": [
            {"id": "a", "text": "\"El software debe reducir el tiempo de onboarding de 15 a 7 días.\""},
            {"id": "b", "text": "\"El software debe integrarse con el HRIS existente sin migraciones.\""},
            {"id": "c", "text": "\"La Gerenta quiere llegar tranquila al board meeting de HR sin ansiedad sobre si los nuevos empleados están rampeando bien, y poder dormir sabiendo que el proceso está contenido.\""},
            {"id": "d", "text": "\"La Gerenta quiere que los nuevos empleados tengan una buena primera impresión.\""},
        ],
        "correct": "c",
        "explanation": (
            "El job emocional es cómo quiere sentirse la persona mientras hace el trabajo. "
            "\"Llegar tranquila\", \"sin ansiedad\", \"poder dormir\" son descriptores de estado interno. "
            "(a) y (b) son dimensión funcional. (d) es dimensión social pero enfocada en los empleados. "
            "Un SDR que escribe solo a la dimensión funcional pierde la mayor conexión — la emoción."
        ),
    },
    {
        "id": "M2.5",
        "topic": "ICP vs buyer persona",
        "section": "sem4",
        "type": "single",
        "prompt": (
            "Un SDR dice: \"Mi ICP es Gerentes de Marketing de fintechs en LATAM.\"\n\n"
            "¿Qué está haciendo mal este SDR?"
        ),
        "choices": [
            {"id": "a", "text": "Nada — así se define un ICP correctamente."},
            {"id": "b", "text": "Está mezclando ICP (la empresa — fintech en LATAM) con buyer persona (la persona — Gerente de Marketing). Un ICP se define por criterios de empresa (industria, tamaño, geografía); un buyer persona se define por criterios de persona (rol, decisión, motivaciones). Son dos filtros distintos y acumulativos."},
            {"id": "c", "text": "Debería haber dicho \"CMO\" en lugar de \"Gerente de Marketing\"."},
            {"id": "d", "text": "\"LATAM\" es demasiado amplio, debería especificar país."},
        ],
        "correct": "b",
        "explanation": (
            "Exacto lo que el Bloque 1 de Sem 4 explica. ICP = empresa, Buyer persona = persona. "
            "Confundirlos genera listas mal filtradas: se agenda con Gerentes de Marketing en "
            "empresas que no son ICP, o se prospectan fintechs sin saber qué rol dentro buscar."
        ),
    },
    {
        "id": "M2.6",
        "topic": "Identificar arquetipo Challenger Customer (Mobilizer/Skeptic)",
        "section": "sem4",
        "type": "single",
        "prompt": (
            "Un prospecto responde a un cold email del SDR con:\n\n"
            "\"Interesante. Antes de programar una llamada: ¿pueden mostrarme 3 casos de uso con "
            "empresas de nuestro tamaño donde hayan medido el impacto específico en nuestra métrica "
            "principal (churn rate)? Necesito data real antes de llevar esto a mi comité interno.\"\n\n"
            "¿Qué arquetipo del Challenger Customer representa esta persona?"
        ),
        "choices": [
            {"id": "a", "text": "Friend — es amable y accesible."},
            {"id": "b", "text": "Guide — comparte información pero pide algo a cambio."},
            {"id": "c", "text": "Skeptic — cuestiona, pide evidencia, evalúa críticamente. Cuando se convence, empuja fuerte. Es Mobilizer."},
            {"id": "d", "text": "Blocker — se opone al cambio."},
        ],
        "correct": "c",
        "explanation": (
            "Señales Skeptic: cuestiona antes de avanzar, pide data específica (3 casos + métrica concreta), "
            "menciona comité interno (va a empujar si se convence), tiene criterio propio. "
            "Es uno de los 3 Mobilizers del Challenger Customer. "
            "Muchos SDRs interpretan \"pide data antes de avanzar\" como obstáculo — en realidad "
            "es la señal más clara de Mobilizer."
        ),
    },
    {
        "id": "M2.7",
        "topic": "Frenos del decisor B2B",
        "section": "sem4",
        "type": "single",
        "prompt": (
            "Una CFO responde a una propuesta con:\n\n"
            "\"La propuesta se ve bien, los números cierran. Pero cambiar de proveedor implica 3 meses "
            "de implementación, coordinar con IT, entrenar a 40 personas, y si algo sale mal me lo cargan "
            "a mí delante del directorio. Hoy tenemos algo que funciona medianamente — prefiero eso a arriesgar.\"\n\n"
            "¿Qué freno del decisor B2B está dominando esta respuesta?"
        ),
        "choices": [
            {"id": "a", "text": "Fatiga de proveedores — recibe muchas propuestas."},
            {"id": "b", "text": "Costo de cambio + miedo al error público (combinación dominante)."},
            {"id": "c", "text": "Falta de presupuesto."},
            {"id": "d", "text": "Desconocimiento del producto."},
        ],
        "correct": "b",
        "explanation": (
            "Dos frenos operando juntos: costo de cambio (\"3 meses, coordinar con IT, entrenar 40 personas\") "
            "+ miedo al error público (\"me lo cargan a mí delante del directorio\"). La combinación es la "
            "que paraliza. Insistir con el ROI no sirve. Lo que podría desbloquear: un caso con plan "
            "de implementación explícito que minimice el riesgo percibido (ej. piloto de 30 días)."
        ),
    },
    {
        "id": "M2.8",
        "topic": "Timing signals reales vs ruido",
        "section": "sem4",
        "type": "multi",
        "prompt": (
            "Un SDR hace research de una empresa potencial y encuentra los siguientes hallazgos. "
            "Marcá todos los que son señales reales de timing:"
        ),
        "choices": [
            {"id": "1", "text": "La empresa contrató un nuevo CMO hace 40 días (primero promoción externa, no interna)."},
            {"id": "2", "text": "El CEO subió una foto del equipo en un offsite corporativo."},
            {"id": "3", "text": "Publicaron 25 ofertas de trabajo para ingeniería + 8 para ventas en las últimas 3 semanas."},
            {"id": "4", "text": "Ganaron un premio de \"Mejor Employer Branding 2026\"."},
            {"id": "5", "text": "Anunciaron expansión de operaciones a Brasil + Colombia para 2026 Q3."},
            {"id": "6", "text": "El Director de Tecnología publicó un post diciendo que \"este año es clave para modernizar nuestro stack\"."},
            {"id": "7", "text": "La competencia directa de la empresa despidió 150 personas."},
            {"id": "8", "text": "Cerraron ronda Serie D por USD 50M la semana pasada."},
        ],
        "correct": ["1", "3", "5", "6", "8"],
        "explanation": (
            "Señales operativas: 1 (nuevo CMO externo → ventana 90-100 días), 3 (28 ofertas → maquinaria comercial escala), "
            "5 (expansión multi-país → necesidades operativas), 6 (declaración explícita del Director de Tecnología), "
            "8 (Serie D → capital + crecimiento). Ruido: 2 (social), 4 (clima interno), 7 (afecta al competidor, no al prospecto)."
        ),
    },
    {
        "id": "M2.9",
        "topic": "No listo vs no fit",
        "section": "sem4",
        "type": "single",
        "prompt": (
            "Un prospecto responde al cold email:\n\n"
            "\"Interesante la propuesta. Te voy a ser franco: nuestro presupuesto de tecnología para "
            "todo el año ya está comprometido con otras prioridades. Pero yo estoy armando el plan del "
            "próximo año entre septiembre y octubre, y el tema que planteás está en mi radar como algo "
            "a considerar. ¿Podés escribirme de nuevo a fines de agosto?\"\n\n"
            "¿Cómo clasificarías este caso?"
        ),
        "choices": [
            {"id": "a", "text": "No fit — no tiene presupuesto."},
            {"id": "b", "text": "No listo con trigger específico (contactar en agosto para planning de Q4/Q1 siguiente). Archivar con fecha."},
            {"id": "c", "text": "Frío — respuesta de cortesía."},
            {"id": "d", "text": "Listo — mencionó que está en su radar."},
        ],
        "correct": "b",
        "explanation": (
            "3 señales claras de \"no listo\" con trigger: (1) bloqueador temporal (presupuesto comprometido); "
            "(2) apertura genuina (\"está en mi radar\"); (3) trigger concreto (\"escribime a fines de agosto\"). "
            "\"No tiene presupuesto ahora\" ≠ \"no va a tener nunca\". El prospecto dio fecha específica — no es cortesía."
        ),
    },
    {
        "id": "M2.10",
        "topic": "Mapeo dolor-solución mal hecho",
        "section": "sem3",
        "type": "single",
        "prompt": (
            "Un SDR que vende plataforma de gestión de ventas B2B escribe este email a un VP de Ventas "
            "de una empresa de servicios financieros:\n\n"
            "\"Hola Ricardo, vi que tu empresa está creciendo. Nuestra plataforma ayuda a equipos de "
            "ventas como el tuyo a optimizar su pipeline y cerrar más deals. Hemos ayudado a empresas "
            "similares a aumentar su conversión en un 30%. ¿Tenés 20 minutos esta semana para ver "
            "cómo podemos ayudar a tu empresa?\"\n\n"
            "¿Qué le falta a este mapeo dolor-solución?"
        ),
        "choices": [
            {"id": "a", "text": "Le falta la fuente del 30% — debería citar de dónde viene el dato."},
            {"id": "b", "text": "Todo lo necesario: señal específica del prospecto + conexión con dolor contextual + propuesta sin prometer + pregunta validadora. El email habla de \"crecer\", \"equipos como el tuyo\", \"empresas similares\" — todo genérico. No hay mapeo; hay producto."},
            {"id": "c", "text": "El CTA — 20 minutos es mucho."},
            {"id": "d", "text": "El saludo debería ser más formal."},
        ],
        "correct": "b",
        "explanation": (
            "Un mapeo bien hecho tiene 3 elementos: dolor específico, impacto cuantificado, conexión "
            "con oferta sin prometer. Este email tiene dolor genérico (\"crecer\"), impacto sin fuente "
            "(\"30%\"), conexión vaga (\"ayudar a tu empresa\"). Es producto con CTA, no mapeo. "
            "La fuente ayudaría pero el problema es estructural, no de cita."
        ),
    },
    {
        "id": "M2.11",
        "topic": "Error #1 del SDR nuevo",
        "section": "sem3",
        "type": "single",
        "prompt": (
            "Un SDR junior recibe feedback del manager:\n\n"
            "\"Tus cold emails están explicando bien lo que hace nuestro producto. Pero están "
            "convirtiendo al 0.4%. El benchmark del equipo está en 1.8%.\"\n\n"
            "¿Cuál es el error más probable que está cometiendo el SDR?"
        ),
        "choices": [
            {"id": "a", "text": "Los emails son muy largos."},
            {"id": "b", "text": "El SDR está vendiendo la solución sin haber entendido el problema del prospecto — escribe desde el producto, no desde el dolor. Error #1 del SDR nuevo (Sem 3 Bloque 7)."},
            {"id": "c", "text": "El SDR no está haciendo enough volume."},
            {"id": "d", "text": "El producto no tiene buen fit con el mercado."},
        ],
        "correct": "b",
        "explanation": (
            "\"Explicando bien lo que hace nuestro producto\" es exactamente el síntoma del error #1. "
            "La conversión baja (0.4% vs 1.8% benchmark) confirma que el problema no es ejecución sino enfoque. "
            "El feedback es sobre conversión, no volumen. El producto sí convierte con otros SDRs (1.8%), "
            "así que el problema es este SDR específico."
        ),
    },
    {
        "id": "M2.12",
        "topic": "Motivador del decisor",
        "section": "sem4",
        "type": "single",
        "prompt": (
            "Un VP de Ventas (recién ascendido hace 4 meses) responde a un cold email con:\n\n"
            "\"Me interesa entender cómo otras empresas similares han medido impacto después de "
            "implementar esto. Necesito poder presentar un caso concreto al CEO en mi primer review "
            "del próximo trimestre. Si hay métricas claras y timeline realista, tiene chance.\"\n\n"
            "¿Cuál es el motor principal que está moviendo la decisión?"
        ),
        "choices": [
            {"id": "a", "text": "Resultados medibles en abstracto."},
            {"id": "b", "text": "Avance de carrera — el VP recién ascendido necesita proyectos visibles que muestren impacto en su primer review."},
            {"id": "c", "text": "Evitar riesgo."},
            {"id": "d", "text": "Status interno."},
        ],
        "correct": "b",
        "explanation": (
            "El VP dice literalmente \"mi primer review del próximo trimestre\" — oportunidad de "
            "demostrar que el ascenso fue acertado. Proyecto exitoso = carrera asegurada; proyecto "
            "fallido = riesgo de salida. Los otros motores están presentes pero son secundarios. "
            "Implicación: mandarle caso con métricas + timeline que él pueda usar en su review."
        ),
    },
    {
        "id": "M2.13",
        "topic": "Encadenada parte 1 — lectura integrada",
        "section": "sem3",
        "type": "single",
        "prompt": (
            "Empresa: AgroExport Argentina (exportadora de commodities agrícolas, 400 empleados, "
            "operación en Argentina, con planes de expansión a Brasil anunciados para 2026 Q4).\n"
            "Contacto potencial: Camilo Díaz — Gerente de Logística. LinkedIn muestra 3 años en el "
            "cargo. Un post reciente: \"Este Q4 nos complica el volumen, las rutas actuales no escalan.\"\n\n"
            "¿Cuál es la hipótesis de dolor más probable que el SDR podría usar como gancho?"
        ),
        "choices": [
            {"id": "a", "text": "El crecimiento de la empresa le genera estrés al equipo."},
            {"id": "b", "text": "Con la expansión anunciada a Brasil + el comentario público sobre que las rutas \"no escalan\", el dolor probable es la necesidad de rediseñar la operación logística para absorber volumen multi-país antes del Q4 2026 sin que los costos se disparen."},
            {"id": "c", "text": "El costo de exportación de commodities está subiendo."},
            {"id": "d", "text": "Los empleados están sobrecargados de trabajo."},
        ],
        "correct": "b",
        "explanation": (
            "Combina 2 señales específicas (expansión anunciada con fecha + queja pública del contacto) "
            "con un contexto operativo real (escalar logística multi-país es caro y complicado). "
            "Las otras opciones son generalidades o derivadas."
        ),
    },
    {
        "id": "M2.14",
        "topic": "Encadenada parte 2 — escritura del gancho",
        "section": "sem4",
        "type": "single",
        "prompt": (
            "Continuación de la pregunta anterior (AgroExport Argentina + Camilo Díaz). "
            "El SDR quiere escribir el gancho del cold email.\n\n"
            "¿Cuál de estos ganchos es el más efectivo para Camilo?"
        ),
        "choices": [
            {"id": "a", "text": "\"Hola Camilo, vi que AgroExport está creciendo. Nuestra plataforma optimiza logística. ¿Tenés 20 minutos?\""},
            {"id": "b", "text": "\"Hola Camilo, vi tu post sobre rutas que no escalan + el anuncio de expansión a Brasil para Q4. En exportadoras con crecimiento multi-país vemos que el mayor costo oculto aparece en los primeros 6 meses — rutas armadas sobre supuestos del mercado original que no funcionan en el nuevo. ¿Les está pasando algo así o tienen mapeado cómo calibrar?\""},
            {"id": "c", "text": "\"Hola Camilo, tenemos 30 años de experiencia en logística internacional. Trabajamos con empresas como Cargill y Bunge. ¿Coordinamos una llamada?\""},
            {"id": "d", "text": "\"Hola Camilo, el crecimiento de AgroExport es impresionante. Nos gustaría ayudar.\""},
        ],
        "correct": "b",
        "explanation": (
            "Señal específica (post + expansión verificables) + conexión al dolor (\"costo oculto de los primeros 6 meses\") + "
            "no promete (ofrece una pregunta) + un solo CTA. (a) genérico, (c) prueba social desajustada "
            "(Cargill y Bunge vs AgroExport de 400 empleados), (d) halago vacío. "
            "La encadenada P13→P14 prueba que el alumno traduce el dolor a gancho bien estructurado."
        ),
    },
    {
        "id": "M2.15",
        "topic": "Mobilizer en el primer email",
        "section": "sem4",
        "type": "single",
        "prompt": (
            "Un SDR escribe el primer email a una empresa B2B prospecto. Dentro de la empresa hay "
            "4 contactos potenciales:\n"
            "● Pablo (CEO) — C-level, pero no suele responder cold emails según su LinkedIn.\n"
            "● Mirta (Directora de Operaciones) — escribe posts frecuentes sobre operaciones, "
            "comparte artículos de industria.\n"
            "● Juan (Gerente de Proyectos) — LinkedIn con pocos posts, actividad limitada.\n"
            "● Cecilia (VP de Finanzas) — sus posts son principalmente de \"buenas vibras\" y citas motivacionales.\n\n"
            "¿A cuál contactar primero para maximizar probabilidad de Mobilizer (Teacher específicamente)?"
        ),
        "choices": [
            {"id": "a", "text": "Pablo — como C-level tiene más peso en la decisión."},
            {"id": "b", "text": "Mirta — escribe y comparte artículos de industria (patrón de Teacher)."},
            {"id": "c", "text": "Juan — como Gerente es decisor operativo."},
            {"id": "d", "text": "Cecilia — su actividad en LinkedIn muestra que es accesible."},
        ],
        "correct": "b",
        "explanation": (
            "\"Escribir posts + compartir artículos de industria\" es la señal conductual más clara de "
            "Teacher (uno de los 3 Mobilizers). Jerarquía ≠ arquetipo. Rol ≠ arquetipo. "
            "Posts de \"buenas vibras\" son señal de Friend (accesible pero no empujador)."
        ),
    },
    {
        "id": "M2.16",
        "topic": "Integradora final — sistema completo",
        "section": "sem4",
        "type": "single",
        "prompt": (
            "Una SDR senior le explica a una junior:\n\n"
            "\"Lo que aprendí en 2 años es esto: antes de escribir un email, paso por 3 filtros mentales. "
            "Primero, el filtro del negocio: ¿entiendo cómo gana plata esta empresa, qué la hace crecer, "
            "qué la frena? Si no puedo contestar eso en 30 segundos, todavía no estoy listo para escribir. "
            "Segundo, el filtro del comprador: ¿la persona a la que le voy a escribir es Mobilizer o Talker? "
            "Si no lo sé, mejor busco señales antes. Tercero, el filtro del timing: ¿hay alguna señal "
            "concreta y reciente que me permita construir un gancho específico? Si no, la empresa no "
            "está lista para el cold email hoy.\"\n\n"
            "Esta reflexión integra principios de qué bloques del Módulo 2?"
        ),
        "choices": [
            {"id": "a", "text": "Solo del Bloque 5 de Sem 4 (señales de timing)."},
            {"id": "b", "text": "Solo del Bloque 7 de Sem 3 (error #1 del SDR nuevo)."},
            {"id": "c", "text": "Integra múltiples bloques: business acumen como primer filtro (Sem 3, Bloques 2-5), Challenger Customer como segundo filtro (Sem 4, Bloque 2), y timing signals como tercer filtro (Sem 4, Bloque 5). La reflexión muestra cómo los tres operan juntos para evitar el error #1 (Sem 3, Bloque 7)."},
            {"id": "d", "text": "Es filosofía general, no integra bloques específicos."},
        ],
        "correct": "c",
        "explanation": (
            "La reflexión conecta múltiples fundamentos en una narrativa coherente: "
            "\"cómo gana plata\" (BMC), \"qué la hace crecer/frena\" (unit economics + Porter), "
            "\"dolor estructural\" (JTBD + mapeo), \"Mobilizer vs Talker\" (Challenger Customer), "
            "\"señal concreta\" (timing signals), \"emails que no cierran\" = evitar el error #1. "
            "Un alumno que identifica esta integración demuestra que el módulo quedó como sistema."
        ),
    },
]


VIDEO_CASES: list[dict] = [
    {
        "id": "case_a",
        "title": "Aplicar BMC + 5 fuerzas de Porter a Mercado Libre Argentina",
        "scenario": (
            "Mercado Libre Argentina está anunciado como cuenta ICP para un cliente que vende "
            "software de optimización de logística. Tu AE te pide armar un brief conceptual de 5 min "
            "antes de la reunión.\n\n"
            "Lo que el alumno debe producir en el video:\n"
            "1. BMC de Mercado Libre Argentina en los 9 componentes (puede enfocarse en el negocio "
            "de e-commerce marketplace, no en Mercado Pago).\n"
            "2. 5 fuerzas de Porter aplicadas a la industria e-commerce en LATAM — identificar las 2 "
            "fuerzas más disruptivas hoy.\n"
            "3. A partir de los dos análisis, proponer el dolor estructural probable que el software "
            "de optimización logística podría atacar."
        ),
        "expected_key_point": (
            "Rivalidad intensa (Amazon, Shein, Temu) + poder creciente del comprador (múltiples "
            "alternativas + comparadores) son las 2 fuerzas más disruptivas. El dolor específico "
            "atacable: eficiencia de última milla + costo variable por envío."
        ),
        "expected_concepts": [
            "BMC en los 9 componentes",
            "5 fuerzas de Porter — distinción de fuerzas dominantes",
            "mapeo dolor-solución estructural",
        ],
        "expected_decision": (
            "Brief que conecta análisis estructural con dolor accionable: optimización de última milla "
            "y costo variable por envío como hipótesis a validar en la reunión con el AE."
        ),
    },
    {
        "id": "case_b",
        "title": "Identificar arquetipos del Challenger Customer en un comité de 6 personas",
        "scenario": (
            "Se muestran 6 respuestas de personas distintas de la misma empresa:\n\n"
            "1) VP Operaciones: \"Estoy cansado de proveedores que prometen y no cumplen. Si no tenés "
            "casos de estudio auditados con métricas claras, no sigo.\"\n"
            "2) Gerente de Proyectos: \"Qué interesante tu propuesta. Encantado de conversar. Decime "
            "cuándo te viene bien.\"\n"
            "3) Director Comercial: \"Leí el paper que me compartiste, me pareció brillante. Se lo pasé "
            "al comité ejecutivo para que lo discutamos en la próxima reunión — esto puede ser parte del plan Q3.\"\n"
            "4) Analista senior: \"Te puedo dar información sobre cómo funciona internamente... pero "
            "necesito saber si vamos a poder incluir mi equipo en el piloto. Hablamos?\"\n"
            "5) Coordinador: \"Mirá, si esto me ayuda a ser visible ante el CEO, estoy dentro. Ayudame a "
            "presentarlo con mi nombre en el brief.\"\n"
            "6) Director de Tecnología: \"No creo que sea el momento. Tenemos otras prioridades.\"\n\n"
            "Lo que el alumno debe producir:\n"
            "1. Identificar el arquetipo (1-7 del Challenger Customer) de cada contacto.\n"
            "2. Separar Mobilizers vs Talkers.\n"
            "3. Proponer estrategia: con quién profundizar, quién neutralizar, quién usar como referidor."
        ),
        "expected_key_point": (
            "Identifica correctamente: 1=Skeptic, 2=Friend, 3=Teacher, 4=Guide, 5=Climber, 6=Blocker. "
            "Mobilizers: 1 y 3. Talkers: 2, 4, 5, 6."
        ),
        "expected_concepts": [
            "7 arquetipos del Challenger Customer",
            "Mobilizers vs Talkers",
            "estrategia de stakeholder mapping",
        ],
        "expected_decision": (
            "Profundizar con #1 (Skeptic — empuja cuando se convence) y #3 (Teacher — evangeliza "
            "internamente). Usar #4 como fuente de info. No pelear con #6."
        ),
    },
    {
        "id": "case_c",
        "title": "Reescribir cold email genérico a Marina de Ualá",
        "scenario": (
            "Un SDR escribió este cold email:\n\n"
            "\"Hola Marina, vi que tu empresa está creciendo rápido. Nuestra plataforma ayuda a empresas "
            "B2B a mejorar su pipeline de ventas y alcanzar resultados increíbles. Trabajamos con clientes "
            "como Globant y Mercado Libre. ¿Tenés 20 minutos esta semana para ver si podemos ayudar?\"\n\n"
            "Contexto adicional que el SDR tiene pero no usó:\n"
            "● Empresa de Marina: Ualá Argentina (neobanco, cerró Serie D hace 3 meses por USD 350M, "
            "anunció expansión a México y Colombia).\n"
            "● Rol de Marina: VP de Growth.\n"
            "● Post reciente de Marina en LinkedIn: \"El desafío más caro de expandir a 3 países a la "
            "vez: mantener CAC estable mientras el canal local aún no está maduro.\"\n\n"
            "Lo que el alumno debe producir en el video:\n"
            "1. Diagnosticar por qué el email es un mapeo dolor-solución mal hecho.\n"
            "2. Reescribir el email aplicando el contexto disponible + principios de Sem 3 y Sem 4.\n"
            "3. Justificar cada cambio con el concepto del curso que lo fundamenta."
        ),
        "expected_key_point": (
            "El email es producto genérico sin señal específica — el SDR ignoró la Serie D, la expansión "
            "tri-país y el post de Marina. Es el Error #1 del SDR nuevo + mapeo dolor-solución mal hecho + "
            "prueba social desajustada (Globant/MeLi son gigantes, no comparables a Ualá del tamaño actual)."
        ),
        "expected_concepts": [
            "Error #1 del SDR nuevo (Sem 3 Bloque 7)",
            "mapeo dolor-solución (Sem 3 Bloque 6)",
            "gancho específico (Sem 4 Bloque 5)",
            "prueba social ajustada al tamaño/contexto",
        ],
        "expected_decision": (
            "Reescribir con gancho específico (\"vi tu post sobre CAC en expansión tri-país + anuncio "
            "Ualá a México y Colombia\"), dolor contextual (CAC distorsionado en mercados nuevos), "
            "conexión sin prometer, un solo CTA."
        ),
    },
    {
        "id": "case_d",
        "title": "Clasificar 10 respuestas a cold email (no listo / no fit / bloqueador / qualified)",
        "scenario": (
            "Un SDR tiene 10 respuestas a cold emails esta semana. El ICP definido es \"empresas B2B "
            "SaaS LATAM, 150-500 empleados, con foco en marketing automation\". Las 10 respuestas:\n\n"
            "1) SoftPlay Perú (120 empleados, SaaS B2C gaming), CTO: \"Interesante, agendemos.\"\n"
            "2) GrowthLab Chile (300 empleados, SaaS B2B), VP Marketing: \"Me interesa. Tengo board "
            "meeting en 6 semanas, después de eso te retomo.\"\n"
            "3) DataFlow Colombia (400 empleados, SaaS B2B), CEO: \"Estamos en proceso de venta de la "
            "empresa a un fondo. Probablemente operación cierra en 4 meses.\"\n"
            "4) CloudRise Argentina (280 empleados, SaaS B2B), CMO: \"Ya firmamos contrato con "
            "[competidor directo] el mes pasado. 2 años de compromiso.\"\n"
            "5) PayStack LATAM (180 empleados, fintech), VP Growth: \"Interesante pero no es prioridad "
            "este año ni el que viene. Nuestra estrategia es consolidar sin sumar herramientas.\"\n"
            "6) ConsultorQ Uruguay (400 empleados, consultoría), CFO: \"Sáqueme de su lista por favor y "
            "no me contacte más.\"\n"
            "7) MetaEdu México (220 empleados, SaaS B2B edtech), CMO: \"Tengo interés. Estamos "
            "justamente evaluando herramientas, 3 opciones activas. ¿Podés mandarme deck?\"\n"
            "8) LogiSmart Perú (90 empleados, SaaS B2B logística), COO: \"Me interesa, pero somos chicos. "
            "¿Tenés descuento para empresas menores?\"\n"
            "9) HealthCore Chile (450 empleados, SaaS B2B salud), Gerente de Marketing: \"Hablé con "
            "nuestro VP de Marketing, está interesada en conocer más. Te paso su contacto: maria@...\"\n"
            "10) PagosGlobal Brasil (600 empleados, fintech), CFO: \"No somos ICP de ustedes — sólo "
            "operamos en Brasil en portugués.\"\n\n"
            "Lo que el alumno debe producir:\n"
            "1. Clasificar cada respuesta en una de: qualified / no listo con trigger / no fit / do not contact.\n"
            "2. Para los \"no listo\": especificar fecha de recontacto.\n"
            "3. Identificar patrones si el SDR está cometiendo errores de segmentación."
        ),
        "expected_key_point": (
            "Clasificación esperada: 1=no fit (B2C), 2=no listo (7 sem), 3=no listo (6-12 meses), "
            "4=no listo (22-24 meses pre-vencimiento), 5=no fit (declaración estructural), "
            "6=do not contact, 7=qualified, 8=no fit (tamaño), 9=qualified (referido válido), "
            "10=no fit geográfico/idioma. Patrón: varios fuera del ICP (1, 8, 10) → problema de segmentación aguas arriba."
        ),
        "expected_concepts": [
            "no listo con trigger vs no fit estructural",
            "do not contact",
            "patrón de error de segmentación en filtros de prospección",
        ],
        "expected_decision": (
            "Avanzar con 7 y 9. Archivar 2, 3, 4 con triggers de fecha. Descartar 1, 5, 6, 8, 10. "
            "Recomendar revisar filtros de Apollo aguas arriba — varios casos fuera de ICP indican "
            "problema de segmentación, no de copy."
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
                {"score": 2, "descriptor": "Usa vocabulario específico (BMC, 5 fuerzas, JTBD, Mobilizer, Skeptic, no listo/no fit, etc.) correctamente aplicado al caso."},
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
