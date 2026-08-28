from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....deps import get_db
from ....models.agent import Agent
from ....models.task import Task
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
            if all(
                capability in agent.capabilities
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
