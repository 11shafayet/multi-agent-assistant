"""
Wires planner -> researcher -> writer into a graph.
"""

from langgraph.graph import StateGraph, START, END
from graph.state import AgentState
from graph.nodes import planner_node, researcher_node, writer_node


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner_node)
    graph.add_node("researcher", researcher_node)
    graph.add_node("writer", writer_node)

    graph.add_edge(START, "planner")
    graph.add_edge("planner", "researcher")
    graph.add_edge("researcher", "writer")
    graph.add_edge("writer", END)

    return graph.compile()


if __name__ == "__main__":
    app = build_graph()

    initial_state = {
        "task": "What are the health benefits of green tea?",
        "plan": None,
        "research_results": None,
        "draft": None,
        "retry_count": 0,
        "error": None,
    }

    final_state = app.invoke(initial_state)
    print("\n--- FINAL STATE ---")
    print(final_state)