# reddit-kb MCP server (build context: repo root)
FROM python:3.14-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Dependencies first so this layer is cached across code-only rebuilds.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# .dockerignore keeps .env and store/chroma out of the image.
COPY . .

EXPOSE 8000

# server.py runs stdio when invoked directly; the fastmcp CLI overrides the
# transport to HTTP for containerised use without touching application code.
CMD ["fastmcp", "run", "server.py", "--transport", "http", "--host", "0.0.0.0", "--port", "8000"]
