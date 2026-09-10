from datetime import date

from mylife import create_app
from mylife.repository import DiaryEntry, MemoryDiaryRepository


def test_list_diaries_api():
    repo = MemoryDiaryRepository()
    repo.save(DiaryEntry(date(2026, 9, 10), "today"))
    response = create_app(repo).test_client().get("/api/diaries?limit=10")
    assert response.status_code == 200
    assert response.get_json()["entries"][0]["text"] == "today"
