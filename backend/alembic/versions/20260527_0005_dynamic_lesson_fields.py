"""dynamic lesson fields: avatar, presentation + lesson_id FK opcional

Revision ID: 0005_dynamic_lesson
Revises: 0004_sync_missing_schema
Create Date: 2026-05-27

Estructura dinámica de la lección (secuencia: Video → Avatar IA → Presentación →
Material → Examen). Todo additive y nullable para no romper data existente.

- lessons.avatar_audio_url, lessons.avatar_script
- lessons.presentation_url, lessons.presentation_blocks (JSON)
- assessments.lesson_id (FK nullable → permite mantener exámenes a nivel módulo)
- module_resources.lesson_id (FK nullable → permite material a nivel lección o módulo)
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0005_dynamic_lesson"
down_revision: Union[str, None] = "0004_sync_missing_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "lessons",
        sa.Column("avatar_audio_url", sa.String(600), nullable=True),
    )
    op.add_column(
        "lessons",
        sa.Column("avatar_script", sa.Text(), nullable=True),
    )
    op.add_column(
        "lessons",
        sa.Column("presentation_url", sa.String(600), nullable=True),
    )
    op.add_column(
        "lessons",
        sa.Column("presentation_blocks", sa.JSON(), nullable=True),
    )

    op.add_column(
        "assessments",
        sa.Column(
            "lesson_id",
            sa.Integer(),
            sa.ForeignKey("lessons.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    op.create_index("ix_assessments_lesson_id", "assessments", ["lesson_id"])

    op.add_column(
        "module_resources",
        sa.Column(
            "lesson_id",
            sa.Integer(),
            sa.ForeignKey("lessons.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    op.create_index("ix_module_resources_lesson_id", "module_resources", ["lesson_id"])


def downgrade() -> None:
    op.drop_index("ix_module_resources_lesson_id", table_name="module_resources")
    op.drop_column("module_resources", "lesson_id")

    op.drop_index("ix_assessments_lesson_id", table_name="assessments")
    op.drop_column("assessments", "lesson_id")

    op.drop_column("lessons", "presentation_blocks")
    op.drop_column("lessons", "presentation_url")
    op.drop_column("lessons", "avatar_script")
    op.drop_column("lessons", "avatar_audio_url")
