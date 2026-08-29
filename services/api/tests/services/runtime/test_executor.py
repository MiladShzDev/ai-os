from datetime import datetime, timezone

from app.db import SessionLocal
from app.models.agent import Agent
from app.models.device import Device
from app.models.permission import Permission
from app.models.task import Task
from app.services.runtime.executor import execute_task


def test_execute_task_selects_agent_and_runs():
    db_session = SessionLocal()

    agent = Agent(
        agent_id="service-runtime-agent",
        agent_type="local",
        node_id="service-runtime-node",
        status="active",
        capabilities=["shell"],
        tools=[],
        permissions=[],
        state={},
    )

    device = Device(
        node_id="service-runtime-node",
        node_type="desktop",
        platform="linux",
        version="1.0",
        status="active",
        capabilities=["shell"],
        agent_id="service-runtime-agent",
        last_seen=datetime.now(timezone.utc),
    )

    permission = Permission(
        permission_id="service-runtime-permission",
        subject="service-runtime-agent",
        capability="shell",
        scope={},
        policy="default",
        decision="allow",
        confirmation_required=False,
        expires_at=None,
    )

    task = Task(
        task_id="service-runtime-task",
        parent_task_id=None,
        request="execute shell task",
        intent="runtime_service_test",
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

    db_session.add(agent)
    db_session.add(device)
    db_session.add(permission)
    db_session.add(task)
    db_session.commit()

    try:
        result = execute_task(
            db_session,
            task,
        )

        assert result.state == "running"
        assert result.selected_agents == [
            "service-runtime-agent"
        ]
        assert result.error is None

    finally:
        db_session.delete(task)
        db_session.delete(permission)
        db_session.delete(device)
        db_session.delete(agent)
        db_session.commit()
        db_session.close()
