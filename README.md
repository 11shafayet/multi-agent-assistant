# Multi-Agent Research Assistant

A multi-agent system built with LangGraph, coordinating a **planner**, **researcher**, and **writer** agent through a shared state graph. The researcher uses a self-built MCP (Model Context Protocol) server to perform live web search.

## Architecture
START -> planner -> researcher -> writer -> END

- **State**: a shared dict (`task`, `plan`, `research_results`, `draft`, `retry_count`, `error`) flows through every node.
- **Planner**: breaks the user's task into concrete research steps (Groq LLM call).
- **Researcher**: calls a custom MCP server exposing a `web_search` tool, which wraps the Tavily search API.
- **Writer**: synthesizes the plan + research into a final answer (Groq LLM call).

## Why a self-built MCP server?

Instead of using Tavily's hosted MCP endpoint, this project wraps Tavily's REST API in a custom MCP server (`mcp_servers/search_server.py`), exposed over stdio and called from a LangGraph node via a standard MCP client. This demonstrates building and exposing MCP tools directly, not just consuming a third-party one.

## Tech stack

- **LangGraph** — agent orchestration / state graph
- **Groq** (`llama-3.3-70b-versatile`) — LLM calls
- **MCP** — tool protocol for the researcher's web search
- **Tavily** — underlying search API

## Setup

```bash
git clone 11shafayet/multi-agent-assistant
cd multi-agent-assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:
GROQ_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here

## Run

```bash
python3 -m graph.build_graph
```

## Project structure
multi-agent-assistant/
├── graph/
│ ├── state.py            # shared AgentState
│ ├── nodes.py            # planner / researcher / writer nodes
│ └── build_graph.py      # wires nodes into the graph
├── mcp_servers/
│ └── search_server.py    # custom MCP server wrapping Tavily
├── tools/
│ └── mcp_client.py       # MCP client used by researcher node
├── agents/
├── tests/
└── requirements.txt

## Status

Work in progress. Next: retry/self-correction logic, agency guardrails (LLM06), deployment.