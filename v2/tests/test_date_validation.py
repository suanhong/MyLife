import pytest

from mylife.date_validation import parse_diary_date


def test_valid_date_parses():
    assert parse_diary_date("2026-09-10").isoformat() == "2026-09-10"


def test_extreme_date_rejected():
    with pytest.raises(ValueError):
        parse_diary_date("1800-01-01")
