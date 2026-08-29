from datetime import datetime, timezone

import pytest

from app.models.task import Task
from app.services.tasks.service import (
    create_task,
    delete_task,
    get_task,
    update_task,
)


def build_task_data(task_id: str):
    return {
        "task_id": task_id,
        "parent_task_id": None,
        "request": "service layer test task",
        "intent": "service_test",
        "target_nodes": [],
        "selected_agents": [],
        "required_capabilities": [],
        "state": "pending",
        "priority": "normal",
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
        "result": None,
        "error": None,
    }


def test_create_task_service(db_session):
    task = create_task(
        db_session,
        build_task_data("service-create-task"),
    )

    assert task.task_id == "service-create-task"
    assert task.state == "pending"


def test_get_task_service(db_session):
    task = Task(
        **build_task_data("service-get-task")
    )

    db_session.add(task)
    db_session.commit()

    result = get_task(
        db_session,
        "service-get-task",
    )

    assert result is not None
    assert result.task_id == "service-get-task"


def test_update_task_service(db_session):
    task = Task(
        **build_task_data("service-update-task")
    )

    db_session.add(task)
    db_session.commit()

    result = update_task(
        db_session,
        task,
        {
            "state": "running",
        },
    )

    assert result.state == "running"


def test_update_task_service_rejects_invalid_transition(db_session):
    task = Task(
        **build_task_data("service-invalid-transition")
    )

    task.state = "completed"

    db_session.add(task)
    db_session.commit()

    with pytest.raises(ValueError):
        update_task(
            db_session,
            task,
            {
                "state": "running",
            },
        )


def test_delete_task_service(db_session):
    task = Task(
        **build_task_data("service-delete-task")
    )

    db_session.add(task)
    db_session.commit()

    delete_task(
        db_session,
        task,
    )

    result = get_task(
        db_session,
        "service-delete-task",
    )

    assert result is None
