from enum import Enum

from .state import AgentState


class AgentStatus(str, Enum):
    CREATED = "created"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"


class LocalAgent:
    def __init__(self, agent_id: str, node_id: str):
        self.state = AgentState(
            agent_id=agent_id,
            node_id=node_id,
        )

    @property
    def agent_id(self) -> str:
        return self.state.agent_id

    @property
    def node_id(self) -> str:
        return self.state.node_id

    @property
    def status(self) -> AgentStatus:
        return self.state.status

    def start(self) -> None:
        if self.status not in {
            AgentStatus.CREATED,
            AgentStatus.STOPPED,
        }:
            raise RuntimeError(
                f"Agent cannot start from state: {self.status.value}"
            )

        self.state.update_status(AgentStatus.STARTING)

        try:
            self.state.update_status(AgentStatus.RUNNING)
        except Exception as exc:
            self.state.set_error(
                {
                    "type": type(exc).__name__,
                    "message": str(exc),
                }
            )
            self.state.update_status(AgentStatus.FAILED)
            raise

    def stop(self) -> None:
        if self.status not in {
            AgentStatus.RUNNING,
            AgentStatus.FAILED,
        }:
            raise RuntimeError(
                f"Agent cannot stop from state: {self.status.value}"
            )

        self.state.update_status(AgentStatus.STOPPING)

        try:
            self.state.update_status(AgentStatus.STOPPED)
        except Exception as exc:
            self.state.set_error(
                {
                    "type": type(exc).__name__,
                    "message": str(exc),
                }
            )
            self.state.update_status(AgentStatus.FAILED)
            raise

    def set_current_task(self, task_id: str | None) -> None:
        self.state.set_task(task_id)

    def clear_error(self) -> None:
        self.state.set_error(None)

    def is_running(self) -> bool:
        return self.status == AgentStatus.RUNNING

    def snapshot(self) -> dict:
        snapshot = self.state.to_dict()
        snapshot["status"] = self.status.value
        return snapshot