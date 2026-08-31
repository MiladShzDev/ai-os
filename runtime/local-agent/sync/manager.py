from __future__ import annotations

from typing import Any


class SyncManager:
    def __init__(self) -> None:
        self._items: list[dict[str, Any]] = []
        self._cursor: str | None = None

    def add_item(self, item: dict[str, Any]) -> None:
        self._items.append(item)

    def get_items(self) -> list[dict[str, Any]]:
        return list(self._items)

    def set_cursor(self, cursor: str | None) -> None:
        self._cursor = cursor

    def get_cursor(self) -> str | None:
        return self._cursor

    def snapshot(self) -> dict[str, Any]:
        return {
            "items": self.get_items(),
            "cursor": self._cursor,
        }

    def clear(self) -> None:
        self._items.clear()
        self._cursor = None