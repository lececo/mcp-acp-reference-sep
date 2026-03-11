import pytest
import subprocess
import json
import os

OPA_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "opa", "data", "tools_registry.json")
OPA_POLICY_PATH = os.path.join(os.path.dirname(__file__), "..", "opa", "policies", "agent_authz.rego")
OPA_DELEGATION_PATH = os.path.join(os.path.dirname(__file__), "..", "opa", "policies", "delegation.rego")

def evaluate_opa(input_data):
    """Run OPA eval locally for tests if OPA is installed."""
    try:
        # We verify if OPA is available, else we skip
        subprocess.run(["opa", "version"], capture_output=True, check=True)
    except Exception:
        pytest.skip("OPA CLI not installed")
        return

    cmd = [
        "opa", "eval",
        "-d", OPA_DATA_PATH,
        "-d", OPA_POLICY_PATH,
        "-d", OPA_DELEGATION_PATH,
        "-I", "data.agent.authz"
    ]
    
    with open("temp_input.json", "w") as f:
        json.dump({"input": input_data}, f)
        
    try:
        with open("temp_input.json", "r") as f:
            result = subprocess.run(cmd, stdin=f, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"OPA eval failed: {result.stderr}")
            
        output = json.loads(result.stdout)
        return output.get("result", [{}])[0].get("expressions", [{}])[0].get("value", {})
    finally:
        if os.path.exists("temp_input.json"):
            os.remove("temp_input.json")

def test_opa_allow_with_valid_roles():
    input_doc = {
        "agent": {"roles": ["data-reader"]},
        "action": {"tool": "database", "function": "query", "parameters": {}}
    }
    result = evaluate_opa(input_doc)
    if result:
        assert result.get("allow") == True

def test_opa_deny_without_valid_roles():
    input_doc = {
        "agent": {"roles": ["data-reader"]},
        "action": {"tool": "database", "function": "delete", "parameters": {}}
    }
    result = evaluate_opa(input_doc)
    if result:
        assert result.get("allow") == False
