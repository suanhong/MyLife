from datetime import date

from mylife.old_posts import anniversary_candidates


def test_anniversary_candidates_are_years_first():
    result = anniversary_candidates(date(2026, 9, 10), years=3)
    assert result == [date(2025, 9, 10), date(2024, 9, 10), date(2023, 9, 10)]


def test_feb_29_invalid_anniversary_is_skipped():
    result = anniversary_candidates(date(2024, 2, 29), years=4)
    assert result == [date(2020, 2, 29)]
