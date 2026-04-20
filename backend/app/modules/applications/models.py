from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    # Aspirante aún no tiene User (aplicación es pre-registro)
    applicant_email: Mapped[str] = mapped_column(String(255), index=True)
    applicant_name: Mapped[str] = mapped_column(String(200))
    applicant_phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    locale: Mapped[str] = mapped_column(String(5), default="es")

    # Respuestas abiertas (question_id -> texto)
    answers: Mapped[dict] = mapped_column(JSON, default=dict)
    # Verificación min 100 palabras se hace en schema
    video_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Scoring Claude (Fase 1). En Fase 0 queda null.
    ai_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ai_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Revisión humana
    status: Mapped[str] = mapped_column(String(20), default="submitted", index=True)
    # submitted | under_review | approved | rejected
    admin_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewed_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
