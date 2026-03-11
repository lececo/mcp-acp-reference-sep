import os
import httpx
from typing import Any, Dict

OPA_URL = os.environ.get("OPA_URL", "http://localhost:8181")

class AuthorizationError(Exception):
    """Raised when an action is denied by the policy."""
    pass

async def check_authorization(input_document: Dict[str, Any]) -> Dict[str, Any]:
    """Call OPA PDP to evaluate authorization rules."""
    fail_behavior = os.environ.get("ACP_FAIL_BEHAVIOR", "closed").lower()
    
    url = f"{OPA_URL}/v1/data/agent/authz"
    payload = {"input": input_document}
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=2.0)
            response.raise_for_status()
            result = response.json()
            return result.get("result", {})
    except (httpx.RequestError, httpx.HTTPStatusError) as e:
        # Network or HTTP error handling
        if fail_behavior == "open":
            # Fail-open: allow by default if OPA is unreachable
            return {"allow": True, "requires_human_approval": False}
        else:
            # Fail-closed (default): raise error
            raise AuthorizationError(f"PDP communication failed (fail-closed): {str(e)}")
