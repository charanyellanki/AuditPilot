"""Shared state passed between nodes of the AuditPilot LangGraph.

Each agent node receives the current `AuditState`, reads what it needs, and
returns a partial update that LangGraph merges into the running state. Keeping
all inter-agent contracts here makes the data flow auditable in one place.

Status: scaffold — types and contracts only.
"""

from __future__ import annotations

from enum import Enum
from typing import Annotated, Any, TypedDict


class TriageDecision(str, Enum):
    """Terminal routing decision produced by the triage agent."""

    AUTO_CLEAR = "auto_clear"
    ESCALATE = "escalate"


class SourceSpan(TypedDict):
    """A verbatim span used to ground a finding.

    `quote` must appear literally in the document identified by `source_id`
    so the grounding verifier can confirm it by exact match.
    """

    source_id: str          # "clinical_note" or a GuidanceChunk.chunk_id
    quote: str              # verbatim text copied from the source
    start: int              # char offset of the quote in the source
    end: int


class GuidanceHit(TypedDict):
    """A retrieved guidance chunk with its similarity score."""

    chunk_id: str
    text: str
    source: str             # "icd10_guidelines" | "cms_policy"
    score: float
    metadata: dict[str, Any]


class Finding(TypedDict):
    """A single potential coding error surfaced by the validation agent."""

    code: str                       # the billed ICD-10/CPT code in question
    code_system: str                # "ICD-10" | "CPT"
    issue: str                      # human-readable description of the problem
    error_type: str                 # aligns with data.inject_errors.ErrorType
    supporting_spans: list[SourceSpan]
    confidence: float
    grounded: bool                  # set by the grounding verifier


def _replace(_old: Any, new: Any) -> Any:
    """Reducer: later writes overwrite earlier ones (last-write-wins)."""
    return new


class AuditState(TypedDict, total=False):
    """End-to-end state for validating one claim.

    Populated incrementally as the graph runs:
      retrieval -> validation -> grounding -> triage.
    """

    # --- Input ---
    claim_id: str
    icd10_codes: list[str]
    cpt_codes: list[str]
    clinical_note: str

    # --- Retrieval agent output ---
    guidance: Annotated[list[GuidanceHit], _replace]

    # --- Validation agent output ---
    findings: Annotated[list[Finding], _replace]

    # --- Grounding verifier output ---
    # Findings whose citations failed verbatim grounding, kept for the audit log.
    rejected_findings: Annotated[list[Finding], _replace]

    # --- Triage agent output ---
    risk_score: float
    decision: TriageDecision

    # --- Cross-cutting ---
    # Per-node trace entries appended for the audit log (reducer concatenates).
    trace: Annotated[list[dict[str, Any]], lambda old, new: (old or []) + new]
    errors: Annotated[list[str], lambda old, new: (old or []) + new]
