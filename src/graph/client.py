import asyncio
from typing import Optional
from mcp_protocol import ClientSession
from mcp.client.streamable_http import streamable_http_client

class MCPClient:
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.session: Optional[ClientSession] = None
        self.tools = []
        self.client_context = None
        self.session_context = None
        
    async def connect(self):
        # Connect to stremable http server
        self.client_context = streamable_http_client(self.server_url)
        read_stream, write_stream, _ = await self.client_context.__aenter__()
        
        # Create session using client streams
        self.session_context = ClientSession(read_stream, write_stream)
        self.session = await self.session_context.__aenter__()
        await self.session.initialize()
        resp = await self.session.list_tools()
        # print("Toold found", resp)
        self.tools = [
            {
                "name": t.name,
                "description": t.description,
                "input_schema": t.inputSchema
            }
            for t in resp.tools
        ]
        print("🔂 Connected: tools available =", [t["name"] for t in self.tools])
        
        return self
        
    async def close(self):
        if self.session_context:
            await self.session_context.__aexit__(None, None, None)
        if self.client_context:
            await self.client_context.__aexit__(None, None, None)
            
# async def main():
#     client = MCPClient("http://localhost:9009/mcp")
#     try:
#         await client.connect()
#         print(client.tools)
#     finally:
#         await client.close()
# if __name__ == "__main__":
#     asyncio.run(main())       
#             # 🚀 MCP Server

