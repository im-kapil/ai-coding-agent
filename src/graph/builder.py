"""
Graph Builder
=============
Assembles the LangGraph state machine from nodes and edges.
"""
from __future__ import annotations

from typing import Any

from langgraph.graph import END, START, StateGraph

from src.graph.edges import after_tools, should_continue
from src.graph.nodes import input_node, output_node, reasoning_node, tool_execution_node
from src.graph.state import AgentState


def build_agent_graph(llm_with_tools: Any, tool_map: dict[str, Any]):
    """
    Build and compile the standard ReAct-style agent graph.

    Parameters
    ----------
    llm_with_tools : LangChain chat model with tools bound
    tool_map       : dict mapping tool name → BaseTool instance
    """
    graph = StateGraph(AgentState)

    # ── Register nodes ────────────────────────────────────────────────────────
    graph.add_node("input",     input_node)
    graph.add_node("reasoning", reasoning_node(llm_with_tools))
    graph.add_node("tools",     tool_execution_node(tool_map))
    graph.add_node("output",    output_node)

    # ── Wire edges ────────────────────────────────────────────────────────────
    graph.add_edge(START,        "input")
    graph.add_edge("input",      "reasoning")

    graph.add_conditional_edges(
        "reasoning",
        should_continue,
        {"tools": "tools", "output": "output", "error": "output"},
    )
    graph.add_conditional_edges(
        "tools",
        after_tools,
        {"reasoning": "reasoning"},
    )
    graph.add_edge("output", END)

    return graph.compile()