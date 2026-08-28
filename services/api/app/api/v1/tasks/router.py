from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ....deps import get_db
from ....models.task import Task
from .schemas import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=201)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
) -> Task:
    if db.get(Task, payload.task_id) is not None:
        raise HTTPException(status_code=409, detail="Task already exists")

    task = Task(**payload.model_dump())
    db.add(task)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Task already exists")

    db.refresh(task)

    return task


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: str,
    db: Session = Depends(get_db),
) -> Task:
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: str,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
) -> Task:
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(
    task_id: str,
    db: Session = Depends(get_db),
) -> None:
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
