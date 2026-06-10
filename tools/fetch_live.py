"""Tools: live Reddit lookups (fetch a thread, search Reddit) via PRAW."""

from __future__ import annotations


def fetch_reddit_thread(url: str, comment_limit: int = 50) -> dict:
    """Will fetch a live Reddit thread by URL and return its post body plus top comments."""
    raise NotImplementedError("fetch_reddit_thread: live thread fetching not implemented yet")


def search_reddit(query: str, subreddit: str | None = None, limit: int = 10) -> list[dict]:
    """Will search Reddit live (optionally scoped to a subreddit) and return matching submissions."""
    raise NotImplementedError("search_reddit: live Reddit search not implemented yet")
