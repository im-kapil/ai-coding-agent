"""LangGraph node functions — pure functions over AgentState."""
from __future__ import annotations

from typing import Any

import structlog
from langchain_core.messages import AIMessage, HumanMessage

from src.graph.state import AgentState

log = structlog.get_logger(__name__)


def input_node(state: AgentState) -> dict[str, Any]:
    """Bootstrap state from the user prompt."""
    log.info("node.input", prompt=state["user_prompt"][:80])
    return {
        "messages":  [HumanMessage(content=state["user_prompt"])],
        "iteration": 0,
        "steps":     [],
        "errors":    [],
    }


def reasoning_node(llm_with_tools: Any):
    """Factory: returns a node that calls the LLM with bound tools."""

    def _node(state: AgentState) -> dict[str, Any]:
        log.info("node.reasoning", iteration=state["iteration"])
        response: AIMessage = llm_with_tools.invoke(state["messages"])
        step = {
            "iteration": state["iteration"],
            "type":      "reasoning",
            "content":   response.content,
        }
        return {
            "messages":  [*state["messages"], response],
            "iteration": state["iteration"] + 1,
            "steps":     [*state["steps"], step],
        }

    return _node


def tool_execution_node(tool_map: dict[str, Any]):
    """Factory: returns a node that dispatches tool calls."""

    async def _node(state: AgentState) -> dict[str, Any]:
        last_msg = state["messages"][-1]
        results = []
        errors  = list(state["errors"])

        for tool_call in getattr(last_msg, "tool_calls", []):
            name   = tool_call["name"]
            args   = tool_call["args"]
            log.info("node.tool_exec", tool=name, args=args)

            if name not in tool_map:
                errors.append(f"Tool {name!r} not found")
                continue

            try:
                result = await tool_map[name].execute(**args)
                results.append({"tool": name, "result": result})
            except Exception as exc:
                errors.append(f"[{name}] {exc}")
                results.append({"tool": name, "error": str(exc)})

        step = {"iteration": state["iteration"], "type": "tool_execution", "results": results}
        return {
            "steps":  [*state["steps"], step],
            "errors": errors,
        }

    return _node


def output_node(state: AgentState) -> dict[str, Any]:
    """Extract the final answer from the last AI message."""
    last_ai = next(
        (m for m in reversed(state["messages"]) if isinstance(m, AIMessage)),
        None,
    )
    output = last_ai.content if last_ai else "No output generated."
    log.info("node.output", output_length=len(output))
    return {"final_output": output}