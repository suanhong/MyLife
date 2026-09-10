from mylife import create_app
from mylife.repository import MemoryDiaryRepository


def test_app_factory_exposes_diary_api():
    app = create_app(MemoryDiaryRepository())
    client = app.test_client()
    assert client.put("/api/diaries/2026-09-10", json={"text": "hello"}).status_code == 200
    assert client.get("/api/diaries/2026-09-10").get_json()["text"] == "hello"
