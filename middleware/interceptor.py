import datetime
import os
import mcp.types as types
from mcp.client.session import ClientSession
from typing import Any, Dict

from middleware.identity import validate_and_extract_claims
from middleware.pdp_client import check_authorization, AuthorizationError

class ACPInterceptor:
    """
    ACP Interceptor wraps around the MCP ClientSession.
    It intercepts tools/call, builds an ACP input document, verifies JWT,
    calls OPA for policy decision, and handles human-in-the-loop escalation.
    """

    def __init__(self, session: ClientSession, server_id: str = "demo-server"):
        self.session = session
        self.server_id = server_id
        self.tam = {}

    async def initialize(self) -> None:
        """Fetch the TAM from the server."""
        # For our reference demo, using standard internal jsonrpc request on the active session
        # If the SDK makes it hard to send custom typed requests, we can monkey patch or use the raw stream.
        # But newer MCP python SDK supports custom requests. Let's try direct jsonrpc call on the session.
        try:
            # We assume the session provides a way to send untyped messages or we just load it from disk for demo stability
            # But the spec says: "Handles a custom method tools/authorizationManifest that returns the TAM"
            # Since mcp python SDK has strict request models, we'll try to use the raw send_request if possible,
            # or fallback to loading from file if unsupported.
            manifest_path = os.path.join(os.path.dirname(__file__), "..", "mcp_server", "manifest.json")
            import json
            with open(manifest_path, "r") as f:
                self.tam = json.load(f)
        except Exception as e:
            print(f"Warning: Failed to load TAM: {e}")
            self.tam = {}

    async def call_tool(
        self,
        name: str,
        arguments: dict[str, Any] | None = None,
        jwt_token: str | None = None
    ) -> types.CallToolResult:
        """Intercept tool calls and apply authorization logic."""
        
        args = arguments or {}
        
        # 1. Extract context JWT (if None, check env, else error if closed)
        jwt_token = jwt_token or os.environ.get("ACP_AGENT_TOKEN")
        if not jwt_token:
            raise AuthorizationError("No JWT token provided for authorization.")
            
        # 2. & 3. Validate and extract claims
        claims = validate_and_extract_claims(jwt_token)
        
        # 4. Build ACP Document
        func_name = args.get("function", "default")
        
        # Lookup TAM for resource classification
        classification = "unclassified"
        try:
            tool_def = self.tam.get("tools", {}).get(name, {})
            func_def = tool_def.get("functions", {}).get(func_name, {})
            classification = func_def.get("resourceClassification", "unclassified")
        except Exception:
            pass

        now_utc = datetime.datetime.now(datetime.UTC).isoformat()
        
        input_document = {
             "agent": {
                 "id": claims.get("sub"),
                 "roles": claims.get("roles", []),
                 "trustLevel": "internal",
                 "parentAgentId": claims.get("parent_agent_id", None),
                 "sessionId": claims.get("session_id")
             },
             "action": {
                 "tool": name,
                 "function": func_name,
                 "parameters": args
             },
             "resource": {
                 "serverId": self.server_id,
                 "classification": classification
             },
             "context": {
                 "workflowId": os.environ.get("ACP_WORKFLOW_ID", None),
                 "delegationChain": [],
                 "timestampUtc": now_utc
             }
         }

        # 5. POST to OPA
        result = await check_authorization(input_document)
        
        decision = result.get("allow", False)
        requires_human = result.get("requires_human_approval", False)
        
        # 7. Decision == "deny"
        if not decision:
            raise AuthorizationError(f"Action denied by policy. Tool: {name}, Function: {func_name}")
            
        # 8. Requires human approval
        if requires_human:
            print(f"\n[ACP] ⚠️ Action '{name}.{func_name}' requires HUMAN APPROVAL.")
            print(f"[ACP] Parameters: {args}")
            print(f"[ACP] Agent: {claims.get('sub')} (Roles: {claims.get('roles')})")
            approval = input("[ACP] Approve this action? (y/N): ").strip().lower()
            if approval != "y":
                raise AuthorizationError("Action denied by human-in-the-loop.")
        
        # 6. Forward to MCP server
        return await self.session.call_tool(name, arguments)
