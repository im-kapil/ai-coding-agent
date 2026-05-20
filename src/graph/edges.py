"""Conditional edge logic for LangGraph."""
from __future__ import annotations

from langchain_core.messages import AIMessage

from src.graph.state import AgentState


def should_continue(state: AgentState) -> str:
    """
    Route after the reasoning node.

    Returns
    -------
    "tools"   → last AI message contains tool calls
    "output"  → no more tool calls; go to final output node
    "error"   → too many iterations
    """
    from src.config.settings import get_settings
    max_iter = get_settings().agent_max_iterations

    if state["iteration"] >= max_iter:
        return "error"

    last_msg = state["messages"][-1] if state["messages"] else None
    if isinstance(last_msg, AIMessage) and getattr(last_msg, "tool_calls", []):
        return "tools"

    return "output"


def after_tools(state: AgentState) -> str:
    """Always loop back to reasoning after tool execution."""
    return "reasoning"