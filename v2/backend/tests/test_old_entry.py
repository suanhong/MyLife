from datetime import date

from app.old_entry import find_old_entry


def test_nearest_existing_anniversary_wins():
    values = {date(2024, 9, 10): "two years", date(2023, 9, 10): "three years"}
    assert find_old_entry(date(2026, 9, 10), values.get) == "two years"
