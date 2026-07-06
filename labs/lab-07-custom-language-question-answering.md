# Lab 07 - Custom Language Models and Question Answering

## Objectives

- Design custom language understanding.
- Define intents, entities, and utterances.
- Plan custom question answering.
- Create a multilingual question answering strategy.

## Scenario

The support assistant must recognize customer intents and answer frequently asked questions from approved sources.

## Steps

### 1. Define Intents and Entities

Create a table:

| Intent | Example Utterance | Entities |
| --- | --- | --- |
| CheckOrderStatus | Where is order 12345? | order number |
| RequestRefund | I want a refund for my laptop | product |

### 2. Plan Training Data

Document:

- Number of example utterances.
- Balanced examples across intents.
- Entity labeling rules.
- Test set.
- Ambiguous utterances.

### 3. Plan Custom Question Answering

Record:

```text
Knowledge sources
Q&A pairs
Alternate phrasing
Chit-chat
Multi-turn prompts
Publishing target
Fallback answer
```

### 4. Multilingual Strategy

Explain whether to translate sources, create separate projects, or translate user input before answering.

### 5. Backup and Recovery

Document export, versioning, backup, and recovery of language projects.

## Validation

You should have intent/entity table, training plan, question answering plan, multilingual strategy, and backup notes.

## Checkpoint Questions

1. What is an intent?
2. What is an entity?
3. Why add alternate phrasing?
4. Why should language projects be backed up?

## Course Focus

Custom language solutions need well-designed examples, evaluation, publishing, and lifecycle management.
