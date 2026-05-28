"""applications: campos MCQ + auto-descarte de Etapa 1 admisión

Revision ID: 0007_admission_mcq
Revises: 0006_lesson_video_url
Create Date: 2026-05-28

Implementa la Etapa 1 de la Prueba de admisión (formulario + 3 abiertas + 26 MCQ).

- applications.started_at: timestamp para detectar bots/lazy (< 15 min = descarte)
- applications.mcq_answers: respuestas del aspirante {question_id: choice_id}
- applications.mcq_score: % total acierto MCQ (0-100)
- applications.mcq_excel_score: % acierto solo sección Excel/BBDD (0-100)
- applications.auto_decision: passed_stage_1 | rejected_text | rejected_mcq_total |
  rejected_mcq_excel | rejected_speed | NULL (legacy/pre-MCQ)

Idempotente: chequea con inspect() si cada columna/índice ya existe antes de
crearlos. Esto cubre el caso en que un seed haya corrido `create_all()` en
una versión anterior del modelo y haya creado el índice de antemano
(incidente 2026-05-28, hotfix PR #13).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision: str = "0007_admission_mcq"
down_revision: Union[str, None] = "0006_lesson_video_url"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


COLUMNS: list[tuple[str, sa.Column]] = [
    ("started_at", sa.Column("started_at", sa.DateTime(), nullable=True)),
    ("mcq_answers", sa.Column("mcq_answers", sa.JSON(), nullable=True)),
    ("mcq_score", sa.Column("mcq_score", sa.Integer(), nullable=True)),
    ("mcq_excel_score", sa.Column("mcq_excel_score", sa.Integer(), nullable=True)),
    ("auto_decision", sa.Column("auto_decision", sa.String(40), nullable=True)),
]


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    existing_cols = {c["name"] for c in inspector.get_columns("applications")}
    for name, column in COLUMNS:
        if name not in existing_cols:
            op.add_column("applications", column)

    existing_indexes = {idx["name"] for idx in inspector.get_indexes("applications")}
    if "ix_applications_auto_decision" not in existing_indexes:
        op.create_index(
            "ix_applications_auto_decision", "applications", ["auto_decision"]
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)

    existing_indexes = {idx["name"] for idx in inspector.get_indexes("applications")}
    if "ix_applications_auto_decision" in existing_indexes:
        op.drop_index("ix_applications_auto_decision", table_name="applications")

    existing_cols = {c["name"] for c in inspector.get_columns("applications")}
    for name, _ in reversed(COLUMNS):
        if name in existing_cols:
            op.drop_column("applications", name)
