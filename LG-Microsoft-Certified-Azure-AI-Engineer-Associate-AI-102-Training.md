# Learner Guide - Microsoft Certified Azure AI Engineer Associate (AI-102) Training

## Course Information

| Item | Details |
| --- | --- |
| Course Code | TGS-2023036651 |
| Course Title | Microsoft Certified Azure AI Engineer Associate (AI-102) Training |
| Registration | https://www.tertiarycourses.com.sg/wsq-microsoft-certified-azure-ai-engineer-associate-ai-102-training.html |
| Microsoft Study Guide | https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ai-102 |

## Certification Status Note

The Microsoft Learn study guide currently states that Exam AI-102 was retired on June 30, 2026. These labs are therefore written as Azure AI Engineer courseware based on the published AI-102 skills outline and Microsoft Foundry/Azure AI engineering practices, rather than as a guarantee of availability for a current exam appointment.

## Course Goal

This course helps learners plan, build, secure, integrate, deploy, monitor, and maintain Azure AI solutions. Learners will work through scenario-based labs covering Microsoft Foundry services, generative AI, agentic AI, computer vision, NLP, speech, translation, knowledge mining, document extraction, content understanding, responsible AI, and operational governance.

## Prerequisites

- Basic Azure knowledge.
- Basic programming awareness in Python or C#.
- Familiarity with REST APIs and SDK concepts.
- Basic understanding of AI workloads, prompts, and data security.
- Access to Microsoft Learn, Azure portal, Azure AI Foundry, or an instructor-provided Azure subscription.

## Learning Outcomes

By the end of the course, learners should be able to:

- Select appropriate Microsoft Foundry and Azure AI services for business requirements.
- Plan, create, deploy, monitor, secure, and manage Azure AI resources.
- Apply responsible AI principles, content safety, filters, blocklists, prompt shields, and harm detection.
- Build generative AI solutions with Microsoft Foundry and Azure OpenAI in Foundry Models.
- Implement prompt flow, RAG, prompt templates, evaluation, tracing, and feedback.
- Explain agentic AI and multi-agent workflow concepts.
- Implement computer vision, custom vision, video, NLP, speech, translation, language understanding, and question answering solutions.
- Implement Azure AI Search, knowledge mining, semantic/vector search, Document Intelligence, and Content Understanding patterns.

## Recommended Course Flow

### Day 1 - Planning, Governance, and Generative AI

1. Course briefing and AI-102 study guide overview.
2. Lab 01: Plan, Manage, Monitor, and Secure an Azure AI Solution.
3. Lab 02: Responsible AI, Content Safety, Governance.
4. Lab 03: Generative AI, Foundry, Azure OpenAI, Prompt Flow, RAG.
5. Review: responsible generative AI and operational controls.

### Day 2 - Agents, Vision, Language, and Speech

1. Lab 04: Agentic AI, Foundry Agent Service, Multi-Agent Concepts.
2. Lab 05: Computer Vision, Custom Vision, Video Insights.
3. Lab 06: NLP, Language, Speech, Translation.
4. Lab 07: Custom Language Models and Question Answering.
5. Review: workload-to-service selection.

### Day 3 - Knowledge Mining, Document AI, and Capstone

1. Lab 08: Azure AI Search, Knowledge Mining, Vector Search.
2. Lab 09: Document Intelligence and Content Understanding.
3. Lab 10: AI-102 Capstone and Course Review.
4. Cleanup, review plan, and course wrap-up.

## Lab Environment Setup

### Step 1 - Confirm Azure Access

1. Open https://portal.azure.com/.
2. Sign in with an instructor-provided account or personal Azure account.
3. Confirm access to a subscription and resource group.
4. If using a personal subscription, set a budget alert before creating resources.

### Step 2 - Create a Resource Group

```bash
az group create --name rg-ai102-lab --location southeastasia
```

### Step 3 - Open Azure AI Foundry

1. Open Azure AI Foundry.
2. Create or open a hub and project if your instructor provides access.
3. Record project name, region, model deployment, endpoint, and key governance settings.

### Step 4 - Create a Notes File

Create:

```text
ai102-lab-notes.md
```

Record:

```text
Subscription:
Resource group:
Foundry hub/project:
AI services resource:
Model deployment:
Search index:
Document model:
Key learning points:
```

## Cost and Safety Guidelines

- Use free or low-cost tiers where available.
- Delete unused model deployments and endpoints.
- Do not upload confidential data into training services.
- Do not expose keys in notebooks, source control, or screenshots.
- Prefer managed identity and role-based access where possible.
- Review content safety settings before testing generative AI.

## Lab Completion Standard

For each lab, learners should complete:

1. Scenario interpretation.
2. Service selection or implementation activity.
3. Validation checks.
4. Responsible AI or security note.
5. Cleanup review.
6. One course takeaway.

## Final Review Checklist

Before completing the course, confirm that you can:

- Select Azure AI services for generative AI, vision, language, speech, search, document, and agentic workloads.
- Plan and secure AI resources, endpoints, keys, authentication, monitoring, and cost controls.
- Explain content safety, filters, blocklists, prompt shields, and responsible AI governance.
- Explain prompt flow, RAG, vector search, model monitoring, tracing, and feedback.
- Explain custom vision, NLP, speech, question answering, AI Search, Document Intelligence, and Content Understanding patterns.
