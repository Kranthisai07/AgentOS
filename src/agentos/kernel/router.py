from __future__ import annotations

from typing import Dict

from agentos.agents.base import Agent


class AgentRouter:
    def __init__(self) -> None:
        self._agents: Dict[str, Agent] = {}

    def register(self, agent: Agent) -> None:
        self._agents[agent.name] = agent

    def get(self, name: str) -> Agent:
        return self._agents[name]
