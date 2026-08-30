from datetime import datetime, timezone

import pytest

from app.models.agent import Agent
from app.models.task import Task
from app.services.agents.executor import execute_agent


def build_agent(
    status: str = "active",
) -> Agent:
    return Agent(
        agent_id="executor-agent",
        agent_type="server",
        node_id="executor-node",
        status=status,
        capabilities=[],
        tools=[],
        permissions=[],
        state={},
    )


def build_task() -> Task:
    now = datetime.now(timezone.utc)

    return Task(
        task_id="executor-task",
        parent_task_id=None,
        request="test agent execution",
        intent="executor_test",
        target_nodes=[],
        selected_agents=[],
        required_capabilities=[],
        state="pending",
        priority="normal",
        created_at=now,
        updated_at=now,
        result=None,
        error=None,
    )


def test_execute_agent_accepts_active_agent(db_session):
    agent = build_agent()
    task = build_task()

    result = execute_agent(
        db_session,
        agent,
        task,
    )

    assert result == {
        "agent_id": "executor-agent",
        "task_id": "executor-task",
        "status": "completed",
        "output": None,
    }


def test_execute_agent_rejects_inactive_agent(db_session):
    agent = build_agent(
        status="offline",
    )
    task = build_task()

    with pytest.raises(
        ValueError,
        match="Agent is not active",
    ):
        execute_agent(
            db_session,
            agent,
            task,
        )


def test_execute_agent_preserves_task_identity(db_session):
    agent = build_agent()
    task = build_task()

    result = execute_agent(
        db_session,
        agent,
        task,
    )

    assert result["agent_id"] == agent.agent_id
    assert result["task_id"] == task.task_id


def test_execute_agent_returns_execution_status(db_session):
    agent = build_agent()
    task = build_task()

    result = execute_agent(
        db_session,
        agent,
        task,
    )

    assert result["status"] == "completed"


def test_execute_agent_contains_output_field(db_session):
    agent = build_agent()
    task = build_task()

    result = execute_agent(
        db_session,
        agent,
        task,
    )

    assert "output" in result
