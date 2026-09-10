import pytest

from mylife.image_store import CloudStorageImageStore


class FakeClient:
    def bucket(self, name):
        raise AssertionError("bucket must not be touched for this validation test")


def test_non_image_rejected():
    store = object.__new__(CloudStorageImageStore)
    store.bucket = None
    with pytest.raises(ValueError):
        store.put("id", b"data", "application/pdf")
