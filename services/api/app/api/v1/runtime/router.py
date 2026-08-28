from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....deps import get_db
from ....models.agent import Agent
from ....models.device import Device
from ....models.permission import Permission
from ....models.task import Task


def has_permission(db, agent_id: str, capability: str) -> bool:
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


from .schemas import RuntimeExecuteRequest, RuntimeExecuteResponse

router = APIRouter(prefix="/runtime", tags=["runtime"])


@router.post("/execute", response_model=RuntimeExecuteResponse)
def execute_task(
    payload: RuntimeExecuteRequest,
    db: Session = Depends(get_db),
) -> RuntimeExecuteResponse:
    task = db.get(Task, payload.task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    selected_agents = []

    if task.required_capabilities:
        agents = db.query(Agent).filter(
            Agent.status == "active"
        ).all()

        for agent in agents:
            device = db.get(Device, agent.node_id)

            if device is None or device.status != "active":
                continue

            if all(
                capability in agent.capabilities
                and has_permission(db, agent.agent_id, capability)
                for capability in task.required_capabilities
            ):
                selected_agents.append(agent.agent_id)

    task.selected_agents = selected_agents
    task.state = "running"

    db.commit()
    db.refresh(task)

    return RuntimeExecuteResponse(
        task_id=task.task_id,
        state=task.state,
        selected_agents=task.selected_agents,
    )
