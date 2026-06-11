# reddit-kb

MCP server that turns your saved Reddit content into a searchable knowledge base.
Saved posts/comments are embedded with `nomic-embed-text` (via Ollama) and stored
in ChromaDB; tools are exposed over MCP with fastmcp.

> **Status:** all four tools are implemented and the server is packaged for
> Docker. Remaining: the first full ingest run.

## Authentication

Reddit closed self-service API access in November 2025, so PRAW/OAuth is no
longer an option. Instead, reddit-kb reads the logged-in old.reddit JSON
listing (`old.reddit.com/user/<username>/saved.json`) authenticated with your
browser's `reddit_session` cookie. The cookie lives only in `.env` (gitignored)
and is never logged.

The saved listing is capped by Reddit at roughly the most recent ~1000 items.
If you need older saves, request a [Reddit data export](https://www.reddit.com/settings/data-request)
and backfill from the CSV it provides (not yet automated).

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

2. Copy `.env.example` to `.env`, set `REDDIT_USERNAME`, and paste the
   `reddit_session` cookie value from a logged-in browser session at
   <https://old.reddit.com> into `REDDIT_SESSION_COOKIE`.

3. Pull the embedding model in Ollama:

   ```sh
   ollama pull nomic-embed-text
   ```

4. Run the server:

   ```sh
   python server.py
   ```

   Or run it in Docker — see below.

## Docker

Build and start the container (from the repo root):

```sh
docker compose -f docker/docker-compose.yml up --build -d
```

> **Ollama caveat:** inside the container, `localhost` is the container itself,
> so the bare-metal default `OLLAMA_BASE_URL=http://localhost:11434` will not
> reach the Ollama instance on your host. Before starting, set
> `OLLAMA_BASE_URL` in `.env` to your host LAN IP or Tailscale IP, e.g.
> `http://192.168.1.x:11434`. Credentials and config arrive only via `.env` at
> runtime — nothing is baked into the image.

Ingest your saved items from inside the container:

```sh
docker compose -f docker/docker-compose.yml exec reddit-kb \
  python -c "from tools.ingest import ingest_saved; print(ingest_saved())"
```

Stop the container:

```sh
docker compose -f docker/docker-compose.yml down
```

The vector store is bind-mounted at `./store/chroma`, so ingested data
persists on the host across restarts and rebuilds.

## Build order

Fill in the stubs in this order — each step builds on the previous:

1. `lib/reddit.py` — cookie-authenticated old.reddit JSON listing client ✅
2. `lib/embeddings.py` — `embed` / `embed_batch` against the Ollama API ✅
3. `lib/chroma.py` — persistent collection at `CHROMA_PATH` ✅
4. `tools/ingest.py` — saved items → embeddings → ChromaDB ✅
5. `tools/search_saved.py` — query embedding → ChromaDB similarity search ✅
6. `tools/fetch_live.py` — live thread fetch + live Reddit search ✅
