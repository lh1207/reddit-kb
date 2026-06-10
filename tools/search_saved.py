"""Tool: semantic search over the user's ingested saved Reddit content."""

from __future__ import annotations


def search_saved(query: str, limit: int = 10) -> list[dict]:
    """Will embed the query and return the top matching saved posts/comments from ChromaDB."""
    raise NotImplementedError("search_saved: semantic search over ingested saved content not implemented yet")
