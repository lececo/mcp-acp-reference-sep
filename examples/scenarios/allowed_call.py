async def run_allowed_call(interceptor):
    """Scenario 1: ALLOW
    Finance agent queries 'transactions' table with limit 100.
    """
    print("\n--- Scenario 1: ALLOW ---")
    print("Finance agent querying 'transactions' table (limit=100)...")
    try:
        args = {"function": "query", "table": "transactions", "limit": 100}
        result = await interceptor.call_tool("database", args)
        print(f"✅ Success: {result}")
        return True, "Allowed"
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False, str(e)
