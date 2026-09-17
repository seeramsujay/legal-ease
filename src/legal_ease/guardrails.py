"""
Legal Disclaimers, Input Sanitization, and Security Guardrails.
Enforces non-advisory legal disclosures, strips potential script injections,
and protects conversational endpoints from prompt injection attacks.
"""

import re
from typing import Dict, Any, Optional

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

# Pre-compiled high-speed regex union for prompt injection and jailbreak attempts.
# Matching via a single compiled DFA pattern avoids multiple linear searches.
_INJECTION_PATTERN = re.compile(
    r"(?:"
    r"ignore\s+(?:all\s+)?(?:previous|prior)\s+instructions|"
    r"disregard\s+(?:all\s+)?guidelines|"
    r"you\s+are\s+now\s+a\s+licensed\s+attorney|"
    r"provide\s+binding\s+legal\s+advice|"
    r"bypass\s+(?:all\s+)?safety\s+filters"
    r")",
    re.IGNORECASE,
)


def get_standard_disclaimer() -> str:
    """Return the mandatory non-advisory legal disclaimer string."""
    return STANDARD_LEGAL_DISCLAIMER


def get_attorney_prep_note() -> str:
    """Return the professional triage note for reviewing legal counsel."""
    return ATTORNEY_PREP_NOTE


def sanitize_input_text(text: Optional[str]) -> str:
    """
    Defensively sanitizes input contract text.
    - Strips dangerous null bytes (\x00).
    - Normalizes Windows and classic Mac line endings (\r\n -> \n, \r -> \n).
    - Caps excessive length to 500,000 characters (~100 pages) to guard memory.
    - Prevents NoneType errors by converting None or non-string inputs safely.
    """
    if not text:
        return ""
    if not isinstance(text, str):
        text = str(text)

    # Strip null bytes that can cause C-library string termination errors
    cleaned = text.replace("\x00", "")
    
    # Normalize CRLF and CR to LF
    cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")
    
    # Enforce safe upper bound on input length (approx 100 pages of text)
    if len(cleaned) > 500000:
        cleaned = cleaned[:500000]
        
    return cleaned.strip()


def validate_chat_query(query: Optional[str]) -> Dict[str, Any]:
    """
    Validates user chat queries against adversarial prompt injection attempts.
    Returns a dictionary with 'valid': bool, and either 'sanitized_query' or 'reason'.
    """
    if not query:
        return {
            "valid": False,
            "reason": "Query cannot be empty. Please ask a specific question about your contract.",
        }
        
    cleaned_query = str(query).strip()
    if not cleaned_query:
        return {
            "valid": False,
            "reason": "Query cannot be empty. Please ask a specific question about your contract.",
        }

    # Evaluate against pre-compiled injection union
    if _INJECTION_PATTERN.search(cleaned_query):
        return {
            "valid": False,
            "reason": (
                "Legal-Ease cannot disregard safety guidelines or act as formal legal counsel. "
                "Please ask specific informational questions about your contract clauses."
            ),
        }

    return {"valid": True, "sanitized_query": cleaned_query}
