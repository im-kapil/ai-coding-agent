"""
Central Registry
================
Single source of truth for every LLM Tool.

Usage
-----
    # Registration (done once, usually in __init__.py)
    registry.register_tool("my_tool", MyTool)

    # Resolution (anywhere in the app)
    tool_cls = registry.get_tool("my_tool")
    tool     = tool_cls()
"""

from ast import TypeVar
import threading
from typing import Type
from langchain.tools import BaseTool
from qdrant_client.models import Dict
import structlog
log = structlog.get_logger(__name__)

T = TypeVar("T")

class ToolRegistry:
    """Thread-safe registry backed by plain dicts."""

    _lock = threading.Lock()

    _registry: Dict[str, Type[BaseTool]] = {}
    
    def __init__(self) -> None:
        self._tools:    dict[str, type[BaseTool]]    = {}

    # ── Generic helpers ───────────────────────────────────────────────────────

    @classmethod
    def _register(cls, name: str, tool_cls: Type[BaseTool]):
        cls._registry[name] = tool_cls

    @classmethod
    def _get(cls, name: str):
        return cls._registry[name]()
    
    @classmethod
    def _list(cls):
        return list(cls._registry.keys())