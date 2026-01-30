from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class MemoryItem:
    key: str
    value: Dict[str, Any]


class MemoryStore:
    tier: str

    def put(self, item: MemoryItem) -> None:
        raise NotImplementedError

    def get(self, key: str) -> MemoryItem | None:
        raise NotImplementedError
