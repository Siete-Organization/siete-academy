"""Definiciones de cada stage del path post-Academy (Documento Maestro Parte IX).

Constantes legibles que el front consume vía `GET /practica/stages` para
mostrarle al alumno qué le espera en cada paso. Single source of truth.
"""

STAGE_DEFINITIONS: list[dict] = [
    {
        "key": "e1_invited",
        "label": "Invitado a Etapa 1",
        "compensation": "Sin compensación",
        "duration_weeks": "—",
        "summary": "Recibiste invitación formal a Etapa 1. Tenés que confirmar disponibilidad y residencia fiscal (Deel) para arrancar.",
        "criteria": [],
    },
    {
        "key": "e1_active",
        "label": "Etapa 1 — Práctica inicial",
        "compensation": "Sin compensación · acceso a infra + mentoría",
        "duration_weeks": "4-6",
        "summary": "Operás cuentas reales bajo supervisión del SDR Manager. Onboarding técnico en las primeras 2 semanas; filtro humano obligatorio hasta Semana 2 y luego soltado gradual.",
        "criteria": [
            "Volumen ejecutado ≥80% del target de un SDR junior",
            "Calidad del copy: 3+ de 5 mensajes correctos al cabo de Semana 3",
            "Capacidad de diagnóstico de anomalías sin ayuda al cabo de Semana 4",
            "Incorpora feedback sin repetir errores",
            "Colaboración: integrado al equipo, sin operar en silo",
            "Sostiene foco tras rechazo repetido — no pierde ritmo al día 20",
        ],
        "decision_rule": "5 de 6 criterios en \"sí claro\" al final de Semana 4 → paso a Etapa 2. 4 o menos → +2 semanas con plan correctivo. Si Semana 6 sin paso, cierre con Camino B.",
    },
    {
        "key": "e2_active",
        "label": "Etapa 2 — Práctica remunerada",
        "compensation": "USD 400/mes (Deel contractor)",
        "duration_weeks": "8-12 (máx 16)",
        "summary": "Contrato Deel formal. Autonomía operativa creciente: revisión asincrónica → muestreo → solo casos complejos. Responsabilidad parcial por KPIs personales declarados.",
        "criteria": [
            "Target individual: 80%+ en 2 de los 3 meses",
            "Calidad mantenida (quality score del SDR Manager ≥7/10 promedio)",
            "Autonomía: opera sin supervisión continua, escala lo apropiado",
            "Iniciativa: propone al menos 1 hipótesis de mejora testeable",
            "Fit cultural sostenido (feedback 360 del Manager + 1 par)",
        ],
        "decision_rule": "5 criterios cumplidos + cupo T2 disponible → paso a Etapa 3. Sin cupo: extensión o cierre con carta de recomendación.",
    },
    {
        "key": "e3_t2_active",
        "label": "Etapa 3 T2 — SDR junior",
        "compensation": "USD 500-950/mes (banda)",
        "duration_weeks": "Indefinida",
        "summary": "Contrato Deel renovado. Asignación a cliente como SDR primario. El monto exacto dentro de la banda lo define el Delivery Manager según desempeño previo + complejidad del cliente.",
        "criteria": [
            "Target sostenido cumplido",
            "Track record de mejora continua + iniciativa",
            "Capacidad de mentoría informal a practicantes nuevos",
        ],
        "decision_rule": "6-12 meses exitosos como T2 → evaluación para T1.",
    },
    {
        "key": "e3_t1_active",
        "label": "Etapa 3 T1 — SDR senior",
        "compensation": "USD 950-1.250/mes (banda)",
        "duration_weeks": "Indefinida",
        "summary": "Senior SDR de planta. Path declarado hacia roles más complejos (AE, Senior SDR, etc.) según contexto del cliente.",
        "criteria": [],
    },
    {
        "key": "closed_camino_b",
        "label": "Camino B — Carta de recomendación",
        "compensation": "—",
        "duration_weeks": "—",
        "summary": "Cierre honesto. Sin cláusula de exclusividad: podés postular a cualquier empresa. Llevás carta de recomendación formal + acceso indefinido a la red de ex-alumni (WhatsApp moderado por el profesor).",
        "criteria": [],
    },
    {
        "key": "declined",
        "label": "Invitación rechazada / no elegible",
        "compensation": "—",
        "duration_weeks": "—",
        "summary": "No continuás con Camino A (rechazaste la invitación o tu residencia fiscal no es soportada por Deel — VE/CU). Camino B disponible: carta de recomendación + red de alumni.",
        "criteria": [],
    },
]


def stage_definition(stage_key: str) -> dict | None:
    for s in STAGE_DEFINITIONS:
        if s["key"] == stage_key:
            return s
    return None
