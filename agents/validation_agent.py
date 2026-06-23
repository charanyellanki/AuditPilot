"""Validation agent.

For each billed code, judge — via an LLM, grounded in the retrieved guidance and
the clinical note — whether the documentation supports the code. Emits `Finding`
objects, each citing the verbatim span(s) it relied on so the grounding verifier
can confirm them.

Status: scaffold — node contract only, no implementation yet.
"""

from __future__ import annotations

from graph.state import AuditState, Finding


VALIDATION_SYSTEM_PROMPT = """\
TODO: instruct the model to decide, per billed code, whether the clinical note
+ retrieved guidance support it. Require every finding to quote the exact note
or guidance text it relies on (verbatim, copy-paste) and to classify the issue
into one of: upcoding, unsupported_procedure, missing_documentation.
"""


def validate_code(
    code: str,
    code_system: str,
    state: AuditState,
) -> Finding | None:
    """Validate one billed code against note + guidance.

    Returns a `Finding` if the code appears unsupported, else None.

    # TODO: assemble prompt (code descriptor + note + relevant guidance hits),
    #       call the configured LLM, parse a structured finding with cited spans.
    """
    raise NotImplementedError


def run(state: AuditState) -> dict:
    """LangGraph node: produce `findings` across all billed codes.

    Returns a partial state update: {"findings": [...], "trace": [...]}.

    # TODO: iterate icd10_codes + cpt_codes, call validate_code, collect
    #       non-null findings; append a trace entry.
    """
    raise NotImplementedError
