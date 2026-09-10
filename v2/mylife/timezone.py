from datetime import datetime
from zoneinfo import ZoneInfo

SEOUL = ZoneInfo("Asia/Seoul")


def seoul_now() -> datetime:
    return datetime.now(SEOUL)
