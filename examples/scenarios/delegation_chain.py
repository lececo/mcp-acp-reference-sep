async def run_delegation_chain(interceptor):
    """Scenario: Delegation Chain
    Shows sub-agent spawning with scoped permissions.
    """
    pass # Replaced by HUMAN APPROVAL in the main 4 script requirement, but keeping skeleton for completeness.
    
async def run_human_approval(interceptor):
    """Scenario 4: HUMAN APPROVAL
    Admin agent triggers payment.execute.
    Requires human interactive approval.
    """
    print("\n--- Scenario 4: HUMAN APPROVAL ---")
    print("Admin agent triggering payment of $500...")
    try:
        args = {"function": "execute", "amount": 500, "to": "vendor-inc"}
        result = await interceptor.call_tool("payment", args)
        print(f"✅ Success: {result}")
        return True, "Allowed (Human Approved)"
    except Exception as e:
        print(f"🛑 Denied: {e}")
        return False, "Denied (Human Rejected)"
