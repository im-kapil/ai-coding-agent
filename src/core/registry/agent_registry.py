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

from langchain.tools import BaseTool
import structlog

from .tool_registry import ToolRegistry
from src.llms.base_llm import base_model

if TYPE_CHECKING:
    from src.core.base_agent import BaseAgent
    from src.core.base_llm import BaseLLM

log = structlog.get_logger(__name__)

T = TypeVar("T")

class AgentRegistry:
    """Thread-safe registry backed by plain dicts."""

    _lock = threading.Lock()

    _registry: Dict[str, Type[BaseAgent]] = {}

    def __init__(self) -> None:
        self._agents:  dict[str, type[BaseAgent]]  = {}
        self._llms:    dict[str, type[BaseLLM]]    = {}
        self.tools:    dict[str, type[BaseTool]]   = {}

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

    @classmethod
    def get_node(cls, name: str, config: dict = None):
        
        if name not in cls._registry:
            raise ValueError(f"Agent '{name}' not registered")

        tools = config.get("tools", []),
                
        config = config or {}        
        agent = cls._registry[name](
            name=name,
            tools=tools,
            llm=base_model()
        )

        # Return callable node
        return agent