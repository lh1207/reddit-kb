"""reddit-kb MCP server: registers search, fetch, and ingest tools with fastmcp."""

from fastmcp import FastMCP

from tools.fetch_live import fetch_reddit_thread, search_reddit
from tools.ingest import ingest_saved
from tools.search_saved import search_saved

mcp = FastMCP("reddit-kb")

mcp.tool(search_saved)
mcp.tool(fetch_reddit_thread)
mcp.tool(search_reddit)
mcp.tool(ingest_saved)

if __name__ == "__main__":
    mcp.run()
