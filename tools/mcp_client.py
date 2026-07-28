"""
MCP client helpers: spawn other MCP servers as subprocesses and call their tools.
"""

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SEARCH_SERVER_PARAMS = StdioServerParameters(
    command="python3",
    args=["mcp_servers/search_server.py"],
)

REPORT_SERVER_PARAMS = StdioServerParameters(
    command="python3",
    args=["mcp_servers/report_server.py"],
)


async def call_web_search(query: str) -> str:
    async with stdio_client(SEARCH_SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("web_search", {"query": query})
            return result.content[0].text


async def call_save_report(filename: str, content: str, overwrite: bool = False) -> str:
    async with stdio_client(REPORT_SERVER_PARAMS) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "save_report",
                {"filename": filename, "content": content, "overwrite": overwrite},
            )
            return result.content[0].text