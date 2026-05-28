"""Post-Academy: practica_candidates + practica_stage_events (Parte IX)

Revision ID: 0008_practica
Revises: 0007_admission_mcq
Create Date: 2026-05-28

Modela el path post-graduación (Documento Maestro Parte IX v1.0):
- Etapa 1 práctica inicial (4-6 sem, no remunerada)
- Etapa 2 práctica remunerada (8-12 sem, USD 400/mes)
- Etapa 3 T2 SDR junior (USD 500-950/mes)
- Etapa 3 T1 SDR senior (USD 950-1.250/mes)
- Camino B (graduado sin continuar o cerrado con carta de recomendación)

practica_candidates: 1 fila por graduado que entra al pipeline.
practica_stage_events: timeline auditable de transiciones (mismo patrón que
placement_events). Migración idempotente con inspect().
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision: str = "0008_practica"
down_revision: Union[str, None] = "0007_admission_mcq"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_tables = set(inspector.get_table_names())

    if "practica_candidates" not in existing_tables:
        op.create_table(
            "practica_candidates",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column(
                "user_id",
                sa.Integer(),
                sa.ForeignKey("users.id", ondelete="CASCADE"),
                nullable=False,
                index=True,
            ),
            sa.Column("stage", sa.String(40), nullable=False, server_default="e1_invited"),
            sa.Column("entered_stage_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
            sa.Column("monthly_usd", sa.Integer(), nullable=True),
            sa.Column("country_deel_ok", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column(
                "assigned_manager_id",
                sa.Integer(),
                sa.ForeignKey("users.id", ondelete="SET NULL"),
                nullable=True,
            ),
            sa.Column("notes", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
            sa.Column(
                "updated_at",
                sa.DateTime(),
                nullable=False,
                server_default=sa.func.now(),
                onupdate=sa.func.now(),
            ),
            sa.UniqueConstraint("user_id", name="uq_practica_candidate_user"),
        )
        op.create_index(
            "ix_practica_candidates_stage", "practica_candidates", ["stage"]
        )

    if "practica_stage_events" not in existing_tables:
        op.create_table(
            "practica_stage_events",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column(
                "candidate_id",
                sa.Integer(),
                sa.ForeignKey("practica_candidates.id", ondelete="CASCADE"),
                nullable=False,
                index=True,
            ),
            sa.Column("from_stage", sa.String(40), nullable=True),
            sa.Column("to_stage", sa.String(40), nullable=False),
            sa.Column("reason", sa.Text(), nullable=True),
            sa.Column(
                "actor_id",
                sa.Integer(),
                sa.ForeignKey("users.id", ondelete="SET NULL"),
                nullable=True,
            ),
            sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_tables = set(inspector.get_table_names())

    if "practica_stage_events" in existing_tables:
        op.drop_table("practica_stage_events")
    if "practica_candidates" in existing_tables:
        existing_indexes = {idx["name"] for idx in inspector.get_indexes("practica_candidates")}
        if "ix_practica_candidates_stage" in existing_indexes:
            op.drop_index("ix_practica_candidates_stage", table_name="practica_candidates")
        op.drop_table("practica_candidates")
