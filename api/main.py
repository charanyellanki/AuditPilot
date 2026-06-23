"""FastAPI app exposing claim validation over HTTP.

Endpoints (planned):
    GET  /health           -> liveness probe
    POST /validate         -> validate a single claim, return findings + decision

Run locally:

    uvicorn api.main:app --reload

Status: scaffold — request/response models + route shells, no logic yet.
"""

from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="AuditPilot",
    description="Validate billed ICD-10/CPT codes against clinical documentation.",
    version="0.0.1",
)


class ClaimRequest(BaseModel):
    """Incoming claim to validate."""

    claim_id: str
    icd10_codes: list[str] = Field(default_factory=list)
    cpt_codes: list[str] = Field(default_factory=list)
    clinical_note: str


class FindingResponse(BaseModel):
    code: str
    code_system: str
    issue: str
    error_type: str
    confidence: float
    grounded: bool
    # Verbatim spans supporting the finding (source_id, quote, offsets).
    supporting_spans: list[dict] = Field(default_factory=list)


class ValidationResponse(BaseModel):
    """Result of running the agent graph over one claim."""

    claim_id: str
    decision: str                     # "auto_clear" | "escalate"
    risk_score: float
    findings: list[FindingResponse] = Field(default_factory=list)


@app.get("/health")
def health() -> dict:
    """Liveness probe."""
    return {"status": "ok", "version": app.version}


@app.post("/validate", response_model=ValidationResponse)
def validate(claim: ClaimRequest) -> ValidationResponse:
    """Validate a single claim through the agent graph.

    # TODO: build initial AuditState from `claim`, invoke graph.get_graph(),
    #       map the resulting state into ValidationResponse, and persist the
    #       decision via audit_log.
    """
    raise NotImplementedError
