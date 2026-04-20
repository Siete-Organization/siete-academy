"""placement + certificates

Revision ID: 0002_placement_certs
Revises: 0001_initial
Create Date: 2026-04-20

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002_placement_certs"
down_revision: Union[str, None] = "0001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "placement_candidates",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("cohort_id", sa.Integer(), sa.ForeignKey("cohorts.id", ondelete="SET NULL"), nullable=True),
        sa.Column("stage", sa.String(40), nullable=False, server_default="applying"),
        sa.Column("assigned_admin_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("portfolio_url", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_placement_candidates_stage", "placement_candidates", ["stage"])
    op.create_index("ix_placement_candidates_cohort_id", "placement_candidates", ["cohort_id"])

    op.create_table(
        "placement_events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("candidate_id", sa.Integer(), sa.ForeignKey("placement_candidates.id", ondelete="CASCADE"), nullable=False),
        sa.Column("event_type", sa.String(40), nullable=False),
        sa.Column("data", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column("actor_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_placement_events_candidate_id", "placement_events", ["candidate_id"])

    op.create_table(
        "certificates",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("cohort_id", sa.Integer(), sa.ForeignKey("cohorts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("verification_code", sa.String(40), nullable=False, unique=True),
        sa.Column("pdf_url", sa.String(500), nullable=True),
        sa.Column("issued_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.UniqueConstraint("user_id", "cohort_id", name="uq_certificate_user_cohort"),
    )
    op.create_index("ix_certificates_user_id", "certificates", ["user_id"])
    op.create_index("ix_certificates_cohort_id", "certificates", ["cohort_id"])
    op.create_index("ix_certificates_verification_code", "certificates", ["verification_code"])


def downgrade() -> None:
    op.drop_index("ix_certificates_verification_code", table_name="certificates")
    op.drop_index("ix_certificates_cohort_id", table_name="certificates")
    op.drop_index("ix_certificates_user_id", table_name="certificates")
    op.drop_table("certificates")
    op.drop_index("ix_placement_events_candidate_id", table_name="placement_events")
    op.drop_table("placement_events")
    op.drop_index("ix_placement_candidates_cohort_id", table_name="placement_candidates")
    op.drop_index("ix_placement_candidates_stage", table_name="placement_candidates")
    op.drop_table("placement_candidates")
