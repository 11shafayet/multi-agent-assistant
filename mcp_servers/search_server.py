"""
Minimal MCP server exposing one tool: web_search.
Wraps Tavily's REST API directly (not their hosted MCP endpoint).
"""

import os
import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("search-server")


@mcp.tool()
def web_search(query: str) -> str:
    """Search the web for a given query and return a summary of top results."""
    response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": os.environ["TAVILY_API_KEY"],
            "query": query,
            "max_results": 5,
        },
        timeout=15,
    )
    response.raise_for_status()
    data = response.json()

    results = data.get("results", [])
    if not results:
        return "No results found."

    formatted = []
    for r in results:
        formatted.append(f"- {r['title']}: {r['content'][:200]}...")

    return "\n".join(formatted)


if __name__ == "__main__":
    mcp.run(transport="stdio")