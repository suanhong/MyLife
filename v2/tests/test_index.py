from mylife import create_app
from mylife.repository import MemoryDiaryRepository


def test_index_renders_diary_form():
    response = create_app(MemoryDiaryRepository()).test_client().get("/")
    assert response.status_code == 200
    assert b"MyLife" in response.data
    assert b"diary-form" in response.data
