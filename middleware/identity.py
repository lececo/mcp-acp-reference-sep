import time
from typing import Any, Dict
from jose import jwt, jws

# For demo purposes, we define a static symmetric key.
# In production, this would be an RS256 key pair.
SECRET_KEY = "demo-super-secret-key-123"
ALGORITHM = "HS256"

def create_agent_jwt(sub: str, roles: list[str], parent_agent_id: str | None = None) -> str:
    """Create a demo JWT for an agent."""
    claims = {
        "sub": sub,
        "roles": roles,
        "session_id": f"session-{time.time_ns()}",
        "parent_agent_id": parent_agent_id,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600
    }
    encoded_jwt = jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def validate_and_extract_claims(token: str) -> Dict[str, Any]:
    """Validate JWT signature and extract claims."""
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except jwt.JWTError as e:
        raise ValueError(f"Invalid JWT: {e}")
