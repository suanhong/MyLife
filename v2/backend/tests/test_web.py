from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_serves_diary_interface() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "MyLife" in response.text
    assert "본문 검색" in response.text


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "mylife-v2"}


def test_entry_search() -> None:
    response = client.get("/api/entries", params={"q": "backend"})
    assert response.status_code == 200
    assert response.json()["total"] == 1


def test_invalid_date_range() -> None:
    response = client.get(
        "/api/entries",
        params={"date_from": "2026-09-15", "date_to": "2026-09-14"},
    )
    assert response.status_code == 422
