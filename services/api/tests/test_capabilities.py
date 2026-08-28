from fastapi.testclient import TestClient

from app.db import SessionLocal
from app.main import app
from app.models.capability import Capability

client = TestClient(app)


def test_get_capability():
    payload = {
        "capability_id": "get-capability",
        "name": "test capability",
        "description": "test description",
        "platforms": ["macos"],
        "risk_level": "low",
        "execution_scope": "local",
        "input_schema": {},
        "output_schema": {},
    }

    created = client.post("/api/v1/capabilities", json=payload)
    assert created.status_code == 201

    try:
        response = client.get("/api/v1/capabilities/get-capability")

        assert response.status_code == 200
        assert response.json()["capability_id"] == "get-capability"
        assert response.json()["name"] == "test capability"

    finally:
        db = SessionLocal()
        try:
            capability = db.get(Capability, "get-capability")
            if capability is not None:
                db.delete(capability)
                db.commit()
        finally:
            db.close()

def test_update_capability():
    payload = {
        "capability_id": "update-capability",
        "name": "update capability",
        "description": "before update",
        "platforms": ["macos"],
        "risk_level": "low",
        "execution_scope": "local",
        "input_schema": {},
        "output_schema": {},
    }

    created = client.post("/api/v1/capabilities", json=payload)
    assert created.status_code == 201

    try:
        response = client.patch(
            "/api/v1/capabilities/update-capability",
            json={"risk_level": "high"},
        )

        assert response.status_code == 200
        assert response.json()["risk_level"] == "high"
        assert response.json()["name"] == "update capability"

    finally:
        db = SessionLocal()
        try:
            capability = db.get(Capability, "update-capability")
            if capability is not None:
                db.delete(capability)
                db.commit()
        finally:
            db.close()

def test_delete_capability():
    payload = {
        "capability_id": "delete-capability",
        "name": "delete capability",
        "description": "delete test",
        "platforms": ["macos"],
        "risk_level": "low",
        "execution_scope": "local",
        "input_schema": {},
        "output_schema": {},
    }

    created = client.post("/api/v1/capabilities", json=payload)
    assert created.status_code == 201

    deleted = client.delete("/api/v1/capabilities/delete-capability")

    assert deleted.status_code == 204
    assert deleted.content == b""

    missing = client.get("/api/v1/capabilities/delete-capability")

    assert missing.status_code == 404
