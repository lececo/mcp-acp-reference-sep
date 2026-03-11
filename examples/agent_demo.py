import asyncio
import os
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client

from examples.agents.finance_agent import get_finance_agent_token
from examples.agents.admin_agent import get_admin_agent_token
from middleware.interceptor import ACPInterceptor

from examples.scenarios.allowed_call import run_allowed_call
from examples.scenarios.denied_call import run_denied_call
from examples.scenarios.param_constraint import run_param_constraint
from examples.scenarios.delegation_chain import run_human_approval

async def main():
    print("="*60)
    print("MCP Action-Level Authorization (ACP) – Reference Demo")
    print("="*60)
    print("This demo connects to the MCP server and executes 4 scenarios")
    print("verifying the integration of ACP middleware and OPA policies.")
    print("="*60)

    results = []

    # Use SSE to connect to the MCP server
    async with sse_client("http://localhost:8000/sse") as streams:
        read_stream, write_stream = streams
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            # 1. Provide Finance Agent JWT
            os.environ["ACP_AGENT_TOKEN"] = get_finance_agent_token()
            interceptor = ACPInterceptor(session)
            await interceptor.initialize()
            
            # Scenario 1: ALLOW
            res, msg = await run_allowed_call(interceptor)
            results.append(("S1: ALLOW (finance -> query limit=100)", "Pass" if res else "Fail", msg))
            
            # Scenario 2: DENY (Role)
            res, msg = await run_denied_call(interceptor)
            # This should raise AuthorizationError, which means run_denied_call returns False normally
            # Wait, in the test snippet, returning False from run_denied_call means it WAS cleanly denied
            results.append(("S2: DENY Role (finance -> delete)", "Pass" if not res else "Fail", msg))
            
            # Scenario 3: DENY (Param)
            res, msg = await run_param_constraint(interceptor)
            results.append(("S3: DENY Param (finance -> query limit=2000)", "Pass" if not res else "Fail", msg))

            # 2. Provide Admin Agent JWT
            os.environ["ACP_AGENT_TOKEN"] = get_admin_agent_token()
            
            # Scenario 4: HUMAN APPROVAL
            # Requires typing 'y' in the console!
            res, msg = await run_human_approval(interceptor)
            results.append(("S4: HUMAN APPROVAL (admin -> payment executor)", "Pass" if res else "Fail", msg))

    print("\n\n" + "="*60)
    print("DEMO SUMMARY")
    print("="*60)
    print(f"{'Scenario':<45} | {'Result':<6} | {'Message':<25}")
    print("-" * 60)
    for name, result, msg in results:
        print(f"{name:<45} | {result:<6} | {msg:<25}")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(main())
