"""Ingest coding guidance into a ChromaDB vector store.

Chunks and embeds two corpora the retrieval agent searches:
  * ICD-10-CM Official Guidelines for Coding and Reporting.
  * CMS coverage policies (NCDs/LCDs) relevant to the claim population.

The persisted collection is later queried by `agents.retrieval_agent`.

Run as a module:

    python -m knowledge_base.ingest --source docs/guidance --reset

Status: scaffold — signatures and contracts only, no implementation yet.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class GuidanceChunk:
    """A single embeddable chunk of source guidance.

    Attributes:
        chunk_id: Stable, deterministic id (e.g. hash of source + offset).
        text: The chunk text to embed.
        source: One of "icd10_guidelines" | "cms_policy".
        metadata: Provenance for citation (doc title, section, code refs, url).
    """

    chunk_id: str
    text: str
    source: str
    metadata: dict = field(default_factory=dict)


def load_documents(source_dir: Path) -> list[tuple[str, str, dict]]:
    """Load raw guidance documents from `source_dir`.

    Returns a list of (source_kind, raw_text, metadata) tuples.

    # TODO: support PDF/HTML/TXT; tag each doc as icd10_guidelines or cms_policy.
    """
    raise NotImplementedError


def chunk_document(text: str, source: str, metadata: dict) -> list[GuidanceChunk]:
    """Split one document into overlapping, citation-friendly chunks.

    # TODO: structure-aware splitting (preserve section headings + code refs)
    #       with a configurable token window and overlap; keep enough context
    #       that a retrieved chunk is independently quotable for grounding.
    """
    raise NotImplementedError


def embed_chunks(chunks: list[GuidanceChunk]) -> list[list[float]]:
    """Embed chunk texts with the configured backend (local ST or OpenAI API).

    # TODO: read EMBEDDING_BACKEND/EMBEDDING_MODEL from settings; batch calls.
    """
    raise NotImplementedError


def build_index(
    chunks: list[GuidanceChunk],
    persist_dir: str,
    collection: str,
    reset: bool = False,
) -> None:
    """Upsert chunks (+embeddings +metadata) into a persistent ChromaDB collection.

    Args:
        chunks: Chunks to index.
        persist_dir: ChromaDB persistence directory (see CHROMA_PERSIST_DIR).
        collection: Target collection name (see CHROMA_COLLECTION).
        reset: If True, drop and recreate the collection before upserting.

    # TODO: chromadb.PersistentClient(...); get_or_create_collection; upsert
    #       ids/documents/embeddings/metadatas in batches.
    """
    raise NotImplementedError


def main() -> None:
    """CLI entry point: load -> chunk -> embed -> build_index.

    # TODO: argparse for --source/--persist-dir/--collection/--reset.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
