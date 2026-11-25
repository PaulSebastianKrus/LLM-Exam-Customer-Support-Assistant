# AcmeFlow Customer Support Assistant

AcmeFlow Customer Support Assistant is an exam MVP that uses a local LLM and retrieval-augmented generation to draft grounded customer-support replies. AcmeFlow is fictional, and its Markdown knowledge base contains exact product limits, refund conditions, security procedures, and troubleshooting steps that a base model cannot reliably know.

The support agent enters a ticket, reviews the retrieved evidence, and receives a draft with source citations. The application never sends a message or changes customer data.

## Why RAG is meaningful

A general model can write a polite support reply, but it cannot know AcmeFlow-specific facts such as the 7-day annual-renewal refund window, 15-minute password-reset expiry, or 7-day workspace recovery period. RAG supplies those facts at answer time and exposes the retrieved evidence for human review.

The optional no-RAG comparison uses the same local model without product documentation. It helps demonstrate differences in project-specific accuracy, unsupported promises, and citations.

## Architecture

1. Markdown documents are split by headings and long sections are divided into overlapping chunks.
2. Ollama creates a local embedding for each chunk.
3. `scripts/build_index.py` normalises the embeddings and saves them with chunk metadata in `data/index.json`.
4. The app embeds a customer ticket and computes cosine similarity against the stored vectors.
5. Chunks must pass both an absolute similarity threshold and a maximum score gap from the best match. This reduces distracting evidence that is only weakly related.
6. The selected chunks, current date, timezone, and customer ticket are inserted into the 4T prompt.
7. A local Ollama chat model drafts the response and cites the supplied chunks.
8. A lightweight quality check flags claims that verification or another action was completed, and flags expiry conclusions based only on relative dates.
9. When a check fails, the same local model receives the failed draft and exact warning for one automatic correction pass. Any remaining warning stays visible for human review.

## Prerequisites

- Python 3.12
- Ollama running locally
- One Ollama chat model
- One Ollama embedding model

The example configuration uses `llama3.2:3b` for chat and `nomic-embed-text` for embeddings. You can change both in `.env` to models available on your machine.

## Installation

From this directory:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Install the models configured in `.env`, for example:

```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

Start Ollama if it is not already running:

```bash
ollama serve
```

## Build the RAG index

With the virtual environment active and Ollama running:

```bash
python scripts/build_index.py
```

Rebuild the index whenever the knowledge-base documents or embedding model change.

## Run the application

```bash
streamlit run app.py
```

Open the local URL printed by Streamlit. Enter a ticket, inspect the retrieved evidence, and generate the reply.

## Suggested demonstration ticket

Subject:

```text
Refund for yesterday's annual renewal
```

Message:

```text
Hi, my Team plan renewed yesterday for EUR 120. I meant to cancel it.
We have not used the workspace since the renewal. Can I receive a refund?
```

The grounded answer should retrieve the annual-renewal policy, mention the 7-day condition, avoid promising approval, and explain that Billing Operations must review the request.

Enable **Also generate a no-RAG comparison** in the sidebar to compare the grounded answer with a response generated without AcmeFlow documentation.

## 4T prompt strategy

The prompt in `src/prompts.py` explicitly defines:

- **Traits:** careful, evidence-bound, privacy-conscious, and honest about uncertainty
- **Task:** draft a reply using retrieved AcmeFlow evidence and add an internal note
- **Tone:** calm, empathetic, concise, and accessible
- **Target:** AcmeFlow customers and the support agents who review drafts

The prompt also prohibits invented policies, unsupported promises, secret collection, and claims that an action has already been completed.

Relative dates such as “Monday” are treated as ambiguous when they affect eligibility. The assistant must request an exact calendar date before claiming that a refund or recovery period has expired. Ticket details are treated as customer-provided rather than verified facts.

## Tests

```bash
pytest
```

The unit tests verify heading-aware document chunking, cosine-similarity ranking, relevance filtering, and high-risk draft warnings without requiring Ollama.

## Project structure

```text
app.py                    Streamlit interface and application flow
knowledge_base/           Fictional AcmeFlow source material
scripts/build_index.py    Local embedding and index creation
src/documents.py          Markdown chunking
src/ollama_client.py      Local Ollama API client
src/rag.py                Vector index and cosine search
src/prompts.py            4T prompt
src/quality.py            Deterministic human-review warnings
tests/                    Unit tests
PROJECT_SCOPE.md          Problem, users, value, scope, and demo cases
```

## Current limitation

Cosine similarity measures semantic closeness, not whether a passage fully answers a ticket. The thresholds reduce weak matches but cannot guarantee relevance. The local LLM can also misapply correctly retrieved facts, especially when dates are ambiguous. The prompt and deterministic warnings reduce this risk, while the support agent remains responsible for inspecting the evidence and reviewing every draft.
