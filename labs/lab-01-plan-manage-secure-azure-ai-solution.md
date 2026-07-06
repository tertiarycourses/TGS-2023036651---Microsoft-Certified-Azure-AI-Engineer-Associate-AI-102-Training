# Lab 01 - Plan, Manage, Monitor, and Secure an Azure AI Solution

## Objectives

- Select appropriate Azure AI services.
- Plan resource deployment and endpoints.
- Identify authentication, keys, monitoring, and cost controls.
- Prepare an AI solution architecture.

## Scenario

A company wants a customer support AI platform with document search, answer generation, sentiment analysis, speech transcription, and image processing. You must plan the Azure AI resources.

## Steps

### 1. Map Requirements to Services

| Requirement | Service |
| --- | --- |
| Generate responses | Azure OpenAI in Foundry Models |
| Search internal documents | Azure AI Search |
| Analyze sentiment | Azure AI Language |
| Transcribe calls | Azure AI Speech |
| Extract text from images | Azure AI Vision |
| Extract invoice fields | Azure AI Document Intelligence |

### 2. Plan Foundry Resources

Document:

```text
Hub or project name
Region
Model deployment
Default endpoint
Connected data source
Responsible AI settings
```

### 3. Plan Security

Record:

- Role-based access control.
- Managed identities.
- Key protection.
- Private endpoint or network controls.
- Logging and diagnostics.
- Secrets storage.

### 4. Plan Monitoring and Cost

Document:

```text
Token or transaction usage
Latency
Errors
Content safety events
Budget alerts
Diagnostic logs
```

### 5. Draw Architecture

Use diagrams.net:

```text
Application -> API layer -> Foundry/Azure AI services -> Search index/storage -> Monitoring
```

## Validation

You should have a service map, security plan, monitoring plan, and architecture diagram.

## Checkpoint Questions

1. Why is service selection part of AI engineering?
2. Why should keys be protected?
3. What should be monitored in an AI service?
4. What is the role of responsible AI planning?

## Course Focus

AI engineering starts with selecting the right service, securing it, monitoring it, and planning for cost and responsible use.
