from __future__ import annotations

from typing import Any


class PermissionEngine:
    def __init__(self) -> None:
        self._decisions: dict[str, str] = {}

    def set_decision(self, permission_id: str, decision: str) -> None:
        self._decisions[permission_id] = decision

    def get_decision(self, permission_id: str) -> str | None:
        return self._decisions.get(permission_id)

    def is_allowed(self, permission_id: str) -> bool:
        return self.get_decision(permission_id) == "allowed"

    def is_denied(self, permission_id: str) -> bool:
        return self.get_decision(permission_id) == "denied"

    def evaluate(
        self,
        permission_id: str,
        capability: str,
        scope: dict[str, Any],
    ) -> str:
        decision = self.get_decision(permission_id)

        if decision is not None:
            return decision

        return "pending"