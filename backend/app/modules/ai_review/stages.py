"""Pipeline stages for AI-assisted review.

Uses the auditable pipeline pattern (`core/pipeline.py`): each stage receives
a defined input (ctx), produces a defined output dict that's merged into ctx,
and every request/response to Anthropic is persisted in `ai_call_logs`.
"""

from __future__ import annotations

import json
import re
from typing import Any

from sqlalchemy.orm import Session

from app.core.anthropic_client import AnthropicClient
from app.core.logging import get_logger
from app.core.pipeline import Stage
from app.modules.applications.models import Application
from app.modules.assessments.models import AIReview, Assessment, Submission
from app.modules.audit.models import StageRun

log = get_logger("app.ai_review")


def _current_stage_run_id(db: Session, pipeline_run_id: int) -> int | None:
    """Returns the in-progress StageRun id for the given pipeline run, if any."""
    sr = (
        db.query(StageRun)
        .filter(StageRun.pipeline_run_id == pipeline_run_id, StageRun.status == "running")
        .order_by(StageRun.created_at.desc())
        .first()
    )
    return sr.id if sr else None


def _parse_json_response(raw: str) -> dict[str, Any]:
    """Claude returns text that should contain a JSON block. Be lenient about fences."""
    m = re.search(r"\{.*\}", raw, flags=re.DOTALL)
    if not m:
        return {"_raw": raw[:2000]}
    try:
        return json.loads(m.group(0))
    except json.JSONDecodeError:
        return {"_raw": raw[:2000]}


# ──────────────────────────────────────────────────────────────────────────────
# Application scoring
# ──────────────────────────────────────────────────────────────────────────────

APPLICATION_SYSTEM_PROMPT = """\
Eres un Director de HR senior revisando una aplicación para Siete Academy,
un programa intensivo de formación SDR. Evalúas:

1. Claridad de pensamiento y comunicación escrita
2. Motivación real vs. motivación superficial
3. Compromiso demostrable (horas/semana realistas, logros concretos)
4. Fit con ventas B2B (resiliencia, orientación a resultados)

Entregas tu análisis como JSON válido con esta forma exacta:
{
  "score": <entero 0-100>,
  "strengths": [<string>, ...],   // 2-4 fortalezas puntuales
  "concerns": [<string>, ...],    // 0-4 banderas o dudas
  "recommendation": "accept" | "review" | "reject",
  "notes": "<síntesis en 2-3 frases para el admin>"
}

No inventes hechos que no estén en la aplicación. Si la aplicación es corta o
evasiva, eso por sí solo es una señal negativa.
"""


class ScoreApplicationStage(Stage):
    name = "score_application"

    def __init__(self) -> None:
        self.client = AnthropicClient()

    def run(self, db: Session, ctx: dict) -> dict:
        application_id = ctx["application_id"]
        pipeline_run_id = ctx["pipeline_run_id"]
        app = db.get(Application, application_id)
        if app is None:
            raise ValueError(f"Application {application_id} not found")

        answers_block = "\n\n".join(
            f"### {qid}\n{text}" for qid, text in app.answers.items()
        )
        user_msg = (
            f"Idioma de respuesta: {app.locale}\n"
            f"Nombre: {app.applicant_name}\n"
            f"Email: {app.applicant_email}\n"
            f"Video: {app.video_url or '(sin video)'}\n\n"
            f"Respuestas:\n{answers_block}"
        )

        stage_run_id = _current_stage_run_id(db, pipeline_run_id)
        resp = self.client.messages(
            db,
            messages=[{"role": "user", "content": user_msg}],
            system=APPLICATION_SYSTEM_PROMPT,
            max_tokens=1024,
            temperature=0.3,
            stage_run_id=stage_run_id,
            purpose="application_scoring",
        )
        text = "".join(
            block.text for block in resp.content if getattr(block, "type", "") == "text"
        )
        data = _parse_json_response(text)

        score = int(data.get("score") or 0)
        notes = data.get("notes") or ""
        app.ai_score = score
        app.ai_notes = notes
        db.commit()

        log.info(
            "ai.application_scored",
            extra={
                "application_id": application_id,
                "score": score,
                "recommendation": data.get("recommendation"),
            },
        )
        return {"score": score, "recommendation": data.get("recommendation"), "ai_data": data}


# ──────────────────────────────────────────────────────────────────────────────
# Submission review (draft feedback visible only to the teacher)
# ──────────────────────────────────────────────────────────────────────────────

SUBMISSION_SYSTEM_PROMPT = """\
Eres un coach de ventas senior evaluando la entrega de un alumno SDR.
Tu trabajo NO es darle feedback al alumno — eso lo hace el profesor humano.
Tu trabajo es entregar al profesor un borrador editable con:

1. Diagnóstico técnico (qué funciona, qué no)
2. Sugerencias específicas (no genéricas) con ejemplos
3. Una calificación sugerida (0-100)

Entregas JSON válido:
{
  "draft_feedback": "<markdown con diagnóstico + sugerencias, 150-400 palabras>",
  "score_suggestion": <0-100>,
  "key_strengths": [<string>, ...],
  "key_gaps": [<string>, ...]
}

Sé honesto y directo. Si la entrega está vacía o es de baja calidad, dilo.
"""


class ReviewSubmissionStage(Stage):
    name = "review_submission"

    def __init__(self) -> None:
        self.client = AnthropicClient()

    def run(self, db: Session, ctx: dict) -> dict:
        submission_id = ctx["submission_id"]
        pipeline_run_id = ctx["pipeline_run_id"]
        sub = db.get(Submission, submission_id)
        if sub is None:
            raise ValueError(f"Submission {submission_id} not found")
        assessment = db.get(Assessment, sub.assessment_id)
        if assessment is None:
            raise ValueError(f"Assessment {sub.assessment_id} not found")

        user_msg = (
            f"Tipo de prueba: {assessment.type}\n"
            f"Título: {assessment.title}\n"
            f"Config (prompt/instructions): {json.dumps(assessment.config, ensure_ascii=False)}\n\n"
            f"Entrega del alumno (payload):\n{json.dumps(sub.payload, ensure_ascii=False, indent=2)}"
        )
        if sub.file_url:
            user_msg += f"\n\nArchivo adjunto: {sub.file_url}"

        stage_run_id = _current_stage_run_id(db, pipeline_run_id)
        resp = self.client.messages(
            db,
            messages=[{"role": "user", "content": user_msg}],
            system=SUBMISSION_SYSTEM_PROMPT,
            max_tokens=1500,
            temperature=0.4,
            stage_run_id=stage_run_id,
            purpose="submission_review",
        )
        text = "".join(
            block.text for block in resp.content if getattr(block, "type", "") == "text"
        )
        data = _parse_json_response(text)

        draft = data.get("draft_feedback") or text[:2000]
        score_sug = data.get("score_suggestion")
        model_used = self.client.model

        # Upsert so re-runs overwrite rather than duplicate
        ai_review = db.query(AIReview).filter_by(submission_id=submission_id).first()
        if ai_review is None:
            ai_review = AIReview(
                submission_id=submission_id,
                draft_feedback=draft,
                score_suggestion=float(score_sug) if score_sug is not None else None,
                model_used=model_used,
            )
            db.add(ai_review)
        else:
            ai_review.draft_feedback = draft
            ai_review.score_suggestion = float(score_sug) if score_sug is not None else None
            ai_review.model_used = model_used
        db.commit()

        log.info(
            "ai.submission_reviewed",
            extra={"submission_id": submission_id, "score_suggestion": score_sug},
        )
        return {"score_suggestion": score_sug}
