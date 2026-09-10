from datetime import date

from .mail_domain import anniversary_candidates


def find_old_entry(day: date, lookup, years: int = 10):
    """lookup(candidate_date) should return an entry or None."""
    for candidate in anniversary_candidates(day, years):
        entry = lookup(candidate)
        if entry is not None:
            return entry
    return None
