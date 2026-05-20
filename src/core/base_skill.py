from abc import ABC, abstractmethod
from typing import Dict, Any

"""
BaseSkill
=========
Every skill in the system inherits from this class.

Concrete skills must implement:
    • `build_graph()`  — return a compiled LangGraph CompiledGraph
    • `run()`          — execute a single user request end-to-end

The class stores an `skillInfo` descriptor (name, version, description, …)
so the registry and MCP server can introspect any agent uniformly.
"""
class BaseSkill(ABC):
    def __init__(
        self,
        name: str,
        llm,
        tools=None,
        skills=None,
    ):
        self.name = name
        self.llm = llm
        self.tools = tools or []
        self.skills = skills or []

    @abstractmethod
    async def execute(self, state: Dict[str, Any]):
        pass