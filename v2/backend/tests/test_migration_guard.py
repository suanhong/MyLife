import pytest

from app.migration_guard import validate_staging_namespace


def test_v2_staging_namespace_required():
    assert validate_staging_namespace("mylife-v2-staging") == "mylife-v2-staging"
    with pytest.raises(ValueError):
        validate_staging_namespace(None)
    with pytest.raises(ValueError):
        validate_staging_namespace("default")
