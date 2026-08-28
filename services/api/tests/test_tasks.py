from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.db import SessionLocal
from app.main import app
from app.models.task import Task

client = TestClient(app)


def test_create_task():
    payload = {
        "task_id": "test-task",
        "parent_task_id": None,
        "request": "run test command",
        "intent": "execute",
        "target_nodes": ["node-1"],
        "selected_agents": ["agent-1"],
        "required_capabilities": ["shell"],
        "state": "pending",
        "priority": "normal",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "result": None,
        "error": None,
    }

    response = client.post("/api/v1/tasks", json=payload)

    assert response.status_code == 201
    assert response.json()["task_id"] == "test-task"

    db = SessionLocal()
    try:
        task = db.get(Task, "test-task")
        if task is not None:
            db.delete(task)
            db.commit()
    finally:
        db.close()


def test_get_task():
    payload = {
        "task_id": "get-task",
        "parent_task_id": None,
        "request": "test request",
        "intent": "testing",
        "target_nodes": ["node-1"],
        "selected_agents": ["agent-1"],
        "required_capabilities": ["test"],
        "state": "pending",
        "priority": "normal",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "result": None,
        "error": None,
    }

    created = client.post("/api/v1/tasks", json=payload)
    assert created.status_code == 201

    try:
        response = client.get("/api/v1/tasks/get-task")

        assert response.status_code == 200
        assert response.json()["task_id"] == "get-task"
        assert response.json()["request"] == "test request"

    finally:
        db = SessionLocal()
        try:
            task = db.get(Task, "get-task")
            if task is not None:
                db.delete(task)
                db.commit()
        finally:
            db.close()


def test_update_task():
    payload = {
        "task_id": "update-task",
        "parent_task_id": None,
        "request": "update test request",
        "intent": "testing",
        "target_nodes": ["node-1"],
        "selected_agents": ["agent-1"],
        "required_capabilities": ["test"],
        "state": "pending",
        "priority": "normal",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "result": None,
        "error": None,
    }

    created = client.post("/api/v1/tasks", json=payload)
    assert created.status_code == 201

    try:
        response = client.patch(
            "/api/v1/tasks/update-task",
            json={"state": "running"},
        )

        assert response.status_code == 200
        assert response.json()["state"] == "running"
        assert response.json()["request"] == "update test request"

    finally:
        db = SessionLocal()
        try:
            task = db.get(Task, "update-task")
            if task is not None:
                db.delete(task)
                db.commit()
        finally:
            db.close()


def test_delete_task():
    payload = {
        "task_id": "delete-task",
        "parent_task_id": None,
        "request": "delete test request",
        "intent": "testing",
        "target_nodes": ["node-1"],
        "selected_agents": ["agent-1"],
        "required_capabilities": ["test"],
        "state": "pending",
        "priority": "normal",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "result": None,
        "error": None,
    }

    created = client.post("/api/v1/tasks", json=payload)
    assert created.status_code == 201

    deleted = client.delete("/api/v1/tasks/delete-task")

    assert deleted.status_code == 204
    assert deleted.content == b""

    missing = client.get("/api/v1/tasks/delete-task")

    assert missing.status_code == 404


def test_create_duplicate_task():
    payload = {
        "task_id": "duplicate-task",
        "parent_task_id": None,
        "request": "duplicate test request",
        "intent": "testing",
        "target_nodes": ["node-1"],
        "selected_agents": ["agent-1"],
        "required_capabilities": ["test"],
        "state": "pending",
        "priority": "normal",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "result": None,
        "error": None,
    }

    first = client.post("/api/v1/tasks", json=payload)

    assert first.status_code == 201

    try:
        second = client.post("/api/v1/tasks", json=payload)

        assert second.status_code == 409
        assert second.json() == {"detail": "Task already exists"}

    finally:
        db = SessionLocal()
        try:
            task = db.get(Task, "duplicate-task")
            if task is not None:
                db.delete(task)
                db.commit()
        finally:
            db.close()


def test_create_task_rejects_too_long_field():
    payload = {
        "task_id": "x" * 256,
        "parent_task_id": None,
        "request": "test request",
        "intent": "testing",
        "target_nodes": [],
        "selected_agents": [],
        "required_capabilities": [],
        "state": "pending",
        "priority": "normal",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "result": None,
        "error": None,
    }

    response = client.post("/api/v1/tasks", json=payload)

    assert response.status_code == 422


def test_task_response_contains_all_fields():
    payload = {
        "task_id": "response-task",
        "parent_task_id": None,
        "request": "schema test request",
        "intent": "execute",
        "target_nodes": ["node-1"],
        "selected_agents": ["agent-1"],
        "required_capabilities": ["shell"],
        "state": "pending",
        "priority": "high",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "result": {"ok": True},
        "error": None,
    }

    created = client.post("/api/v1/tasks", json=payload)
    assert created.status_code == 201

    try:
        task = created.json()

        assert task["task_id"] == "response-task"
        assert task["request"] == "schema test request"
        assert task["intent"] == "execute"
        assert task["target_nodes"] == ["node-1"]
        assert task["selected_agents"] == ["agent-1"]
        assert task["required_capabilities"] == ["shell"]
        assert task["state"] == "pending"
        assert task["priority"] == "high"
        assert task["result"] == {"ok": True}
        assert task["error"] is None
        assert task["created_at"] is not None
        assert task["updated_at"] is not None

    finally:
        db = SessionLocal()
        try:
            task = db.get(Task, "response-task")
            if task is not None:
                db.delete(task)
                db.commit()
        finally:
            db.close()


def test_update_task_keeps_unmodified_fields():
    payload = {
        "task_id": "partial-update-task",
        "parent_task_id": None,
        "request": "partial update request",
        "intent": "testing",
        "target_nodes": ["node-1"],
        "selected_agents": ["agent-1"],
        "required_capabilities": ["shell"],
        "state": "pending",
        "priority": "normal",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "result": None,
        "error": None,
    }

    created = client.post("/api/v1/tasks", json=payload)
    assert created.status_code == 201

    try:
        response = client.patch(
            "/api/v1/tasks/partial-update-task",
            json={"state": "running"},
        )

        assert response.status_code == 200
        task = response.json()

        assert task["state"] == "running"
        assert task["request"] == "partial update request"
        assert task["priority"] == "normal"
        assert task["intent"] == "testing"

    finally:
        db = SessionLocal()
        try:
            task = db.get(Task, "partial-update-task")
            if task is not None:
                db.delete(task)
                db.commit()
        finally:
            db.close()
