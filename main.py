from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph
from agents.planner import planner_agent
from agents.executor import executor_agent
from agents.verifier import verifier_agent
from typing import TypedDict, List, Any
from agents.schemas import Plan, ExecutionResult, FinalAnswer

class AgentState(TypedDict):
    task: str
    plan: Plan
    result: List[ExecutionResult]
    final: FinalAnswer

graph = StateGraph(AgentState)

def planner(state):
    """Node for the planner agent."""
    plan = planner_agent(state["task"])
    return {"plan": plan}

def executor(state):
    """Node for the executor agent."""
    result = executor_agent(state["plan"])
    return {"result": result}

def verifier(state):
    """Node for the verifier agent."""
    final = verifier_agent(state["task"], state["result"])
    return {"final": final}

graph.add_node("planner", planner)
graph.add_node("executor", executor)
graph.add_node("verifier", verifier)

graph.set_entry_point("planner")
graph.add_edge("planner", "executor")
graph.add_edge("executor", "verifier")
graph.set_finish_point("verifier")

app = graph.compile()

if __name__ == "__main__":
    task = input("Enter your task: ")
    output = app.invoke({"task": task})
    print("\nFINAL OUTPUT:\n")
    print(output["final"])
