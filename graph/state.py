"""
Shared state that flows through every node in the graph.
Every agent (planner, researcher, writer) reads from this and writes back to it.
"""

from typing import TypedDict, List, Optional


class AgentState(TypedDict):
    task: str                        # the original user request
    plan: Optional[List[str]]        # steps produced by the planner
    research_results: Optional[str]  # findings gathered by the researcher
    draft: Optional[str]             # final output from the writer

    # bookkeeping fields for retries / self-correction
    retry_count: int
    error: Optional[str]