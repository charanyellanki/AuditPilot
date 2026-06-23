"""Grounding verifier — quote-grounded LLM-as-judge.

The validation agent can hallucinate a justification. This node is the guardrail:
for every finding, it (1) confirms each cited span appears *verbatim* in its named
source, and (2) asks a judge LLM whether those spans actually substantiate the
finding. Any finding that fails either check is moved to `rejected_findings` so
the audit trail records *why* it was dropped.

Status: scaffold — node contract only, no implementation yet.
"""

from __future__ import annotations

from graph.state import AuditState, Finding, SourceSpan


JUDGE_SYSTEM_PROMPT = """\
TODO: instruct the judge to answer a single question per finding — do the quoted
spans, taken verbatim, actually support the claimed coding issue? Reject if the
quote is irrelevant, taken out of context, or does not entail the finding.
"""


def verify_spans_verbatim(finding: Finding, state: AuditState) -> bool:
    """Check that every cited span is an exact substring of its named source.

    Source resolution: span.source_id == "clinical_note" -> state["clinical_note"];
    otherwise match against the retrieved guidance chunk with that chunk_id.

    # TODO: resolve each SourceSpan's source text and confirm an exact match
    #       (optionally validate start/end offsets); return False on any miss.
    """
    raise NotImplementedError


def judge_finding(finding: Finding, state: AuditState) -> bool:
    """LLM-as-judge: do the verbatim spans substantiate the finding?

    # TODO: call JUDGE_MODEL with the finding + its spans; parse a boolean
    #       verdict (+ optional rationale for the trace).
    """
    raise NotImplementedError


def run(state: AuditState) -> dict:
    """LangGraph node: split findings into grounded vs. rejected.

    Returns a partial state update:
        {"findings": [grounded...], "rejected_findings": [...], "trace": [...]}.

    # TODO: for each finding, require verify_spans_verbatim AND judge_finding;
    #       mark grounded=True on survivors, route the rest to rejected_findings.
    """
    raise NotImplementedError
