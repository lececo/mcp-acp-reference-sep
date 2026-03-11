import json
import logging
import os
from typing import Any, Dict

import mcp.types as types
from mcp.server import Server
from mcp_server.tools import execute_database_tool, execute_payment_tool, list_tools

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Server("demo-server")

def get_manifest() -> Dict[str, Any]:
    manifest_path = os.path.join(os.path.dirname(__file__), "manifest.json")
    with open(manifest_path, "r") as f:
        return json.load(f)

@app.list_tools()
async def _list_tools() -> list[types.Tool]:
    """List available tools."""
    return list_tools()

@app.call_tool()
async def _call_tool(
    name: str,
    arguments: dict[str, Any] | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Execute a tool."""
    if name == "database":
        result = execute_database_tool(arguments or {})
    elif name == "payment":
        result = execute_payment_tool(arguments or {})
    else:
        raise ValueError(f"Unknown tool: {name}")

    return [types.TextContent(type="text", text=str(result))]

# Custom method handling is simulated at the HTTP layer, or via file read in the interceptor
# Due to strict Pydantic models in mcp SDK, registering custom methods natively requires hacking.
async def handle_authz_manifest_simulated(request: Any) -> Any:
    return get_manifest()

# SSE Setup
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse
import uvicorn

sse = SseServerTransport("/messages")

async def handle_sse(request: Request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())

async def handle_messages(request: Request):
    await sse.handle_post_message(request.scope, request.receive, request._send)

starlette_app = Starlette(
    debug=True,
    routes=[
        Route("/sse", endpoint=handle_sse),
        Route("/messages", endpoint=handle_messages, methods=["POST"])
    ]
)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    logger.info(f"Starting MCP Server on port {port}")
    uvicorn.run(starlette_app, host="0.0.0.0", port=port)
