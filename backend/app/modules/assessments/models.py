from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, String, Text, func  # noqa: F401
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(primary_key=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id", ondelete="CASCADE"), index=True)
    # mcq | written | prospection_db | cold_call_video | team_exercise
    type: Mapped[str] = mapped_column(String(30), index=True)
    title: Mapped[str] = mapped_column(String(200))
    # Por tipo: MCQ → preguntas, written → prompt, cold_call → escenario, etc.
    config: Mapped[dict] = mapped_column(JSON, default=dict)
    passing_score: Mapped[float] = mapped_column(Float, default=70.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    assessment_id: Mapped[int] = mapped_column(
        ForeignKey("assessments.id", ondelete="CASCADE"), index=True
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    # payload depende del tipo: MCQ → {answers:{qid:choice}}, written → {text}, db → {file_url}
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    file_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # auto_graded (mcq) | pending_review | reviewed
    status: Mapped[str] = mapped_column(String(20), default="pending_review", index=True)
    auto_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    submitted_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class TeacherReview(Base):
    __tablename__ = "teacher_reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    submission_id: Mapped[int] = mapped_column(
        ForeignKey("submissions.id", ondelete="CASCADE"), unique=True, index=True
    )
    teacher_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    score: Mapped[float] = mapped_column(Float)
    feedback: Mapped[str] = mapped_column(Text)
    # Archivo opcional que el profesor sube al dar feedback (PDF anotado, audio, etc.)
    attachment_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    approved_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class AIReview(Base):
    """Fase 1: Claude analiza la submission y propone feedback + score al profesor.

    El alumno NO ve esto directamente — solo lo usa el profesor como borrador.
    """

    __tablename__ = "ai_reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    submission_id: Mapped[int] = mapped_column(
        ForeignKey("submissions.id", ondelete="CASCADE"), unique=True, index=True
    )
    draft_feedback: Mapped[str] = mapped_column(Text)
    score_suggestion: Mapped[float | None] = mapped_column(Float, nullable=True)
    model_used: Mapped[str] = mapped_column(String(80))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
