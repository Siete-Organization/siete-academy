"""Tests para grading + auto-descarte de Etapa 1 admisión."""

from datetime import datetime, timedelta

from app.modules.applications.admission_grading import (
    MCQ_EXCEL_PASS_PCT,
    MCQ_TOTAL_PASS_PCT,
    decide_auto_decision,
    grade_mcq,
)
from app.modules.applications.admission_questions_es import MCQ, OPEN_PROMPTS


def _all_correct() -> dict[str, str]:
    return {q["id"]: q["correct"] for q in MCQ}


def _all_wrong() -> dict[str, str]:
    # Pick first option that's not the correct one
    out: dict[str, str] = {}
    for q in MCQ:
        wrong = next(c["id"] for c in q["choices"] if c["id"] != q["correct"])
        out[q["id"]] = wrong
    return out


def _valid_open_answers() -> dict[str, str]:
    """Devuelve respuestas que cumplen el rango min/max de cada prompt."""
    out: dict[str, str] = {}
    for p in OPEN_PROMPTS:
        # Genera texto de exactamente min_words+5 palabras
        wc = p["min_words"] + 5
        out[p["id"]] = " ".join(["palabra"] * wc)
    return out


class TestGradeMcq:
    def test_all_correct_returns_100(self):
        result = grade_mcq(_all_correct())
        assert result["mcq_score"] == 100
        assert result["mcq_excel_score"] == 100

    def test_all_wrong_returns_0(self):
        result = grade_mcq(_all_wrong())
        assert result["mcq_score"] == 0
        assert result["mcq_excel_score"] == 0

    def test_none_returns_0(self):
        result = grade_mcq(None)
        assert result == {"mcq_score": 0, "mcq_excel_score": 0}

    def test_partial_excel_only(self):
        # Acierta solo el primer Excel (C1.1)
        answers = {"C1.1": next(q["correct"] for q in MCQ if q["id"] == "C1.1")}
        result = grade_mcq(answers)
        # 1 correcta de 26 ≈ 4
        assert result["mcq_score"] == 4
        # 1 correcta de 11 excel ≈ 9
        assert result["mcq_excel_score"] == 9


class TestAutoDecision:
    def test_all_correct_passes(self):
        result = decide_auto_decision(
            open_answers=_valid_open_answers(),
            mcq_score=100,
            mcq_excel_score=100,
            started_at=datetime(2026, 5, 28, 10, 0, 0),
            submitted_at=datetime(2026, 5, 28, 11, 0, 0),
        )
        assert result == "passed_stage_1"

    def test_open_answer_below_min_rejects_text(self):
        answers = _valid_open_answers()
        answers["B.1"] = "muy corto"  # 2 words, min is 80
        result = decide_auto_decision(
            open_answers=answers,
            mcq_score=100,
            mcq_excel_score=100,
            started_at=datetime(2026, 5, 28, 10, 0, 0),
            submitted_at=datetime(2026, 5, 28, 11, 0, 0),
        )
        assert result == "rejected_text"

    def test_open_answer_above_max_rejects_text(self):
        answers = _valid_open_answers()
        answers["B.1"] = " ".join(["palabra"] * 200)  # max is 150
        result = decide_auto_decision(
            open_answers=answers,
            mcq_score=100,
            mcq_excel_score=100,
            started_at=datetime(2026, 5, 28, 10, 0, 0),
            submitted_at=datetime(2026, 5, 28, 11, 0, 0),
        )
        assert result == "rejected_text"

    def test_excel_below_floor_rejects(self):
        result = decide_auto_decision(
            open_answers=_valid_open_answers(),
            mcq_score=80,
            mcq_excel_score=MCQ_EXCEL_PASS_PCT - 1,
            started_at=datetime(2026, 5, 28, 10, 0, 0),
            submitted_at=datetime(2026, 5, 28, 11, 0, 0),
        )
        assert result == "rejected_mcq_excel"

    def test_total_below_floor_rejects(self):
        result = decide_auto_decision(
            open_answers=_valid_open_answers(),
            mcq_score=MCQ_TOTAL_PASS_PCT - 1,
            mcq_excel_score=80,
            started_at=datetime(2026, 5, 28, 10, 0, 0),
            submitted_at=datetime(2026, 5, 28, 11, 0, 0),
        )
        assert result == "rejected_mcq_total"

    def test_under_15_min_rejects_speed(self):
        start = datetime(2026, 5, 28, 10, 0, 0)
        result = decide_auto_decision(
            open_answers=_valid_open_answers(),
            mcq_score=100,
            mcq_excel_score=100,
            started_at=start,
            submitted_at=start + timedelta(minutes=10),
        )
        assert result == "rejected_speed"

    def test_no_started_at_skips_speed_check(self):
        result = decide_auto_decision(
            open_answers=_valid_open_answers(),
            mcq_score=100,
            mcq_excel_score=100,
            started_at=None,
            submitted_at=datetime(2026, 5, 28, 11, 0, 0),
        )
        assert result == "passed_stage_1"

    def test_text_violation_takes_priority_over_mcq(self):
        # Texto malo + MCQ excel bajo → debe ser rejected_text (prioridad 1)
        answers = _valid_open_answers()
        answers["B.2"] = ""
        result = decide_auto_decision(
            open_answers=answers,
            mcq_score=10,
            mcq_excel_score=10,
            started_at=None,
            submitted_at=datetime(2026, 5, 28, 11, 0, 0),
        )
        assert result == "rejected_text"


class TestQuestionsContent:
    def test_mcq_count_is_26(self):
        assert len(MCQ) == 26

    def test_excel_section_has_11(self):
        excel = [q for q in MCQ if q["section"] == "excel"]
        assert len(excel) == 11

    def test_each_question_has_4_choices(self):
        for q in MCQ:
            assert len(q["choices"]) == 4, q["id"]

    def test_each_correct_is_in_choices(self):
        for q in MCQ:
            choice_ids = [c["id"] for c in q["choices"]]
            assert q["correct"] in choice_ids, q["id"]

    def test_ids_are_unique(self):
        ids = [q["id"] for q in MCQ]
        assert len(ids) == len(set(ids))

    def test_open_prompts_have_word_ranges(self):
        for p in OPEN_PROMPTS:
            assert p["min_words"] > 0
            assert p["max_words"] > p["min_words"]


class TestAdmissionQuestionsEndpoint:
    def test_get_questions_returns_full_payload(self, client):
        r = client.get("/admission/questions")
        assert r.status_code == 200
        data = r.json()
        assert data["locale"] == "es"
        assert len(data["mcq"]) == 26
        assert len(data["open_prompts"]) == 3
        assert "comprehension_text" in data
        assert data["rules"]["mcq_total_pass_pct"] == 60
        assert data["rules"]["mcq_excel_pass_pct"] == 40

    def test_get_questions_strips_explanations_and_correct(self, client):
        r = client.get("/admission/questions")
        data = r.json()
        for q in data["mcq"]:
            assert "explanation" not in q
            assert "correct" not in q

    def test_get_questions_rejects_unsupported_locale(self, client):
        r = client.get("/admission/questions?locale=en")
        assert r.status_code == 404
