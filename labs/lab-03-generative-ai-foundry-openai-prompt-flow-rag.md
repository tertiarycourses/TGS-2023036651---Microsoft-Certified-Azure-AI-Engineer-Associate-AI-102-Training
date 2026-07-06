# Lab 03 - Generative AI, Foundry, Azure OpenAI, Prompt Flow, RAG

## Objectives

- Plan a generative AI solution with Microsoft Foundry.
- Select and deploy a model conceptually.
- Design prompt templates and prompt flow.
- Implement a RAG pattern conceptually.
- Evaluate model and flow outputs.

## Scenario

The company wants a grounded assistant that answers questions from internal support articles and generates draft replies.

## Steps

### 1. Select a Model

Record:

```text
Model name
Use case fit
Context window
Latency
Cost
Safety settings
Deployment option
```

### 2. Design Prompt Templates

Create templates for:

1. Direct answer.
2. Answer with sources.
3. Escalation when context is missing.

### 3. Plan Prompt Flow

Draw:

```text
User question -> classify intent -> retrieve context -> prompt template -> model -> safety check -> response
```

### 4. Design RAG

Document:

- Source documents.
- Cleaning.
- Chunking.
- Embeddings.
- Vector store.
- Retrieval filters.
- Citation format.
- Evaluation method.

### 5. Evaluate Outputs

Score:

| Criterion | Score 1-5 |
| --- | --- |
| Correctness |  |
| Grounding |  |
| Helpfulness |  |
| Safety |  |
| Conciseness |  |

## Validation

You should have model selection notes, prompt templates, prompt flow diagram, RAG design, and evaluation table.

## Checkpoint Questions

1. What is RAG?
2. Why are prompt templates useful?
3. What does tracing help debug?
4. How can feedback improve a generative AI solution?

## Course Focus

Generative AI solutions need grounded data, evaluation, safety settings, monitoring, and feedback loops.
