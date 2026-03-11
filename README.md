# MCP Action-Level Authorization – Reference Implementation

This repository is a proof-of-concept reference implementation for a proposed MCP Specification Enhancement Proposal (SEP) that adds action-level authorization to the Model Context Protocol. It demonstrates the technical feasibility and production-readiness of the Authorization Checkpoint Protocol (ACP) and Tool Authorization Manifest (TAM) in a comprehensive, end-to-end Python monorepo.

> **Note:** `tools/authorizationManifest` is a draft extension pending SEP approval.

## Architecture

```
+----------------+      (tools/call)       +-------------------+       (tools/call)       +----------------+
|                | ----------------------> |                   | -----------------------> |                |
|   MCP Client   |                         |  ACP Interceptor  |                          |   MCP Server   |
|  (with Agent)  | <---------------------- |   (Middleware)    | <----------------------- |  (w/ TAM def)  |
|                |         Result          |                   |          Result          |                |
+-------+--------+                         +---------+---------+                          +--------+-------+
        |                                            |  |
        | injects JWT                                |  | (POST /v1/data/agent/authz)
        | context                                    |  v
        |                                  +---------+---------+
        +--------------------------------> |                   |
                                           |     OPA Policy    |
                                           |   Decision Point  |
                                           |                   |
                                           +-------------------+
```

## Quickstart

1. Start the backend services (OPA and MCP Server):
   ```bash
   docker compose up -build -d
   ```

2. Install dependencies via `uv`:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -e .[dev]
   ```

3. Run the end-to-end demo:
   ```bash
   python examples/agent_demo.py
   ```

## Demo Scenarios

The demo script `examples/agent_demo.py` runs through four distinct scenarios to test the ACP capabilities:

1. **ALLOW**: A finance agent with the `data-reader` role queries the `transactions` table with a limit of 100. This is allowed by the policies.
2. **DENY (role)**: A finance agent tries to use the `delete` tool. This is denied because the agent is missing the required `data-admin` role for this action.
3. **DENY (param)**: A finance agent queries the database with a limit of 2000. This is denied because it exceeds the `maxLimit` of 1000 defined in the parameter constraints.
4. **HUMAN APPROVAL**: An admin agent triggers `payment.execute`. This requires human approval according to the manifest, so the execution pauses and waits for 'y/n' input on the console.

## Relationship to existing MCP SEPs

- **SEP-990**: This proposal complements SEP-990 by formalizing authorization manifests for tools.
- **SEP-1046**: Action-level authorization aligns with the granular control objectives of SEP-1046.
- **SEP-1024**: ACP could integrate seamlessly with the identity verification mechanisms introduced in SEP-1024.
