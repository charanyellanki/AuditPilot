"""Triage agent.

Aggregates the grounded findings into a single claim-level risk score, then
decides whether to auto-clear the claim or escalate it to human review. The
threshold is configurable so the eval harness can sweep the operating point on
the business readout (recovery-$ vs. review-hours).

Status: scaffold — node contract only, no implementation yet.
"""

from __future__ import annotations

from graph.state import AuditState, TriageDecision


# Claims scoring at or above this go to human review. Tunable operating point.
DEFAULT_ESCALATION_THRESHOLD = 0.5


def score_risk(state: AuditState) -> float:
    """Aggregate grounded findings into a 0..1 claim-level risk score.

    # TODO: combine finding count, per-finding confidence, error-type severity
    #       (e.g. upcoding weighted higher), and estimated dollar exposure.
    """
    raise NotImplementedError


def decide(risk_score: float, threshold: float = DEFAULT_ESCALATION_THRESHOLD) -> TriageDecision:
    """Map a risk score to a routing decision."""
    return (
        TriageDecision.ESCALATE
        if risk_score >= threshold
        else TriageDecision.AUTO_CLEAR
    )


def run(state: AuditState) -> dict:
    """LangGraph node: set `risk_score` and `decision`.

    Returns a partial state update: {"risk_score": float, "decision": ...,
    "trace": [...]}.

    # TODO: score_risk -> decide -> append a trace entry; the audit log
    #       persists the final decision.
    """
    raise NotImplementedError
