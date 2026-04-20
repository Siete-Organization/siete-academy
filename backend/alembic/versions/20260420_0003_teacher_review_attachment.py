"""add attachment_url to teacher_reviews

Revision ID: 0003_tr_attachment
Revises: 0002_placement_certs
Create Date: 2026-04-20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0003_tr_attachment"
down_revision: Union[str, None] = "0002_placement_certs"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "teacher_reviews",
        sa.Column("attachment_url", sa.String(500), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("teacher_reviews", "attachment_url")
