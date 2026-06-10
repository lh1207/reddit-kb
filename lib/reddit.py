"""Reddit client factory backed by PRAW."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import praw


def get_reddit_client() -> praw.Reddit:
    """Will build an authenticated praw.Reddit instance from REDDIT_* environment variables."""
    # TODO: read REDDIT_* env vars and construct praw.Reddit
    pass
