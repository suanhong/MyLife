import pytest

from mylife.pagination import page_size


def test_page_size_is_bounded():
    assert page_size(None) == 30
    assert page_size(500) == 100
    with pytest.raises(ValueError):
        page_size(0)
