# reddit-kb

MCP server that turns your Reddit content into a searchable knowledge base.
Saved posts/comments are embedded with `nomic-embed-text` (via Ollama) and stored
in ChromaDB; tools are exposed over MCP with fastmcp.

## Purpose

I kept bookmarking useful Reddit comments, the kind with a real answer buried in them,
and wanted to actually reference them later and keep them intact. Reddit's saved list
is basically a junk drawer: no search, no tags, and posts can get edited or deleted
out from under you.

This pulls that content into a local index you control, so a vague memory like
"that thread about Proxmox ghost nodes" can turn into an actual search instead of a
lost cause.

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
> `OLLAMA_BASE_URL` in `.env` to `http://host.docker.internal:11434`
> (provided natively by Docker Desktop and OrbStack on macOS; OrbStack's
> `http://host.orb.internal:11434` also works), or to your host LAN /
> Tailscale IP on Linux. Credentials and config arrive only via `.env` at
> runtime — nothing is baked into the image. Note that changes to `.env`
> require recreating the container (`up -d`), not just restarting it.

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

## Connecting an MCP client

The container serves MCP over streamable HTTP at `http://localhost:8000/mcp`.
Any MCP-compatible client can connect to that endpoint.

**Claude Code:**

```sh
claude mcp add --transport http reddit-kb http://localhost:8000/mcp
```

**Generic client config** (e.g. `mcpServers` in Claude Desktop, Cursor, etc.):

```json
{
  "mcpServers": {
    "reddit-kb": {
      "type": "http",
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

**stdio (no Docker):** clients that spawn servers themselves can run it
directly — `python server.py` uses stdio transport by default:

```json
{
  "mcpServers": {
    "reddit-kb": {
      "command": "/path/to/reddit-kb/.venv/bin/python",
      "args": ["/path/to/reddit-kb/server.py"]
    }
  }
}
```

## Layout

- `server.py` — FastMCP server; registers the four tools (stdio locally, HTTP in Docker)
- `lib/reddit.py` — cookie-authenticated old.reddit JSON listing client
- `lib/embeddings.py` — `embed` / `embed_batch` against the Ollama API
- `lib/chroma.py` — persistent collection at `CHROMA_PATH`
- `tools/ingest.py` — saved items → embeddings → ChromaDB
- `tools/search_saved.py` — query embedding → ChromaDB similarity search
- `tools/fetch_live.py` — live thread fetch + live Reddit search
- `docker/` — Dockerfile + compose for the containerised HTTP server
