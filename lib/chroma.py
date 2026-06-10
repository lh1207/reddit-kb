"""ChromaDB persistent collection access."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import chromadb


def get_collection() -> chromadb.Collection:
    """Will open (or create) the persistent reddit-kb collection at CHROMA_PATH."""
    # TODO: create chromadb.PersistentClient(CHROMA_PATH) and get_or_create_collection
    pass
