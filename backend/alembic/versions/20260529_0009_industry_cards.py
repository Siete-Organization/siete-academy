"""Library: industry_cards + industry_card_translations (Doc Maestro Parte II)

Revision ID: 0009_industry_cards
Revises: 0008_practica
Create Date: 2026-05-29

Modela el anexo de industrias (Parte II del Documento Maestro): 10 tarjetas
B2B en LATAM con estructura fija de 8 campos. Material de consulta transversal,
no evaluado.

Migración idempotente con inspect().
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision: str = "0009_industry_cards"
down_revision: Union[str, None] = "0008_practica"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_tables = set(inspector.get_table_names())

    if "industry_cards" not in existing_tables:
        op.create_table(
            "industry_cards",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("slug", sa.String(80), nullable=False),
            sa.Column("order_index", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("examples", sa.JSON(), nullable=True),
            sa.Column("tags", sa.JSON(), nullable=True),
            sa.Column(
                "created_at",
                sa.DateTime(),
                nullable=False,
                server_default=sa.func.now(),
            ),
            sa.UniqueConstraint("slug", name="uq_industry_cards_slug"),
        )
        op.create_index(
            "ix_industry_cards_slug", "industry_cards", ["slug"], unique=True
        )

    if "industry_card_translations" not in existing_tables:
        op.create_table(
            "industry_card_translations",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column(
                "industry_card_id",
                sa.Integer(),
                sa.ForeignKey("industry_cards.id", ondelete="CASCADE"),
                nullable=False,
                index=True,
            ),
            sa.Column("locale", sa.String(5), nullable=False),
            sa.Column("name", sa.String(200), nullable=False),
            sa.Column("what_is", sa.Text(), nullable=True),
            sa.Column("how_makes_money", sa.Text(), nullable=True),
            sa.Column("what_sells", sa.Text(), nullable=True),
            sa.Column("sells_to", sa.Text(), nullable=True),
            sa.Column("buys_to_operate", sa.Text(), nullable=True),
            sa.Column("dynamics", sa.Text(), nullable=True),
            sa.Column("deepen_in", sa.Text(), nullable=True),
            sa.UniqueConstraint(
                "industry_card_id", "locale", name="uq_industry_card_locale"
            ),
        )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing_tables = set(inspector.get_table_names())

    if "industry_card_translations" in existing_tables:
        op.drop_table("industry_card_translations")
    if "industry_cards" in existing_tables:
        existing_indexes = {idx["name"] for idx in inspector.get_indexes("industry_cards")}
        if "ix_industry_cards_slug" in existing_indexes:
            op.drop_index("ix_industry_cards_slug", table_name="industry_cards")
        op.drop_table("industry_cards")
