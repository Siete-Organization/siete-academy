"""lesson_translations.video_url — URL del MP4 por locale (HeyGen)

Revision ID: 0006_lesson_translation_video_url
Revises: 0005_dynamic_lesson
Create Date: 2026-05-28

El MP4 generado por HeyGen contiene avatar + slides + audio embebidos y es
distinto por idioma. Vive en LessonTranslation, no en Lesson.

Cuando la lección tiene video_url, el front lo prefiere sobre youtube_id.
youtube_id queda como fallback legacy.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0006_lesson_video_url"
down_revision: Union[str, None] = "0005_dynamic_lesson"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "lesson_translations",
        sa.Column("video_url", sa.String(600), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("lesson_translations", "video_url")
