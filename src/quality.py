from __future__ import annotations

import re


COMPLETED_ACTION_PATTERNS = {
    r"\bwe (?:have|'ve) verified\b": "The draft claims verification was completed.",
    r"\bwe (?:have|'ve) confirmed\b": "The draft claims confirmation was completed.",
    r"\bwe (?:have|'ve) restored\b": "The draft claims restoration was completed.",
    r"\bwe (?:have|'ve) cancelled\b": "The draft claims cancellation was completed.",
    r"\brefund (?:has been|was) approved\b": "The draft claims a refund was approved.",
    r"\bwe (?:have|'ve) escalated\b": "The draft claims escalation was completed.",
}

RELATIVE_DATE_PATTERN = re.compile(
    r"\b(today|yesterday|tomorrow|monday|tuesday|wednesday|thursday|friday|saturday|sunday|last week)\b",
    re.IGNORECASE,
)
TEMPORAL_CONCLUSION_PATTERN = re.compile(
    r"\b(already expired|has expired|window expired|period expired|too late|has not yet passed|is still within|remains within)\b",
    re.IGNORECASE,
)


def review_draft(ticket_text: str, draft: str) -> list[str]:
    """Flag a few high-risk claims for the human support agent."""
    warnings: list[str] = []
    for pattern, warning in COMPLETED_ACTION_PATTERNS.items():
        if re.search(pattern, draft, re.IGNORECASE):
            warnings.append(warning)

    if RELATIVE_DATE_PATTERN.search(ticket_text) and TEMPORAL_CONCLUSION_PATTERN.search(draft):
        warnings.append(
            "The ticket uses a relative date, but the draft concludes whether a time window has "
            "or has not passed. Request an exact calendar date before making that decision."
        )
    return warnings
