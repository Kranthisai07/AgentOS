from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class PolicyDecision:
    allow: bool
    reason: str
    risk: str


class PolicyEngine:
    def evaluate(self, tool_name: str, action: str, metadata: Dict[str, str]) -> PolicyDecision:
        return PolicyDecision(allow=True, reason="default allow", risk="low")
