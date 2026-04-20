"""Celery tasks for AI review pipelines.

Kicks off the audited pipeline from `stages.py`. All HTTP calls to Anthropic
are logged in `ai_call_logs` and each stage in `stage_runs`.
"""

from __future__ import annotations

from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.core.logging import get_logger
from app.core.pipeline import run_pipeline
from app.modules.ai_review.stages import ReviewSubmissionStage, ScoreApplicationStage
from app.modules.audit.models import PipelineRun

log = get_logger("app.ai_review.tasks")


def _pipeline_run_id(db, name: str, initial_ctx: dict) -> int:
    """Open a PipelineRun up-front so stages can reference it."""
    run = PipelineRun(name=name, initial_ctx=initial_ctx, status="running")
    db.add(run)
    db.commit()
    db.refresh(run)
    return run.id


@celery_app.task(name="ai_review.score_application")
def score_application_task(application_id: int) -> None:
    db = SessionLocal()
    try:
        pid = _pipeline_run_id(
            db, "application_scoring", {"application_id": application_id}
        )
        ctx = {"application_id": application_id, "pipeline_run_id": pid}
        try:
            run_pipeline(
                db,
                "application_scoring",
                ctx,
                [ScoreApplicationStage()],
                existing_run_id=pid,
            )
        except Exception:
            log.exception(
                "ai.application_scoring_failed", extra={"application_id": application_id}
            )
    finally:
        db.close()


@celery_app.task(name="ai_review.review_submission")
def review_submission_task(submission_id: int) -> None:
    db = SessionLocal()
    try:
        pid = _pipeline_run_id(
            db, "submission_review", {"submission_id": submission_id}
        )
        ctx = {"submission_id": submission_id, "pipeline_run_id": pid}
        try:
            run_pipeline(
                db,
                "submission_review",
                ctx,
                [ReviewSubmissionStage()],
                existing_run_id=pid,
            )
        except Exception:
            log.exception(
                "ai.submission_review_failed", extra={"submission_id": submission_id}
            )
    finally:
        db.close()
