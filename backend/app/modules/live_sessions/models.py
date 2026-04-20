from datetime import datetime

from sqlalchemy import JSON, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class LiveSession(Base):
    __tablename__ = "live_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    module_window_id: Mapped[int] = mapped_column(
        ForeignKey("module_windows.id", ondelete="CASCADE"), unique=True, index=True
    )
    title: Mapped[str] = mapped_column(String(200))
    zoom_url: Mapped[str] = mapped_column(String(500))
    recording_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # { user_id: {joined_at, left_at} }
    attendance: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
