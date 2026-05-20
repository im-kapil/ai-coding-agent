import asyncio
from typing import Dict, Any, List, Optional

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent


class MCPAgentClient:

    def __init__(
        self,
        servers: Dict[str, Dict[str, Any]]    
        ):
        """
        Initialize MCP Agent Client

        Args:
            servers: MCP server configurations
            model: LLM model name
        """

        self.servers = servers

        self.client: Optional[MultiServerMCPClient] = None
        self.tools = []

    async def connect(self):
        """
        Connect to MCP servers
        """

        self.client = MultiServerMCPClient(
            self.servers
        )

        self.tools = await self.client.get_tools()
        
        return self.client
    
    async def get_mcp_tools(self):
        """
        Return MCP tools
        """

        if not self.tools:
            await self.connect()

        return self.tools

    async def close(self):
        """
        Cleanup resources
        """

        if self.client:
            await self.client.close()
