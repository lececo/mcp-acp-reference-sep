package agent.authz

# Sub-agent cannot have more roles than parent
delegation_violation {
    input.agent.parentAgentId != null
    parent := data.agent_sessions[input.agent.parentAgentId]
    role := input.agent.roles[_]
    not role in parent.roles
}
