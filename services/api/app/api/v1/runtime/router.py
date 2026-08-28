from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....deps import get_db
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

    task.state = "running"

    if not task.selected_agents:
        task.selected_agents = []

    db.commit()
    db.refresh(task)

    return RuntimeExecuteResponse(
        task_id=task.task_id,
        state=task.state,
        selected_agents=task.selected_agents,
    )
