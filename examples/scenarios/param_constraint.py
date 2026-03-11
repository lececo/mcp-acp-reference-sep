async def run_param_constraint(interceptor):
    """Scenario 3: DENY (param)
    Finance agent queries 'transactions' table with limit 2000.
    Exceeds maxLimit of 1000.
    """
    print("\n--- Scenario 3: DENY (param limit) ---")
    print("Finance agent querying 'transactions' table (limit=2000)...")
    try:
        args = {"function": "query", "table": "transactions", "limit": 2000}
        result = await interceptor.call_tool("database", args)
        print(f"✅ Success: {result}")
        return True, "Allowed (unexpected)"
    except Exception as e:
        print(f"🛑 Denied cleanly: {e}")
        return False, "Denied (Param Limit)"
