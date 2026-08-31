from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class AgentState:
    agent_id: str
    node_id: str
    status: str = "created"
    current_task_id: str | None = None
    last_error: dict[str, Any] | None = None
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def update_status(self, status: str) -> None:
        self.status = status
        self.updated_at = datetime.now(timezone.utc)

    def set_task(self, task_id: str | None) -> None:
        self.current_task_id = task_id
        self.updated_at = datetime.now(timezone.utc)

    def set_error(self, error: dict[str, Any] | None) -> None:
        self.last_error = error
        self.updated_at = datetime.now(timezone.utc)

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "node_id": self.node_id,
            "status": self.status,
            "current_task_id": self.current_task_id,
            "last_error": self.last_error,
            "updated_at": self.updated_at.isoformat(),
        }