# AcmeFlow support process

## Purpose of a draft

The assistant creates a draft for a human support agent. The agent remains responsible for checking the retrieved evidence, editing the response, and deciding whether to send it. The assistant never sends messages or changes customer accounts.

## Required reply qualities

A customer reply should acknowledge the problem, answer the question directly, provide the smallest useful set of next steps, and avoid internal queue names. Exact limits, prices, and deadlines require a source citation in the assistant's internal note.

Support should not blame the customer. Avoid phrases such as “you failed to” and prefer neutral descriptions such as “the invitation has expired.”

## Escalation rules

Escalate to Billing Operations for refund decisions, duplicate charges, or unexplained billing errors. Escalate to Data Operations for workspace restoration and exports stuck for more than 24 hours. Escalate to Security for unknown administrators, unexpected exports, or changed billing owners.

When the knowledge base does not contain enough information, the draft should say that the support agent will investigate further. It must not fill the gap with a plausible-sounding policy.

## Sensitive information

Support may request a workspace ID, invoice ID suffix, charge date, and account email. Support must never request passwords, full card numbers, bank credentials, authenticator codes, recovery codes, or session tokens.
