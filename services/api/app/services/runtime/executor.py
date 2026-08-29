from datetime import datetime, timezone

from sqlalchemy.orm import Session

from ...models.agent import Agent
from ...models.device import Device
from ...models.permission import Permission
from ...models.task import Task
from ..tasks.lifecycle import update_task_state


def has_permission(
    db: Session,
    agent_id: str,
    capability: str,
) -> bool:
    permissions = db.query(Permission).filter(
        Permission.subject == agent_id,
        Permission.capability == capability,
        Permission.decision == "allow",
    ).all()

    now = datetime.now(timezone.utc)

    for permission in permissions:
        if permission.expires_at is None or permission.expires_at > now:
            return True

    return False


def select_agents(
    db: Session,
    task: Task,
) -> list[str]:
    selected_agents = []

    agents = db.query(Agent).filter(
        Agent.status == "active"
    ).all()

    for agent in agents:
        device = db.get(Device, agent.node_id)

        if device is None or device.status != "active":
            continue

        if all(
            capability in agent.capabilities
            and has_permission(
                db,
                agent.agent_id,
                capability,
            )
            for capability in task.required_capabilities
        ):
            selected_agents.append(agent.agent_id)

    return selected_agents


def execute_task(
    db: Session,
    task: Task,
) -> Task:
    selected_agents = select_agents(
        db,
        task,
    )

    if not selected_agents:
        update_task_state(
            db,
            task,
            "failed",
            {
                "reason": "No available agent",
            },
        )

    else:
        task.selected_agents = selected_agents

        update_task_state(
            db,
            task,
            "running",
        )

    return task
