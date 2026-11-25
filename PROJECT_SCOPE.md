# AcmeFlow Customer Support Assistant — MVP scope

## Problem

Support agents must search across product documentation and policies while responding to customers. This causes slow replies and creates a risk of giving outdated or unsupported information.

## Intended users

The primary user is a first-line support agent for the fictional AcmeFlow project-management product. The customer receives the final response only after the agent reviews it.

## Value

The application retrieves the most relevant internal documentation and drafts a concise reply grounded in those sources. A visible evidence panel lets the agent verify the answer before using it. Local processing keeps customer tickets and internal policies on the user's computer.

## Core MVP flow

1. The agent enters a ticket subject and customer message.
2. The app embeds the ticket with a local Ollama embedding model.
3. Cosine similarity selects the most relevant knowledge chunks.
4. The selected chunks and ticket enter a 4T prompt.
5. A local Ollama chat model drafts a customer reply and internal note.
6. The interface displays the retrieved chunks, scores, citations, and draft.

## In scope

- A local Streamlit interface
- A fictional but internally consistent product knowledge base
- Heading-aware chunking
- Local embeddings and cosine-similarity retrieval
- Similarity threshold and escalation behaviour
- Relative-score filtering to remove weak retrieved chunks
- Local LLM answer generation
- Source citations
- Current-date context and human-review warnings for risky claims
- Optional no-RAG comparison for the exam demonstration

## Outside the MVP

- Sending messages to customers
- Connecting to a real support platform
- Authentication and multi-user access
- Modifying customer accounts or billing
- Production monitoring
- Automatically learning from previous tickets
- Fine-tuning an LLM

## Demonstration cases

1. Annual Team renewal charged yesterday: retrieve the 7-day renewal policy and usage condition.
2. Workspace deleted 4 days ago: retrieve the 7-day restoration procedure and Data Operations escalation.
3. Fourth Starter member cannot accept an invitation: retrieve the 3-member limit and guest alternative.
4. An unrelated question with a high similarity threshold: show insufficient evidence and escalation.
