"""
MCP client helper: spawns our search_server.py as a subprocess and calls its tools.
"""

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_PARAMS = StdioServerParameters(
    command="python3",
    args=["mcp_servers/search_server.py"],
)


async def call_web_search(query: str) -> str:
    async with stdio_client(SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("web_search", {"query": query})
            return result.content[0].text