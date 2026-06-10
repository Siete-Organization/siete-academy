"""Una aplicación por email: dedup + índice único funcional lower(applicant_email)

Revision ID: 0010_uq_application_email
Revises: 0009_industry_cards
Create Date: 2026-06-10

Respaldo a nivel BD del chequeo idempotente en services.create_application.
Antes de crear el índice único deduplicamos las filas existentes conservando,
por email (case-insensitive), la "más avanzada" (approved > under_review >
submitted > rejected), desempatando por id menor. Idempotente vía inspect().
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision: str = "0010_uq_application_email"
down_revision: Union[str, None] = "0009_industry_cards"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_INDEX = "uq_applications_email_lower"

_STATUS_RANK = (
    "CASE status WHEN 'approved' THEN 4 WHEN 'under_review' THEN 3 "
    "WHEN 'submitted' THEN 2 WHEN 'rejected' THEN 1 ELSE 0 END"
)


def upgrade() -> None:
    bind = op.get_bind()
    inspector = inspect(bind)
    existing = {ix["name"] for ix in inspector.get_indexes("applications")}
    if _INDEX in existing:
        return

    # Dedup: borra la fila `a` si existe otra `b` (mismo email) estrictamente
    # "mejor" — más avanzada en status, o igual status pero id menor.
    bind.execute(
        sa.text(
            f"""
            DELETE FROM applications
            WHERE id IN (
                SELECT a.id
                FROM applications a
                JOIN applications b
                  ON lower(a.applicant_email) = lower(b.applicant_email)
                 AND a.id <> b.id
                WHERE ({_STATUS_RANK.replace('status', 'b.status')})
                      > ({_STATUS_RANK.replace('status', 'a.status')})
                   OR (
                        ({_STATUS_RANK.replace('status', 'b.status')})
                          = ({_STATUS_RANK.replace('status', 'a.status')})
                        AND b.id < a.id
                   )
            )
            """
        )
    )
    op.create_index(
        _INDEX,
        "applications",
        [sa.text("lower(applicant_email)")],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index(_INDEX, table_name="applications")
