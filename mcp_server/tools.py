from typing import Any, Dict
import mcp.types as types

def list_tools() -> list[types.Tool]:
    """Return a list of tool definitions."""
    return [
        types.Tool(
            name="database",
            description="Database tool with query and delete functions.",
            inputSchema={
                "type": "object",
                "properties": {
                    "function": {"type": "string", "enum": ["query", "delete"]},
                    "table": {"type": "string"},
                    "limit": {"type": "integer"},
                    "where": {"type": "string"}
                },
                "required": ["function", "table"]
            }
        ),
        types.Tool(
            name="payment",
            description="Payment tool with execute function.",
            inputSchema={
                "type": "object",
                "properties": {
                    "function": {"type": "string", "enum": ["execute"]},
                    "amount": {"type": "number"},
                    "to": {"type": "string"}
                },
                "required": ["function", "amount", "to"]
            }
        )
    ]

def execute_database_tool(args: Dict[str, Any]) -> str:
    """Execute dummy database functions."""
    func = args.get("function")
    table = args.get("table")
    limit = args.get("limit", "all")
    if func == "query":
        return f"Querying {limit} rows from table '{table}'..."
    elif func == "delete":
        return f"Deleting rows from table '{table}'..."
    else:
        raise ValueError(f"Unknown database function: {func}")

def execute_payment_tool(args: Dict[str, Any]) -> str:
    """Execute dummy payment functions."""
    func = args.get("function")
    amount = args.get("amount")
    to = args.get("to")
    if func == "execute":
        return f"Executing payment of ${amount} to '{to}'..."
    else:
        raise ValueError(f"Unknown payment function: {func}")
