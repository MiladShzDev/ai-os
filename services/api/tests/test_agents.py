from app.db import SessionLocal
from app.models.agent import Agent
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_agent():
    payload = {
        "agent_id": "test-agent",
        "agent_type": "server",
        "node_id": "test-node",
        "status": "online",
        "capabilities": ["test"],
        "tools": [],
        "permissions": [],
        "state": {},
    }

    response = client.post("/api/v1/agents", json=payload)

    assert response.status_code == 201
    assert response.json()["agent_id"] == "test-agent"

    db = SessionLocal()
    try:
        agent = db.get(Agent, "test-agent")
        if agent is not None:
            db.delete(agent)
            db.commit()
    finally:
        db.close()


def test_get_missing_agent():
    response = client.get("/api/v1/agents/missing-agent")

    assert response.status_code == 404
    assert response.json() == {"detail": "Agent not found"}


def test_get_agent():
    payload = {
        "agent_id": "get-test-agent",
        "agent_type": "client",
        "node_id": "get-test-node",
        "status": "online",
        "capabilities": ["test"],
        "tools": [],
        "permissions": [],
        "state": {},
    }

    created = client.post("/api/v1/agents", json=payload)
    assert created.status_code == 201

    try:
        response = client.get("/api/v1/agents/get-test-agent")

        assert response.status_code == 200
        assert response.json()["agent_id"] == "get-test-agent"
        assert response.json()["node_id"] == "get-test-node"

    finally:
        db = SessionLocal()
        try:
            agent = db.get(Agent, "get-test-agent")
            if agent is not None:
                db.delete(agent)
                db.commit()
        finally:
            db.close()


def test_create_duplicate_agent():
    payload = {
        "agent_id": "duplicate-agent",
        "agent_type": "client",
        "node_id": "duplicate-node",
        "status": "online",
        "capabilities": [],
        "tools": [],
        "permissions": [],
        "state": {},
    }

    first = client.post("/api/v1/agents", json=payload)
    assert first.status_code == 201

    try:
        second = client.post("/api/v1/agents", json=payload)

        assert second.status_code == 409
        assert second.json() == {"detail": "Agent already exists"}

    finally:
        db = SessionLocal()
        try:
            agent = db.get(Agent, "duplicate-agent")
            if agent is not None:
                db.delete(agent)
                db.commit()
        finally:
            db.close()


def test_update_agent():
    payload = {
        "agent_id": "update-agent",
        "agent_type": "client",
        "node_id": "update-node",
        "status": "online",
        "capabilities": [],
        "tools": [],
        "permissions": [],
        "state": {},
    }

    created = client.post("/api/v1/agents", json=payload)
    assert created.status_code == 201

    try:
        response = client.patch(
            "/api/v1/agents/update-agent",
            json={"status": "offline"},
        )

        assert response.status_code == 200
        assert response.json()["status"] == "offline"
        assert response.json()["agent_type"] == "client"

    finally:
        db = SessionLocal()
        try:
            agent = db.get(Agent, "update-agent")
            if agent is not None:
                db.delete(agent)
                db.commit()
        finally:
            db.close()


def test_update_missing_agent():
    response = client.patch(
        "/api/v1/agents/missing-update-agent",
        json={"status": "offline"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Agent not found"}


def test_delete_missing_agent():
    response = client.delete("/api/v1/agents/missing-delete-agent")

    assert response.status_code == 404
    assert response.json() == {"detail": "Agent not found"}


def test_delete_agent():
    payload = {
        "agent_id": "delete-agent",
        "agent_type": "client",
        "node_id": "delete-node",
        "status": "online",
        "capabilities": [],
        "tools": [],
        "permissions": [],
        "state": {},
    }

    created = client.post("/api/v1/agents", json=payload)
    assert created.status_code == 201

    deleted = client.delete("/api/v1/agents/delete-agent")

    assert deleted.status_code == 204
    assert deleted.content == b""

    missing = client.get("/api/v1/agents/delete-agent")
    assert missing.status_code == 404


def test_create_agent_rejects_missing_required_field():
    payload = {
        "agent_id": "invalid-agent",
        "agent_type": "client",
        "node_id": "invalid-node",
        "status": "online",
        "capabilities": [],
        "tools": [],
        "permissions": [],
    }

    response = client.post("/api/v1/agents", json=payload)

    assert response.status_code == 422


def test_create_agent_rejects_empty_required_field():
    payload = {
        "agent_id": "",
        "agent_type": "client",
        "node_id": "invalid-node",
        "status": "online",
        "capabilities": [],
        "tools": [],
        "permissions": [],
        "state": {},
    }

    response = client.post("/api/v1/agents", json=payload)

    assert response.status_code == 422


def test_create_agent_rejects_too_long_field():
    payload = {
        "agent_id": "x" * 256,
        "agent_type": "client",
        "node_id": "invalid-node",
        "status": "online",
        "capabilities": [],
        "tools": [],
        "permissions": [],
        "state": {},
    }

    response = client.post("/api/v1/agents", json=payload)

    assert response.status_code == 422


def test_agent_response_contains_all_fields():
    payload = {
        "agent_id": "response-agent",
        "agent_type": "server",
        "node_id": "response-node",
        "status": "online",
        "capabilities": ["execute"],
        "tools": ["shell"],
        "permissions": ["read"],
        "state": {"ready": True},
    }

    created = client.post("/api/v1/agents", json=payload)
    assert created.status_code == 201

    try:
        agent = created.json()

        assert agent["agent_id"] == "response-agent"
        assert agent["agent_type"] == "server"
        assert agent["node_id"] == "response-node"
        assert agent["status"] == "online"
        assert agent["capabilities"] == ["execute"]
        assert agent["tools"] == ["shell"]
        assert agent["permissions"] == ["read"]
        assert agent["state"] == {"ready": True}

    finally:
        db = SessionLocal()
        try:
            agent = db.get(Agent, "response-agent")
            if agent is not None:
                db.delete(agent)
                db.commit()
        finally:
            db.close()
