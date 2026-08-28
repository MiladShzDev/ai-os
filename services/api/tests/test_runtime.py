from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.db import SessionLocal
from app.main import app
from app.models.task import Task

client = TestClient(app)


def test_runtime_execute_task():
    db = SessionLocal()

    task = Task(
        task_id="runtime-test-task",
        parent_task_id=None,
        request="execute runtime task",
        intent="runtime_test",
        target_nodes=[],
        selected_agents=[],
        required_capabilities=[],
        state="pending",
        priority="normal",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        result=None,
        error=None,
    )

    db.add(task)
    db.commit()
    db.close()

    try:
        response = client.post(
            "/api/v1/runtime/execute",
            json={
                "task_id": "runtime-test-task"
            },
        )

        assert response.status_code == 200
        assert response.json()["task_id"] == "runtime-test-task"
        assert response.json()["state"] == "running"
        assert response.json()["selected_agents"] == []

    finally:
        db = SessionLocal()
        try:
            task = db.get(Task, "runtime-test-task")
            if task is not None:
                db.delete(task)
                db.commit()
        finally:
            db.close()
