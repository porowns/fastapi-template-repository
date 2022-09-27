from fastapi.testclient import TestClient

from api.main import api

client = TestClient(api)


def test_health():
    response = client.get("/v1/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
