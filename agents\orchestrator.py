from typing import Annotated, TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from agents.researcher import ResearcherAgent
from agents.coder import CoderAgent
from memory.store import ConversationMemory
from config.settings import settings
import operator


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    task: str
    task_type: str
    research_result: dict
    code_result: dict
    final_answer: str
    iterations: int


def classify_task(state: AgentState) -> AgentState:
    """Classify the incoming task to route it to the right agent."""
    llm = ChatOpenAI(model=settings.MODEL_NAME, temperature=0, api_key=settings.OPENAI_API_KEY)
    response = llm.invoke([
        HumanMessage(content=f"""Classify this task as either 'research', 'coding', or 'both'.
Reply with only one word.

Task: {state['task']}""")
    ])
    task_type = response.content.strip().lower()
    if task_type not in ("research", "coding", "both"):
        task_type = "research"
    return {**state, "task_type": task_type, "iterations": state.get("iterations", 0) + 1}


def run_researcher(state: AgentState) -> AgentState:
    agent = ResearcherAgent()
    result = agent.research(state["task"])
    return {**state, "research_result": result}


def run_coder(state: AgentState) -> AgentState:
    agent = CoderAgent()
    result = agent.generate_and_run(state["task"])
    return {**state, "code_result": result}


def synthesize(state: AgentState) -> AgentState:
    """Combine results from all agents into a final answer."""
    llm = ChatOpenAI(model=settings.MODEL_NAME, temperature=0.2, api_key=settings.OPENAI_API_KEY)

    context_parts = []
    if state.get("research_result"):
        context_parts.append(f"RESEARCH:\n{state['research_result'].get('report', '')}")
    if state.get("code_result"):
        context_parts.append(
            f"CODE OUTPUT:\n{state['code_result'].get('output', '')}\n"
            f"CODE:\n{state['code_result'].get('code', '')}"
        )

    response = llm.invoke([HumanMessage(content=f"""Synthesize the following into a clear final answer for the user:

ORIGINAL TASK: {state['task']}

{chr(10).join(context_parts)}

Provide a concise, well-structured final answer.""")])
    return {**state, "final_answer": response.content}


def route_task(state: AgentState) -> Literal["researcher", "coder", "both_r"]:
    t = state.get("task_type", "research")
    if t == "coding":
        return "coder"
    if t == "both":
        return "both_r"
    return "researcher"


def build_graph() -> StateGraph:
    graph = StateGraph(AgentState)
    graph.add_node("classify", classify_task)
    graph.add_node("researcher", run_researcher)
    graph.add_node("coder", run_coder)
    graph.add_node("synthesize", synthesize)

    graph.set_entry_point("classify")
    graph.add_conditional_edges("classify", route_task, {
        "researcher": "researcher",
        "coder": "coder",
        "both_r": "researcher",
    })
    graph.add_edge("researcher", "synthesize")
    graph.add_edge("coder", "synthesize")
    graph.add_edge("synthesize", END)
    return graph.compile()


AGENT_GRAPH = build_graph()


def run_agent(task: str) -> dict:
    state = AgentState(
        messages=[HumanMessage(content=task)],
        task=task,
        task_type="",
        research_result={},
        code_result={},
        final_answer="",
        iterations=0,
    )
    final_state = AGENT_GRAPH.invoke(state)
    return {
        "task": task,
        "task_type": final_state["task_type"],
        "answer": final_state["final_answer"],
        "research": final_state.get("research_result"),
        "code": final_state.get("code_result"),
    }
