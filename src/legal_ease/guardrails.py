"""
Legal disclaimers, input sanitization, and guardrail enforcement.
"""

import re
from typing import Dict, Any

STANDARD_LEGAL_DISCLAIMER = (
    "LEGAL DISCLAIMER: Legal-Ease is an AI-powered document literacy and analysis tool "
    "developed for educational and informational purposes only. It does not provide formal "
    "legal advice, legal representation, or establish an attorney-client relationship. "
    "Contract interpretation varies by jurisdiction and specific factual context. "
    "Always consult a licensed attorney in your relevant jurisdiction before signing or "
    "modifying legally binding contracts."
)

ATTORNEY_PREP_NOTE = (
    "NOTICE FOR COUNSEL: This briefing is an automated triage generated to streamline "
    "professional legal review. Clauses and issues flagged herein should be verified "
    "by licensed legal counsel against applicable governing statutes."
)


def get_standard_disclaimer() -> str:
    """Return the formal legal disclaimer."""
    return STANDARD_LEGAL_DISCLAIMER


def get_attorney_prep_note() -> str:
    """Return the attorney prep notice."""
    return ATTORNEY_PREP_NOTE


def sanitize_input_text(text: str) -> str:
    """
    Sanitize input text against dangerous script injections and null bytes.
    """
    if not text:
        return ""
    # Strip null bytes
    cleaned = text.replace("\x00", "")
    # Normalize excessive carriage returns
    cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")
    # Limit max contract length to 500,000 characters (~100 pages) for safe memory usage
    if len(cleaned) > 500000:
        cleaned = cleaned[:500000]
    return cleaned.strip()


def validate_chat_query(query: str) -> Dict[str, Any]:
    """
    Check chat query for prompt injections or adversarial attempts to bypass disclaimers.
    """
    cleaned_query = query.strip()
    if not cleaned_query:
        return {"valid": False, "reason": "Query cannot be empty."}

    # Detect blatant system prompt overrides
    injection_patterns = [
        r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
        r"disregard\s+(all\s+)?guidelines",
        r"you\s+are\s+now\s+a\s+licensed\s+attorney",
        r"provide\s+binding\s+legal\s+advice",
    ]
    for pattern in injection_patterns:
        if re.search(pattern, cleaned_query, re.IGNORECASE):
            return {
                "valid": False,
                "reason": (
                    "Legal-Ease cannot disregard safety guidelines or act as formal legal counsel. "
                    "Please ask specific informational questions about your contract clauses."
                ),
            }

    return {"valid": True, "sanitized_query": cleaned_query}
