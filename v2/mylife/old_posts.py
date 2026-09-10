from __future__ import annotations

from datetime import date


def anniversary_candidates(today: date, years: int = 10) -> list[date]:
    """Return same-calendar-day anniversaries, newest first.

    Feb 29 anniversaries are skipped in non-leap target years rather than being
    silently shifted to another date.
    """
    result = []
    for offset in range(1, years + 1):
        try:
            result.append(today.replace(year=today.year - offset))
        except ValueError:
            continue
    return result
