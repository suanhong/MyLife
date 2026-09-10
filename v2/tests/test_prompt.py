from datetime import date

from mylife.prompt import OldEntry, compose_prompt


def test_prompt_includes_old_entry_when_present():
    subject, body = compose_prompt(
        date(2026, 9, 10),
        OldEntry(date(2025, 9, 10), "old diary"),
    )
    assert "2026-09-10" in subject
    assert "2025-09-10" in body
    assert "old diary" in body
