from __future__ import annotations

import re
from datetime import date
from zoneinfo import ZoneInfo

TOKEN_RE = re.compile(r"\[MyLife:([A-Za-z0-9_-]+)\]")
SEOUL = ZoneInfo("Asia/Seoul")


def subject_with_token(subject: str, token: str) -> str:
    return f"{subject} [MyLife:{token}]"


def token_from_subject(subject: str) -> str | None:
    match = TOKEN_RE.search(subject or "")
    return match.group(1) if match else None


def anniversary_candidates(today: date, years: int = 10) -> list[date]:
    result = []
    for offset in range(1, years + 1):
        try:
            result.append(today.replace(year=today.year - offset))
        except ValueError:
            continue
    return result


def should_send(*, already_sent: bool) -> bool:
    return not already_sent
