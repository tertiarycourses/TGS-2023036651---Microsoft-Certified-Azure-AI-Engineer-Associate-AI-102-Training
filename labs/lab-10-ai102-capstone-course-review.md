# Lab 10 - AI-102 Capstone and Course Review

## Objectives

- Design an end-to-end Azure AI solution.
- Map requirements to Microsoft Foundry and Azure AI services.
- Include security, monitoring, responsible AI, and cost controls.
- Build a personal review plan.

## Scenario

You must design a production-ready customer support AI platform that supports grounded chat, document search, sentiment analysis, speech transcription, image OCR, document extraction, and human escalation.

## Steps

### 1. Build a Service Map

| Requirement | Service |
| --- | --- |
| Grounded assistant | Foundry, Azure OpenAI, prompt flow, RAG |
| Agent workflow | Foundry Agent Service |
| Document search | Azure AI Search |
| Sentiment and PII | Azure AI Language |
| Speech transcription | Azure AI Speech |
| Image OCR | Azure AI Vision |
| Invoice extraction | Document Intelligence |
| Multi-content extraction | Content Understanding |
| Safety controls | Content Safety and responsible AI governance |

### 2. Draw the Architecture

Include:

```text
User application
API layer
Foundry project
Model deployment
AI Search index
Storage
Language/Speech/Vision/Document services
Monitoring
Human review queue
```

### 3. Add Governance Controls

Document:

- RBAC.
- Managed identity.
- Key protection.
- Prompt filters.
- Content safety.
- Logging and monitoring.
- Budget alerts.
- Data retention.
- Human escalation.

### 4. Rate Skill Confidence

| Skill Area | Confidence 1-5 | Study Action |
| --- | --- | --- |
| Plan and manage Azure AI solution |  |  |
| Implement generative AI solutions |  |  |
| Implement agentic solution |  |  |
| Implement computer vision solutions |  |  |
| Implement NLP solutions |  |  |
| Implement knowledge mining and information extraction |  |  |

### 5. Clean Up Resources

If you created resources:

```bash
az group delete --name rg-ai102-lab --yes --no-wait
```

Confirm with your instructor before deleting shared resources.

### 6. Create a 7-Day Review Plan

1. Day 1: Planning, security, monitoring, responsible AI.
2. Day 2: Generative AI, prompt flow, RAG.
3. Day 3: Agents and orchestration.
4. Day 4: Vision and video.
5. Day 5: NLP, speech, translation, question answering.
6. Day 6: AI Search, Document Intelligence, Content Understanding.
7. Day 7: Capstone review and mistakes log.

## Validation

You should have a service map, architecture diagram, governance checklist, confidence matrix, cleanup plan, and review plan.

## Checkpoint Questions

1. Which service should power grounded document search?
2. When should a human review AI output?
3. What is the difference between RAG and fine-tuning?
4. Which AI workload do you need to review most?

## Course Focus

Azure AI engineering is about integrating the right AI services into secure, monitored, responsible, production-ready solutions.
