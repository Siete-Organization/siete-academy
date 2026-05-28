"""applications: campos MCQ + auto-descarte de Etapa 1 admisión

Revision ID: 0007_admission_mcq
Revises: 0006_lesson_translation_video_url
Create Date: 2026-05-28

Implementa la Etapa 1 de la Prueba de admisión (formulario + 3 abiertas + 26 MCQ).

- applications.started_at: timestamp para detectar bots/lazy (< 15 min = descarte)
- applications.mcq_answers: respuestas del aspirante {question_id: choice_id}
- applications.mcq_score: % total acierto MCQ (0-100)
- applications.mcq_excel_score: % acierto solo sección Excel/BBDD (0-100)
- applications.auto_decision: passed_stage_1 | rejected_text | rejected_mcq_total |
  rejected_mcq_excel | rejected_speed | NULL (legacy/pre-MCQ)

Todo additive y nullable para no romper applications existentes.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0007_admission_mcq"
down_revision: Union[str, None] = "0006_lesson_translation_video_url"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "applications",
        sa.Column("started_at", sa.DateTime(), nullable=True),
    )
    op.add_column(
        "applications",
        sa.Column("mcq_answers", sa.JSON(), nullable=True),
    )
    op.add_column(
        "applications",
        sa.Column("mcq_score", sa.Integer(), nullable=True),
    )
    op.add_column(
        "applications",
        sa.Column("mcq_excel_score", sa.Integer(), nullable=True),
    )
    op.add_column(
        "applications",
        sa.Column("auto_decision", sa.String(40), nullable=True, index=True),
    )
    op.create_index(
        "ix_applications_auto_decision", "applications", ["auto_decision"]
    )


def downgrade() -> None:
    op.drop_index("ix_applications_auto_decision", table_name="applications")
    op.drop_column("applications", "auto_decision")
    op.drop_column("applications", "mcq_excel_score")
    op.drop_column("applications", "mcq_score")
    op.drop_column("applications", "mcq_answers")
    op.drop_column("applications", "started_at")
