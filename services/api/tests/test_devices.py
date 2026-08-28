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


def test_create_device_rejects_missing_required_field():
    payload = {
        "node_id": "invalid-device-test-node",
        "node_type": "client",
        "platform": "macos",
        "version": "1.0.0",
        "status": "online",
        "capabilities": ["test"],
        "last_seen": "2026-08-27T12:00:00Z",
    }

    response = client.post("/api/v1/devices", json=payload)

    assert response.status_code == 422


def test_create_device_rejects_empty_required_field():
    payload = {
        "node_id": "",
        "node_type": "client",
        "platform": "macos",
        "version": "1.0.0",
        "status": "online",
        "capabilities": ["test"],
        "agent_id": "validation-test-agent",
        "last_seen": "2026-08-27T12:00:00Z",
    }

    response = client.post("/api/v1/devices", json=payload)

    assert response.status_code == 422


def test_list_devices_pagination():
    payloads = [
        {
            "node_id": "pagination-node-1",
            "node_type": "client",
            "platform": "macos",
            "version": "1.0.0",
            "status": "online",
            "capabilities": ["test"],
            "agent_id": "pagination-agent-1",
            "last_seen": "2026-08-27T12:00:00Z",
        },
        {
            "node_id": "pagination-node-2",
            "node_type": "client",
            "platform": "macos",
            "version": "1.0.0",
            "status": "online",
            "capabilities": ["test"],
            "agent_id": "pagination-agent-2",
            "last_seen": "2026-08-27T12:00:00Z",
        },
    ]

    try:
        for payload in payloads:
            response = client.post("/api/v1/devices", json=payload)
            assert response.status_code == 201

        response = client.get(
            "/api/v1/devices",
            params={"limit": 1, "offset": 0},
        )

        assert response.status_code == 200
        assert len(response.json()) == 1
    finally:
        db = SessionLocal()
        try:
            for node_id in ["pagination-node-1", "pagination-node-2"]:
                device = db.get(Device, node_id)
                if device is not None:
                    db.delete(device)
            db.commit()
        finally:
            db.close()


def test_list_devices_rejects_invalid_pagination():
    response = client.get(
        "/api/v1/devices",
        params={"limit": 0},
    )

    assert response.status_code == 422

    response = client.get(
        "/api/v1/devices",
        params={"limit": 101},
    )

    assert response.status_code == 422

    response = client.get(
        "/api/v1/devices",
        params={"offset": -1},
    )

    assert response.status_code == 422


def test_list_devices_filter_by_status():
    payloads = [
        {
            "node_id": "filter-online-node",
            "node_type": "client",
            "platform": "macos",
            "version": "1.0.0",
            "status": "online",
            "capabilities": ["test"],
            "agent_id": "filter-agent-1",
            "last_seen": "2026-08-27T12:00:00Z",
        },
        {
            "node_id": "filter-offline-node",
            "node_type": "client",
            "platform": "macos",
            "version": "1.0.0",
            "status": "offline",
            "capabilities": ["test"],
            "agent_id": "filter-agent-2",
            "last_seen": "2026-08-27T12:00:00Z",
        },
    ]

    try:
        for payload in payloads:
            response = client.post("/api/v1/devices", json=payload)
            assert response.status_code == 201

        response = client.get(
            "/api/v1/devices",
            params={"status": "offline"},
        )

        assert response.status_code == 200
        devices = response.json()

        assert len(devices) == 1
        assert devices[0]["node_id"] == "filter-offline-node"

    finally:
        db = SessionLocal()
        try:
            for node_id in ["filter-online-node", "filter-offline-node"]:
                device = db.get(Device, node_id)
                if device is not None:
                    db.delete(device)
            db.commit()
        finally:
            db.close()


def test_list_devices_filter_by_agent_id():
    payload = {
        "node_id": "filter-agent-node",
        "node_type": "client",
        "platform": "macos",
        "version": "1.0.0",
        "status": "online",
        "capabilities": ["test"],
        "agent_id": "specific-agent-id",
        "last_seen": "2026-08-27T12:00:00Z",
    }

    created = client.post("/api/v1/devices", json=payload)
    assert created.status_code == 201

    try:
        response = client.get(
            "/api/v1/devices",
            params={"agent_id": "specific-agent-id"},
        )

        assert response.status_code == 200
        devices = response.json()

        assert len(devices) == 1
        assert devices[0]["node_id"] == "filter-agent-node"

    finally:
        db = SessionLocal()
        try:
            device = db.get(Device, "filter-agent-node")
            if device is not None:
                db.delete(device)
                db.commit()
        finally:
            db.close()


def test_list_devices_filter_by_platform():
    payload = {
        "node_id": "filter-platform-node",
        "node_type": "client",
        "platform": "linux",
        "version": "1.0.0",
        "status": "online",
        "capabilities": ["test"],
        "agent_id": "platform-agent",
        "last_seen": "2026-08-27T12:00:00Z",
    }

    created = client.post("/api/v1/devices", json=payload)
    assert created.status_code == 201

    try:
        response = client.get(
            "/api/v1/devices",
            params={"platform": "linux"},
        )

        assert response.status_code == 200
        devices = response.json()

        assert len(devices) == 1
        assert devices[0]["node_id"] == "filter-platform-node"

    finally:
        db = SessionLocal()
        try:
            device = db.get(Device, "filter-platform-node")
            if device is not None:
                db.delete(device)
                db.commit()
        finally:
            db.close()


def test_list_devices_filter_by_node_type():
    payload = {
        "node_id": "filter-node-type-node",
        "node_type": "server",
        "platform": "linux",
        "version": "1.0.0",
        "status": "online",
        "capabilities": ["test"],
        "agent_id": "node-type-agent",
        "last_seen": "2026-08-27T12:00:00Z",
    }

    created = client.post("/api/v1/devices", json=payload)
    assert created.status_code == 201

    try:
        response = client.get(
            "/api/v1/devices",
            params={"node_type": "server"},
        )

        assert response.status_code == 200
        devices = response.json()

        assert len(devices) == 1
        assert devices[0]["node_id"] == "filter-node-type-node"

    finally:
        db = SessionLocal()
        try:
            device = db.get(Device, "filter-node-type-node")
            if device is not None:
                db.delete(device)
                db.commit()
        finally:
            db.close()


def test_list_devices_combined_filters():
    payloads = [
        {
            "node_id": "combined-filter-match-node",
            "node_type": "client",
            "platform": "linux",
            "version": "1.0.0",
            "status": "online",
            "capabilities": ["test"],
            "agent_id": "combined-agent-1",
            "last_seen": "2026-08-27T12:00:00Z",
        },
        {
            "node_id": "combined-filter-other-node",
            "node_type": "client",
            "platform": "linux",
            "version": "1.0.0",
            "status": "offline",
            "capabilities": ["test"],
            "agent_id": "combined-agent-2",
            "last_seen": "2026-08-27T12:00:00Z",
        },
    ]

    try:
        for payload in payloads:
            response = client.post("/api/v1/devices", json=payload)
            assert response.status_code == 201

        response = client.get(
            "/api/v1/devices",
            params={
                "platform": "linux",
                "status": "online",
            },
        )

        assert response.status_code == 200
        devices = response.json()

        assert len(devices) == 1
        assert devices[0]["node_id"] == "combined-filter-match-node"

    finally:
        db = SessionLocal()
        try:
            for node_id in [
                "combined-filter-match-node",
                "combined-filter-other-node",
            ]:
                device = db.get(Device, node_id)
                if device is not None:
                    db.delete(device)
            db.commit()
        finally:
            db.close()


def test_list_devices_order_by_node_id():
    payloads = [
        {
            "node_id": "order-z-node",
            "node_type": "client",
            "platform": "linux",
            "version": "1.0.0",
            "status": "online",
            "capabilities": ["test"],
            "agent_id": "order-agent-z",
            "last_seen": "2026-08-27T12:00:00Z",
        },
        {
            "node_id": "order-a-node",
            "node_type": "client",
            "platform": "linux",
            "version": "1.0.0",
            "status": "online",
            "capabilities": ["test"],
            "agent_id": "order-agent-a",
            "last_seen": "2026-08-27T12:00:00Z",
        },
    ]

    try:
        for payload in payloads:
            response = client.post("/api/v1/devices", json=payload)
            assert response.status_code == 201

        response = client.get("/api/v1/devices")

        assert response.status_code == 200
        devices = response.json()

        ids = [
            device["node_id"]
            for device in devices
            if device["node_id"] in [
                "order-z-node",
                "order-a-node",
            ]
        ]

        assert ids == [
            "order-a-node",
            "order-z-node",
        ]

    finally:
        db = SessionLocal()
        try:
            for node_id in [
                "order-z-node",
                "order-a-node",
            ]:
                device = db.get(Device, node_id)
                if device is not None:
                    db.delete(device)
            db.commit()
        finally:
            db.close()


def test_update_device_rejects_empty_field():
    payload = {
        "node_id": "invalid-update-test-node",
        "node_type": "client",
        "platform": "macos",
        "version": "1.0.0",
        "status": "online",
        "capabilities": ["test"],
        "agent_id": "invalid-update-agent",
        "last_seen": "2026-08-27T12:00:00Z",
    }

    created = client.post("/api/v1/devices", json=payload)
    assert created.status_code == 201

    try:
        response = client.patch(
            "/api/v1/devices/invalid-update-test-node",
            json={"status": ""},
        )

        assert response.status_code == 422

    finally:
        db = SessionLocal()
        try:
            device = db.get(Device, "invalid-update-test-node")
            if device is not None:
                db.delete(device)
                db.commit()
        finally:
            db.close()


def test_create_device_rejects_too_long_field():
    payload = {
        "node_id": "x" * 256,
        "node_type": "client",
        "platform": "macos",
        "version": "1.0.0",
        "status": "online",
        "capabilities": ["test"],
        "agent_id": "validation-test-agent",
        "last_seen": "2026-08-27T12:00:00Z",
    }

    response = client.post("/api/v1/devices", json=payload)

    assert response.status_code == 422
