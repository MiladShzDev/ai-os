from __future__ import annotations

from agent.agent import LocalAgent
from config.settings import RuntimeSettings
from events.bus import EventBus
from permissions.engine import PermissionEngine
from storage.store import LocalStore
from sync.manager import SyncManager
from tools.runtime import ToolRuntime


class LocalAgentRuntime:
    def __init__(self, settings: RuntimeSettings) -> None:
        self.settings = settings

        self.agent = LocalAgent(
            settings.agent_id,
            settings.node_id,
        )

        self.events = EventBus()
        self.permissions = PermissionEngine()
        self.storage = LocalStore()
        self.sync = SyncManager()
        self.tools = ToolRuntime()

    def start(self) -> None:
        self.agent.start()

    def stop(self) -> None:
        self.agent.stop()

    def snapshot(self) -> dict:
        return {
            "settings": self.settings.snapshot(),
            "agent": self.agent.snapshot(),
            "storage": self.storage.snapshot(),
            "sync": self.sync.snapshot(),
        }


def main() -> None:
    settings = RuntimeSettings()
    runtime = LocalAgentRuntime(settings)

    runtime.start()
    print(runtime.snapshot())
    runtime.stop()


if __name__ == "__main__":
    main()