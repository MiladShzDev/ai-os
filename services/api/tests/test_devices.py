from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_missing_device():
    response = client.get("/api/v1/devices/missing-node")

    assert response.status_code == 404
    assert response.json() == {"detail": "Device not found"}
