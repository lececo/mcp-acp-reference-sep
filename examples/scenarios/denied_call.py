async def run_denied_call(interceptor):
    """Scenario 2: DENY (role)
    Finance agent tries to 'delete' from 'transactions'.
    Missing 'data-admin' role.
    """
    print("\n--- Scenario 2: DENY (role) ---")
    print("Finance agent trying to 'delete' from 'transactions'...")
    try:
        args = {"function": "delete", "table": "transactions"}
        result = await interceptor.call_tool("database", args)
        print(f"✅ Success: {result}")
        return True, "Allowed (unexpected)"
    except Exception as e:
        print(f"🛑 Denied cleanly: {e}")
        return False, "Denied (Missing Role)"
