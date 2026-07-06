# Lab 04 - Agentic AI, Foundry Agent Service, Multi-Agent Concepts

## Objectives

- Explain agent roles and use cases.
- Plan Foundry Agent Service resources.
- Design custom agent tools and workflows.
- Review multi-agent orchestration concepts.

## Scenario

The support AI assistant needs to look up order status, search support documents, draft a reply, and escalate complex cases to a human agent.

## Steps

### 1. Define Agent Use Case

Write:

```text
Agent goal:
User types:
Allowed tools:
Disallowed actions:
Human escalation trigger:
Success metric:
```

### 2. Plan Agent Resources

Document:

- Foundry project.
- Model deployment.
- Search tool.
- Function or API tools.
- Authentication.
- Logging and trace settings.

### 3. Design Tool Calls

Create a table:

| Tool | Purpose | Input | Output |
| --- | --- | --- | --- |
| Search knowledge base | Retrieve support articles | Query | Relevant passages |
| Order lookup | Get order status | Order ID | Status summary |

### 4. Design Orchestration

Draw:

```text
User request -> agent plan -> tool call -> observation -> model reasoning -> response -> feedback
```

### 5. Multi-Agent Review

Explain when separate agents might be useful for retrieval, billing, technical support, and escalation review.

## Validation

You should have agent use case, resource plan, tool table, orchestration diagram, and multi-agent notes.

## Checkpoint Questions

1. What is an AI agent?
2. Why do agents need tool permissions?
3. What is orchestration?
4. Why should autonomous actions be constrained?

## Course Focus

Agentic solutions combine models, tools, workflows, monitoring, safety controls, and human escalation.
