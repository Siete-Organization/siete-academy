"""teacher_reviews.details — desglose por ítem para grading híbrido del caso final

Revision ID: 0011_review_details
Revises: 0010_uq_application_email
Create Date: 2026-06-10

Capa 3: el profesor califica respuestas cortas (/2) + tablas + rúbrica de video
(/30) por ítem. Se guarda como JSON en teacher_reviews.details. Idempotente.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision: str = "0011_review_details"
down_revision: Union[str, None] = "0010_uq_application_email"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    cols = {c["name"] for c in inspect(bind).get_columns("teacher_reviews")}
    if "details" not in cols:
        op.add_column("teacher_reviews", sa.Column("details", sa.JSON(), nullable=True))


def downgrade() -> None:
    bind = op.get_bind()
    cols = {c["name"] for c in inspect(bind).get_columns("teacher_reviews")}
    if "details" in cols:
        op.drop_column("teacher_reviews", "details")
