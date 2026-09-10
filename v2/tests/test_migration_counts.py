import pytest

from mylife.migration_counts import assert_expected_legacy_counts


def test_verified_recovery_counts_are_accepted():
    assert_expected_legacy_counts(2822, 252, 252)


def test_count_drift_is_rejected():
    with pytest.raises(ValueError):
        assert_expected_legacy_counts(2821, 252, 252)
