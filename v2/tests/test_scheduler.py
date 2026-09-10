from datetime import datetime, timezone

from mylife.scheduler import intended_diary_date


def test_utc_time_resolves_to_seoul_date():
    now = datetime(2026, 9, 10, 16, 0, tzinfo=timezone.utc)
    assert intended_diary_date(now).isoformat() == "2026-09-11"
