"""Biblioteca de referencia transversal (Documento Maestro Parte II).

IndustryCard: una tarjeta por industria B2B relevante en LATAM. Material
de consulta, no evaluado. Estructura fija de 8 campos por el doc.

Patrón de traducción es/en/pt igual que courses/Module/Lesson.
"""
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class IndustryCard(Base):
    __tablename__ = "industry_cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    # Listas idiomáticamente neutras: nombres propios y etiquetas cortas
    examples: Mapped[list | None] = mapped_column(JSON, nullable=True)
    tags: Mapped[list | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    translations: Mapped[list["IndustryCardTranslation"]] = relationship(
        back_populates="card", cascade="all, delete-orphan"
    )


class IndustryCardTranslation(Base):
    __tablename__ = "industry_card_translations"
    __table_args__ = (
        UniqueConstraint("industry_card_id", "locale", name="uq_industry_card_locale"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    industry_card_id: Mapped[int] = mapped_column(
        ForeignKey("industry_cards.id", ondelete="CASCADE"), index=True
    )
    locale: Mapped[str] = mapped_column(String(5))
    name: Mapped[str] = mapped_column(String(200))
    # Los 8 campos del doc (Parte II §"Cómo leer cada tarjeta")
    what_is: Mapped[str | None] = mapped_column(Text, nullable=True)
    how_makes_money: Mapped[str | None] = mapped_column(Text, nullable=True)
    what_sells: Mapped[str | None] = mapped_column(Text, nullable=True)
    sells_to: Mapped[str | None] = mapped_column(Text, nullable=True)
    buys_to_operate: Mapped[str | None] = mapped_column(Text, nullable=True)
    dynamics: Mapped[str | None] = mapped_column(Text, nullable=True)
    deepen_in: Mapped[str | None] = mapped_column(Text, nullable=True)

    card: Mapped[IndustryCard] = relationship(back_populates="translations")
