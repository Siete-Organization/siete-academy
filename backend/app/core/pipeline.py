"""Pipeline stages with auditable persistence.

Each PipelineRun has an ID. Each Stage within a run persists its input, output,
and result/error. No silent failures — every stage is captured with full context.

Usage:
    class ScoreApplicationStage(Stage):
        name = "score_application"

        def run(self, db, ctx: dict) -> dict:
            # ctx is the pipeline context dict; return dict is merged into ctx
            ...

    run_pipeline(db, "application_scoring", ctx={"application_id": 123}, stages=[...])
"""

from __future__ import annotations

import logging
import traceback
from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.orm import Session

log = logging.getLogger(__name__)


class Stage(ABC):
    name: str = "unnamed"

    @abstractmethod
    def run(self, db: Session, ctx: dict[str, Any]) -> dict[str, Any]:
        """Receive a defined input (ctx), produce a defined output (dict merged into ctx)."""


def run_pipeline(
    db: Session,
    pipeline_name: str,
    ctx: dict[str, Any],
    stages: list[Stage],
    *,
    existing_run_id: int | None = None,
) -> dict[str, Any]:
    """Execute stages sequentially, persisting every step.

    If `existing_run_id` is provided, joins an already-opened PipelineRun
    (useful when the caller needs the id before invoking the pipeline, e.g.
    to pass it into stage contexts). Otherwise creates a new one.

    Returns the final ctx. Raises on first stage failure, after persisting.
    """
    from app.modules.audit.models import PipelineRun, StageRun

    if existing_run_id is not None:
        run = db.get(PipelineRun, existing_run_id)
        if run is None:
            raise ValueError(f"PipelineRun {existing_run_id} not found")
    else:
        run = PipelineRun(name=pipeline_name, initial_ctx=dict(ctx), status="running")
        db.add(run)
        db.commit()
        db.refresh(run)

    for stage in stages:
        stage_run = StageRun(
            pipeline_run_id=run.id,
            name=stage.name,
            input_payload=dict(ctx),
            status="running",
        )
        db.add(stage_run)
        db.commit()
        db.refresh(stage_run)

        try:
            output = stage.run(db, ctx) or {}
            ctx.update(output)
            stage_run.output_payload = output
            stage_run.status = "succeeded"
            db.commit()
        except Exception as e:
            stage_run.status = "failed"
            stage_run.error = f"{type(e).__name__}: {e}\n{traceback.format_exc()}"
            run.status = "failed"
            run.final_ctx = dict(ctx)
            db.commit()
            log.exception("Pipeline '%s' failed at stage '%s'", pipeline_name, stage.name)
            raise

    run.status = "succeeded"
    run.final_ctx = dict(ctx)
    db.commit()
    return ctx
