from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

# Stages del pipeline ATS (orden importa para el Kanban)
STAGES: tuple[str, ...] = (
    "applying",        # graduado, aún sin entrevista
    "siete_interview", # entrevista interna con área comercial Siete
    "siete_test",      # prueba práctica
    "approved",        # aprobó la prueba, disponible para clientes
    "presented",       # presentado a un cliente
    "placed",          # colocado exitosamente
    "rejected",        # no avanzó
)


class PlacementCandidate(Base):
    __tablename__ = "placement_candidates"
    __table_args__ = (UniqueConstraint("user_id", name="uq_placement_candidate_user"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True
    )
    cohort_id: Mapped[int | None] = mapped_column(
        ForeignKey("cohorts.id", ondelete="SET NULL"), nullable=True, index=True
    )
    stage: Mapped[str] = mapped_column(String(40), default="applying", index=True)
    assigned_admin_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Campos visibles al reclutador externo
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    portfolio_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    events: Mapped[list["PlacementEvent"]] = relationship(
        back_populates="candidate", cascade="all, delete-orphan", order_by="PlacementEvent.created_at.desc()"
    )


class PlacementEvent(Base):
    """Timeline auditable de cambios por candidato."""

    __tablename__ = "placement_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    candidate_id: Mapped[int] = mapped_column(
        ForeignKey("placement_candidates.id", ondelete="CASCADE"), index=True
    )
    event_type: Mapped[str] = mapped_column(String(40))
    # stage_changed | note_added | assigned | presented_to_client | placed | rejected
    data: Mapped[dict] = mapped_column(JSON, default=dict)
    actor_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    candidate: Mapped[PlacementCandidate] = relationship(back_populates="events")
