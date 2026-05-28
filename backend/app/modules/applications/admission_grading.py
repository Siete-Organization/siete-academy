"""Grading + auto-descarte de Etapa 1 — Prueba de admisión.

Reglas (Documento Maestro v1.2):
- mcq_score < 60% → rejected_mcq_total
- mcq_excel_score < 40% (< 5 de 11) → rejected_mcq_excel
- Cualquier respuesta abierta en blanco o bajo mínimo de palabras → rejected_text
- Completó la prueba en < 15 minutos → rejected_speed
- Si pasa todos los filtros → passed_stage_1
"""
from datetime import datetime, timedelta

from app.modules.applications.admission_questions_es import MCQ, OPEN_PROMPTS

MCQ_TOTAL_PASS_PCT = 60
MCQ_EXCEL_PASS_PCT = 40
MIN_COMPLETION_MINUTES = 15


def _word_count(text: str | None) -> int:
    if not text:
        return 0
    return len(text.strip().split())


def grade_mcq(answers: dict[str, str] | None) -> dict[str, int]:
    """Devuelve mcq_score y mcq_excel_score como porcentajes (0-100)."""
    if not answers:
        return {"mcq_score": 0, "mcq_excel_score": 0}
    correct_total = 0
    correct_excel = 0
    excel_total = 0
    for q in MCQ:
        if q["section"] == "excel":
            excel_total += 1
        given = answers.get(q["id"])
        if given is not None and given == q["correct"]:
            correct_total += 1
            if q["section"] == "excel":
                correct_excel += 1
    total = len(MCQ)
    return {
        "mcq_score": round((correct_total / total) * 100) if total else 0,
        "mcq_excel_score": (
            round((correct_excel / excel_total) * 100) if excel_total else 0
        ),
    }


def _open_answer_violations(answers_by_id: dict[str, str]) -> list[str]:
    """Devuelve lista de question_ids con violación de mín/máx palabras o blanco."""
    violations: list[str] = []
    for prompt in OPEN_PROMPTS:
        qid = prompt["id"]
        text = answers_by_id.get(qid, "")
        wc = _word_count(text)
        if wc < prompt["min_words"] or wc > prompt["max_words"]:
            violations.append(qid)
    return violations


def decide_auto_decision(
    open_answers: dict[str, str],
    mcq_score: int,
    mcq_excel_score: int,
    started_at: datetime | None,
    submitted_at: datetime,
) -> str:
    """Aplica reglas en orden de prioridad y devuelve el primer fallo."""
    # 1. Texto en blanco / fuera de rango de palabras
    if _open_answer_violations(open_answers):
        return "rejected_text"
    # 2. MCQ Excel debajo del piso (filtro fuerte de pensamiento estructurado)
    if mcq_excel_score < MCQ_EXCEL_PASS_PCT:
        return "rejected_mcq_excel"
    # 3. MCQ total debajo del piso
    if mcq_score < MCQ_TOTAL_PASS_PCT:
        return "rejected_mcq_total"
    # 4. Speed check — completó todo en menos de 15 minutos (imposible hacerlo bien)
    if started_at is not None:
        if submitted_at - started_at < timedelta(minutes=MIN_COMPLETION_MINUTES):
            return "rejected_speed"
    return "passed_stage_1"
