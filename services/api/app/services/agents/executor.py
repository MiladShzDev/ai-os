from sqlalchemy.orm import Session

from ...models.agent import Agent
from ...models.task import Task


def execute_agent(
    db: Session,
    agent: Agent,
    task: Task,
) -> dict:
    if agent.status != "active":
        raise ValueError("Agent is not active")

    result = {
        "agent_id": agent.agent_id,
        "task_id": task.task_id,
        "status": "completed",
        "output": None,
    }

    return result
