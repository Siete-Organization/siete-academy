"""Modelo del path post-Academy (Documento Maestro Parte IX v1.0).

PracticaCandidate: 1 fila por graduado que entra al pipeline de práctica.
PracticaStageEvent: timeline auditable de transiciones de stage.
"""
from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


# Orden importa: refleja la progresión esperada. closed_camino_b es terminal.
STAGES: tuple[str, ...] = (
    "e1_invited",        # invitado a Etapa 1, aún no arrancó
    "e1_active",         # operando en Etapa 1 (no remunerada)
    "e2_active",         # Etapa 2 (USD 400/mes)
    "e3_t2_active",      # SDR planta T2 (USD 500-950)
    "e3_t1_active",      # SDR planta T1 (USD 950-1.250)
    "closed_camino_b",   # cerrado con carta de recomendación / Camino B
    "declined",          # rechazó invitación / sin Deel
)


class PracticaCandidate(Base):
    __tablename__ = "practica_candidates"
    __table_args__ = (UniqueConstraint("user_id", name="uq_practica_candidate_user"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    stage: Mapped[str] = mapped_column(String(40), default="e1_invited", index=True)
    entered_stage_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    # USD/mes vigente en el stage actual (None para e1_invited / e1_active / closed_*).
    monthly_usd: Mapped[int | None] = mapped_column(Integer, nullable=True)
    # Si False, no puede continuar al Camino A (VE, CU u otros sin Deel).
    country_deel_ok: Mapped[bool] = mapped_column(Boolean, default=True)
    assigned_manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    events: Mapped[list["PracticaStageEvent"]] = relationship(
        back_populates="candidate",
        cascade="all, delete-orphan",
        order_by="PracticaStageEvent.created_at.desc()",
    )


class PracticaStageEvent(Base):
    """Una fila por transición de stage. Auditable, append-only."""

    __tablename__ = "practica_stage_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("practica_candidates.id", ondelete="CASCADE"), index=True
    )
    # from_stage es NULL en la primera invitación
    from_stage: Mapped[str | None] = mapped_column(String(40), nullable=True)
    to_stage: Mapped[str] = mapped_column(String(40))
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    actor_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    candidate: Mapped[PracticaCandidate] = relationship(back_populates="events")
