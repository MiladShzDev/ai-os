from datetime import datetime, timezone

import pytest

from app.models.task import Task
from app.services.tasks.lifecycle import (
    can_transition,
    update_task_state,
)


def test_can_transition_allows_valid_states():
    assert can_transition(
        "pending",
        "running",
    )

    assert can_transition(
        "running",
        "completed",
    )

    assert can_transition(
        "running",
        "failed",
    )


def test_can_transition_blocks_invalid_states():
    assert not can_transition(
        "completed",
        "running",
    )

    assert not can_transition(
        "failed",
        "running",
    )


def test_update_task_state_updates_state(db_session):
    task = Task(
        task_id="lifecycle-test-task",
        parent_task_id=None,
        request="test lifecycle",
        intent="lifecycle_test",
        target_nodes=[],
        selected_agents=[],
        required_capabilities=[],
        state="pending",
        priority="normal",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        result=None,
        error=None,
    )

    db_session.add(task)
    db_session.commit()

    result = update_task_state(
        db_session,
        task,
        "running",
    )

    assert result.state == "running"
    assert result.error is None


def test_update_task_state_rejects_invalid_transition(db_session):
    task = Task(
        task_id="lifecycle-invalid-task",
        parent_task_id=None,
        request="test invalid lifecycle",
        intent="lifecycle_test",
        target_nodes=[],
        selected_agents=[],
        required_capabilities=[],
        state="completed",
        priority="normal",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        result=None,
        error=None,
    )

    db_session.add(task)
    db_session.commit()

    with pytest.raises(ValueError):
        update_task_state(
            db_session,
            task,
            "running",
        )
