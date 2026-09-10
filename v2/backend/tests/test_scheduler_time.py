from datetime import datetime, timezone

from app.scheduler_time import diary_date_for


def test_utc_converts_to_seoul_date():
    assert diary_date_for(datetime(2026, 9, 10, 16, 0, tzinfo=timezone.utc)).isoformat() == "2026-09-11"
