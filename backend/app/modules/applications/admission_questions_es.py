"""Contenido Etapa 1 — Prueba de admisión SDR Academy (ES).

Fuente: SDR_Academy_Siete_Documento_Maestro.md, Parte III, v1.2 MVP (2026-04-24).

Estructura:
- OPEN_PROMPTS: 3 preguntas abiertas (Parte B) con límite estricto de palabras
- MCQ: 26 preguntas (Parte C) — 11 Excel/BBDD + 5 lógica + 5 negocio + 5 comprensión
- COMPREHENSION_TEXT: texto base ~500 palabras que el aspirante lee para responder C.4

`correct` es el id de la respuesta correcta. `explanation` es interno (no se muestra
al candidato; útil para revisores y análisis post-prueba).
"""

OPEN_PROMPTS: list[dict] = [
    {
        "id": "B.1",
        "title": "Timeline",
        "prompt": (
            "Contame cómo llegaste a aplicar a esta Academy. Quién te habló primero "
            "de esto, cuándo fue, qué investigaste después, qué te hizo dudar, qué te "
            "terminó de convencer. Sé específico con nombres, fechas aproximadas y "
            "fuentes."
        ),
        "min_words": 80,
        "max_words": 150,
    },
    {
        "id": "B.2",
        "title": "Costo de oportunidad",
        "prompt": (
            "Para hacer esta Academy de 8 semanas vas a dejar de hacer algo concreto. "
            "No me digas \"tiempo libre\" en general. Decime exactamente qué: un "
            "trabajo, horas de estudio de otra cosa, tiempo con alguien específico, un "
            "proyecto personal. ¿Quién se va a ver afectado y cómo vas a manejarlo?"
        ),
        "min_words": 50,
        "max_words": 100,
    },
    {
        "id": "B.3",
        "title": "Qué NO te gusta del rol",
        "prompt": (
            "Investigá qué hace un SDR (Sales Development Representative) antes de "
            "responder. Podés usar Google, ChatGPT o lo que quieras. Decime 2 cosas "
            "que NO te gustan de ese rol, o que te preocupan si lo hicieras vos. No "
            "podés responder \"nada me preocupa\". Elegí dos y explicá."
        ),
        "min_words": 50,
        "max_words": 100,
    },
]


MCQ: list[dict] = [
    # ───────── C.1 — Excel y manejo básico de BBDD (11) ─────────
    {
        "id": "C1.1",
        "section": "excel",
        "prompt": (
            "En la celda B1 tenés el factor de conversión USD→ARS (un solo número). "
            "En la columna A (A2:A100) tenés montos en USD. Querés escribir una "
            "fórmula en C2 y arrastrarla hacia abajo hasta C100 para tener todos los "
            "montos convertidos. ¿Cuál es la fórmula correcta para C2?"
        ),
        "choices": [
            {"id": "a", "text": "=A2*B1"},
            {"id": "b", "text": "=A2*$B$1"},
            {"id": "c", "text": "=$A$2*B1"},
            {"id": "d", "text": "=A$2*B1"},
        ],
        "correct": "b",
        "explanation": (
            "Anclaje absoluto del factor común al arrastrar. Si elige a, al arrastrar "
            "B1 se convierte en B2, B3… y rompe todo."
        ),
    },
    {
        "id": "C1.2",
        "section": "excel",
        "prompt": (
            "En A2 tenés el texto: carlos.rojas@empresa.com.ar. Querés extraer solo "
            "la parte del dominio (empresa.com.ar) en una fórmula. ¿Cuál funciona?"
        ),
        "choices": [
            {"id": "a", "text": '=LEFT(A2, FIND("@",A2))'},
            {"id": "b", "text": '=RIGHT(A2, LEN(A2)-FIND("@",A2))'},
            {"id": "c", "text": '=MID(A2, FIND("@",A2), LEN(A2))'},
            {"id": "d", "text": '=FIND("@",A2)'},
        ],
        "correct": "b",
        "explanation": "FIND+RIGHT+LEN para parsing de texto post-arroba.",
    },
    {
        "id": "C1.3",
        "section": "excel",
        "prompt": (
            "Tenés dos hojas. Hoja Clientes tiene en columna A el email y en B el "
            "nombre de la empresa. Hoja Pedidos tiene en columna A el email del "
            "comprador. Querés agregar en Pedidos!B2 el nombre de la empresa "
            "cruzando por email. ¿Cuál fórmula usás?"
        ),
        "choices": [
            {"id": "a", "text": "=VLOOKUP(A2, Clientes!A:B, 1, FALSE)"},
            {"id": "b", "text": "=VLOOKUP(A2, Clientes!A:B, 2, TRUE)"},
            {"id": "c", "text": "=VLOOKUP(A2, Clientes!A:B, 2, FALSE)"},
            {"id": "d", "text": "=VLOOKUP(Clientes!A:B, A2, 2, FALSE)"},
        ],
        "correct": "c",
        "explanation": (
            "Argumentos del VLOOKUP. a devuelve la key (col 1). b usa TRUE (búsqueda "
            "aproximada, falla con texto). d invierte argumentos."
        ),
    },
    {
        "id": "C1.4",
        "section": "excel",
        "prompt": (
            "Tenés que cruzar dos tablas pero el match correcto requiere DOS columnas "
            "(ej.: hay dos contactos llamados \"Juan Pérez\" en empresas distintas, "
            "necesitás matchear por nombre+empresa). ¿Cuál es la solución estándar "
            "en Excel?"
        ),
        "choices": [
            {
                "id": "a",
                "text": "Hacer dos VLOOKUPs separados y combinar resultados con CONCATENAR.",
            },
            {
                "id": "b",
                "text": (
                    "Crear una columna auxiliar con la concatenación nombre & empresa "
                    "en ambas tablas y hacer VLOOKUP sobre esa columna nueva."
                ),
            },
            {
                "id": "c",
                "text": "Pasar a VLOOKUP dos valores de búsqueda separados por coma.",
            },
            {
                "id": "d",
                "text": "Excel no soporta lookups con dos criterios — hay que exportar a SQL.",
            },
        ],
        "correct": "b",
        "explanation": (
            "Solución estándar de \"left join por 2 campos\" en Excel: columna "
            "auxiliar concatenada."
        ),
    },
    {
        "id": "C1.5",
        "section": "excel",
        "prompt": (
            "Tenés una tabla de 2.000 prospectos con columnas: Industria, País, "
            "Estado_contacto (agendada / respondida / sin_respuesta). Querés contar "
            "cuántos prospectos están en estado \"agendada\" en industria \"Fintech\" "
            "en país \"México\". ¿Qué fórmula usás?"
        ),
        "choices": [
            {"id": "a", "text": '=COUNT(Estado_contacto, "agendada")'},
            {
                "id": "b",
                "text": (
                    '=COUNTIF(Industria, "Fintech") + COUNTIF(País, "México") + '
                    'COUNTIF(Estado_contacto, "agendada")'
                ),
            },
            {
                "id": "c",
                "text": (
                    '=COUNTIFS(Industria, "Fintech", País, "México", '
                    'Estado_contacto, "agendada")'
                ),
            },
            {
                "id": "d",
                "text": '=SUMIFS(Industria, "Fintech", País, "México")',
            },
        ],
        "correct": "c",
        "explanation": "COUNTIFS con múltiples criterios — intersección, no suma de rangos.",
    },
    {
        "id": "C1.6",
        "section": "excel",
        "prompt": (
            "Querés clasificar prospectos por su reply_rate (en columna A): si >5% = "
            "\"alto\", si entre 2% y 5% = \"medio\", si <2% = \"bajo\". ¿Qué fórmula "
            "es correcta?"
        ),
        "choices": [
            {
                "id": "a",
                "text": (
                    '=IF(A2>5%, "alto") OR IF(A2>=2%, "medio") OR IF(A2<2%, "bajo")'
                ),
            },
            {
                "id": "b",
                "text": '=IF(A2>5%, "alto", IF(A2>=2%, "medio", "bajo"))',
            },
            {"id": "c", "text": '=IF(A2>5%, "alto", "medio", "bajo")'},
            {
                "id": "d",
                "text": (
                    '=IF(A2>5%; "alto"; IF(A2>=2%; "medio"); IF(A2<2%; "bajo"))'
                ),
            },
        ],
        "correct": "b",
        "explanation": "IF anidado correcto + orden lógico mayor → menor.",
    },
    {
        "id": "C1.7",
        "section": "excel",
        "prompt": (
            "Querés marcar como \"prioritario\" aquellos prospectos donde la empresa "
            "tiene más de 100 empleados Y (la industria es \"Fintech\" O la industria "
            "es \"SaaS\"). Caso contrario, marcar \"no\". empleados está en columna "
            "A, industria en B. ¿Cuál fórmula es correcta?"
        ),
        "choices": [
            {
                "id": "a",
                "text": '=IF(A2>100 AND B2="Fintech" OR B2="SaaS", "prioritario", "no")',
            },
            {
                "id": "b",
                "text": (
                    '=IF(AND(A2>100, OR(B2="Fintech", B2="SaaS")), "prioritario", "no")'
                ),
            },
            {
                "id": "c",
                "text": (
                    '=IF(OR(A2>100, AND(B2="Fintech", B2="SaaS")), "prioritario", "no")'
                ),
            },
            {
                "id": "d",
                "text": '=AND(A2>100, OR(B2="Fintech", B2="SaaS"))',
            },
        ],
        "correct": "b",
        "explanation": "Jerarquía AND-de-OR + sintaxis Excel (AND/OR como funciones).",
    },
    {
        "id": "C1.8",
        "section": "excel",
        "prompt": (
            "Tenés una tabla de 500 reuniones con columnas: SDR_asignado, Mes, "
            "Reuniones_agendadas (1 fila por reunión). Querés ver una matriz con SDR "
            "en filas, Mes en columnas, y total de reuniones en cada celda. ¿Cuál es "
            "la solución óptima?"
        ),
        "choices": [
            {
                "id": "a",
                "text": (
                    "Filtrar por SDR uno por uno y sumar manualmente cada mes."
                ),
            },
            {
                "id": "b",
                "text": (
                    "Una tabla dinámica con SDR_asignado en filas, Mes en columnas y "
                    "SUM(Reuniones_agendadas) en valores."
                ),
            },
            {
                "id": "c",
                "text": (
                    "Escribir una fórmula SUMIFS por cada combinación SDR-Mes (con 6 "
                    "SDRs × 12 meses = 72 fórmulas)."
                ),
            },
            {"id": "d", "text": "Exportar a Power BI."},
        ],
        "correct": "b",
        "explanation": "Tabla dinámica es la solución óptima cuando hay matriz pivotable.",
    },
    {
        "id": "C1.9",
        "section": "excel",
        "prompt": (
            "Estás en la celda A2 de una tabla con 5.000 filas. Querés seleccionar "
            "todo el rango desde A2 hasta el final de la columna A (A5000) en un solo "
            "gesto, sin scroll ni click. ¿Qué shortcut usás?"
        ),
        "choices": [
            {"id": "a", "text": "Click en A2 y arrastrar hasta A5000."},
            {"id": "b", "text": "Ctrl + Shift + Flecha abajo"},
            {"id": "c", "text": "Ctrl + A"},
            {"id": "d", "text": "Shift + End"},
        ],
        "correct": "b",
        "explanation": "Shortcut esencial de selección rápida hasta el final del rango contiguo.",
    },
    {
        "id": "C1.10",
        "section": "excel",
        "prompt": (
            "Tenés dos tablas: Pedidos (1 fila por pedido, columnas pedido_id, "
            "cliente_id, monto, 5.000 filas) y Clientes (1 fila por cliente_id, "
            "columnas cliente_id, nombre, ciudad, 1.200 filas). Querés agregar a "
            "Pedidos el nombre y ciudad del cliente, manteniendo la granularidad "
            "\"1 fila por pedido\". ¿Qué operación usás?"
        ),
        "choices": [
            {"id": "a", "text": "UNION de Pedidos y Clientes (apila las dos tablas)."},
            {
                "id": "b",
                "text": "LEFT JOIN de Pedidos hacia Clientes usando cliente_id como key.",
            },
            {
                "id": "c",
                "text": (
                    "INNER JOIN, que cambia la granularidad a \"1 fila por cliente\"."
                ),
            },
            {
                "id": "d",
                "text": (
                    "CROSS JOIN, que cruza cada pedido con cada cliente "
                    "(5.000 × 1.200 = 6 millones de filas)."
                ),
            },
        ],
        "correct": "b",
        "explanation": (
            "Distinguir UNION vs JOIN y mantener granularidad. UNION apila filas, "
            "INNER cambia granularidad, CROSS es absurdo."
        ),
    },
    {
        "id": "C1.11",
        "section": "excel",
        "prompt": (
            "En una columna Empresa hay nombres con problemas: \"Mercado Libre\", "
            "\"mercado libre\", \"MERCADO LIBRE\", \"Mercado  Libre\" (con doble "
            "espacio), \"Mercado Libre \" (con espacios al final). Querés contar "
            "cuántas empresas únicas reales hay. ¿Cuál es la secuencia correcta?"
        ),
        "choices": [
            {
                "id": "a",
                "text": "Aplicar filtro y borrar duplicados manualmente mirando a ojo.",
            },
            {
                "id": "b",
                "text": "Ordenar alfabéticamente y eliminar lo que parezca duplicado.",
            },
            {
                "id": "c",
                "text": (
                    "En una columna auxiliar aplicar TRIM(LOWER(A2)) (o equivalente) "
                    "para normalizar espacios y casing; recién entonces usar "
                    "\"Eliminar duplicados\" o =COUNTA(UNIQUE(...)) sobre la columna "
                    "limpia."
                ),
            },
            {"id": "d", "text": "Usar COUNT directamente sobre la columna original."},
        ],
        "correct": "c",
        "explanation": "Normalizar primero, contar después. Pensamiento estructurado sobre datos sucios.",
    },
    # ───────── C.2 — Lógica y números (5) ─────────
    {
        "id": "C2.1",
        "section": "logic",
        "prompt": (
            "Una tienda sube el precio de un producto 20% y después vende 15% menos "
            "unidades. ¿Qué pasó con sus ingresos totales?"
        ),
        "choices": [
            {"id": "a", "text": "Bajaron 5%"},
            {"id": "b", "text": "Subieron 5%"},
            {"id": "c", "text": "Subieron 2%"},
            {"id": "d", "text": "Quedaron iguales"},
        ],
        "correct": "c",
        "explanation": "1.20 × 0.85 = 1.02 → +2%. La \"intuición de empate\" es el error común.",
    },
    {
        "id": "C2.2",
        "section": "logic",
        "prompt": (
            "Una empresa duplica su fuerza de ventas y al año siguiente sus ingresos "
            "crecen solo 40% (en vez del 100% que se esperaría con el doble de "
            "vendedores). ¿Cuál de las siguientes explicaciones NO es coherente con "
            "ese resultado (es decir, no explica por qué los ingresos crecieron solo "
            "40%)?"
        ),
        "choices": [
            {
                "id": "a",
                "text": (
                    "Los nuevos vendedores tardaron en volverse productivos y "
                    "aportaron menos de lo esperado en el primer año."
                ),
            },
            {
                "id": "b",
                "text": (
                    "Los vendedores originales bajaron su productividad individual "
                    "por competencia interna (canibalización)."
                ),
            },
            {"id": "c", "text": "Los gastos subieron más rápido que los ingresos."},
            {
                "id": "d",
                "text": "El mercado no tenía capacidad de absorber el doble de ventas.",
            },
        ],
        "correct": "c",
        "explanation": (
            "Distinguir ingresos de utilidad. c habla de gastos, no explica brecha "
            "de ingresos."
        ),
    },
    {
        "id": "C2.3",
        "section": "logic",
        "prompt": (
            "Una empresa quiere decidir si abre una sucursal en Arequipa. Tiene 3 "
            "datos: (1) población de Arequipa, (2) ventas actuales en Lima, (3) "
            "costo promedio de abrir una sucursal. ¿Puede decidir con esos datos?"
        ),
        "choices": [
            {"id": "a", "text": "Sí, con regla de 3 sobre la población."},
            {
                "id": "b",
                "text": (
                    "No, falta información esencial como poder adquisitivo, "
                    "competencia local y tasa de conversión."
                ),
            },
            {"id": "c", "text": "Sí, porque las ventas en Lima son proyectables."},
            {"id": "d", "text": "Sí, basta calcular el break-even con el costo."},
        ],
        "correct": "b",
        "explanation": "Honestidad intelectual: reconocer que faltan datos.",
    },
    {
        "id": "C2.4",
        "section": "logic",
        "prompt": (
            "Un vendedor contacta 1.000 prospectos al mes y cierra 10 ventas (1%). "
            "Si su objetivo es cerrar 25 ventas al mes, ¿qué tiene más impacto?"
        ),
        "choices": [
            {
                "id": "a",
                "text": "Contactar 2.500 prospectos manteniendo 1% de conversión.",
            },
            {
                "id": "b",
                "text": "Subir la conversión a 2.5% manteniendo 1.000 prospectos.",
            },
            {
                "id": "c",
                "text": "Ambas son igual de buenas porque llegan al mismo número.",
            },
            {
                "id": "d",
                "text": (
                    "Depende del costo de cada palanca — con solo esos datos no "
                    "puedo decidir."
                ),
            },
        ],
        "correct": "d",
        "explanation": (
            "Pregunta-trampa de honestidad. a y b dan el mismo resultado matemático "
            "pero con costos muy distintos. d es la respuesta madura."
        ),
    },
    {
        "id": "C2.5",
        "section": "logic",
        "prompt": (
            "Datos de una campaña de ventas:\n"
            "• Prospectos contactados: 2.000\n"
            "• Respondieron: 40\n"
            "• Agendaron reunión: 20\n"
            "• Cerraron venta: 5\n"
            "¿Cuál es la tasa de conversión de \"respuesta a reunión\"?"
        ),
        "choices": [
            {"id": "a", "text": "1%"},
            {"id": "b", "text": "2%"},
            {"id": "c", "text": "25%"},
            {"id": "d", "text": "50%"},
        ],
        "correct": "d",
        "explanation": "20/40 = 50%. Cada tasa se calcula sobre el paso anterior, no sobre el total.",
    },
    # ───────── C.3 — Lectura de un negocio (5) ─────────
    # Caso base: Café Luna (8 cafeterías en Lima, ticket S/.18, 70% ventas 7-10am)
    {
        "id": "C3.1",
        "section": "business",
        "prompt": (
            "[Caso Café Luna] ¿Cuál es la mayor palanca de crecimiento de Café Luna "
            "en el corto plazo?"
        ),
        "choices": [
            {"id": "a", "text": "Abrir más tiendas en nuevas zonas de Lima."},
            {
                "id": "b",
                "text": "Aumentar las ventas después de las 10am (hoy solo 30% del día).",
            },
            {"id": "c", "text": "Subir el ticket promedio con productos más caros."},
            {"id": "d", "text": "Exportar el modelo a provincias."},
        ],
        "correct": "b",
        "explanation": (
            "Palanca con menor inversión y mayor impacto inmediato: ya tiene tiendas "
            "y empleados, solo falta tráfico en horas muertas."
        ),
    },
    {
        "id": "C3.2",
        "section": "business",
        "prompt": "[Caso Café Luna] ¿Cuál es el mayor riesgo estructural?",
        "choices": [
            {"id": "a", "text": "Que abra una nueva cafetería en frente."},
            {
                "id": "b",
                "text": (
                    "Que las empresas de sus zonas sigan con trabajo remoto y bajen "
                    "los clientes corporativos."
                ),
            },
            {"id": "c", "text": "Que suba el precio del café como commodity."},
            {"id": "d", "text": "Que sus empleados part-time pidan ser full-time."},
        ],
        "correct": "b",
        "explanation": (
            "Riesgo estructural, no táctico: 8 tiendas en zonas de oficinas + 70% "
            "ventas en desayuno = dependencia del cliente corporativo."
        ),
    },
    {
        "id": "C3.3",
        "section": "business",
        "prompt": (
            "[Caso Café Luna] El delivery propio que lanzaron en 2024, ¿qué problema "
            "principal resuelve?"
        ),
        "choices": [
            {
                "id": "a",
                "text": "Les da una nueva fuente de ingresos además del local.",
            },
            {
                "id": "b",
                "text": (
                    "Les permite capturar la demanda del 30% del día que antes se "
                    "perdía."
                ),
            },
            {
                "id": "c",
                "text": "Reduce dependencia del cliente corporativo de oficina.",
            },
            {
                "id": "d",
                "text": (
                    "Todas las anteriores, pero la principal es la c porque ataca el "
                    "riesgo estructural."
                ),
            },
        ],
        "correct": "d",
        "explanation": "Jerarquización: ataca el riesgo estructural identificado.",
    },
    {
        "id": "C3.4",
        "section": "business",
        "prompt": (
            "[Caso Café Luna] Si fueras el dueño y tuvieras $50.000 USD para invertir "
            "en UNA sola cosa:"
        ),
        "choices": [
            {"id": "a", "text": "Abrir una novena tienda en una nueva zona."},
            {"id": "b", "text": "Campaña de marketing digital para delivery."},
            {
                "id": "c",
                "text": (
                    "Rediseñar el menú de tarde/noche para subir ventas en horas "
                    "muertas."
                ),
            },
            {"id": "d", "text": "Renovar el diseño de las 8 tiendas actuales."},
        ],
        "correct": "c",
        "explanation": "Máximo retorno sobre la palanca ya identificada en la pregunta 1.",
    },
    {
        "id": "C3.5",
        "section": "business",
        "prompt": (
            "[Caso Café Luna] ¿Qué dato FALTA en este brief que sería lo más útil "
            "para decidir estrategia?"
        ),
        "choices": [
            {"id": "a", "text": "El margen bruto por producto."},
            {"id": "b", "text": "El nombre del dueño."},
            {"id": "c", "text": "El año exacto en que abrieron la primera tienda."},
            {"id": "d", "text": "Cuántos empleados full-time tienen exactamente."},
        ],
        "correct": "a",
        "explanation": "Criterio sobre qué datos importan para tomar decisiones.",
    },
    # ───────── C.4 — Comprensión de texto denso (5) ─────────
    {
        "id": "C4.1",
        "section": "comprehension",
        "prompt": (
            "Según el análisis de CB Insights que cita el texto, ¿qué porcentaje de "
            "las startups fallidas tenía producto con demanda real pero no supo "
            "encontrarla a costo sostenible?"
        ),
        "choices": [
            {"id": "a", "text": "25%"},
            {"id": "b", "text": "35%"},
            {"id": "c", "text": "50%"},
            {"id": "d", "text": "65%"},
        ],
        "correct": "b",
        "explanation": "Literal. Párrafo 2 del texto base.",
    },
    {
        "id": "C4.2",
        "section": "comprehension",
        "prompt": (
            "El texto implica que \"falta de capital\" es mencionada por fundadores "
            "como causa del fracaso, pero en realidad:"
        ),
        "choices": [
            {
                "id": "a",
                "text": (
                    "Es la verdadera causa principal, aunque los fundadores no lo "
                    "sepan."
                ),
            },
            {
                "id": "b",
                "text": (
                    "Suele ser un síntoma de problemas anteriores (falta de progreso "
                    "en métricas clave), más que una causa raíz."
                ),
            },
            {"id": "c", "text": "Solo aplica a startups sin inversionistas."},
            {
                "id": "d",
                "text": "Es una causa independiente del desempeño del equipo.",
            },
        ],
        "correct": "b",
        "explanation": "Inferencia del párrafo 2: \"suele ser un síntoma de lo primero\".",
    },
    {
        "id": "C4.3",
        "section": "comprehension",
        "prompt": (
            "De acuerdo con el texto, ¿qué tienen en común las causas citadas por "
            "Wasserman (conflicto entre fundadores) y por Ries (escalar antes de "
            "tiempo)?"
        ),
        "choices": [
            {"id": "a", "text": "Ambas son problemas de financiamiento."},
            {"id": "b", "text": "Ambas son problemas de producto."},
            {
                "id": "c",
                "text": (
                    "Ambas son problemas que el equipo podía prevenir con mejor "
                    "juicio interno, no determinados por el mercado."
                ),
            },
            {
                "id": "d",
                "text": "Ambas afectan más a las startups pequeñas que a las grandes.",
            },
        ],
        "correct": "c",
        "explanation": (
            "Inferencia: el autor las agrupa bajo la tesis de fracasos \"operativos "
            "y humanos\"."
        ),
    },
    {
        "id": "C4.4",
        "section": "comprehension",
        "prompt": (
            "¿Cuál es el argumento del texto que tiene la evidencia más débil?"
        ),
        "choices": [
            {
                "id": "a",
                "text": (
                    "El dato de CB Insights sobre el 35% (basado en análisis "
                    "cuantitativo de 250+ autopsias)."
                ),
            },
            {
                "id": "b",
                "text": (
                    "La hipótesis de Wasserman sobre conflictos entre cofundadores "
                    "(basada en datos de Harvard)."
                ),
            },
            {
                "id": "c",
                "text": (
                    "La tesis de Graham sobre la \"determinación\" como predictor "
                    "(admitida por el texto como potencialmente circular)."
                ),
            },
            {
                "id": "d",
                "text": (
                    "La crítica de los economistas a Graham (citada como \"algunos "
                    "economistas\" sin fuente específica)."
                ),
            },
        ],
        "correct": "c",
        "explanation": (
            "El propio texto reconoce que el argumento de Graham es el de mayor "
            "riesgo de circularidad."
        ),
    },
    {
        "id": "C4.5",
        "section": "comprehension",
        "prompt": (
            "Imaginá que sos inversionista y tenés que elegir entre dos startups del "
            "mismo sector, con productos de calidad similar y capital similar. "
            "Según el texto, ¿qué mirarías primero para decidir?"
        ),
        "choices": [
            {"id": "a", "text": "El tamaño del mercado potencial."},
            {
                "id": "b",
                "text": (
                    "El comportamiento del equipo fundador bajo presión y su "
                    "capacidad de resolver desalineaciones."
                ),
            },
            {"id": "c", "text": "El número de competidores directos."},
            {"id": "d", "text": "La experiencia técnica de los fundadores."},
        ],
        "correct": "b",
        "explanation": "Aplicación directa del penúltimo párrafo del texto base.",
    },
]


COMPREHENSION_TEXT = """Por qué fracasan las startups

Cuando una startup cierra, es tentador atribuirlo a mala suerte o a un mercado hostil. La evidencia acumulada, sin embargo, apunta a otra dirección: la mayoría de las startups muere por causas predecibles, y varias de ellas son consecuencia directa de decisiones del fundador.

Un análisis de CB Insights sobre más de 250 autopsias de startups fallidas identifica como causa más frecuente citada por los propios fundadores la falta de mercado para el producto. Es la explicación más cómoda: "nadie lo quería". Pero esa misma investigación muestra que, en el 35% de los casos, el producto sí tenía demanda real — lo que fallaba era la capacidad del equipo para encontrar esa demanda a un costo sostenible. El segundo motivo más citado, la falta de capital, suele ser un síntoma de lo primero más que una causa independiente: los inversionistas dejan de poner dinero cuando no ven progreso en métricas clave.

Otra explicación recurrente es el conflicto entre fundadores. Noam Wasserman, profesor de Harvard, documentó en The Founder's Dilemmas que el 65% de las startups en su base de datos atravesaron al menos una disputa grave entre cofundadores, y que aquellas que no lograron resolver esa disputa tuvieron una probabilidad significativamente mayor de cerrar en los primeros cinco años. La hipótesis de Wasserman es que las startups no fracasan por falta de talento, sino por exceso de desalineación temprana.

Una tercera causa, más sutil, es lo que Eric Ries denomina "la trampa de escalar antes de tiempo". En The Lean Startup, Ries argumenta que muchas startups con producto prometedor mueren no porque el producto sea malo, sino porque invierten en infraestructura, marketing y headcount antes de tener evidencia sólida de que su modelo funciona. El dinero se acaba mientras el equipo todavía está aprendiendo.

Paul Graham, cofundador de Y Combinator, ha señalado que el denominador común de las startups que sobreviven es uno solo: la capacidad del fundador de seguir operando cuando las señales son ambiguas. En sus ensayos repite que el factor predictor no es la calidad de la idea ni el tamaño del mercado, sino la "determinación" del equipo — que Graham define como la mezcla de perseverancia y capacidad de ajustar sin romperse. Sin embargo, la tesis de Graham tiene críticos. Algunos economistas argumentan que atribuir el éxito a la "determinación" es circular: solo se identifica como determinados a los que ya sobrevivieron, y la causalidad queda difusa. Esta crítica es relevante cuando se la lleva al extremo, pero omite un punto: entre dos startups con producto similar y capital similar, la variable que los propios inversionistas reportan como decisiva es el comportamiento del equipo bajo presión.

La lección útil para un fundador es menos heroica que inspiradora: las startups fracasan, en su mayoría, por razones operativas y humanas antes que por mala suerte. Reconocer eso cambia el foco de "encontrar la idea perfecta" a "construir un equipo que pueda ejecutar, discutir y corregir sin romperse"."""


def total_question_count() -> int:
    return len(MCQ)


def section_counts() -> dict[str, int]:
    out: dict[str, int] = {}
    for q in MCQ:
        out[q["section"]] = out.get(q["section"], 0) + 1
    return out
