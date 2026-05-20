from langgraph.graph import StateGraph
from typing import TypedDict

class AgentState(TypedDict):
    user_prompt: str
    generated_code: str

workflow = StateGraph(AgentState)

def planner_node(state):
    return state

def coding_node(state):
    return state

workflow.add_node("planner", planner_node)
workflow.add_node("coding", coding_node)

workflow.set_entry_point("planner")
workflow.add_edge("planner", "coding")

graph = workflow.compile()