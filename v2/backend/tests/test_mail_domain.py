from datetime import date

from app.mail_domain import anniversary_candidates, subject_with_token, token_from_subject


def test_token_round_trip():
    assert token_from_subject(subject_with_token("Diary", "abc_123")) == "abc_123"


def test_anniversary_candidates_are_years_first():
    assert anniversary_candidates(date(2026, 9, 10), 3) == [
        date(2025, 9, 10), date(2024, 9, 10), date(2023, 9, 10)
    ]
