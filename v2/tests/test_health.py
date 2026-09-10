from mylife import create_app
from mylife.repository import MemoryDiaryRepository


def test_healthz():
    app = create_app(MemoryDiaryRepository())
    client = app.test_client()
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.get_json() == {"service": "mylife-v2", "status": "ok"}
