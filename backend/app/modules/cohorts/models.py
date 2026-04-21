from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Cohort(Base):
    __tablename__ = "cohorts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    locale: Mapped[str] = mapped_column(String(5), default="es")
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20), default="draft")
    # draft | open_applications | in_progress | completed | archived
    max_students: Mapped[int] = mapped_column(Integer, default=20)
    # Link de invitación al canal de Slack de la cohorte (ej: https://join.slack.com/t/...).
    # El alumno lo ve en su dashboard/perfil. Al enrolarse recibe un email con este link.
    slack_invite_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    module_windows: Mapped[list["ModuleWindow"]] = relationship(
        back_populates="cohort", cascade="all, delete-orphan"
    )


class ModuleWindow(Base):
    __tablename__ = "module_windows"
    __table_args__ = (UniqueConstraint("cohort_id", "module_id", name="uq_cohort_module"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    cohort_id: Mapped[int] = mapped_column(ForeignKey("cohorts.id", ondelete="CASCADE"), index=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id", ondelete="CASCADE"), index=True)
    opens_at: Mapped[datetime] = mapped_column(DateTime)
    closes_at: Mapped[datetime] = mapped_column(DateTime)
    live_session_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    cohort: Mapped[Cohort] = relationship(back_populates="module_windows")
