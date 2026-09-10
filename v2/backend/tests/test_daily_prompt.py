from datetime import date

from app.daily_prompt import compose_daily_prompt


def test_old_entry_is_included():
    subject, body = compose_daily_prompt(date(2026, 9, 10), date(2025, 9, 10), "old diary")
    assert "2026-09-10" in subject
    assert "2025-09-10" in body
    assert "old diary" in body
