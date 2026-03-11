from middleware.identity import create_agent_jwt

def get_admin_agent_token() -> str:
    """Create a token for an admin agent with all necessary roles."""
    return create_agent_jwt(sub="agent-admin-01", roles=["data-reader", "data-admin", "finance-writer", "admin"])
