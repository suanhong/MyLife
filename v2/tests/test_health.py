from mylife import create_app
from mylife.repository import MemoryDiaryRepository


def test_healthz():
    app = create_app(MemoryDiaryRepository())
    response = app.test_client().get("/healthz")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["service"] == "mylife-v2"
    assert payload["status"] == "ok"
    assert payload["version"] == "0.1.0-foundation"
