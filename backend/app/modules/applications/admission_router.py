"""Endpoint público que sirve el contenido de la Prueba de admisión Etapa 1.

El front carga este JSON al abrir /apply, randomiza orden de preguntas/opciones
del lado cliente y envía las respuestas en POST /applications. El control de
tiempo es server-side: started_at/submitted_at + el filtro min_completion_minutes
(no hay timer por pregunta en el cliente).

ES-only por ahora; EN/PT se añaden en PRs futuros cuando llegue el contenido.
"""
from fastapi import APIRouter, HTTPException, Query

from app.modules.applications.admission_questions_es import (
    COMPREHENSION_TEXT,
    MCQ,
    OPEN_PROMPTS,
)

router = APIRouter()


@router.get("/questions")
def get_admission_questions(locale: str = Query("es")) -> dict:
    """Devuelve preguntas + texto base sin las explicaciones internas (`explanation`)."""
    if locale != "es":
        raise HTTPException(
            status_code=404,
            detail=f"Locale '{locale}' not yet available — only 'es' for now",
        )
    return {
        "locale": "es",
        "open_prompts": OPEN_PROMPTS,
        "comprehension_text": COMPREHENSION_TEXT,
        "mcq": [
            {
                "id": q["id"],
                "section": q["section"],
                "prompt": q["prompt"],
                "choices": q["choices"],
            }
            for q in MCQ
        ],
        "rules": {
            "mcq_total_pass_pct": 60,
            "mcq_excel_pass_pct": 40,
            "seconds_per_question": 90,
            "min_completion_minutes": 15,
        },
    }
