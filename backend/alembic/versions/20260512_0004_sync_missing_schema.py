"""sync schema drift: cols faltantes + tablas module_resources, teacher_notes

Revision ID: 0004_sync_missing_schema
Revises: 0003_tr_attachment
Create Date: 2026-05-12

Cierra drift detectado entre modelos SQLAlchemy y migraciones Alembic:
- cohorts.slack_invite_url (causa /cohorts 500)
- users.photo_url
- applications.linkedin_url, applications.country
- lessons.kind (con server_default="video" para backfill)
- tabla module_resources (no existía)
- tabla teacher_notes (no existía)
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0004_sync_missing_schema"
down_revision: Union[str, None] = "0003_tr_attachment"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "cohorts",
        sa.Column("slack_invite_url", sa.String(500), nullable=True),
    )
    op.add_column(
        "users",
        sa.Column("photo_url", sa.String(500), nullable=True),
    )
    op.add_column(
        "applications",
        sa.Column("linkedin_url", sa.String(500), nullable=True),
    )
    op.add_column(
        "applications",
        sa.Column("country", sa.String(80), nullable=True),
    )
    op.add_column(
        "lessons",
        sa.Column("kind", sa.String(16), nullable=False, server_default="video"),
    )

    op.create_table(
        "module_resources",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "module_id",
            sa.Integer(),
            sa.ForeignKey("modules.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("kind", sa.String(16), nullable=False, server_default="link"),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("url", sa.String(600), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index("ix_module_resources_module_id", "module_resources", ["module_id"])

    op.create_table(
        "teacher_notes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "teacher_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "student_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("attachment_kind", sa.String(16), nullable=True),
        sa.Column("attachment_url", sa.String(600), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.func.now(),
        ),
    )
    op.create_index("ix_teacher_notes_teacher_id", "teacher_notes", ["teacher_id"])
    op.create_index("ix_teacher_notes_student_id", "teacher_notes", ["student_id"])


def downgrade() -> None:
    op.drop_index("ix_teacher_notes_student_id", table_name="teacher_notes")
    op.drop_index("ix_teacher_notes_teacher_id", table_name="teacher_notes")
    op.drop_table("teacher_notes")

    op.drop_index("ix_module_resources_module_id", table_name="module_resources")
    op.drop_table("module_resources")

    op.drop_column("lessons", "kind")
    op.drop_column("applications", "country")
    op.drop_column("applications", "linkedin_url")
    op.drop_column("users", "photo_url")
    op.drop_column("cohorts", "slack_invite_url")
