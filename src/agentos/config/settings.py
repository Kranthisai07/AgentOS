from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Settings:
    project_name: str = "AgentOS"
    environment: str = "dev"
