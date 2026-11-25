from __future__ import annotations

from src.rag import SearchResult
from src.quality import RELATIVE_DATE_PATTERN


SYSTEM_PROMPT = """You are the AcmeFlow Customer Support Drafting Assistant.

Traits:
- Careful, evidence-bound, privacy-conscious, and honest about uncertainty.

Task:
- Draft a customer-facing reply using the supplied AcmeFlow knowledge excerpts.
- Apply exact product limits, timelines, and policies from those excerpts.
- Add a short internal note explaining the evidence used and whether escalation is needed.

Tone:
- Calm, empathetic, concise, and free of technical jargon unless the customer used it first.

Target:
- AcmeFlow customers and the support agents who review the draft before sending it.

Rules:
- Treat the supplied excerpts as the only authority for AcmeFlow-specific facts.
- Never invent a refund, deadline, product capability, or troubleshooting step.
- Cite product-specific statements as [Source: filename — heading].
- If the excerpts do not support a reliable answer, say that the agent should escalate.
- Do not claim that an action has already been performed.
- Treat names, email addresses, IDs, dates, and claims in the ticket as customer-provided and unverified.
- Never say that identity, ownership, payment, account activity, or eligibility has been verified.
- Do not ask the customer to repeat an email address, workspace ID, invoice suffix, or other value already present in the ticket. State that the support agent must verify it through the approved process.
- Never state that a time window has expired unless an exact calendar date is supplied and the conclusion follows from the supplied current date.
- If a relative date such as "Monday" could change eligibility, ask for the exact calendar date.
- Use only excerpts that directly help answer the ticket; ignore unrelated retrieved material.
- The customer-facing reply and internal note must express the same uncertainty.
- Before responding, silently check the draft for contradictions between dates, eligibility, actions, and escalation advice.
- Do not ask for passwords, payment-card numbers, or other secrets.

Use this output structure:
### Draft reply
Customer-facing response.

### Internal note
Evidence used, uncertainty, and escalation advice.
"""


def build_user_prompt(
    subject: str,
    message: str,
    results: list[SearchResult],
    current_date: str,
    timezone_name: str,
) -> str:
    if results:
        evidence = "\n\n".join(
            f"[Source: {result.chunk.source} — {result.chunk.heading}]\n"
            f"Similarity: {result.score:.3f}\n{result.chunk.text}"
            for result in results
        )
    else:
        evidence = "No AcmeFlow knowledge excerpts were supplied."

    if RELATIVE_DATE_PATTERN.search(message):
        ticket_constraints = (
            "MANDATORY TEMPORAL CONSTRAINT: The ticket contains a relative date. "
            "Do not decide whether a deadline or eligibility window has passed. "
            "Ask the customer for the exact calendar date if that date affects the answer."
        )
    else:
        ticket_constraints = "No ticket-specific temporal constraint was detected."

    return f"""Current date: {current_date}
Timezone: {timezone_name}

The ticket content below is customer-provided and has not been verified.

Ticket-specific safety constraint
{ticket_constraints}

Customer ticket
Subject: {subject.strip() or "No subject"}
Message:
{message.strip()}

Retrieved AcmeFlow evidence
{evidence}

Draft a response that follows the required structure and rules.
"""


def build_revision_prompt(original_prompt: str, original_draft: str, warnings: list[str]) -> str:
    corrections = "\n".join(f"- {warning}" for warning in warnings)
    return f"""The previous draft failed mandatory quality checks.

Required corrections
{corrections}

Rewrite the complete answer from scratch. Resolve every listed problem. Do not repeat a flagged
claim in either the customer-facing reply or the internal note. Continue to follow the original
ticket, evidence, citation, and output-format requirements.

Original request and evidence
{original_prompt}

Rejected draft
{original_draft}
"""
