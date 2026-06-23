"""Retrieval agent.

Given a claim's billed codes and clinical note, retrieve the most relevant
coding-guidance chunks (ICD-10 guidelines + CMS policies) from the ChromaDB
collection built by `knowledge_base.ingest`. Output feeds the validation agent.

Status: scaffold — node contract only, no implementation yet.
"""

from __future__ import annotations

from graph.state import AuditState, GuidanceHit


def build_queries(state: AuditState) -> list[str]:
    """Derive retrieval queries from the claim.

    # TODO: construct per-code queries (code + descriptor + note context) so
    #       each billed ICD-10/CPT code can be checked against its own guidance.
    """
    raise NotImplementedError


def retrieve(query: str, k: int = 5) -> list[GuidanceHit]:
    """Query the ChromaDB collection and return the top-`k` guidance hits.

    # TODO: open the persistent collection (CHROMA_PERSIST_DIR/CHROMA_COLLECTION),
    #       embed the query with the configured backend, return scored hits.
    """
    raise NotImplementedError


def run(state: AuditState) -> dict:
    """LangGraph node: populate `guidance` for downstream validation.

    Returns a partial state update: {"guidance": [...], "trace": [...]}.

    # TODO: build_queries -> retrieve per query -> dedupe/merge by chunk_id ->
    #       sort by score; append a trace entry.
    """
    raise NotImplementedError
