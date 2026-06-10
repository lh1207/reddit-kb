# reddit-kb

MCP server that turns your saved Reddit content into a searchable knowledge base.
Saved posts/comments are embedded with `nomic-embed-text` (via Ollama) and stored
in ChromaDB; tools are exposed over MCP with fastmcp. Live thread fetching and
Reddit search are also available via PRAW.

> **Status:** wireframe. All tools are registered but raise `NotImplementedError`.

## Tools

| Tool | Purpose |
|---|---|
| `search_saved` | Semantic search over ingested saved content |
| `fetch_reddit_thread` | Fetch a live thread (post + top comments) by URL |
| `search_reddit` | Live Reddit search, optionally scoped to a subreddit |
| `ingest_saved` | Pull saved items, embed them, upsert into ChromaDB |

## Setup

1. Create a venv and install dependencies:

   ```sh
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and fill in your Reddit API credentials
   (create an app at <https://www.reddit.com/prefs/apps>).

3. Pull the embedding model in Ollama:

   ```sh
   ollama pull nomic-embed-text
   ```

4. Run the server:

   ```sh
   python server.py
   ```

   Or with Docker: `docker compose -f docker/docker-compose.yml up`.

## Build order

Fill in the stubs in this order — each step builds on the previous:

1. `lib/reddit.py` — authenticated PRAW client from env vars
2. `lib/embeddings.py` — `embed` / `embed_batch` against the Ollama API
3. `lib/chroma.py` — persistent collection at `CHROMA_PATH`
4. `tools/ingest.py` — saved items → embeddings → ChromaDB
5. `tools/search_saved.py` — query embedding → ChromaDB similarity search
6. `tools/fetch_live.py` — live thread fetch + live Reddit search
