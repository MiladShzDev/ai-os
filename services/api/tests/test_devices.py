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


def test_create_duplicate_device():
    payload = {
        "node_id": "duplicate-test-node",
        "node_type": "client",
        "platform": "macos",
        "version": "1.0.0",
        "status": "online",
        "capabilities": [],
        "agent_id": "duplicate-test-agent",
        "last_seen": "2026-08-27T12:00:00Z",
    }

    first = client.post("/api/v1/devices", json=payload)

    assert first.status_code == 201

    try:
        second = client.post("/api/v1/devices", json=payload)

        assert second.status_code == 409
        assert second.json() == {"detail": "Device already exists"}
    finally:
        db = SessionLocal()
        try:
            device = db.get(Device, "duplicate-test-node")
            if device is not None:
                db.delete(device)
                db.commit()
        finally:
            db.close()


def test_create_duplicate_device_race_safe():
    payload = {
        "node_id": "race-test-node",
        "node_type": "client",
        "platform": "macos",
        "version": "1.0.0",
        "status": "online",
        "capabilities": ["test"],
        "agent_id": "race-test-agent",
        "last_seen": "2026-08-27T12:00:00Z",
    }

    db = SessionLocal()
    try:
        existing = db.get(Device, "race-test-node")
        if existing is not None:
            db.delete(existing)
            db.commit()
    finally:
        db.close()

    first = client.post("/api/v1/devices", json=payload)
    assert first.status_code == 201

    second = client.post("/api/v1/devices", json=payload)
    assert second.status_code == 409
    assert second.json() == {"detail": "Device already exists"}

    db = SessionLocal()
    try:
        device = db.get(Device, "race-test-node")
        assert device is not None
        db.delete(device)
        db.commit()
    finally:
        db.close()


def test_delete_missing_device():
    response = client.delete("/api/v1/devices/missing-delete-node")

    assert response.status_code == 404
    assert response.json() == {"detail": "Device not found"}


def test_delete_device():
    payload = {
        "node_id": "delete-test-node",
        "node_type": "client",
        "platform": "macos",
        "version": "1.0.0",
        "status": "online",
        "capabilities": ["test"],
        "agent_id": "delete-test-agent",
        "last_seen": "2026-08-27T12:00:00Z",
    }

    created = client.post("/api/v1/devices", json=payload)
    assert created.status_code == 201

    deleted = client.delete("/api/v1/devices/delete-test-node")
    assert deleted.status_code == 204
    assert deleted.content == b""

    missing = client.get("/api/v1/devices/delete-test-node")
    assert missing.status_code == 404


def test_update_device():
    payload = {
        "node_id": "update-test-node",
        "node_type": "client",
        "platform": "macos",
        "version": "1.0.0",
        "status": "online",
        "capabilities": ["test"],
        "agent_id": "update-test-agent",
        "last_seen": "2026-08-27T12:00:00Z",
    }

    created = client.post("/api/v1/devices", json=payload)
    assert created.status_code == 201

    try:
        response = client.patch(
            "/api/v1/devices/update-test-node",
            json={
                "version": "2.0.0",
                "status": "offline",
            },
        )

        assert response.status_code == 200
        assert response.json()["node_id"] == "update-test-node"
        assert response.json()["version"] == "2.0.0"
        assert response.json()["status"] == "offline"
        assert response.json()["platform"] == "macos"
        assert response.json()["agent_id"] == "update-test-agent"
    finally:
        db = SessionLocal()
        try:
            device = db.get(Device, "update-test-node")
            if device is not None:
                db.delete(device)
                db.commit()
        finally:
            db.close()


def test_update_missing_device():
    response = client.patch(
        "/api/v1/devices/missing-update-node",
        json={"status": "offline"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Device not found"}


def test_update_device_empty_payload():
    payload = {
        "node_id": "empty-update-test-node",
        "node_type": "client",
        "platform": "macos",
        "version": "1.0.0",
        "status": "online",
        "capabilities": ["test"],
        "agent_id": "empty-update-test-agent",
        "last_seen": "2026-08-27T12:00:00Z",
    }

    created = client.post("/api/v1/devices", json=payload)
    assert created.status_code == 201

    try:
        response = client.patch(
            "/api/v1/devices/empty-update-test-node",
            json={},
        )

        assert response.status_code == 200
        assert response.json()["node_id"] == "empty-update-test-node"
        assert response.json()["version"] == "1.0.0"
        assert response.json()["status"] == "online"
    finally:
        db = SessionLocal()
        try:
            device = db.get(Device, "empty-update-test-node")
            if device is not None:
                db.delete(device)
                db.commit()
        finally:
            db.close()
