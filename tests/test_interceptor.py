import pytest
from unittest.mock import AsyncMock, patch

from middleware.interceptor import ACPInterceptor, AuthorizationError
from middleware.identity import create_agent_jwt

@pytest.fixture
def mock_session():
    session = AsyncMock()
    session.call_tool = AsyncMock(return_value="mock_result")
    return session

@pytest.mark.asyncio
async def test_interceptor_missing_jwt(mock_session):
    interceptor = ACPInterceptor(mock_session)
    with pytest.raises(AuthorizationError) as exc_info:
        await interceptor.call_tool("database", {"function": "query"})
    assert "No JWT token provided" in str(exc_info.value)

@pytest.mark.asyncio
@patch("middleware.interceptor.check_authorization")
async def test_interceptor_allow(mock_check_authz, mock_session):
    mock_check_authz.return_value = {"allow": True, "requires_human_approval": False}
    
    interceptor = ACPInterceptor(mock_session)
    token = create_agent_jwt("agent-01", ["data-reader"])
    
    result = await interceptor.call_tool("database", {"function": "query"}, jwt_token=token)
    assert result == "mock_result"
    mock_session.call_tool.assert_called_once_with("database", {"function": "query"})

@pytest.mark.asyncio
@patch("middleware.interceptor.check_authorization")
async def test_interceptor_deny(mock_check_authz, mock_session):
    mock_check_authz.return_value = {"allow": False}
    
    interceptor = ACPInterceptor(mock_session)
    token = create_agent_jwt("agent-01", ["data-reader"])
    
    with pytest.raises(AuthorizationError) as exc_info:
        await interceptor.call_tool("database", {"function": "delete"}, jwt_token=token)
    assert "Action denied by policy" in str(exc_info.value)
    mock_session.call_tool.assert_not_called()
