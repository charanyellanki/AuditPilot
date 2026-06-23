"""Assemble the AuditPilot agent graph with LangGraph.

First cut is a linear pipeline:

    retrieval -> validation -> grounding -> triage -> END

Conditional routing is intentionally deferred (see TODOs) so the structure can
be reviewed before behavior is added.

Status: scaffold — wiring sketch only, no execution yet.
"""

from __future__ import annotations

from agents import (
    grounding_verifier,
    retrieval_agent,
    triage_agent,
    validation_agent,
)
from graph.state import AuditState, TriageDecision

# langgraph import kept local to build_graph() so the module is importable
# (e.g. for docs/introspection) before the dependency is installed.


# Node names (single source of truth for edges + the audit log).
RETRIEVAL = "retrieval"
VALIDATION = "validation"
GROUNDING = "grounding"
TRIAGE = "triage"


def route_after_triage(state: AuditState) -> str:
    """Conditional edge target after triage.

    # TODO: branch to distinct terminal nodes for AUTO_CLEAR vs. ESCALATE once
    #       those nodes exist (e.g. notify/queue-for-review). For now both end.
    """
    decision = state.get("decision")
    return "escalate" if decision == TriageDecision.ESCALATE else "auto_clear"


def build_graph():
    """Construct and compile the LangGraph StateGraph.

    Returns the compiled graph (a Runnable).

    # TODO (conditional edges, deferred):
    #   - retrieval -> validation only if guidance is non-empty, else short-circuit.
    #   - skip grounding when validation produced zero findings.
    #   - add_conditional_edges(TRIAGE, route_after_triage, {...}).
    #   - optional retrieval retry loop on low-confidence findings.
    """
    from langgraph.graph import END, START, StateGraph

    graph = StateGraph(AuditState)

    graph.add_node(RETRIEVAL, retrieval_agent.run)
    graph.add_node(VALIDATION, validation_agent.run)
    graph.add_node(GROUNDING, grounding_verifier.run)
    graph.add_node(TRIAGE, triage_agent.run)

    # Linear edges for the first cut.
    graph.add_edge(START, RETRIEVAL)
    graph.add_edge(RETRIEVAL, VALIDATION)
    graph.add_edge(VALIDATION, GROUNDING)
    graph.add_edge(GROUNDING, TRIAGE)
    graph.add_edge(TRIAGE, END)

    # TODO: replace the linear TRIAGE -> END edge with conditional routing
    #       via route_after_triage.

    return graph.compile()


# Singleton accessor so the API/UI/eval share one compiled graph.
_compiled = None


def get_graph():
    """Return a lazily-compiled, cached graph instance."""
    global _compiled
    if _compiled is None:
        _compiled = build_graph()
    return _compiled
