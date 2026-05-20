from __future__ import annotations

from typing import Any, TypedDict

from langchain_core.messages import BaseMessage

from src.core.helpers.agent_response_formats import PlannerAgentResponseFormat


class AgentState(TypedDict):
    """Shared mutable state threaded through every LangGraph node."""

    # Core I/O
    messages:       list[BaseMessage]   # full conversation / tool-call history
    user_prompt:    str                 # original user request (immutable)
    final_output:   str                 # populated by the final node
    plan:         PlannerAgentResponseFormat      # structured plan output from planner agent

    # Execution tracking
    iteration:      int                 # current iteration count
    steps:          list[dict[str, Any]]  # structured trace of each step
    errors:         list[str]           # accumulated error messages

    # Context
    workspace:      str                 # filesystem workspace path
    metadata:       dict[str, Any]      # arbitrary agent-specific state