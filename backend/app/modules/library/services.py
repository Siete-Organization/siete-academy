from app.core.i18n import DEFAULT_LOCALE
from app.modules.library.models import IndustryCard, IndustryCardTranslation


def _pick_translation(
    card: IndustryCard, locale: str
) -> IndustryCardTranslation | None:
    by_locale = {t.locale: t for t in card.translations}
    return by_locale.get(locale) or by_locale.get(DEFAULT_LOCALE) or next(
        iter(by_locale.values()), None
    )


def card_summary(card: IndustryCard, locale: str) -> dict:
    t = _pick_translation(card, locale)
    return {
        "slug": card.slug,
        "order_index": card.order_index,
        "name": t.name if t else card.slug,
        "what_is": t.what_is if t else None,
        "examples": card.examples,
        "tags": card.tags,
    }


def card_detail(card: IndustryCard, locale: str) -> dict:
    t = _pick_translation(card, locale)
    return {
        "slug": card.slug,
        "order_index": card.order_index,
        "name": t.name if t else card.slug,
        "what_is": t.what_is if t else None,
        "how_makes_money": t.how_makes_money if t else None,
        "what_sells": t.what_sells if t else None,
        "sells_to": t.sells_to if t else None,
        "buys_to_operate": t.buys_to_operate if t else None,
        "dynamics": t.dynamics if t else None,
        "deepen_in": t.deepen_in if t else None,
        "examples": card.examples,
        "tags": card.tags,
    }
