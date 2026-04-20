from typing import Literal

Locale = Literal["es", "en", "pt"]
SUPPORTED_LOCALES: tuple[Locale, ...] = ("es", "en", "pt")
DEFAULT_LOCALE: Locale = "es"


def pick_translation(translations: dict[str, dict], locale: str, field: str) -> str:
    """Return translated field, falling back to default locale, then any value."""
    if locale in translations and field in translations[locale]:
        return translations[locale][field]
    if DEFAULT_LOCALE in translations and field in translations[DEFAULT_LOCALE]:
        return translations[DEFAULT_LOCALE][field]
    for loc in translations.values():
        if field in loc:
            return loc[field]
    return ""


def normalize_locale(locale: str | None) -> Locale:
    if locale and locale in SUPPORTED_LOCALES:
        return locale  # type: ignore[return-value]
    return DEFAULT_LOCALE
