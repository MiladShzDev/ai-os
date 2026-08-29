from sqlalchemy.orm import Session

from ...models.task import Task


ALLOWED_TRANSITIONS = {
    "pending": {"running", "failed"},
    "running": {"completed", "failed"},
    "completed": set(),
    "failed": set(),
}


def can_transition(
    current_state: str,
    new_state: str,
) -> bool:
    if current_state == new_state:
        return True

    return new_state in ALLOWED_TRANSITIONS.get(
        current_state,
        set(),
    )


def update_task_state(
    db: Session,
    task: Task,
    new_state: str,
    error: dict | None = None,
) -> Task:
    if not can_transition(
        task.state,
        new_state,
    ):
        raise ValueError(
            "Invalid task state transition"
        )

    task.state = new_state
    task.error = error

    db.commit()
    db.refresh(task)

    return task
