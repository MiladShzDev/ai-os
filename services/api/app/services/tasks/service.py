from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ...models.task import Task
from .lifecycle import update_task_state


def create_task(
    db: Session,
    task_data: dict,
) -> Task:
    task = Task(**task_data)

    db.add(task)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise

    db.refresh(task)

    return task


def get_task(
    db: Session,
    task_id: str,
) -> Task | None:
    return db.get(Task, task_id)


def update_task(
    db: Session,
    task: Task,
    updates: dict,
) -> Task:
    if "state" in updates:
        update_task_state(
            db,
            task,
            updates.pop("state"),
        )

    for field, value in updates.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    db: Session,
    task: Task,
) -> None:
    db.delete(task)
    db.commit()
