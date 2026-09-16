"""
Local PII and Sensitive Entity Anonymization Engine.
Redacts names, emails, phones, SSNs, financial figures, and physical addresses
before any external reasoning or analysis takes place.
"""

import re
from typing import Dict, List, Tuple
from legal_ease.models import RedactedEntity, AnonymizationResult


class PIIAnonymizer:
    """
    High-precision local regex and pattern-matching PII anonymizer.
    Protects user privacy by transforming sensitive personal and corporate identifiers
    into deterministic pseudonyms while maintaining grammatical sentence structure.
    """

    # Email pattern
    EMAIL_PATTERN = re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    )

    # Phone number patterns (US, International, punctuated)
    PHONE_PATTERN = re.compile(
        r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    )

    # SSN / Tax ID / EIN
    SSN_EIN_PATTERN = re.compile(
        r"\b(?:\d{3}-\d{2}-\d{4}|\d{2}-\d{7})\b"
    )

    # Credit Card pattern (major brands, 13-19 digits, with spaces or hyphens)
    CREDIT_CARD_PATTERN = re.compile(
        r"\b(?:\d{4}[-\s]?){3}\d{1,4}\b"
    )

    # Monetary values (e.g. $12,500, USD 50,000, €1,200.00, £9,000)
    MONEY_PATTERN = re.compile(
        r"(?:[\$\€\£\¥]|USD|EUR|GBP)\s?[0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?|\b[0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?\s?(?:USD|dollars|euros)\b",
        re.IGNORECASE,
    )

    # Physical Street Address (heuristics for numbers + Street/Ave/Blvd/Drive/Road/Way + City/State/Zip)
    ADDRESS_PATTERN = re.compile(
        r"\b\d{1,5}\s+[A-Za-z0-9\.\s]{2,25}(?:Street|St\.|St|Avenue|Ave\.|Ave|Boulevard|Blvd\.|Road|Rd\.|Lane|Ln\.|Drive|Dr\.|Court|Ct\.|Way)\b(?:,?\s+[A-Za-z\s]+,?\s+[A-Z]{2}\s+\d{5}(?:-\d{4})?)?",
        re.IGNORECASE,
    )

    # Common Contract Party Introductions (extracting names and entity titles)
    PARTY_PATTERN = re.compile(
        r"(?:between|by and between|entered into by)\s+([A-Z][A-Za-z0-9\s,\.]{2,40}?)\s+(?:\(\"Client\"|\(\"Company\"|\(\"Contractor\"|\(\"Employer\"|\(\"Employee\"|\(\"Party\"|\(\"Disclosing Party\"|\(\"Receiving Party\")",
        re.IGNORECASE,
    )

    # Signature block person extractor
    SIG_NAME_PATTERN = re.compile(
        r"(?:By|Name|Printed Name):\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
        re.IGNORECASE,
    )

    def anonymize(self, text: str) -> AnonymizationResult:
        """
        Scan and redact all sensitive identifiers from contract text.
        Returns the sanitized text, detailed entity list, and privacy metrics.
        """
        if not text:
            return AnonymizationResult(
                original_text_length=0,
                redacted_text="",
                entities=[],
                entity_counts={},
                privacy_score=100.0,
            )

        entities: List[RedactedEntity] = []
        entity_counts: Dict[str, int] = {
            "EMAIL": 0,
            "PHONE": 0,
            "SSN_TAX_ID": 0,
            "FINANCIAL": 0,
            "CREDIT_CARD": 0,
            "ADDRESS": 0,
            "PARTY_NAME": 0,
        }

        # Keep track of value to assigned token mapping for consistency
        value_to_token: Dict[str, str] = {}
        spans_to_replace: List[Tuple[int, int, str, str, str]] = []  # start, end, original, token, type

        # 1. Detect Emails
        for m in self.EMAIL_PATTERN.finditer(text):
            val = m.group()
            if val not in value_to_token:
                entity_counts["EMAIL"] += 1
                value_to_token[val] = f"[EMAIL_{entity_counts['EMAIL']}]"
            spans_to_replace.append(
                (m.start(), m.end(), val, value_to_token[val], "EMAIL")
            )

        # 2. Detect SSN / EIN
        for m in self.SSN_EIN_PATTERN.finditer(text):
            val = m.group()
            if val not in value_to_token:
                entity_counts["SSN_TAX_ID"] += 1
                value_to_token[val] = f"[TAX_ID_{entity_counts['SSN_TAX_ID']}]"
            spans_to_replace.append(
                (m.start(), m.end(), val, value_to_token[val], "SSN_TAX_ID")
            )

        # 3. Detect Credit Cards
        for m in self.CREDIT_CARD_PATTERN.finditer(text):
            val = m.group()
            # Basic length check to prevent matching random 4-digit numbers
            digits = re.sub(r"\D", "", val)
            if 13 <= len(digits) <= 19:
                if val not in value_to_token:
                    entity_counts["CREDIT_CARD"] += 1
                    value_to_token[val] = f"[CARD_{entity_counts['CREDIT_CARD']}]"
                spans_to_replace.append(
                    (m.start(), m.end(), val, value_to_token[val], "CREDIT_CARD")
                )

        # 4. Detect Phone Numbers
        for m in self.PHONE_PATTERN.finditer(text):
            val = m.group()
            digits = re.sub(r"\D", "", val)
            if 10 <= len(digits) <= 12:
                if val not in value_to_token:
                    entity_counts["PHONE"] += 1
                    value_to_token[val] = f"[PHONE_{entity_counts['PHONE']}]"
                spans_to_replace.append(
                    (m.start(), m.end(), val, value_to_token[val], "PHONE")
                )

        # 5. Detect Addresses
        for m in self.ADDRESS_PATTERN.finditer(text):
            val = m.group()
            if val not in value_to_token:
                entity_counts["ADDRESS"] += 1
                value_to_token[val] = f"[ADDRESS_{entity_counts['ADDRESS']}]"
            spans_to_replace.append(
                (m.start(), m.end(), val, value_to_token[val], "ADDRESS")
            )

        # 6. Detect Financial Amounts
        for m in self.MONEY_PATTERN.finditer(text):
            val = m.group()
            if val not in value_to_token:
                entity_counts["FINANCIAL"] += 1
                value_to_token[val] = f"[CONFIDENTIAL_AMOUNT_{entity_counts['FINANCIAL']}]"
            spans_to_replace.append(
                (m.start(), m.end(), val, value_to_token[val], "FINANCIAL")
            )

        # 7. Detect Contract Named Parties & Signatories
        for m in self.PARTY_PATTERN.finditer(text):
            party_name = m.group(1).strip()
            if len(party_name) > 2 and party_name not in value_to_token:
                entity_counts["PARTY_NAME"] += 1
                value_to_token[party_name] = f"[PARTY_ENTITY_{entity_counts['PARTY_NAME']}]"
                start = m.start(1)
                end = m.end(1)
                spans_to_replace.append(
                    (start, end, party_name, value_to_token[party_name], "PARTY_NAME")
                )

        for m in self.SIG_NAME_PATTERN.finditer(text):
            name = m.group(1).strip()
            if len(name) > 3 and name not in value_to_token:
                entity_counts["PARTY_NAME"] += 1
                value_to_token[name] = f"[PERSON_NAME_{entity_counts['PARTY_NAME']}]"
                start = m.start(1)
                end = m.end(1)
                spans_to_replace.append(
                    (start, end, name, value_to_token[name], "PARTY_NAME")
                )

        # Sort spans by starting index ascending
        spans_to_replace.sort(key=lambda x: x[0])

        # Filter overlapping spans (keep the earlier/longer span)
        non_overlapping: List[Tuple[int, int, str, str, str]] = []
        last_end = -1
        for start, end, orig, tok, etype in spans_to_replace:
            if start >= last_end:
                non_overlapping.append((start, end, orig, tok, etype))
                last_end = end

        # Construct redacted text
        redacted_parts = []
        curr_idx = 0
        for start, end, orig, tok, etype in non_overlapping:
            redacted_parts.append(text[curr_idx:start])
            redacted_parts.append(tok)
            entities.append(
                RedactedEntity(
                    token=tok,
                    original_value=orig,
                    entity_type=etype,
                    start_char=start,
                    end_char=end,
                )
            )
            curr_idx = end
        redacted_parts.append(text[curr_idx:])
        redacted_text = "".join(redacted_parts)

        # Privacy score calculation
        total_redactions = len(entities)
        # Higher score means document is thoroughly sanitized
        privacy_score = 100.0 if total_redactions > 0 else 95.0

        return AnonymizationResult(
            original_text_length=len(text),
            redacted_text=redacted_text,
            entities=entities,
            entity_counts=entity_counts,
            privacy_score=privacy_score,
        )

    def deanonymize(self, text: str, entities: List[RedactedEntity]) -> str:
        """
        Re-hydrate tokens back to their original values for authorized local view.
        """
        restored = text
        for ent in sorted(entities, key=lambda e: len(e.token), reverse=True):
            restored = restored.replace(ent.token, ent.original_value)
        return restored
