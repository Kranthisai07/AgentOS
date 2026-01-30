from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable


@dataclass(frozen=True)
class ToolResponse:
    ok: bool
    data: Dict[str, Any]
    error: str | None = None


class ToolError(Exception):
    pass


class Tool:
    name: str
    description: str

    def handle(self, **kwargs: Any) -> ToolResponse:
        raise NotImplementedError


def require_keys(payload: Dict[str, Any], keys: Iterable[str]) -> None:
    missing = [key for key in keys if key not in payload]
    if missing:
        raise ToolError(f"Missing required fields: {', '.join(missing)}")
