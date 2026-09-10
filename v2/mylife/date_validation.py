from datetime import date


def parse_diary_date(value: str) -> date:
    day = date.fromisoformat(value)
    if day.year < 1900 or day.year > 2200:
        raise ValueError("diary date outside supported range")
    return day
