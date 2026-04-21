from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class TeacherNote(Base):
    """Nota directa del profesor al alumno — independiente de submissions.

    Uso: feedback puntual, coaching, anuncios por alumno, compartir un recurso extra.
    Opcionalmente lleva un adjunto por URL (Drive/Loom/Dropbox) — Fase 0 no sube archivos.
    """

    __tablename__ = "teacher_notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    student_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    body: Mapped[str] = mapped_column(Text)
    # "pdf" | "ppt" | "video" | "doc" | "link" | None
    attachment_kind: Mapped[str | None] = mapped_column(String(16), nullable=True)
    attachment_url: Mapped[str | None] = mapped_column(String(600), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
