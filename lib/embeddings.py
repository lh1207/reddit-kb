"""Text embeddings via the Ollama API (nomic-embed-text)."""

from __future__ import annotations


def embed(text: str) -> list[float]:
    """Will embed a single text with EMBED_MODEL via OLLAMA_BASE_URL and return its vector."""
    # TODO: POST to Ollama /api/embed with EMBED_MODEL
    pass


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Will embed a batch of texts with EMBED_MODEL via OLLAMA_BASE_URL and return their vectors."""
    # TODO: batch POST to Ollama /api/embed with EMBED_MODEL
    pass
