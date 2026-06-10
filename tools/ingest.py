"""Tool: ingest the user's saved Reddit items into the ChromaDB knowledge base."""

from __future__ import annotations


def ingest_saved(limit: int | None = None) -> dict:
    """Will fetch the user's saved posts/comments, embed them, upsert into ChromaDB, and return ingest stats."""
    raise NotImplementedError("ingest_saved: saved-content ingestion pipeline not implemented yet")
