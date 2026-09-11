from __future__ import annotations

from types import SimpleNamespace

from app.datastore_repository import count_kind, normalize_refs


class FakeAggregation:
    def __init__(self, value: int) -> None:
        self.value = value
        self.alias: str | None = None
        self.timeout: int | None = None

    def count(self, *, alias: str) -> None:
        self.alias = alias

    def fetch(self, *, timeout: int):
        self.timeout = timeout
        return [[SimpleNamespace(value=self.value)]]


class FakeClient:
    def __init__(self, value: int) -> None:
        self.kind: str | None = None
        self.query_object = object()
        self.aggregation = FakeAggregation(value)

    def query(self, *, kind: str):
        self.kind = kind
        return self.query_object

    def aggregation_query(self, query):
        assert query is self.query_object
        return self.aggregation


def test_count_kind_uses_aggregation_query() -> None:
    client = FakeClient(2822)

    assert count_kind(client, "DiaryEntryV2") == 2822
    assert client.kind == "DiaryEntryV2"
    assert client.aggregation.alias == "total"
    assert client.aggregation.timeout == 120


def test_normalize_refs_handles_list() -> None:
    assert normalize_refs(["a", "b", None]) == ["a", "b"]


def test_normalize_refs_handles_projection_scalar() -> None:
    assert normalize_refs("ImageKey(123)") == ["ImageKey(123)"]


def test_normalize_refs_handles_none() -> None:
    assert normalize_refs(None) == []
