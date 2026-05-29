from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.core.i18n import normalize_locale
from app.modules.library import services
from app.modules.library.models import IndustryCard
from app.modules.library.schemas import IndustryCardDetail, IndustryCardSummary

router = APIRouter()


@router.get("/industries", response_model=list[IndustryCardSummary])
def list_industries(
    locale: str = Query("es"),
    db: Session = Depends(get_db),
) -> list[dict]:
    loc = normalize_locale(locale)
    cards = (
        db.query(IndustryCard)
        .options(selectinload(IndustryCard.translations))
        .order_by(IndustryCard.order_index)
        .all()
    )
    return [services.card_summary(c, loc) for c in cards]


@router.get("/industries/{slug}", response_model=IndustryCardDetail)
def get_industry(
    slug: str,
    locale: str = Query("es"),
    db: Session = Depends(get_db),
) -> dict:
    loc = normalize_locale(locale)
    card = (
        db.query(IndustryCard)
        .options(selectinload(IndustryCard.translations))
        .filter(IndustryCard.slug == slug)
        .first()
    )
    if not card:
        raise HTTPException(404, "industry card not found")
    return services.card_detail(card, loc)
