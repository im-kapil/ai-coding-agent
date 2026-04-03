import asyncio
from typing import Any, Optional
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


class MCPClient:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.session: Optional[ClientSession] = None
        self.tools = []
        self.client_context = None
        self.session_context = None
        
    async def connect(self):
        self.client_context = streamable_http_client(self.server_url)
        read_stream, write_stream, _ = await self.client_context.__aenter__()
        
        self.session_context = ClientSession(read_stream, write_stream)
        self.session = await self.session_context.__aenter__()
        
        await self.session.initialize()
        resp = await self.session.list_tools()
        
        self.tools = [
            {
                "name": t.name,
                "description": t.description,
                "input_schema": t.inputSchema
            }
            for t in resp.tools
        ]

        print("🔂 Connected: tools available =", [t["name"] for t in self.tools])
        
    def tool_list(self) -> list[dict[str, Any]]:
        print("self.tools::::::", self.tools)
        return self.tools
    
    async def close(self):
        if self.session_context:
            await self.session_context.__aexit__(None, None, None)
        if self.client_context:
            await self.client_context.__aexit__(None, None, None)

async def main():
    client = MCPClient("http://localhost:9009/mcp")
    try:   
        await client.connect()
    finally:
        client.close()
    
    # tools = client.tool_list()
    # print("TOOLS:", tools)


if __name__ == "__main__":
    asyncio.run(main())