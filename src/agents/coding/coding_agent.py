from langchain.agents import create_agent
from langchain.messages import HumanMessage
from mcp_protocol.client import MCPAgentClient
from src.core.base_agent import BaseAgent
from src.core.prompts.coding_agent_prompt import CODING_AGENT_SYSTEM_PROMPT

class CodingAgent(BaseAgent):
    
    async def execute(self, state):        

        # print("State in CodingAgent: ", state)
        
        client = MCPAgentClient(
            servers={
                "Ai coding Agent MCP Client": {
                "transport": "http",
                "url": "http://localhost:9009/mcp",
                }
            }        
        )
        
        print("Initializing MCP client...", client)
        
        mcp_tools = await client.get_mcp_tools()
        
        print(":::::::::::::::::::::::Tools inside Coding Agent:::::::::::::::: \n ", mcp_tools)
        print(":::::::::::::::::::::::Tools inside Coding Agent:::::::::::::::: \n ")

            
        agent = create_agent(
            model = self.llm,
            tools = mcp_tools,
            system_prompt=CODING_AGENT_SYSTEM_PROMPT,
            # response_format=ToolStrategy(ResponseFormat),
            # response_format=ToolStrategy(ResponseFormat),
            # context_schema=Context,
            # checkpointer=InMemorySaver(),
            name="Coding Agent",
            # interrupt_before=['coding']
        )
        
        response = await agent.ainvoke(
            {"messages": [HumanMessage(state["plan"])]}
        )
        
        print(f"[{self.name}] Generated code: ", response)
        
        return { "messages": response, "current_agent": self.name }
