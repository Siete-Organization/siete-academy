"""Tests for courses i18n translation helpers.

Verifies the locale fallback chain: requested → es (default) → any → empty.
"""

import pytest

from app.core.i18n import normalize_locale, pick_translation
from app.modules.courses.services import (
    course_to_dict,
    create_course,
    create_lesson,
    create_module,
    lesson_to_dict,
    module_to_dict,
)


class TestPickTranslation:
    def test_returns_requested_locale_when_present(self):
        t = {"es": {"title": "Hola"}, "en": {"title": "Hello"}}
        assert pick_translation(t, "en", "title") == "Hello"

    def test_falls_back_to_default_locale(self):
        t = {"es": {"title": "Hola"}}
        assert pick_translation(t, "pt", "title") == "Hola"

    def test_falls_back_to_any_available_locale(self):
        t = {"fr": {"title": "Bonjour"}}
        assert pick_translation(t, "pt", "title") == "Bonjour"

    def test_returns_empty_string_when_field_absent_everywhere(self):
        t = {"es": {"description": "desc"}}
        assert pick_translation(t, "en", "title") == ""

    def test_returns_empty_string_when_no_translations(self):
        assert pick_translation({}, "es", "title") == ""


class TestNormalizeLocale:
    @pytest.mark.parametrize("given, expected", [
        ("es", "es"),
        ("en", "en"),
        ("pt", "pt"),
        ("fr", "es"),
        (None, "es"),
        ("", "es"),
    ])
    def test_supported_pass_through_unknown_falls_to_default(self, given, expected):
        assert normalize_locale(given) == expected


class TestCourseCreationAndSerialization:
    def test_course_to_dict_uses_locale_and_falls_back(self, db):
        c = create_course(
            db,
            slug="fundamentos",
            translations=[
                {"locale": "es", "title": "Fundamentos", "description": "Intro"},
                {"locale": "en", "title": "Fundamentals", "description": "Intro EN"},
            ],
        )
        es = course_to_dict(c, "es")
        en = course_to_dict(c, "en")
        pt = course_to_dict(c, "pt")  # fallback to es
        assert es["title"] == "Fundamentos"
        assert en["title"] == "Fundamentals"
        assert pt["title"] == "Fundamentos"

    def test_module_and_lesson_serialization_respects_locale(self, db):
        c = create_course(
            db,
            slug="fundamentos",
            translations=[{"locale": "es", "title": "Fundamentos"}],
        )
        m = create_module(
            db,
            course_id=c.id,
            slug="icp",
            order_index=1,
            translations=[
                {"locale": "es", "title": "ICP", "summary": "Clientes ideales"},
                {"locale": "en", "title": "ICP", "summary": "Ideal customers"},
            ],
        )
        le = create_lesson(
            db,
            module_id=m.id,
            order_index=0,
            youtube_id="abc123",
            duration_seconds=600,
            translations=[{"locale": "es", "title": "Introducción", "body": "texto"}],
        )
        assert module_to_dict(m, "en")["summary"] == "Ideal customers"
        assert module_to_dict(m, "pt")["summary"] == "Clientes ideales"  # fallback
        assert lesson_to_dict(le, "es")["youtube_id"] == "abc123"
