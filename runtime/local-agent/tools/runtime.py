from __future__ import annotations

from typing import Any, Callable


ToolHandler = Callable[[dict[str, Any]], Any]


class ToolRuntime:
    def __init__(self) -> None:
        self._tools: dict[str, ToolHandler] = {}

    def register(self, tool_id: str, handler: ToolHandler) -> None:
        self._tools[tool_id] = handler

    def unregister(self, tool_id: str) -> None:
        self._tools.pop(tool_id, None)

    def has_tool(self, tool_id: str) -> bool:
        return tool_id in self._tools

    def execute(self, tool_id: str, input_data: dict[str, Any]) -> Any:
        handler = self._tools.get(tool_id)

        if handler is None:
            raise KeyError(f"Tool not registered: {tool_id}")

        return handler(input_data)