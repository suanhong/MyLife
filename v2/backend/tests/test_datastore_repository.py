from __future__ import annotations

from app.datastore_repository import normalize_refs


def test_normalize_refs_handles_list() -> None:
    assert normalize_refs(["a", "b", None]) == ["a", "b"]


def test_normalize_refs_handles_projection_scalar() -> None:
    assert normalize_refs("ImageKey(123)") == ["ImageKey(123)"]


def test_normalize_refs_handles_none() -> None:
    assert normalize_refs(None) == []
