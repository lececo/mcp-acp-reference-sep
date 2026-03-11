package agent.authz

default allow = false
default requires_human_approval = false

# Load tool requirements from registry
tool_requirements := data.tools[input.action.tool].functions[input.action.function]

# Allow if agent has all required roles
allow {
    required := tool_requirements.requiredRoles
    every role in required {
        role in input.agent.roles
    }
    not parameter_violation
    not delegation_violation
}

# Parameter constraints

# Query limit constraint
parameter_violation {
    tool_requirements.parameterConstraints.maxLimit
    input.action.parameters.limit > tool_requirements.parameterConstraints.maxLimit
}

# Allowed tables constraint
parameter_violation {
    allowed := tool_requirements.parameterConstraints.allowedTables
    not input.action.parameters.table in allowed
}

# Payment amount constraint
parameter_violation {
    tool_requirements.parameterConstraints.maxAmount
    input.action.parameters.amount > tool_requirements.parameterConstraints.maxAmount
}

requires_human_approval {
    tool_requirements.requiresHumanApproval == true
}
