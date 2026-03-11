import pytest

def test_tam_manifest_endpoint():
    """
    Test that the server exposes the manifest at tools/authorizationManifest.
    """
    from mcp_server.server import get_manifest
    
    manifest = get_manifest()
    assert "schemaVersion" in manifest
    assert "tools" in manifest
    assert "database" in manifest["tools"]
    assert "query" in manifest["tools"]["database"]["functions"]

