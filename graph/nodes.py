"""
Node functions. Each one takes the current state, does its job,
and returns a dict with the fields it updated (LangGraph merges this back into state).
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from graph.state import AgentState
import asyncio
from tools.mcp_client import call_web_search

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.environ["GROQ_API_KEY"],
    temperature=0,
)


def planner_node(state: AgentState) -> dict:
    print(f"[planner] received task: {state['task']}")

    prompt = f"""Break this task into 3-5 clear, actionable research steps.
    Task: {state['task']}
    Return ONLY a numbered list, nothing else."""

    response = llm.invoke(prompt)
    steps = [line.strip() for line in response.content.split("\n") if line.strip()]

    return {"plan": steps}


def researcher_node(state: AgentState) -> dict:
    print(f"[researcher] working through plan: {state['plan']}")

    query = state["task"]
    results = asyncio.run(call_web_search(query))

    return {"research_results": results}

def writer_node(state: AgentState) -> dict:
    print(f"[writer] writing from research: {state['research_results']}")

    prompt = f"""Using the research below, write a clear, well-organized answer to the task.

    Task: {state['task']}

    Research findings:
    {state['research_results']}

    Write a concise, accurate answer (150-250 words). Cite claims naturally without fake links."""

    response = llm.invoke(prompt)
    return {"draft": response.content}