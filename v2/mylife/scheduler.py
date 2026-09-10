from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo


def intended_diary_date(now: datetime, timezone_name: str = "Asia/Seoul"):
    """Resolve scheduled work by the configured local calendar date."""
    zone = ZoneInfo(timezone_name)
    if now.tzinfo is None:
        raise ValueError("scheduler datetime must be timezone-aware")
    return now.astimezone(zone).date()
