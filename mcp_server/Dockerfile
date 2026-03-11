FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml /app/
# Actually we can just install dependencies individually to avoid needing the full repo structure
RUN pip install "mcp>=1.2.0" "python-jose>=3.3.0"

COPY mcp_server /app/mcp_server

# Run the server script
CMD ["python", "-m", "mcp_server.server"]
