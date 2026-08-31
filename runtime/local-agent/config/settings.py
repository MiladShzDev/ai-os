from __future__ import annotations

import os


class RuntimeSettings:
    def __init__(self) -> None:
        self.agent_id = os.getenv("AIOS_AGENT_ID", "local-agent")
        self.node_id = os.getenv("AIOS_NODE_ID", "local-node")
        self.environment = os.getenv("AIOS_ENV", "development")
        self.log_level = os.getenv("AIOS_LOG_LEVEL", "INFO")

    def snapshot(self) -> dict[str, str]:
        return {
            "agent_id": self.agent_id,
            "node_id": self.node_id,
            "environment": self.environment,
            "log_level": self.log_level,
        }