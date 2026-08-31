from __future__ import annotations

from typing import Any


class LocalStore:
    def __init__(self) -> None:
        self._items: dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self._items[key] = value

    def get(self, key: str) -> Any | None:
        return self._items.get(key)

    def delete(self, key: str) -> None:
        self._items.pop(key, None)

    def exists(self, key: str) -> bool:
        return key in self._items

    def clear(self) -> None:
        self._items.clear()

    def snapshot(self) -> dict[str, Any]:
        return dict(self._items)