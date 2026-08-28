from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.db import SessionLocal
from app.main import app
from app.models.agent import Agent
from app.models.device import Device
from app.models.permission import Permission
from app.models.task import Task

client = TestClient(app)


def test_runtime_execute_selects_agent_by_capability():
    db = SessionLocal()

    agent = Agent(
        agent_id="runtime-agent",
        agent_type="local",
        node_id="runtime-node",
        status="active",
        capabilities=["shell"],
        tools=[],
        permissions=[],
        state={},
    )

    device = Device(
        node_id="runtime-node",
        node_type="desktop",
        platform="linux",
        version="1.0",
        status="active",
        capabilities=["shell"],
        agent_id="runtime-agent",
        last_seen=datetime.now(timezone.utc),
    )

    permission = Permission(
        permission_id="runtime-permission",
        subject="runtime-agent",
        capability="shell",
        scope={},
        policy="default",
        decision="allow",
        confirmation_required=False,
        expires_at=None,
    )

    task = Task(
        task_id="runtime-capability-task",
        parent_task_id=None,
        request="execute shell task",
        intent="runtime_test",
        target_nodes=[],
        selected_agents=[],
        required_capabilities=["shell"],
        state="pending",
        priority="normal",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        result=None,
        error=None,
    )

    db.add(agent)
    db.add(device)
    db.add(permission)
    db.add(task)
    db.commit()
    db.close()

    try:
        response = client.post(
            "/api/v1/runtime/execute",
            json={
                "task_id": "runtime-capability-task"
            },
        )

        assert response.status_code == 200
        assert response.json()["state"] == "running"
        assert response.json()["selected_agents"] == [
            "runtime-agent"
        ]

    finally:
        db = SessionLocal()

        try:
            task = db.get(Task, "runtime-capability-task")
            if task is not None:
                db.delete(task)

            agent = db.get(Agent, "runtime-agent")
            if agent is not None:
                db.delete(agent)

            device = db.get(Device, "runtime-node")
            if device is not None:
                db.delete(device)

            permission = db.get(Permission, "runtime-permission")
            if permission is not None:
                db.delete(permission)

            db.commit()

        finally:
            db.close()
