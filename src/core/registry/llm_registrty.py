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
from typing import TYPE_CHECKING, Any, Type, TypeVar, Dict

import structlog

from .tool_registry import ToolRegistry
from src.llms.base_llm import base_model

if TYPE_CHECKING:
    from src.core.base_agent import BaseAgent
    from src.core.base_llm import BaseLLM

log = structlog.get_logger(__name__)

T = TypeVar("T")

class LLMRegistry:
    """Thread-safe registry backed by plain dicts."""

    _lock = threading.Lock()

    _registry: Dict[str, Type[BaseLLM]] = {}

    def __init__(self) -> None:
        self._agents:  dict[str, type[BaseAgent]]  = {}
        self._llms:    dict[str, type[BaseLLM]]    = {}

    # ── Generic helpers ───────────────────────────────────────────────────────
    
    @classmethod
    def _register(cls, name: str, agent_cls: Type[BaseAgent]):
        cls._registry[name] = agent_cls
        
    @classmethod
    def _get(cls, name: str):
        if name not in cls._registry:
            raise ValueError(f"Agent '{name}' not registered")
        return cls._registry[name]
    
    @classmethod
    def _list(cls):
        return list(cls._registry.keys())

    # ── Agents ────────────────────────────────────────────────────────────────
    @classmethod
    def register_agent(cls, name: str, agent_cls: Type[BaseAgent]):
        cls._register(name, agent_cls)

    @classmethod
    def get_agent(cls, name: str) -> type[BaseAgent]:
        return cls._get(name)
    
    @classmethod
    def get_node(cls, name: str, config: dict = None):
        if name not in cls._registry:
            raise ValueError(f"Agent '{name}' not registered")

        config = config or {}

        # Inject tools
        tools = [ToolRegistry.get(t) for t in config.get("tools", [])]
        
        agent = cls._registry[name](
            name=name,
            tools=tools,
            llm=base_model()
        )

        # Return callable node
        return agent
    
    @classmethod
    def list_agents(self) -> list[str]:
        return self._list(self._agents)

    # ── LLMs ─────────────────────────────────────────────────────────────────

    def register_llm(self, name: str, cls: type[BaseLLM]) -> None:
        self._register(self._llms, name, cls)

    def get_llm(self, name: str) -> type[BaseLLM]:
        return self._get(self._llms, name, "LLM")

    def list_llms(self) -> list[str]:
        return self._list(self._llms)

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
    
    @classmethod
    def snapshot(self) -> dict[str, list[str]]:
        """Return a dict snapshot of all registered entries — useful for /health."""
        return {
            "agents": self.list_agents(),
            "llms":   self.list_llms(),
        }


# ── Singleton export ──────────────────────────────────────────────────────────
# registry = _Registry()