from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.db import SessionLocal
from app.main import app
from app.models.device import Device

client = TestClient(app)


def test_get_missing_device():
    response = client.get("/api/v1/devices/missing-node")

    assert response.status_code == 404
    assert response.json() == {"detail": "Device not found"}


def test_get_device():
    db = SessionLocal()

    device = Device(
        node_id="test-node",
        node_type="client",
        platform="macos",
        version="1.0.0",
        status="online",
        capabilities=[],
        agent_id="test-agent",
        last_seen=datetime.now(timezone.utc),
    )

    try:
        db.add(device)
        db.commit()

        response = client.get("/api/v1/devices/test-node")

        assert response.status_code == 200
        assert response.json()["node_id"] == "test-node"
        assert response.json()["node_type"] == "client"
        assert response.json()["platform"] == "macos"
        assert response.json()["agent_id"] == "test-agent"
    finally:
        db.delete(device)
        db.commit()
        db.close()


def test_list_devices():
    response = client.get("/api/v1/devices")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_device():
    payload = {
        "node_id": "create-test-node",
        "node_type": "client",
        "platform": "macos",
        "version": "1.0.0",
        "status": "online",
        "capabilities": ["test"],
        "agent_id": "create-test-agent",
        "last_seen": "2026-08-27T12:00:00Z",
    }

    response = client.post("/api/v1/devices", json=payload)

    assert response.status_code == 201
    assert response.json()["node_id"] == "create-test-node"
    assert response.json()["agent_id"] == "create-test-agent"

    db = SessionLocal()
    try:
        device = db.get(Device, "create-test-node")
        assert device is not None
        db.delete(device)
        db.commit()
    finally:
        db.close()
