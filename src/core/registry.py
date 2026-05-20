"""
Central Registry
================
Single source of truth for every Agent, LLM, Tool, and Skill.

Usage
-----
    # Registration (done once, usually in __init__.py)
    registry.register_agent("coding", CodingAgent)

    # Resolution (anywhere in the app)
    agent_cls = registry.get_agent("coding")
    agent     = agent_cls(agent_info)
"""

from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Any, TypeVar

import structlog

from src.llms.base_llm import base_model

if TYPE_CHECKING:
    from src.core.base_agent import BaseAgent
    from src.core.base_llm import BaseLLM
    from src.core.base_skill import BaseSkill
    from src.core.base_tool import BaseTool

log = structlog.get_logger(__name__)

T = TypeVar("T")


class Registry:
    """Thread-safe registry backed by plain dicts."""

    _lock = threading.Lock()

    def __init__(self) -> None:
        self._agents:  dict[str, type[BaseAgent]]  = {}
        self._llms:    dict[str, type[BaseLLM]]    = {}
        self._tools:   dict[str, type[BaseTool]]   = {}
        self._skills:  dict[str, type[BaseSkill]]  = {}

    # ── Generic helpers ───────────────────────────────────────────────────────

    def _register(self, store: dict[str, type[T]], key: str, cls: type[T]) -> None:
        with self._lock:
            if key in store:
                log.warning("registry.overwrite", key=key, old=store[key].__name__, new=cls.__name__)
            store[key] = cls
            log.debug("registry.registered", key=key, cls=cls.__name__)

    def _get(self, store: dict[str, type[T]], key: str, kind: str) -> type[T]:
        try:
            return store[key]
        except KeyError:
            available = list(store.keys())
            raise KeyError(
                f"{kind!r} named {key!r} not found. Available: {available}"
            ) from None

    def _list(self, store: dict[str, Any]) -> list[str]:
        return list(store.keys())

    # ── Agents ────────────────────────────────────────────────────────────────

    def register_agent(self, name: str, cls: type[BaseAgent]) -> None:
        self._register(self._agents, name, cls)

    def get_agent(self, name: str) -> type[BaseAgent]:
        return self._get(self._agents, name, "Agent")
    
    def get_node(self, name: str, config: dict | None = None):
        """
        Create an instance of a registered agent node.
        """

        if name not in self._agents:
            raise ValueError(f"Agent '{name}' not registered")

        config = config or {}

        agent_cls = self._agents[name]
        
        # tools = [self.get_tool(t) for t in config.get("tools", [])]

        agent = agent_cls(
            # name=name,
            # tools=tools,
            llm=base_model()
        )

        return agent

    def list_agents(self) -> list[str]:
        return self._list(self._agents)

    # ── LLMs ─────────────────────────────────────────────────────────────────

    def register_llm(self, name: str, cls: type[BaseLLM]) -> None:
        self._register(self._llms, name, cls)

    def get_llm(self, name: str) -> type[BaseLLM]:
        return self._get(self._llms, name, "LLM")

    def list_llms(self) -> list[str]:
        return self._list(self._llms)

    # ── Tools ─────────────────────────────────────────────────────────────────

    def register_tool(self, name: str, cls: type[BaseTool]) -> None:
        self._register(self._tools, name, cls)

    def get_tool(self, name: str) -> type[BaseTool]:
        return self._get(self._tools, name, "Tool")

    def list_tools(self) -> list[str]:
        return self._list(self._tools)

    # ── Skills ────────────────────────────────────────────────────────────────

    def register_skill(self, name: str, cls: type[BaseSkill]) -> None:
        self._register(self._skills, name, cls)

    def get_skill(self, name: str) -> type[BaseSkill]:
        return self._get(self._skills, name, "Skill")

    def list_skills(self) -> list[str]:
        return self._list(self._skills)

    # ── Decorator helpers ─────────────────────────────────────────────────────

    def agent(self, name: str):
        """Class decorator: @registry.agent("coding")"""
        def decorator(cls: type[BaseAgent]) -> type[BaseAgent]:
            self.register_agent(name, cls)
            return cls
        return decorator

    def llm(self, name: str):
        def decorator(cls: type[BaseLLM]) -> type[BaseLLM]:
            self.register_llm(name, cls)
            return cls
        return decorator

    def tool(self, name: str):
        def decorator(cls: type[BaseTool]) -> type[BaseTool]:
            self.register_tool(name, cls)
            return cls
        return decorator

    def skill(self, name: str):
        def decorator(cls: type[BaseSkill]) -> type[BaseSkill]:
            self.register_skill(name, cls)
            return cls
        return decorator

    def snapshot(self) -> dict[str, list[str]]:
        """Return a dict snapshot of all registered entries — useful for /health."""
        return {
            "agents": self.list_agents(),
            "llms":   self.list_llms(),
            "tools":  self.list_tools(),
            "skills": self.list_skills(),
        }


# ── Singleton export ──────────────────────────────────────────────────────────
# registry = _Registry()