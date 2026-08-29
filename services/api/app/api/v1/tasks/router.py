from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ....deps import get_db
from ....models.task import Task
from ....services.tasks.service import (
    create_task,
    delete_task,
    get_task,
    update_task,
)

from .schemas import TaskCreate, TaskResponse, TaskUpdate


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=201)
def create_task_endpoint(
    payload: TaskCreate,
    db: Session = Depends(get_db),
) -> Task:
    try:
        task = create_task(
            db,
            payload.model_dump(),
        )

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Task already exists",
        )

    return task


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_endpoint(
    task_id: str,
    db: Session = Depends(get_db),
) -> Task:
    task = get_task(
        db,
        task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_endpoint(
    task_id: str,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
) -> Task:
    task = get_task(
        db,
        task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    try:
        task = update_task(
            db,
            task,
            payload.model_dump(exclude_unset=True),
        )

    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid task state transition",
        )

    return task


@router.delete("/{task_id}", status_code=204)
def delete_task_endpoint(
    task_id: str,
    db: Session = Depends(get_db),
) -> None:
    task = get_task(
        db,
        task_id,
    )

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    delete_task(
        db,
        task,
    )
