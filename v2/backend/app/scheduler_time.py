from datetime import datetime
from zoneinfo import ZoneInfo

SEOUL = ZoneInfo("Asia/Seoul")


def diary_date_for(now: datetime):
    if now.tzinfo is None:
        raise ValueError("timezone-aware datetime required")
    return now.astimezone(SEOUL).date()
