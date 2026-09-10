from datetime import date

from flask import Flask

from mylife.repository import MemoryDiaryRepository
from mylife.web import create_diary_blueprint


def client_and_repo():
    app = Flask(__name__)
    repo = MemoryDiaryRepository()
    app.register_blueprint(create_diary_blueprint(repo))
    return app.test_client(), repo


def test_put_get_delete_diary():
    client, repo = client_and_repo()
    response = client.put("/api/diaries/2026-09-10", json={"text": "hello"})
    assert response.status_code == 200
    assert repo.get(date(2026, 9, 10)).text == "hello"

    response = client.get("/api/diaries/2026-09-10")
    assert response.get_json()["text"] == "hello"

    assert client.delete("/api/diaries/2026-09-10").status_code == 204
    assert client.get("/api/diaries/2026-09-10").status_code == 404
