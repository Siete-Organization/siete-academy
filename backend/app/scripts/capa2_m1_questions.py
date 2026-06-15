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
            "Tomás es SDR y vende una plataforma de gestión de contratos B2B "
            "(SaaS) a empresas medianas. Su amigo Matías vende televisores en una "
            "cadena de retail (B2C). Comparten anécdotas del trabajo.\n\n"
            "Tomás: \"Hoy me pasó algo raro. Después de 4 meses de ida y vuelta "
            "con una empresa, la directora me dijo que tiene el contrato listo, "
            "pero no lo puede firmar hasta que pase el board meeting de abril. "
            "Necesita 'legitimar la decisión' con el directorio.\"\n"
            "Matías: \"Qué raro. Yo ayer vendí un TV de USD 3.000 en 20 minutos: "
            "llegó la clienta, preguntó tres cosas, pagó con tarjeta y se lo llevó.\"\n\n"
            "¿Cuál es la diferencia estructural más importante entre los dos casos?"
        ),
        "choices": [
            {"id": "a", "text": "El precio: USD 3.000 del TV frente a un contrato de varios miles de USD por mes en SaaS hace que la compra de Tomás sea naturalmente más lenta y cuidada."},
            {"id": "b", "text": "La duración del proceso: el caso de Tomás llevó meses y el de Matías minutos, y esa diferencia de tiempo es lo que separa al B2B del B2C."},
            {"id": "c", "text": "El tipo de producto: uno es físico y se entrega al instante, y el otro es digital y exige implementación, lo que alarga el proceso de compra."},
            {"id": "d", "text": "La cantidad de personas que intervienen en la decisión: la clienta de Matías decide sola, mientras que la directora, aun con autoridad de firma, necesita el respaldo del directorio para avanzar."},
        ],
        "correct": "d",
        "explanation": (
            "La diferencia central B2B vs B2C no es precio, producto ni duración — es que en B2B rara vez decide una sola persona. "
            "La directora tiene autoridad técnica pero opera en un sistema de consenso. La duración es consecuencia, no causa."
        ),
    },
    {
        "id": "M1.2",
        "topic": "Cómo decide realmente el comprador",
        "section": "sem1",
        "type": "single",
        "prompt": (
            "Un CFO recibe dos propuestas de CRM (A y B) para su empresa. Estas son "
            "las observaciones internas que compartió con su equipo:\n\n"
            "\"Propuesta A: tiene todo lo que necesitamos técnicamente. El ROI "
            "calculado es 2,1x a 3 años. El proveedor es mediano, con referencias "
            "sólidas en nuestra industria. Propuesta B: también cumple los "
            "requerimientos técnicos. ROI similar (2,0x). El proveedor es una "
            "empresa grande reconocida, con un precio 15% más alto. Voy con B. Si "
            "algo sale mal con A, el directorio me va a preguntar por qué no elegí "
            "la opción 'segura'. Con B, si sale mal, nadie va a cuestionar la "
            "elección.\"\n\n"
            "Según lo que enseña el curso, ¿qué está haciendo el CFO?"
        ),
        "choices": [
            {"id": "a", "text": "Una decisión movida por el miedo a quedar mal frente al directorio si la apuesta falla, que después se justificará con argumentos técnicos: pesó más proteger su carrera que los números."},
            {"id": "b", "text": "Una decisión racional basada en el ROI: elige B porque su mejor reputación de marca reduce el riesgo real del proyecto."},
            {"id": "c", "text": "Una decisión política basada en una relación personal previa con el proveedor B, que lo inclina a favorecerlo aunque no lo diga abiertamente."},
            {"id": "d", "text": "Una mala decisión comercial: A era claramente superior por ROI y el CFO se equivoca al no elegir la opción con mejores números."},
        ],
        "correct": "a",
        "explanation": (
            "El CFO lo dice literalmente: eligió B por protección de carrera. Caso textbook de Kahneman aplicado a compra B2B. "
            "Un SDR que entiende esto vende prueba social (\"misma decisión que [Banco conocido]\"), no \"2.5x ROI garantizado\"."
        ),
    },
    {
        "id": "M1.3",
        "topic": "Etapa del ciclo de compra",
        "section": "sem1",
        "type": "single",
        "prompt": (
            "Un SDR recibe esta respuesta a un cold email:\n\n"
            "\"Gracias por escribir. La verdad es que hace unos meses empezamos a "
            "sentir que el tema que mencionas (gestión de pipeline comercial) se "
            "nos está quedando corto con nuestras herramientas actuales. Empecé a "
            "investigar alternativas el mes pasado. Estamos mirando tres opciones "
            "en papel, todavía no pedimos demos formales. ¿Puedes enviarme un "
            "overview para sumarlos a la shortlist?\"\n\n"
            "¿En qué etapa del ciclo de compra está este prospecto?"
        ),
        "choices": [
            {"id": "a", "text": "Awareness: todavía no detecta el problema y sigue con su operación habitual sin buscar soluciones."},
            {"id": "b", "text": "Consideración: reconoce el problema y explora opciones de forma preliminar, sin compararlas todavía de manera formal."},
            {"id": "c", "text": "Evaluación: ya armó una lista corta y compara en serio, con demos, tablas y llamadas a otros clientes."},
            {"id": "d", "text": "Decisión: ya eligió un proveedor y está negociando precio, alcance y contrato."},
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
            "En una empresa de 220 empleados están evaluando un software de "
            "gestión de logística interna. Lee la descripción de cada persona y "
            "asígnale el rol que cumple:\n\n"
            "1. Ramiro — Director de Compras. Entra al final del proceso para negociar precio, SLAs y cláusulas contractuales.\n"
            "2. Ana — Coordinadora de Logística. No firma, pero odia el sistema actual y fue quien trajo el tema al COO. Te conectó.\n"
            "3. Sofía — COO. Tiene presupuesto propio, firma la orden de compra y reporta al CEO.\n"
            "4. Gabriel — VP de Operaciones (otra área). No evalúa, pero su opinión pesa porque también usa sistemas integrados.\n"
            "5. Lucía — Directora de IT. Puede vetar si no hay integración con el ERP corporativo.\n"
            "6. Carlos — Gerente de TI que firmó con el proveedor actual hace 3 años. Se opone al cambio."
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
            {"id": "C", "text": "Champion + referidor"},
            {"id": "D", "text": "Influenciador"},
            {"id": "E", "text": "Bloqueador"},
            {"id": "F", "text": "Compras (procurement)"},
        ],
        "correct": {"1": "F", "2": "C", "3": "A", "4": "D", "5": "B", "6": "E"},
        "explanation": (
            "Distinción crítica: bloqueador (Carlos, se opone explícitamente) vs influenciador (Gabriel, opina pero no se opone). "
            "Confundirlos quema la estrategia de prospección."
        ),
    },
    {
        "id": "M1.5",
        "topic": "Ciclo de vida del prospecto vs ciclo del cliente",
        "section": "sem1",
        "type": "single",
        "prompt": (
            "En una reunión interna, un SDR nuevo dice:\n\n"
            "\"Tenemos un prospecto que ya está en la etapa de Renewal (renovación). "
            "Creo que deberíamos pasarlo a Customer Success para que lo manejen.\"\n\n"
            "¿Cuál es el problema con lo que dijo el SDR?"
        ),
        "choices": [
            {"id": "a", "text": "Confunde dos ciclos distintos: \"renovación\" pertenece al ciclo del cliente ya firmado (lo maneja Customer Success), no al ciclo de vida del prospecto, que termina cuando la empresa se vuelve cliente."},
            {"id": "b", "text": "Confunde las etiquetas: el prospecto debería figurar como \"Oportunidad\" y no como \"Renewal\", aunque el área que lo maneja sí sería la correcta."},
            {"id": "c", "text": "El error es de secuencia: antes de Renewal el prospecto tiene que pasar por MQL y SQL, y el SDR se está salteando esas etapas."},
            {"id": "d", "text": "No hay error de fondo: un prospecto puede estar en renovación si tuvo un contrato previo que venció, y derivarlo a Customer Success es lo correcto."},
        ],
        "correct": "a",
        "explanation": (
            "Dos lifecycles distintos: prospecto (Prospect → MQL → SQL → Opportunity → Customer) vs cliente firmado "
            "(Onboarding → Use → Engage → Adopt → Optimize → Renew → Advocate). Renewal pertenece al segundo."
        ),
    },
    {
        "id": "M1.6",
        "topic": "Quién paga, quién usa, quién aprueba",
        "section": "sem1",
        "type": "single",
        "prompt": (
            "Una SDR va a prospectar a una empresa de 500 empleados para vender un "
            "software de productividad específico para equipos de marketing. La "
            "herramienta la usaría el equipo de marketing (10 personas), pero el "
            "presupuesto de tecnología es centralizado y lo aprueba Finanzas "
            "Corporativas.\n\n"
            "¿Cuál es el mejor enfoque para esta prospección?"
        ),
        "choices": [
            {"id": "a", "text": "Contactar solo al CMO (jefe de marketing), porque es quien quiere la herramienta y su equipo es el que la va a usar todos los días."},
            {"id": "b", "text": "Contactar solo al CFO (finanzas), porque sin la aprobación del presupuesto centralizado el resto de la conversación no avanza."},
            {"id": "c", "text": "Identificar temprano las tres capas (usuario en marketing, decisor económico en finanzas, decisor técnico si hay integración), empezar por un champion entre los usuarios y mapear en paralelo al decisor económico."},
            {"id": "d", "text": "Contactar a las tres capas al mismo tiempo con el mismo mensaje, para ganar tiempo y que todas lleguen al tema a la vez."},
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
        "topic": "Canales de generación de demanda (selección múltiple)",
        "section": "sem2",
        "type": "multi",
        "prompt": (
            "Una empresa de SaaS B2B evalúa sus canales de generación de demanda "
            "para el siguiente escenario.\n\n"
            "Escenario: cliente ideal muy concentrado (30 a 50 empresas a nivel "
            "LATAM), deals de ticket alto (USD 100K+ anuales), ciclo de 12 a 18 "
            "meses.\n\n"
            "¿Qué canales aplican mejor? (marca todos los que correspondan)"
        ),
        "choices": [
            {"id": "1", "text": "Inbound masivo (SEO + ads + blog)"},
            {"id": "2", "text": "Outbound hiperpersonalizado"},
            {"id": "3", "text": "Alianzas con consultoras del segmento"},
            {"id": "4", "text": "Referidos trabajados de forma sistemática"},
        ],
        "correct": ["2", "3", "4"],
        "explanation": (
            "Con 30-50 cuentas objetivo, el enfoque no masivo es obligatorio. Inbound masivo genera volumen disperso — "
            "ruido que no aporta. Outbound hiperpersonalizado, alianzas con consultoras y referidos sistemáticos = profundidad sobre cuentas específicas."
        ),
    },
    {
        "id": "M1.8",
        "topic": "Cuándo NO aplica el outbound",
        "section": "sem2",
        "type": "single",
        "prompt": (
            "Una empresa vende una herramienta de gestión de tareas en la nube por "
            "USD 29 al mes por empresa, dirigida a \"cualquier empresa que quiera "
            "organizar mejor su trabajo\". El fundador está pensando en armar un "
            "equipo de SDRs para hacer outbound.\n\n"
            "¿Por qué el outbound NO tiene sentido en este caso?"
        ),
        "choices": [
            {"id": "a", "text": "Porque el producto está mal diseñado y primero hay que mejorarlo antes de pensar en cualquier canal de venta."},
            {"id": "b", "text": "Porque un producto nuevo siempre debe empezar por marketing de contenido y recién después sumar un equipo de outbound."},
            {"id": "c", "text": "Porque el ciclo de venta es demasiado largo para sostener el modelo de outbound, que necesita cerrar rápido para ser rentable."},
            {"id": "d", "text": "Porque falla en dos de las tres condiciones del outbound: el cliente ideal no es identificable (\"cualquier empresa\" no es un ICP) y el ticket (USD 29 al mes) no justifica el costo de un SDR."},
        ],
        "correct": "d",
        "explanation": (
            "Las 3 condiciones para outbound: ICP alcanzable, ticket justificable, ciclo manejable. "
            "Un ticket de USD 29/mes por empresa vs un SDR que cuesta miles/mes no cierra números, y \"cualquier empresa\" no es un ICP identificable."
        ),
    },
    {
        "id": "M1.9",
        "topic": "Cruce de hitos del SDR",
        "section": "sem2",
        "type": "single",
        "prompt": (
            "Un SDR termina una cold call exitosa: logró agendar una reunión para "
            "el jueves con el VP de Ingeniería. Al cerrar, el VP dice:\n\n"
            "\"Perfecto, agendado. Una cosa antes de colgar: ¿me puedes enviar un "
            "caso de éxito con una empresa de software parecida a la nuestra? Me "
            "viene bien llegar a la reunión con algo de contexto.\"\n\n"
            "¿Qué debería hacer el SDR?"
        ),
        "choices": [
            {"id": "a", "text": "Enviar tres casos de éxito completos para que el VP llegue muy preparado y la reunión avance más rápido."},
            {"id": "b", "text": "Enviar un caso breve y relevante al contexto que mencionó el VP, dejando espacio para que el AE profundice en la reunión."},
            {"id": "c", "text": "Responder que los casos los presenta el AE en la reunión y no enviar nada, para no adelantar material que le corresponde al AE."},
            {"id": "d", "text": "Enviar el brochure completo del producto, que incluye varios casos y cubre todo lo que el VP pueda llegar a necesitar."},
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
            "Empresa: BioLogic S.A., laboratorio farmacéutico peruano de 180 "
            "empleados (el ICP definido es \"laboratorios farmacéuticos LATAM de "
            "150 a 500 empleados\"). Contacto: Carla Espinosa, Directora de "
            "Calidad. Llegó a la reunión. Confirmó que BioLogic tiene un proceso "
            "manual de tracking de lotes que \"genera errores mensualmente\" y que "
            "están \"viendo opciones\", aunque \"no hay urgencia\". Nota del SDR: "
            "\"Califica, cumple los 4 criterios.\"\n\n"
            "Aplicando los 4 criterios de reunión calificada, ¿la reunión realmente califica?"
        ),
        "choices": [
            {"id": "a", "text": "No: falta validar si Carla es decisora (KDM) o champion validado; ser Directora de Calidad no garantiza autoridad de compra, y el SDR no lo verificó."},
            {"id": "b", "text": "Sí: cumple el ICP, el contacto asistió, hay un problema real y un mínimo de interés, así que pasa los cuatro criterios."},
            {"id": "c", "text": "No: el problema es que la empresa no entra en el ICP definido, porque un laboratorio de 180 empleados queda fuera del rango."},
            {"id": "d", "text": "No: no se cumple el criterio de asistencia, porque la reunión todavía no se realizó efectivamente."},
        ],
        "correct": "a",
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
            "Un SDR entrega este handoff al AE:\n\n"
            "Handoff — reunión lunes 10am. Empresa: TechGrow (SaaS B2B de marketing "
            "automation), 320 empleados, oficinas en CDMX y BA. Contacto: Mariela "
            "Castro, VP de Marketing. La señal fue el anuncio de su ronda Serie B "
            "(USD 18M con Kaszek) de enero 2026. Gancho del cold email: \"en "
            "post-Serie B, lo que vemos es que el pipeline comercial no escala tan "
            "rápido como el headcount\". Mariela respondió que \"justamente estamos "
            "pasando por eso\". Precalificación: (1) Situación: el equipo comercial "
            "pasó de 12 a 22 AEs en 4 meses, el pipeline no creció al mismo ritmo. "
            "(2) Necesidad: duplicar el pipeline en 60 días. (3) Timing: presupuesto "
            "2026 ya asignado, buscan implementar en Q2. Otros stakeholders: Joaquín "
            "López (VP de Ventas), va a evaluar cualquier propuesta antes de la "
            "decisión final. Advertencia: Mariela mencionó que ya hablaron con dos "
            "proveedores similares el mes pasado, y que una de ellas (LeadMachine) "
            "mandó una propuesta que están comparando.\n\n"
            "¿Cuál es el valor más importante que este handoff le da al AE?"
        ),
        "choices": [
            {"id": "a", "text": "Que la agenda de la reunión ya quedó cerrada y confirmada, lo que le ahorra al AE tener que coordinarla."},
            {"id": "b", "text": "Que menciona la ronda Serie B reciente, un dato que genera buena impresión y ayuda a abrir la conversación con el AE."},
            {"id": "c", "text": "Que es un handoff extenso y detallado, y esa cantidad de información es en sí misma una señal de la calidad del trabajo del SDR."},
            {"id": "d", "text": "Que el AE entra conociendo el contexto competitivo, el timing, el dolor específico y los otros stakeholders, y puede preparar respuestas en vez de descubrir todo en la reunión."},
        ],
        "correct": "d",
        "explanation": (
            "Valor de un handoff bien hecho: AE llega preparado sin tener que preguntar desde cero. "
            "Acá da contexto competitivo + timing + dolor cuantificado + stakeholders + señal original. Longitud por sí sola no es valor."
        ),
    },
    {
        "id": "M1.12",
        "topic": "Mindset del SDR ante un caso borderline",
        "section": "sem2",
        "type": "single",
        "prompt": (
            "En una empresa B2B, el equipo de SDRs tiene este esquema de "
            "incentivos: Salario base USD 1.500/mes. USD 40 por cada reunión "
            "calificada agendada. USD 200 adicionales si la reunión termina en "
            "contrato firmado. Meta del trimestre: 60 reuniones calificadas.\n\n"
            "Un SDR nuevo, en su segundo mes, está corto contra la meta. Detecta un "
            "prospecto borderline: cumple el ICP, pero la precalificación mostró un "
            "timing débil (\"no sabemos si vamos a avanzar con esto este año\").\n\n"
            "¿Qué decisión refleja el mindset correcto del SDR?"
        ),
        "choices": [
            {"id": "a", "text": "Agendar la reunión y reportarla como calificada: está cumpliendo la meta y el AE decidirá en la reunión si el deal avanza."},
            {"id": "b", "text": "Descartar el prospecto sin reportarlo, para no arriesgar un número si después el AE se queja de la calidad."},
            {"id": "c", "text": "Escalar el caso al manager con transparencia (\"cumple ICP pero el timing es débil, ¿lo agendo o lo dejo en pausa?\"), aplicando criterio y protegiendo la métrica real."},
            {"id": "d", "text": "Reportarlo como calificado igual, anotando internamente la debilidad de timing para cubrirse si el AE lo cuestiona después."},
        ],
        "correct": "c",
        "explanation": (
            "Mindset: ejecutor con criterio. Escalar dudas con honestidad construye track record con el manager y protege la métrica real "
            "(reunión calificada, no agendada). Las otras opciones queman credibilidad a mediano plazo."
        ),
    },
    {
        "id": "M1.13",
        "topic": "Lead inbound: qué hacer antes de accionar",
        "section": "sem2",
        "type": "single",
        "prompt": (
            "Un SDR recibe este lead inbound (formulario web completado):\n\n"
            "Nombre: Federico Pérez. Rol: Gerente de Desarrollo de Negocio. "
            "Empresa: LogiSur (operador logístico regional, 480 empleados). "
            "Mensaje: \"Vi su blog sobre optimización de rutas. Estamos en proceso "
            "de evaluar mejoras a nuestra operación de última milla, ¿pueden "
            "mostrarnos cómo trabajan?\"\n\n"
            "Antes de accionar, ¿qué debe hacer el SDR?"
        ),
        "choices": [
            {"id": "a", "text": "Agendar de inmediato la reunión con el AE: al ser inbound, el lead ya viene calificado y no necesita filtro."},
            {"id": "b", "text": "Calificar igual aunque sea inbound: validar el ICP, ver si Federico decide o es champion, entender en qué etapa del ciclo está y revisar que no haya bloqueadores."},
            {"id": "c", "text": "Descartar el lead: los formularios web suelen traer contactos poco serios que hacen perder tiempo."},
            {"id": "d", "text": "Investigar a fondo todo sobre LogiSur antes de responder, sin importar cuánto tiempo tome, para llegar muy preparado."},
        ],
        "correct": "b",
        "explanation": (
            "Inbound NO equivale a calificado. Los 4 criterios no desaparecen porque el lead haya levantado la mano. "
            "Agendar todo inbound automáticamente carga al AE con reuniones que pueden no servir."
        ),
    },
    {
        "id": "M1.14",
        "topic": "Acción concreta según la etapa",
        "section": "sem2",
        "type": "single",
        "prompt": (
            "Continuación de la pregunta anterior. El SDR llamó a Federico y "
            "confirmó:\n"
            "- ICP: LogiSur (480 empleados) califica (el ICP es 200 a 1.000 empleados en logística).\n"
            "- Federico no es el decisor (decide el Director de Operaciones). Está evaluando opciones para presentarlas al Director.\n"
            "- Están en consideración: exploran varios proveedores en papel, todavía no pidieron demos formales.\n"
            "- No hay bloqueadores absolutos. Timing: Q2-Q3 2026.\n\n"
            "¿Qué debería hacer el SDR ahora?"
        ),
        "choices": [
            {"id": "a", "text": "Agendar de inmediato la reunión con el AE, porque Federico pidió ver cómo trabajan y el interés está caliente."},
            {"id": "b", "text": "Pedirle a Federico el contacto directo del Director y escribirle en paralelo, para llegar antes a quien realmente decide."},
            {"id": "c", "text": "Descartar el caso, porque Federico no es el decisor y avanzar sin el KDM no tiene sentido."},
            {"id": "d", "text": "Tratar a Federico como champion potencial: darle material útil para presentar internamente, preguntar por el Director y ofrecer traerlo a una reunión cuando esté listo."},
        ],
        "correct": "d",
        "explanation": (
            "Federico es champion potencial en consideración. Saltearlo (b) destruye la relación; descartarlo (c) elimina al aliado interno; "
            "demo prematura (a) sin el Director quema oportunidad. Respetar el proceso interno + dar herramientas para presentar."
        ),
    },
    {
        "id": "M1.15",
        "topic": "Estrategia de prospección en un comité",
        "section": "sem2",
        "type": "single",
        "prompt": (
            "Un SDR va a prospectar a TextileVision (400 empleados, fabricante "
            "textil peruano) con un software de gestión de producción, ticket "
            "estimado de USD 80K anuales. Identifica cuatro contactos:\n"
            "- José Ramírez — Gerente de Planta. Maneja la operación día a día.\n"
            "- Carla López — Directora de Operaciones. Reporta al CEO. Firma decisiones operativas hasta USD 100K.\n"
            "- Pedro Muñoz — CFO. Aprueba cualquier contrato de tecnología que supere los USD 50K.\n"
            "- Ana Morales — Asistente ejecutiva del CEO. Tiene visibilidad de las prioridades del CEO y coordina las agendas del equipo directivo.\n\n"
            "¿Cuál es la estrategia de prospección más efectiva?"
        ),
        "choices": [
            {"id": "a", "text": "Empezar por Carla como decisora económica, porque el ticket de USD 80K entra dentro de su límite de firma de USD 100K, y cerrar el avance con ella."},
            {"id": "b", "text": "Empezar por José como champion potencial (siente el dolor operativo), usar a Ana como puerta de entrada al equipo directivo e involucrar a Pedro como decisor económico real, porque el ticket supera su umbral de USD 50K."},
            {"id": "c", "text": "Contactar directo a Pedro (CFO), porque es quien aprueba el monto, y dejar que él baje el tema al resto de las áreas si le interesa."},
            {"id": "d", "text": "Escribir a los cuatro en paralelo con el mismo mensaje, para cubrir todo el comité y que el tema avance por donde primero responda."},
        ],
        "correct": "b",
        "explanation": (
            "Integra los 9 roles + quién paga/quién usa + estrategia secuencial. Pedro es el decisor económico REAL del ticket "
            "(USD 80K excede el umbral CFO de USD 50K). Carla parecía decidir pero su firma queda subordinada. "
            "Construir consenso desde el champion hacia arriba."
        ),
    },
    {
        "id": "M1.16",
        "topic": "Aplicar la filosofía del rol",
        "section": "sem2",
        "type": "single",
        "prompt": (
            "Un SDR senior comparte su filosofía con un junior:\n\n"
            "\"Lo que aprendí en 2 años en este rol es que el trabajo del SDR no es "
            "agendar reuniones: es hacerle llegar al AE reuniones donde el deal "
            "tiene posibilidad real de cerrar. Cada reunión calificada que paso es "
            "un voto de confianza: verifiqué que la empresa cumple el ICP, que el "
            "contacto tiene llegada al decisor, que hay dolor real y que no hay "
            "bloqueadores. Si meto reuniones basura, el AE deja de confiar en mí. "
            "Eso no significa ser cobarde con el volumen: tengo que hacer mi "
            "número. Significa aplicar criterio.\"\n\n"
            "Un SDR junior quiere aplicar esta filosofía. ¿Cuál de estas decisiones la refleja mejor?"
        ),
        "choices": [
            {"id": "a", "text": "Bajar el volumen de prospección para asegurarse de que cada reunión sea perfecta, aunque eso signifique no llegar a la meta del mes."},
            {"id": "b", "text": "Agendar todas las reuniones posibles y dejar que el AE filtre en la reunión cuáles sirven y cuáles no."},
            {"id": "c", "text": "Mantener el volumen, pero antes de pasar cada reunión verificar que cumpla los 4 criterios y escalar al manager las que queden en zona gris."},
            {"id": "d", "text": "Priorizar las cuentas más grandes y pasar solo esas, descartando las medianas aunque cumplan los criterios."},
        ],
        "correct": "c",
        "explanation": (
            "La filosofía es ejecutor con criterio: mantener el volumen (hacer el número) sin sacrificar la calidad. "
            "Verificar los 4 criterios y escalar las zonas grises protege la confianza del AE sin caer en bajar volumen (a), "
            "agendar basura (b) ni descartar cuentas válidas por tamaño (d)."
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
            "\"Paula, gracias por la paciencia. Mira, te soy franco: el sistema "
            "actual lo trajo nuestra CIO hace 4 años, y ella lidera un equipo con "
            "mucha visibilidad del directorio. Cambiar de proveedor no es solo una "
            "decisión operativa, implica una conversación difícil con ella delante "
            "de gente que la escucha. En 6 semanas hay board meeting. Si cambio "
            "esto antes, abro un frente que no necesito hoy. Quizás después del board.\""
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
