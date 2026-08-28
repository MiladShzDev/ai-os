from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.db import SessionLocal
from app.main import app
from app.models.permission import Permission

client = TestClient(app)


def test_create_permission():
    payload = {
        "permission_id": "test-permission",
        "subject": "test-agent",
        "capability": "test-capability",
        "scope": {},
        "policy": "default",
        "decision": "allow",
        "confirmation_required": False,
        "expires_at": datetime.now(timezone.utc).isoformat(),
    }

    response = client.post("/api/v1/permissions", json=payload)

    assert response.status_code == 201
    assert response.json()["permission_id"] == "test-permission"

    db = SessionLocal()
    try:
        permission = db.get(Permission, "test-permission")
        if permission is not None:
            db.delete(permission)
            db.commit()
    finally:
        db.close()


def test_get_permission():
    payload = {
        "permission_id": "get-permission",
        "subject": "get-agent",
        "capability": "get-capability",
        "scope": {},
        "policy": "default",
        "decision": "allow",
        "confirmation_required": False,
        "expires_at": None,
    }

    created = client.post("/api/v1/permissions", json=payload)
    assert created.status_code == 201

    try:
        response = client.get("/api/v1/permissions/get-permission")

        assert response.status_code == 200
        assert response.json()["permission_id"] == "get-permission"
        assert response.json()["subject"] == "get-agent"

    finally:
        db = SessionLocal()
        try:
            permission = db.get(Permission, "get-permission")
            if permission is not None:
                db.delete(permission)
                db.commit()
        finally:
            db.close()


def test_update_permission():
    payload = {
        "permission_id": "update-permission",
        "subject": "update-agent",
        "capability": "update-capability",
        "scope": {},
        "policy": "default",
        "decision": "deny",
        "confirmation_required": False,
        "expires_at": None,
    }

    created = client.post("/api/v1/permissions", json=payload)
    assert created.status_code == 201

    try:
        response = client.patch(
            "/api/v1/permissions/update-permission",
            json={"decision": "allow"},
        )

        assert response.status_code == 200
        assert response.json()["decision"] == "allow"
        assert response.json()["subject"] == "update-agent"

    finally:
        db = SessionLocal()
        try:
            permission = db.get(Permission, "update-permission")
            if permission is not None:
                db.delete(permission)
                db.commit()
        finally:
            db.close()


def test_delete_permission():
    payload = {
        "permission_id": "delete-permission",
        "subject": "delete-agent",
        "capability": "delete-capability",
        "scope": {},
        "policy": "default",
        "decision": "allow",
        "confirmation_required": False,
        "expires_at": None,
    }

    created = client.post("/api/v1/permissions", json=payload)
    assert created.status_code == 201

    deleted = client.delete("/api/v1/permissions/delete-permission")

    assert deleted.status_code == 204
    assert deleted.content == b""

    missing = client.get("/api/v1/permissions/delete-permission")

    assert missing.status_code == 404


def test_create_duplicate_permission():
    payload = {
        "permission_id": "duplicate-permission",
        "subject": "duplicate-agent",
        "capability": "duplicate-capability",
        "scope": {},
        "policy": "default",
        "decision": "allow",
        "confirmation_required": False,
        "expires_at": None,
    }

    first = client.post("/api/v1/permissions", json=payload)

    assert first.status_code == 201

    try:
        second = client.post("/api/v1/permissions", json=payload)

        assert second.status_code == 409
        assert second.json() == {
            "detail": "Permission already exists"
        }

    finally:
        db = SessionLocal()
        try:
            permission = db.get(Permission, "duplicate-permission")
            if permission is not None:
                db.delete(permission)
                db.commit()
        finally:
            db.close()


def test_create_duplicate_permission():
    payload = {
        "permission_id": "duplicate-permission",
        "subject": "duplicate-agent",
        "capability": "duplicate-capability",
        "scope": {},
        "policy": "default",
        "decision": "allow",
        "confirmation_required": False,
        "expires_at": None,
    }

    first = client.post("/api/v1/permissions", json=payload)

    assert first.status_code == 201

    try:
        second = client.post("/api/v1/permissions", json=payload)

        assert second.status_code == 409
        assert second.json() == {
            "detail": "Permission already exists"
        }

    finally:
        db = SessionLocal()
        try:
            permission = db.get(Permission, "duplicate-permission")
            if permission is not None:
                db.delete(permission)
                db.commit()
        finally:
            db.close()


def test_create_permission_rejects_too_long_field():
    payload = {
        "permission_id": "x" * 256,
        "subject": "test-subject",
        "capability": "test-capability",
        "scope": {},
        "policy": "default",
        "decision": "allow",
        "confirmation_required": False,
        "expires_at": None,
    }

    response = client.post("/api/v1/permissions", json=payload)

    assert response.status_code == 422
