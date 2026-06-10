"""Reddit client factory backed by PRAW."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import praw

_REQUIRED_VARS = (
    "REDDIT_CLIENT_ID",
    "REDDIT_CLIENT_SECRET",
    "REDDIT_USERNAME",
    "REDDIT_PASSWORD",
)


def get_reddit_client() -> praw.Reddit:
    """Build an authenticated praw.Reddit instance (script app / password flow) from REDDIT_* environment variables. Loads .env first; no network call is made."""
    from dotenv import load_dotenv

    load_dotenv()

    missing = [var for var in _REQUIRED_VARS if not os.environ.get(var)]
    if missing:
        raise RuntimeError(
            "Missing required environment variables: " + ", ".join(missing)
        )

    username = os.environ["REDDIT_USERNAME"]
    user_agent = os.environ.get(
        "REDDIT_USER_AGENT", f"reddit-kb/0.1 by u/{username}"
    )

    import praw

    return praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        username=username,
        password=os.environ["REDDIT_PASSWORD"],
        user_agent=user_agent,
        check_for_async=False,
    )
