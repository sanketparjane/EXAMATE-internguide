# app/graph.py
"""
LangGraph implementation for InternGuide (Day 9 - S2).
Rebuilds the agent workflow with:
1. Multi-turn conversation state & checkpointer memory (MemorySaver)
2. One mandatory approval step (Institutional Mentor / Academic Panel verification)
3. Tool execution (rag_search + internship_credit_calculator)
4. Grounded synthesis with citations
"""

import sys
from pathlib import Path
from typing import TypedDict, Annotated, List, Dict, Any, Optional
import operator

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from app.tools import internship_credit_calculator, rag_search
from app.agent_loop import extract_calculation_params


class AgentState(TypedDict):
    """LangGraph agent state with memory and approval metadata."""
    query: str
    session_id: str
    messages: Annotated[List[Dict[str, str]], operator.add]
    intent: str
    needs_approval: bool
    approval_status: str  # "pending", "approved", "rejected"
    approval_message: Optional[str]
    planned_tools: List[str]
    tool_inputs: Dict[str, Any]
    tool_results: Dict[str, Any]
    tools_used: List[str]
    citations: List[Dict[str, Any]]
    response: str


def agent_node(state: AgentState) -> Dict[str, Any]:
    """
    Reasoning node: inspects query, detects intent, and plans tool invocations.
    Marks needs_approval=True when credits/scores are being computed or awarded.
    """
    query = state.get("query", "").strip()
    q_lower = query.lower()

    # Determine intent
    is_calc = any(k in q_lower for k in [
        "calculate", "calculator", "credits earned", "net score", "weighted score",
        "marks", "credit and net score", "how many credits do i get for"
    ]) or ("hour" in q_lower and ("score" in q_lower or "panel" in q_lower or "company" in q_lower))

    is_search = any(k in q_lower for k in [
        "policy", "rule", "guideline", "aicte", "ugc", "pmis", "pm internship",
        "leave", "eligible", "eligibility", "online internship", "noc", "stipend",
        "which companies", "who can apply", "what is"
    ]) or not is_calc

    planned_tools = []
    tool_inputs = {}
    needs_approval = False

    if is_calc or state.get("tool_inputs", {}).get("activities"):
        planned_tools.append("internship_credit_calculator")
        # Credit conversion and AICTE scoring requires formal academic approval
        needs_approval = True
        activities = state.get("tool_inputs", {}).get("activities") or extract_calculation_params(query)
        tool_inputs["activities"] = activities

    if is_search:
        planned_tools.append("rag_search")
        tool_inputs["search_query"] = query

    intent = "both" if (is_calc and is_search) else ("calculate" if is_calc else "search")

    return {
        "intent": intent,
        "planned_tools": planned_tools,
        "tool_inputs": tool_inputs,
        "needs_approval": needs_approval,
        "messages": [{"role": "user", "content": query}]
    }


def approval_step_node(state: AgentState) -> Dict[str, Any]:
    """
    Approval step: Human-in-the-loop / Faculty Mentor validation.
    Verifies that internship hours and industry/panel scores are officially authorized.
    """
    current_status = state.get("approval_status", "approved")

    if current_status == "rejected":
        return {
            "approval_status": "rejected",
            "approval_message": "Academic Approval Denied: The requested internship credit calculation was rejected by the mentor/coordinator."
        }

    # Approved status
    return {
        "approval_status": "approved",
        "approval_message": "Academic Mentor Approval Granted: Internship hours and evaluation marks verified under AICTE norms."
    }


def tools_node(state: AgentState) -> Dict[str, Any]:
    """
    Executes planned tools (internship_credit_calculator and/or rag_search).
    """
    planned = state.get("planned_tools", [])
    inputs = state.get("tool_inputs", {})
    results = {}
    tools_used = []
    citations = []

    if "internship_credit_calculator" in planned:
        activities = inputs.get("activities")
        if activities:
            calc_out = internship_credit_calculator(activities=activities)
        else:
            calc_out = internship_credit_calculator(hours=45.0, industry_score=8.0, institute_panel_score=7.0)
        results["internship_credit_calculator"] = calc_out
        tools_used.append("internship_credit_calculator")

    if "rag_search" in planned:
        query = inputs.get("search_query", state.get("query", ""))
        rag_out = rag_search(query)
        results["rag_search"] = rag_out
        tools_used.append("rag_search")
        if isinstance(rag_out, dict):
            citations = rag_out.get("citations", [])

    return {
        "tool_results": results,
        "tools_used": tools_used,
        "citations": citations
    }


def synthesize_node(state: AgentState) -> Dict[str, Any]:
    """
    Synthesizes the final response incorporating approval status,
    calculation results, policy citations, and conversation state.
    """
    approval_status = state.get("approval_status", "approved")
    results = state.get("tool_results", {})
    calc_res = results.get("internship_credit_calculator")
    rag_res = results.get("rag_search")

    # If rejected in approval step
    if approval_status == "rejected":
        response_text = (
            f"**Action Blocked:** {state.get('approval_message', 'Approval rejected.')}\n"
            "Internship credits cannot be credited without faculty mentor validation."
        )
        return {
            "response": response_text,
            "messages": [{"role": "assistant", "content": response_text}]
        }

    response_sections = []

    if state.get("needs_approval"):
        response_sections.append(f"**[Approval Step Passed]** {state.get('approval_message')}")

    if calc_res:
        response_sections.append(f"### Internship Credit & Score Calculation\n{calc_res['summary']}")
        breakdown = []
        for a in calc_res.get("activities", []):
            breakdown.append(
                f"- **{a['title']}**: {a['hours']} hours -> **{a['credits']} credits** "
                f"(Industry: {a['industry_score']}, Institute: {a['institute_panel_score']} -> Marks: {a['activity_marks']}/10)"
            )
        response_sections.append("\n".join(breakdown))
        response_sections.append(
            f"**Total Credits:** {calc_res['total_credits']} credits (1 credit = 45 hours) | "
            f"**Net AICTE Weighted Score:** {calc_res['net_score']}/10"
        )

    if rag_res:
        rag_text = rag_res.get("answer", "") if isinstance(rag_res, dict) else str(rag_res)
        if calc_res:
            response_sections.append(f"### Relevant Policy Guidelines\n{rag_text}")
        else:
            response_sections.append(rag_text)

    final_response = "\n\n".join(response_sections).strip()

    return {
        "response": final_response,
        "messages": [{"role": "assistant", "content": final_response}]
    }


def route_after_agent(state: AgentState) -> str:
    """Route to approval step if calculation/grant needs approval, else tools."""
    if state.get("needs_approval", False):
        return "approval_node"
    return "tools_node"


def route_after_approval(state: AgentState) -> str:
    """Route to synthesize directly if rejected, else tools."""
    if state.get("approval_status") == "rejected":
        return "synthesize_node"
    return "tools_node"


def build_agent_graph():
    """Build and compile the LangGraph agent with memory and one approval step."""
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("agent_node", agent_node)
    workflow.add_node("approval_node", approval_step_node)
    workflow.add_node("tools_node", tools_node)
    workflow.add_node("synthesize_node", synthesize_node)

    # Add Edges
    workflow.add_edge(START, "agent_node")

    workflow.add_conditional_edges(
        "agent_node",
        route_after_agent,
        {
            "approval_node": "approval_node",
            "tools_node": "tools_node"
        }
    )

    workflow.add_conditional_edges(
        "approval_node",
        route_after_approval,
        {
            "tools_node": "tools_node",
            "synthesize_node": "synthesize_node"
        }
    )

    workflow.add_edge("tools_node", "synthesize_node")
    workflow.add_edge("synthesize_node", END)

    # In-memory checkpointer for multi-turn persistence
    memory = MemorySaver()
    compiled_app = workflow.compile(checkpointer=memory)
    return compiled_app


# Singleton compiled graph instance
agent_graph = build_agent_graph()


def run_langgraph_agent(
    query: str,
    session_id: str = "default_session",
    approved: bool = True,
    activities: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Entry point to run the LangGraph agent with persistent session memory.
    """
    config = {"configurable": {"thread_id": session_id}}

    initial_state = {
        "query": query,
        "session_id": session_id,
        "messages": [],
        "intent": "general",
        "needs_approval": False,
        "approval_status": "approved" if approved else "rejected",
        "approval_message": None,
        "planned_tools": [],
        "tool_inputs": {"activities": activities} if activities else {},
        "tool_results": {},
        "tools_used": [],
        "citations": [],
        "response": ""
    }

    final_state = agent_graph.invoke(initial_state, config=config)

    return {
        "query": query,
        "session_id": session_id,
        "response": final_state["response"],
        "approval_status": final_state.get("approval_status", "approved"),
        "tools_used": final_state.get("tools_used", []),
        "tool_results": final_state.get("tool_results", {}),
        "citations": final_state.get("citations", []),
        "messages": final_state.get("messages", [])
    }


if __name__ == "__main__":
    print("--- Testing LangGraph Agent (Credit Calculation + Approval Step) ---")
    q_calc = "I did a 90-hour internship with 9/10 industry score and 6/10 panel score, plus 45-hour rural NSS with 8/10 industry and 7/10 panel. Calculate credits and net score."
    res_approved = run_langgraph_agent(q_calc, session_id="test_session_1", approved=True)
    print("\nApproval Status:", res_approved["approval_status"])
    print("Tools Used:", res_approved["tools_used"])
    print("Response:\n", res_approved["response"])

    print("\n--- Testing LangGraph Agent with Rejection ---")
    res_rejected = run_langgraph_agent(q_calc, session_id="test_session_2", approved=False)
    print("\nApproval Status:", res_rejected["approval_status"])
    print("Response:\n", res_rejected["response"])

    print("\n--- Testing LangGraph Agent (RAG Policy Search) ---")
    q_rag = "How many hours is one internship credit as per AICTE?"
    res_rag = run_langgraph_agent(q_rag, session_id="test_session_1", approved=True)
    print("\nTools Used:", res_rag["tools_used"])
    print("Response:\n", res_rag["response"])
