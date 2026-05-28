"""Contenido Capa 2 — Prueba del Módulo 1 (El juego y el jugador).

Fuente: SDR_Academy_Siete_Documento_Maestro.md, Parte IV §Prueba del Módulo 1, v0.1.

Estructura:
- MCQ: 16 preguntas (Sem 1 + Sem 2 del Módulo 1). 70% del peso de la prueba.
- VIDEO_CASES: 4 casos de banco para video narrado (1 asignado al azar). 30% del peso.
- VIDEO_RUBRIC: 3 criterios × 0-2 puntos → /6 → conversión a %.

Nota: el campo `correct` y `explanation` es solo para el grader/profesor; el
front pública (al alumno) recibe el shape sin ellos.
"""

MCQ: list[dict] = [
    {
        "id": "M1.1",
        "topic": "Diferencia estructural B2B vs B2C",
        "section": "sem1",
        "type": "single",
        "prompt": (
            "Tomás trabaja como SDR vendiendo una plataforma de gestión de "
            "contratos B2B (SaaS) a empresas medianas. Su amigo Matías vende "
            "televisores inteligentes en una retail chain (B2C).\n\n"
            "Tomás: \"Hoy me pasó algo rarísimo. Después de 4 meses de ida y "
            "vuelta con una empresa, la directora me dijo que tiene el contrato "
            "listo, pero no lo puede firmar hasta que pase el board meeting de "
            "abril. Dice que necesita 'legitimar la decisión' con el directorio.\"\n"
            "Matías: \"Qué raro. Yo ayer vendí un TV de USD 3.000 en 20 minutos "
            "— llegó la clienta, preguntó 3 cosas, pagó con tarjeta, se lo llevó.\"\n\n"
            "¿Cuál es la diferencia estructural más importante entre los dos casos?"
        ),
        "choices": [
            {"id": "a", "text": "El precio — USD 3.000 del TV vs un contrato de varios miles de USD/mes en SaaS."},
            {"id": "b", "text": "La cantidad de gente involucrada en la decisión. La clienta de Matías decide sola; la directora de Tomás necesita consenso/legitimación del directorio aunque técnicamente tenga autoridad de firma."},
            {"id": "c", "text": "El tipo de producto — físico vs digital."},
            {"id": "d", "text": "La cantidad de tiempo que duró el ciclo."},
        ],
        "correct": "b",
        "explanation": (
            "La diferencia central B2B vs B2C no es precio, producto ni duración — es que en B2B rara vez decide una sola persona. "
            "La directora tiene autoridad técnica pero opera en un sistema de consenso. La duración es consecuencia, no causa."
        ),
    },
    {
        "id": "M1.2",
        "topic": "Racionalidad aparente + emocionalidad real",
        "section": "sem1",
        "type": "single",
        "prompt": (
            "Un CFO recibe 2 propuestas de CRM (A y B) y comparte estas observaciones "
            "con su equipo:\n\n"
            "\"Propuesta A: tiene todo lo que necesitamos técnicamente. ROI calculado "
            "2.1x a 3 años. Proveedor mediano, con referencias sólidas en nuestra "
            "industria. Propuesta B: cumple requerimientos técnicos. ROI similar "
            "(2.0x). Proveedor grande reconocido. Precio 15% más alto. Voy con B. "
            "Si algo sale mal con A, el directorio me va a preguntar por qué no fui "
            "con la opción 'segura'. Con B, si sale mal, nadie me va a cuestionar.\"\n\n"
            "¿Qué está haciendo el CFO?"
        ),
        "choices": [
            {"id": "a", "text": "Una decisión racional basada en ROI — B tiene mejor reputación de marca."},
            {"id": "b", "text": "Una decisión donde el factor emocional (miedo al error público, riesgo de carrera) pesó más que el factor técnico/económico, y después se justificará como técnica. \"Sistema 1 decide, Sistema 2 justifica\" aplicado a compra B2B."},
            {"id": "c", "text": "Una decisión política — el CFO tiene relación personal con el proveedor B."},
            {"id": "d", "text": "Una mala decisión comercial — A era claramente mejor por ROI."},
        ],
        "correct": "b",
        "explanation": (
            "El CFO lo dice literalmente: eligió B por protección de carrera. Caso textbook de Kahneman aplicado a compra B2B. "
            "Un SDR que entiende esto vende prueba social (\"misma decisión que [Banco conocido]\"), no \"2.5x ROI garantizado\"."
        ),
    },
    {
        "id": "M1.3",
        "topic": "Etapa del buying cycle",
        "section": "sem1",
        "type": "single",
        "prompt": (
            "Respuesta a un cold email:\n\n"
            "\"Gracias por escribir. La verdad es que hace unos meses empezamos a "
            "sentir que el tema que mencionás [gestión de pipeline comercial] se nos "
            "está quedando corto con nuestras herramientas actuales. Empecé a "
            "investigar alternativas el mes pasado. Estamos mirando 3 opciones en "
            "papel, todavía no pedimos demos formales. ¿Podés mandarme un overview "
            "para que los sume a la shortlist?\"\n\n"
            "¿En qué etapa del buying cycle está este prospecto?"
        ),
        "choices": [
            {"id": "a", "text": "Awareness — recién toma conciencia del problema."},
            {"id": "b", "text": "Consideración — reconoce el problema y explora soluciones sin evaluar formalmente."},
            {"id": "c", "text": "Evaluación activa — está pidiendo demos y armando comparativos formales."},
            {"id": "d", "text": "Decisión — va a elegir un proveedor."},
        ],
        "correct": "b",
        "explanation": (
            "Reconoce dolor (\"se está quedando corto\"), explora en papel (\"3 opciones\"), pero NO pidió demos formales. "
            "Implicación SDR: mandar overview para shortlist es correcto; agendar demo de 1h sería prematuro."
        ),
    },
    {
        "id": "M1.4",
        "topic": "Pareo de roles en comité de compra",
        "section": "sem1",
        "type": "match",
        "prompt": (
            "En una empresa de 220 empleados están evaluando software de gestión "
            "de logística interna. Apareá cada persona con su rol en el comité "
            "de compra:\n\n"
            "1. Ramiro — Director de Compras. Entra al final para negociar precio, SLAs y cláusulas.\n"
            "2. Ana — Coordinadora de Logística. No firma, pero odia el sistema actual, trajo el tema al COO y te conectó.\n"
            "3. Sofía — COO. Tiene presupuesto propio, firma la PO, reporta al CEO.\n"
            "4. Gabriel — VP de Operaciones (otra área). No evalúa pero su opinión pesa porque también usa sistemas integrados.\n"
            "5. Lucía — Directora de IT. Puede vetar si no hay integración con el ERP corporativo.\n"
            "6. Carlos — Gerente de TI viejo que firmó con el proveedor actual hace 3 años. Se opone al cambio."
        ),
        "left": [
            {"id": "1", "text": "Ramiro (Compras, entra al final)"},
            {"id": "2", "text": "Ana (Coord. Logística, trajo el tema, conectó)"},
            {"id": "3", "text": "Sofía (COO, presupuesto y firma)"},
            {"id": "4", "text": "Gabriel (VP otra área, opinión pesa)"},
            {"id": "5", "text": "Lucía (Dir. IT, puede vetar por integración)"},
            {"id": "6", "text": "Carlos (Gerente TI, se opone al cambio)"},
        ],
        "right": [
            {"id": "A", "text": "Decisor económico"},
            {"id": "B", "text": "Decisor técnico (puede vetar)"},
            {"id": "C", "text": "Coach / champion + referidor"},
            {"id": "D", "text": "Influenciador"},
            {"id": "E", "text": "Bloqueador"},
            {"id": "F", "text": "Compras / procurement"},
        ],
        "correct": {"1": "F", "2": "C", "3": "A", "4": "D", "5": "B", "6": "E"},
        "explanation": (
            "Distinción crítica: bloqueador (Carlos, se opone explícitamente) vs influenciador (Gabriel, opina pero no se opone). "
            "Confundirlos quema la estrategia de prospección."
        ),
    },
    {
        "id": "M1.5",
        "topic": "Lifecycle prospecto vs cliente",
        "section": "sem1",
        "type": "single",
        "prompt": (
            "En reunión interna un nuevo SDR dice:\n\n"
            "\"Tenemos un prospecto de nuestro cliente Acme que ya está en la "
            "etapa de Renewal. Creo que deberíamos pasar a Customer Success "
            "para que lo manejen.\"\n\n"
            "¿Cuál es el problema con lo que dijo el SDR?"
        ),
        "choices": [
            {"id": "a", "text": "\"Renewal\" no es etapa del lifecycle del prospecto — es del lifecycle del cliente ya firmado (post-venta, gestionado por CS). Un prospecto no puede estar en renewal. Confundió ambos lifecycles."},
            {"id": "b", "text": "El problema es que dijo \"prospecto\" en vez de \"lead\"."},
            {"id": "c", "text": "Debería decir \"renovación\" en español, no \"renewal\"."},
            {"id": "d", "text": "No hay problema — el razonamiento es correcto."},
        ],
        "correct": "a",
        "explanation": (
            "Dos lifecycles distintos: prospecto (Prospect → MQL → SQL → Opportunity → Customer) vs cliente firmado "
            "(Onboarding → Use → Engage → Adopt → Optimize → Renew → Advocate). Renewal pertenece al segundo."
        ),
    },
    {
        "id": "M1.6",
        "topic": "Quién paga vs quién usa",
        "section": "sem1",
        "type": "single",
        "prompt": (
            "Una SDR va a prospectar a una empresa de 500 empleados para vender "
            "un software de productividad para equipos de marketing. La herramienta "
            "la usaría marketing (10 personas) pero el presupuesto de tecnología "
            "es centralizado (lo aprueba Finanzas Corporativa).\n\n"
            "¿Cuál es el mejor approach para esta prospección?"
        ),
        "choices": [
            {"id": "a", "text": "Contactar solo al CMO (jefe de marketing) porque es el que \"quiere\" la herramienta."},
            {"id": "b", "text": "Contactar solo al CFO (finanzas) porque es quien aprueba el presupuesto."},
            {"id": "c", "text": "Identificar las 3 capas temprano (usuario, decisor económico, decisor técnico). Contactar primero al champion potencial entre usuarios o marketing (que traiga el tema), y en paralelo mapear al decisor económico."},
            {"id": "d", "text": "Contactar simultáneamente a las 3 capas con el mismo mensaje."},
        ],
        "correct": "c",
        "explanation": (
            "Quien paga / quien usa / quien aprueba técnicamente son 3 personas distintas. "
            "Contactar solo CMO: champion sin decisor económico → deal estancado. Solo CFO: sin contexto operativo. "
            "Los 3 al mismo tiempo: viola \"a cada rol le hablás distinto\" + satura."
        ),
    },
    {
        "id": "M1.7",
        "topic": "Canales de demanda",
        "section": "sem2",
        "type": "multi",
        "prompt": (
            "Una empresa SaaS B2B: ICP muy concentrado (30-50 empresas a nivel "
            "LATAM), deals de ticket alto (USD 100K+ anuales), ciclo de 12-18 meses.\n\n"
            "¿Qué canales aplican mejor? (marcá todos los que correspondan)"
        ),
        "choices": [
            {"id": "1", "text": "Inbound masivo (SEO + ads + blog)"},
            {"id": "2", "text": "ABM (Account-Based Marketing)"},
            {"id": "3", "text": "Outbound hiper-personalizado"},
            {"id": "4", "text": "Partnerships con consultoras del segmento"},
            {"id": "5", "text": "Referidos trabajados sistemáticamente"},
        ],
        "correct": ["2", "3", "4", "5"],
        "explanation": (
            "Con 30-50 cuentas objetivo, el enfoque no masivo es obligatorio. Inbound masivo genera volumen disperso — "
            "ruido que no aporta. ABM/outbound personalizado/partnerships/referidos = profundidad sobre cuentas específicas."
        ),
    },
    {
        "id": "M1.8",
        "topic": "Cuándo outbound NO aplica",
        "section": "sem2",
        "type": "single",
        "prompt": (
            "Una empresa vende una herramienta de productividad personal por USD "
            "15/mes, dirigida a \"cualquier profesional digital que trabaje con "
            "muchas tareas\". El fundador considera armar un equipo de SDRs para "
            "hacer outbound.\n\n"
            "¿Por qué outbound NO tiene sentido para este caso?"
        ),
        "choices": [
            {"id": "a", "text": "El producto está mal diseñado."},
            {"id": "b", "text": "No se cumplen 2 de las 3 condiciones para outbound B2B: (1) ICP no está identificable ni alcanzable — \"cualquier profesional digital\" no es ICP, y (2) el ticket (USD 15/mes) no justifica el costo de un SDR. Inbound o PLG son caminos más apropiados."},
            {"id": "c", "text": "Porque es B2C, no B2B."},
            {"id": "d", "text": "Porque es un producto nuevo y primero hay que hacer marketing de contenido."},
        ],
        "correct": "b",
        "explanation": (
            "Las 3 condiciones para outbound: ICP alcanzable, ticket justificable, ciclo manejable. "
            "USD 180/año vs SDR que cuesta miles/mes → necesitaría 100+ clientes nuevos/mes para recuperar costo. No cierran números."
        ),
    },
    {
        "id": "M1.9",
        "topic": "Cruce de hitos — caso \"facilitar contexto ligero\"",
        "section": "sem2",
        "type": "single",
        "prompt": (
            "Un SDR termina una cold call exitosa — logró agendar reunión para el "
            "jueves con el VP de Ingeniería. Al cerrar, el VP dice:\n\n"
            "\"Dale, agendado. Una cosa antes de colgar — ¿podés mandarme un caso "
            "de éxito con una empresa de software similar a la nuestra? Me viene "
            "bien llegar a la reunión con algo de contexto.\"\n\n"
            "¿Qué debería hacer el SDR?"
        ),
        "choices": [
            {"id": "a", "text": "Mandar inmediatamente 3 casos de éxito completos para que el VP llegue \"super preparado\"."},
            {"id": "b", "text": "Mandar 1 caso breve (3-4 párrafos) relevante al contexto que mencionó el VP, dejando espacio para que el AE profundice. No cruza hito — es facilitar contexto, no hacer el trabajo del AE."},
            {"id": "c", "text": "Responder \"los casos los presenta [AE] en la reunión\" y no mandar nada."},
            {"id": "d", "text": "Mandar un brochure completo del producto."},
        ],
        "correct": "b",
        "explanation": (
            "El matiz: el SDR puede facilitar contexto ligero, no puede reemplazar la demo del AE. "
            "3 casos completos = el VP llega diciendo \"ya vi los casos\" → AE pierde material. 1 caso breve = enriquece sin reemplazar."
        ),
    },
    {
        "id": "M1.10",
        "topic": "4 criterios de reunión calificada",
        "section": "sem2",
        "type": "single",
        "prompt": (
            "Un SDR reporta esta reunión al AE como \"calificada\":\n\n"
            "Empresa: BioLogic SA, laboratorio farmacéutico peruano de 180 empleados "
            "(el ICP es \"laboratorios farmacéuticos LATAM de 150-500 empleados\"). "
            "Cumple. Contacto: Carla Espinosa, Directora de Calidad. Llegó a la "
            "reunión. Confirmó que BioLogic tiene un proceso manual de tracking "
            "de lotes que \"genera errores mensualmente\", y que están \"viendo "
            "opciones\" aunque \"no hay urgencia\". Nota del SDR: \"Califica — "
            "cumple los 4 criterios.\"\n\n"
            "Aplicando los 4 criterios, ¿la reunión realmente califica?"
        ),
        "choices": [
            {"id": "a", "text": "Sí, cumple los 4 criterios."},
            {"id": "b", "text": "No, falta validar si Carla es KDM o champion. Directora de Calidad puede tener autoridad de compra para herramientas de su área, o puede depender del Director de Operaciones / CFO. El SDR no lo verificó."},
            {"id": "c", "text": "No, el problema es que el ICP es incorrecto."},
            {"id": "d", "text": "No, no cumple criterio 3 porque la reunión no se realizó efectivamente."},
        ],
        "correct": "b",
        "explanation": (
            "ICP ✓, Asiste ✓, Precalifica ⚠ débil pero pasa. Criterio 2 (KDM/champion) NO validado: "
            "el SDR dio por hecho rol = autoridad sin verificar. Aplicar los 4 criterios con rigor, no por inercia."
        ),
    },
    {
        "id": "M1.11",
        "topic": "Calidad del handoff",
        "section": "sem2",
        "type": "single",
        "prompt": (
            "Handoff del SDR al AE:\n\n"
            "\"Handoff — reunión lunes 10am: Empresa: TechGrow (SaaS B2B marketing "
            "automation), 320 empleados, oficinas en CDMX y BA. Contacto: Mariela "
            "Castro, VP de Marketing. La señal fue el anuncio de su ronda Serie B "
            "(USD 18M con Kaszek) de enero 2026. Gancho del cold email: 'en post-Serie "
            "B, lo que vemos es que el pipeline comercial no escala tan rápido como "
            "el headcount'. Mariela respondió que 'justamente estamos pasando por eso'. "
            "Precalificación: (1) Situación: equipo comercial pasó de 12 a 22 AEs en 4 "
            "meses, pipeline no creció al mismo ritmo. (2) Necesidad: necesitan 2x su "
            "pipeline en 60 días. (3) Timing: presupuesto 2026 asignado, buscan "
            "implementar en Q2. Otros stakeholders: Joaquín López (VP de Ventas) — "
            "también está en el tema, va a evaluar cualquier propuesta antes de "
            "decisión final. Advertencia: Mariela dijo 'ya hablamos con 2 proveedores "
            "similares el mes pasado. LeadMachine mandó propuesta que están comparando'.\"\n\n"
            "¿Cuál es el valor más importante que este handoff le da al AE?"
        ),
        "choices": [
            {"id": "a", "text": "La agenda de la reunión ya está cerrada."},
            {"id": "b", "text": "El AE puede entrar a la reunión conociendo exactamente el contexto competitivo (LeadMachine en evaluación), timing del cliente (Q2), dolor específico (pipeline no escala con headcount), y sabiendo que hay otro stakeholder (Joaquín). Puede preparar respuestas específicas en lugar de descubrir todo en la reunión."},
            {"id": "c", "text": "El handoff es largo — eso es bueno en sí mismo."},
            {"id": "d", "text": "Menciona la ronda Serie B, que siempre impresiona."},
        ],
        "correct": "b",
        "explanation": (
            "Valor de un handoff bien hecho: AE llega preparado sin tener que preguntar desde cero. "
            "Acá da contexto competitivo + timing + dolor cuantificado + stakeholders + señal original. Longitud por sí sola no es valor."
        ),
    },
    {
        "id": "M1.12",
        "topic": "Mindset del SDR ante incentivo complejo",
        "section": "sem2",
        "type": "single",
        "prompt": (
            "Esquema de incentivos: Salario base USD 1.500/mes. USD 40 por reunión "
            "calificada agendada. USD 200 adicional si la reunión termina en contrato "
            "firmado. Meta del trimestre: 60 reuniones calificadas.\n\n"
            "Un SDR nuevo en su segundo mes está corto contra la meta. Detecta un "
            "prospecto borderline: cumple ICP pero timing débil (\"no sabemos si "
            "vamos a avanzar este año\"). ¿Agendar y reportar como calificada, o "
            "descartar?\n\n"
            "¿Qué decisión refleja el mindset correcto del SDR?"
        ),
        "choices": [
            {"id": "a", "text": "Agendar la reunión. Está cumpliendo la meta y el AE puede decidir si el deal avanza."},
            {"id": "b", "text": "Descartar el prospecto silenciosamente. Mejor no arriesgar a que se rompa un número si el AE después se queja."},
            {"id": "c", "text": "Escalar al manager: \"Tengo este prospecto en frontera. Cumple ICP pero timing débil. ¿Lo agendo o lo dejo en pausa?\". Aplicar criterio + transparencia + usar al manager para calibrar."},
            {"id": "d", "text": "Llamar al prospecto y presionar para que diga \"sí vamos a avanzar este año\" aunque no sea verdad."},
        ],
        "correct": "c",
        "explanation": (
            "Mindset: ejecutor con criterio. Escalar dudas con honestidad construye track record con el manager y protege la métrica real "
            "(reunión calificada, no agendada). Las otras opciones queman credibilidad a mediano plazo."
        ),
    },
    {
        "id": "M1.13",
        "topic": "Inbound lead — calificación obligatoria (parte 1)",
        "section": "sem2",
        "type": "single",
        "prompt": (
            "Lead inbound (formulario web):\n\n"
            "Nombre: Federico Pérez. Rol: Gerente de Desarrollo de Negocio. "
            "Empresa: LogiSur (operador logístico regional, 480 empleados). "
            "Mensaje: \"Vi su blog sobre optimización de rutas. Estamos en proceso "
            "de evaluar mejoras a nuestra operación de última milla, ¿pueden "
            "mostrarnos cómo trabajan?\"\n\n"
            "Antes de accionar, ¿qué debe hacer el SDR?"
        ),
        "choices": [
            {"id": "a", "text": "Agendar inmediatamente reunión con el AE — es inbound, salta la calificación."},
            {"id": "b", "text": "Calificar igualmente aunque sea inbound: (1) validar ICP (LogiSur, 480 empleados), (2) validar si Federico es KDM o champion, (3) entender etapa del buying cycle (\"están evaluando\" puede ser consideración o evaluación activa), (4) verificar bloqueadores."},
            {"id": "c", "text": "Descartar el lead — los inbound suelen ser poco serios."},
            {"id": "d", "text": "Investigar todo sobre LogiSur antes de responder, sin importar el tiempo que tome."},
        ],
        "correct": "b",
        "explanation": (
            "Inbound NO equivale a calificado. Los 4 criterios no desaparecen porque el lead haya levantado la mano. "
            "Agendar todo inbound automáticamente carga al AE con reuniones que pueden no servir."
        ),
    },
    {
        "id": "M1.14",
        "topic": "Champion en consideración (parte 2)",
        "section": "sem2",
        "type": "single",
        "prompt": (
            "Continuación de la P13. El SDR llamó a Federico y confirmó:\n"
            "- ICP: LogiSur con 480 empleados califica (ICP 200-1000 logística).\n"
            "- Federico NO es KDM. Decide el Director de Operaciones. Federico evalúa para presentar al Director.\n"
            "- Están en consideración: exploran proveedores en papel, sin demos formales.\n"
            "- Sin bloqueadores absolutos. Timing: Q2-Q3 2026.\n\n"
            "¿Qué debería hacer el SDR ahora?"
        ),
        "choices": [
            {"id": "a", "text": "Agendar reunión con el AE inmediatamente — Federico quiere la demo."},
            {"id": "b", "text": "Tratar a Federico como champion potencial: mandarle info útil (overview de 2 páginas, un caso de logística relevante) para que pueda presentar al Director. Preguntar por el Director y ofrecer traerlo a una reunión con el AE cuando Federico esté listo internamente."},
            {"id": "c", "text": "Pedir que Federico le pase el contacto directo del Director y contactarlo en paralelo sin pasar por Federico."},
            {"id": "d", "text": "Descartar — Federico no es KDM."},
        ],
        "correct": "b",
        "explanation": (
            "Federico es champion potencial en consideración. Saltearlo (c) destruye la relación; descartarlo (d) elimina al aliado interno; "
            "demo prematura (a) sin el Director quema oportunidad. Respetar el proceso interno + dar herramientas para presentar."
        ),
    },
    {
        "id": "M1.15",
        "topic": "Estrategia escalonada con 4 stakeholders",
        "section": "sem2",
        "type": "single",
        "prompt": (
            "Empresa: TextileVision (textil peruano, 400 empleados). 4 contactos:\n"
            "1. José Ramírez — Gerente de Planta. Maneja operación día a día.\n"
            "2. Carla López — Directora de Operaciones. Firma decisiones hasta USD 100K.\n"
            "3. Pedro Muñoz — CFO. Aprueba contratos de tecnología que superen USD 50K.\n"
            "4. Ana Morales — Asistente ejecutiva del CEO. Visibilidad de prioridades estratégicas.\n\n"
            "Producto: software de gestión de producción, ticket USD 80K anuales.\n\n"
            "¿Cuál es la estrategia de prospección más efectiva?"
        ),
        "choices": [
            {"id": "a", "text": "Contactar primero a los 4 en paralelo con el mismo mensaje."},
            {"id": "b", "text": "Contactar solo a Pedro (CFO) — es quien aprueba el monto."},
            {"id": "c", "text": "Identificar roles: José (usuario), Carla (decisor económico parcial — ticket excede), Pedro (decisor económico real por monto), Ana (referidora). Estrategia escalonada: José primero como champion, Ana como puerta de entrada, Carla cuando José valide, Pedro en momento de decisión."},
            {"id": "d", "text": "Contactar a Carla directamente — es quien decide."},
        ],
        "correct": "c",
        "explanation": (
            "Integra los 9 roles + quién paga/quién usa + estrategia secuencial. Pedro es el decisor económico REAL del ticket "
            "(USD 80K excede el umbral CFO de USD 50K). Carla parecía decidir pero su firma queda subordinada. "
            "Construir consenso desde el champion hacia arriba."
        ),
    },
    {
        "id": "M1.16",
        "topic": "Integración conceptual del módulo",
        "section": "sem2",
        "type": "single",
        "prompt": (
            "Un SDR senior comparte su filosofía con un junior:\n\n"
            "\"El trabajo del SDR no es 'agendar reuniones' — es hacer llegar al AE "
            "reuniones donde el deal tiene posibilidad real de cerrar. Cada reunión "
            "calificada que paso al AE es un voto de confianza: verifiqué ICP, "
            "llegada al decisor, dolor real, sin bloqueadores absolutos. Si meto "
            "reuniones basura, el AE deja de confiar en mí. Eso no significa ser "
            "cobarde con el volumen — tengo que hacer mi número. Significa aplicar "
            "criterio: ¿pasa los 4 filtros? ¿Entendí qué hito le corresponde a cada "
            "quien? ¿Estoy cayendo en cruce de hitos por querer mostrar números rápidos?\"\n\n"
            "Esta reflexión combina principios de qué bloques del Módulo 1?"
        ),
        "choices": [
            {"id": "a", "text": "Solo el Bloque 5 de Sem 2 (reunión calificada con 4 criterios)."},
            {"id": "b", "text": "Integra múltiples: arquitectura del rol y relación con AE (Bloques 1, 4 de Sem 2), 4 criterios de reunión calificada (Bloque 5 Sem 2), mindset del SDR como ejecutor con criterio (Bloque 7 Sem 2), y la dinámica del comité B2B que hace que el KDM y los bloqueadores existan (Bloques 2 y 4 de Sem 1)."},
            {"id": "c", "text": "Solo el Bloque 7 de Sem 2 (mindset)."},
            {"id": "d", "text": "Ninguno específico, es filosofía general de ventas."},
        ],
        "correct": "b",
        "explanation": (
            "Pregunta meta: el alumno demuestra que ve los conceptos conectados, no aislados. "
            "La reflexión integra arquitectura SDR/AE + 4 criterios + cruce de hitos + mindset + dinámica del comité."
        ),
    },
]


VIDEO_CASES: list[dict] = [
    {
        "id": "CASO_A",
        "title": "Política interna que frena un deal aparentemente \"fácil\"",
        "context": (
            "Paula es SDR en una empresa de software de supply chain. Hace 3 "
            "semanas que intercambia emails con Roberto, Director de Operaciones "
            "de una cadena de farmacias. El producto resolvería un dolor real: "
            "Roberto confirmó que su sistema actual \"es un caos\". La propuesta "
            "es económicamente viable. Todas las señales son positivas.\n\n"
            "Pero Roberto no avanza. Finalmente responde:\n\n"
            "\"Paula, gracias por la paciencia. Te soy franco: el sistema actual lo "
            "trajo nuestra CIO hace 4 años, y ella lidera un equipo con mucha "
            "visibilidad del directorio. Cambiar de proveedor no es solo una decisión "
            "operativa — implica tener una conversación difícil con ella delante de "
            "gente que la escucha. En 6 semanas hay board meeting. Si cambio esto "
            "antes, abro un frente que no necesito hoy. Capaz después del board.\""
        ),
        "expected_key_point": (
            "El bloqueador no es técnico ni económico — es política interna "
            "(Bloque 2 Sem 1). Cambiar de proveedor implica contradecir una "
            "decisión histórica de la CIO con alta exposición (board meeting)."
        ),
        "expected_concepts": [
            "política interna",
            "dinámica de comité",
            "racionalidad aparente, decisión emocional",
        ],
        "expected_decision": (
            "3 movimientos paralelos: (1) NO forzar antes del board, (2) archivar "
            "con recontacto en 8-10 semanas, (3) ofrecer material útil a Roberto "
            "(1-2 casos breves) para que arme caso interno cuando el momento llegue. "
            "Posicionarse como aliado, no como vendedor que presiona."
        ),
    },
    {
        "id": "CASO_B",
        "title": "Reunión que parece calificada pero no lo es",
        "context": (
            "Luis (SDR) reporta 15 reuniones agendadas este trimestre. El manager "
            "le pide presentar las 5 más \"atractivas\". Luis elige esta:\n\n"
            "Empresa: InnovaSoft, consultora de tecnología argentina. 80 empleados. "
            "Contacto: Andrea Fernández, Gerente de Proyectos. Andrea llegó por "
            "LinkedIn después de que Luis la contactó. Mostró interés genuino en "
            "automatización de gestión de proyectos, confirmó que \"el equipo tiene "
            "el problema\", agendó con el AE.\n\n"
            "Notas adicionales en CRM:\n"
            "- ICP del cliente de Luis: \"empresas B2B de servicios profesionales, "
            "100-500 empleados, con operación multi-país\".\n"
            "- InnovaSoft tiene SOLO operación en Argentina.\n"
            "- Andrea menciona que \"el Director de Ingeniería valida todas las "
            "compras de tecnología, yo propongo\".\n"
            "- Cuando Luis preguntó por timing, Andrea dijo \"es algo que nos "
            "gustaría resolver en 2026 o 2027, depende de prioridades\"."
        ),
        "expected_key_point": (
            "Múltiples fallas en los 4 criterios: (1) ICP falla en 2 dimensiones "
            "(80 empleados < 100, solo Argentina vs multi-país); (2) KDM falla "
            "(Andrea no decide, valida el Director de Ingeniería); (4) precalificación "
            "falla (timing 2026-2027 sin urgencia). Falla 3 de 4 criterios."
        ),
        "expected_concepts": [
            "4 criterios de reunión calificada",
            "ICP",
            "KDM vs champion",
            "precalificación / timing",
        ],
        "expected_decision": (
            "La reunión NO debería haberse reportado como calificada. Acciones: "
            "(1) no pasar al AE o pasarla con advertencia de \"3 criterios en falla\"; "
            "(2) pedirle a Andrea que invite al Director de Ingeniería; "
            "(3) revisar el proceso de calificación del SDR para entender por qué "
            "entró un caso que falla tanto."
        ),
    },
    {
        "id": "CASO_C",
        "title": "SDR que cruza múltiples hitos en una sola conversación",
        "context": (
            "Transcripción de cold call entre Martín (SDR) y Federico (Gerente de "
            "Ventas, telecom B2B). 18 minutos.\n\n"
            "Martín: \"...en empresas como la tuya vemos que la fricción más cara "
            "suele estar en el handoff entre SDR y AE...\"\n"
            "Federico: \"Exacto, eso nos pasa. Contame más.\"\n"
            "Martín: \"Dale. Nuestra plataforma básicamente hace lo siguiente: "
            "[explicación de 6 minutos con 3 screenshots del producto enviados por "
            "email durante la llamada]. La integración con Salesforce es nativa, "
            "sincroniza en tiempo real. La implementación típica son 14 días. "
            "Nuestro pricing está entre USD 2.500 y USD 7.500 por mes dependiendo "
            "de volumen — pero con lo que describiste, te diría que estarías en la "
            "banda USD 4.000.\"\n"
            "Federico: \"Interesante. ¿Cuánto se puede negociar en precio?\"\n"
            "Martín: \"La verdad, por lo que contaste, podrías perfectamente pedir "
            "un 15% de descuento con términos anuales. Eso te dejaría cerca de los "
            "USD 3.400. Te mando propuesta con ese número ahora mismo si querés.\""
        ),
        "expected_key_point": (
            "Múltiples cruces de hitos en una sola call: (3) demo — 6 min de "
            "producto + screenshots; (4) propuesta — pricing específico USD 4.000 "
            "sin discovery del AE; (5) cierre/negociación — 15% descuento + términos "
            "anuales + USD 3.400 específico. El AE se queda sin producto que mostrar "
            "y con margen regalado de entrada."
        ),
        "expected_concepts": [
            "cruce de hitos",
            "venta por hitos",
            "regalar margen sin contraprestación",
            "handoff",
        ],
        "expected_decision": (
            "Lo que debió hacer Martín en cada momento:\n"
            "- \"Contame más\": redirigir al AE. \"Me alegra que resuene. [AE] tiene "
            "toda la visibilidad del producto en detalle. ¿Agendamos 20 min con él/ella?\"\n"
            "- Pregunta por pricing: NO dar número. \"El pricing depende de factores "
            "que [AE] va a entender mejor en tu caso. En la reunión definen el número.\"\n"
            "- Pregunta por descuento: NO ofrecer. \"Los ajustes comerciales los maneja "
            "[AE] directamente.\""
        ),
    },
    {
        "id": "CASO_D",
        "title": "Handoff defectuoso que el AE no puede usar",
        "context": (
            "Handoff que un SDR le pasó a una AE para una reunión agendada para "
            "el miércoles a las 3pm:\n\n"
            "\"Handoff para Carolina (AE) — miércoles 15hs:\n"
            "La reunión es con Juan Sánchez de una empresa de servicios. Le "
            "interesa lo que hacemos. Cree que podría servirles. Lo conocí por "
            "LinkedIn, le mandé varios mensajes y finalmente me contestó. "
            "Hablamos 2 veces por teléfono y agendamos. Tenía una buena actitud. "
            "Te pido que le des prioridad porque es un deal grande potencialmente. "
            "Cualquier cosa avisame.\""
        ),
        "expected_key_point": (
            "El handoff viola todos los principios del Bloque 6 de Sem 2 (formato "
            "operativo de 1 página con campos concretos). Faltan: "
            "(1) info de la empresa (industria, tamaño); (2) rol exacto y autoridad "
            "de Juan; (3) la señal que activó la conversación; (4) precalificación "
            "S→N→T concreta; (5) advertencia sobre otros stakeholders; "
            "(6) la frase \"deal grande potencialmente\" es especulación sin base."
        ),
        "expected_concepts": [
            "formato operativo de handoff",
            "qué va y qué no en un handoff",
            "precalificación Situación / Necesidad / Timing",
        ],
        "expected_decision": (
            "Antes que Carolina tenga la reunión el miércoles, el SDR debe reescribir "
            "el handoff completo con: empresa (nombre, industria, tamaño), contacto "
            "(rol de Juan, LinkedIn), señal (qué gancho funcionó), precalificación "
            "(3 líneas S+N+T), otros stakeholders, agenda sugerida, advertencias. "
            "Si no tiene esa info, la obtiene antes del miércoles — no deja que "
            "Carolina entre a ciegas."
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
                {"score": 2, "descriptor": "Usa vocabulario específico del curso correctamente (política interna, 4 criterios, cruce de hitos, handoff, ejecutor con criterio, etc.) y lo conecta con el caso."},
            ],
        },
        {
            "key": "decision",
            "label": "Decisión concreta y aterrizada",
            "scale": [
                {"score": 0, "descriptor": "No decide o decide algo desconectado del diagnóstico."},
                {"score": 1, "descriptor": "Decide algo razonable pero poco específico."},
                {"score": 2, "descriptor": "Decide algo específico, aterrizado al caso, trazable al diagnóstico."},
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


# Pesos para nota final del módulo (Documento Maestro Parte IV §Cálculo de nota)
WEIGHTS = {"mcq": 0.7, "video": 0.3}
PASSING_SCORE = 65.0


def total_question_count() -> int:
    return len(MCQ)


def section_counts() -> dict[str, int]:
    out: dict[str, int] = {}
    for q in MCQ:
        out[q["section"]] = out.get(q["section"], 0) + 1
    return out
