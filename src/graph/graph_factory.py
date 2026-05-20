from mcp_protocol.client import MCPAgentClient
from src.agents.planner.planner_agent import PlannerAgent
from src.core.registry.agent_registry import AgentRegistry
from src.core.registry.tool_registry import ToolRegistry
from src.tools.filesystem.write_file_tool import write_file

from .state import AgentState
from langgraph.graph import START, StateGraph, END
from src.agents.coding.coding_agent import CodingAgent
from langgraph.checkpoint.memory import InMemorySaver
from src.core.registry.agent_registry import AgentRegistry  

class GraphFactory:

    @staticmethod
    async def build():

        graph = StateGraph(AgentState)
        
        AgentRegistry._register("coding_agent", CodingAgent) 
        AgentRegistry._register("planner_agent", PlannerAgent)
        
        # ToolRegistry._register("write_file", write_file)
    
        client = MCPAgentClient(
            servers={
                "Ai coding Agent MCP Client": {
                "transport": "http",
                "url": "http://localhost:9009/mcp",
                }
            }        
        )
        
        print("Initializing MCP client...", client)
        
        tools = await client.get_mcp_tools()
        
        print("Tools fetched from MCP server: ", len(tools))
        
        planner_agent = AgentRegistry.get_node(
            "planner_agent",
            { "tools": tools }
        )
        
        coding_agent = AgentRegistry.get_node(
            "coding_agent",
            { "tools": tools }
        )
            
        # Add nodes
        graph.add_node("planner_agent", planner_agent)
        graph.add_node("coding_agent", coding_agent)
        # graph.add_node("screening", screening_node)

        # Define flow
        # graph.set_entry_point("intent_classifier")
        graph.add_edge(START, "planner_agent")
        graph.add_edge("planner_agent", "coding_agent")
        graph.add_edge("coding_agent", END)

        checkpointer = InMemorySaver()
        
        return graph.compile(checkpointer=checkpointer)