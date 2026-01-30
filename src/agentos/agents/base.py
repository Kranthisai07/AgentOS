from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class AgentContext:
    state: Dict[str, Any]


class Agent:
    name: str

    def run(self, context: AgentContext) -> AgentContext:
        raise NotImplementedError
