from middleware.identity import create_agent_jwt

def get_finance_agent_token() -> str:
    """Create a token for a finance agent with data-reader role."""
    return create_agent_jwt(sub="agent-finance-01", roles=["data-reader"])

def get_finance_writer_agent_token() -> str:
    """Create a token for a finance agent with writer role."""
    return create_agent_jwt(sub="agent-finance-02", roles=["data-reader", "finance-writer"])

