from fastapi.testclient import TestClient

from api.main import api

client = TestClient(api)


def test_ready():
    response = client.get("/v1/readyz")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}
