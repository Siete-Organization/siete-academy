from pydantic import BaseModel, ConfigDict


class IndustryCardSummary(BaseModel):
    """Para el listado: solo lo mínimo para renderizar la grilla."""

    model_config = ConfigDict(from_attributes=True)

    slug: str
    order_index: int
    name: str
    what_is: str | None = None
    examples: list[str] | None = None
    tags: list[str] | None = None


class IndustryCardDetail(BaseModel):
    """Para la vista de detalle: los 8 campos del doc."""

    model_config = ConfigDict(from_attributes=True)

    slug: str
    order_index: int
    name: str
    what_is: str | None = None
    how_makes_money: str | None = None
    what_sells: str | None = None
    sells_to: str | None = None
    buys_to_operate: str | None = None
    dynamics: str | None = None
    deepen_in: str | None = None
    examples: list[str] | None = None
    tags: list[str] | None = None
