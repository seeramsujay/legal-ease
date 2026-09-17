"""
Structural Contract Parser and Clause Segmenter.
Splits raw contract documents into discrete structural clauses, detecting numbered sections,
article headers, legal titles, and categorizing legal domains via high-speed regex engines.
"""

import re
from typing import List, Tuple, Optional, Pattern
from legal_ease.models import ClauseCategory


class RawClause:
    """
    Represents an unanalyzed, segmented contract provision.
    """
    def __init__(
        self,
        clause_id: int,
        title: str,
        text: str,
        category: ClauseCategory,
    ) -> None:
        self.clause_id = clause_id
        self.title = title or f"Section {clause_id}"
        self.text = text.strip() if text else ""
        self.category = category


# Canonical categorization keywords mapped to contract categories
CATEGORY_KEYWORDS = {
    ClauseCategory.INDEMNIFICATION: [
        "indemnif",
        "hold harmless",
        "defend and hold",
        "indemnity",
    ],
    ClauseCategory.LIMITATION_OF_LIABILITY: [
        "limitation of liability",
        "cap on liability",
        "consequential damages",
        "maximum liability",
        "indirect damages",
        "punitive damages",
    ],
    ClauseCategory.DISPUTE_RESOLUTION: [
        "dispute resolution",
        "arbitration",
        "class action waiver",
        "jury trial",
        "mediation",
        "venue",
        "jurisdiction",
    ],
    ClauseCategory.TERMINATION: [
        "termination",
        "term and termination",
        "cancellation",
        "convenience",
        "breach and cure",
        "survival",
    ],
    ClauseCategory.INTELLECTUAL_PROPERTY: [
        "intellectual property",
        "work for hire",
        "work made for hire",
        "ip rights",
        "ownership of deliverables",
        "pre-existing",
        "proprietary rights",
        "patent",
        "copyright",
    ],
    ClauseCategory.RESTRICTIVE_COVENANTS: [
        "non-compete",
        "non compete",
        "non-solicitation",
        "non solicitation",
        "exclusivity",
        "restrictive covenant",
    ],
    ClauseCategory.CONFIDENTIALITY: [
        "confidentiality",
        "confidential information",
        "non-disclosure",
        "trade secret",
        "proprietary information",
    ],
    ClauseCategory.PAYMENT_TERMS: [
        "payment",
        "compensation",
        "fees and expenses",
        "invoicing",
        "billing",
        "late fee",
        "net 30",
        "net 60",
        "net 90",
    ],
    ClauseCategory.WARRANTY_DISCLAIMER: [
        "warranty",
        "warranties",
        "as is",
        "disclaimer of warranties",
        "fitness for a particular purpose",
        "merchantability",
    ],
    ClauseCategory.GOVERNING_LAW: [
        "governing law",
        "applicable law",
        "choice of law",
        "jurisdiction",
    ],
}

# Pre-compile single-pass regex unions for each category for instant O(1) matching
_COMPILED_CATEGORY_MATCHERS: List[Tuple[ClauseCategory, Pattern[str]]] = [
    (
        cat,
        re.compile(
            r"(?:" + "|".join(re.escape(k) for k in keywords) + r")",
            re.IGNORECASE,
        ),
    )
    for cat, keywords in CATEGORY_KEYWORDS.items()
]

# Paragraph fallback splitting regex
_PARAGRAPH_SPLIT_PATTERN = re.compile(r"\n\s*\n+")


class ClauseSegmenter:
    """
    Parses unstructured contract text into structural clauses,
    detecting numbered sections, headings, and legal categories.
    """

    HEADER_PATTERNS: List[Pattern[str]] = [
        # E.g. "Section 1. Indemnification" or "Article 2: Limitation of Liability"
        re.compile(
            r"^(?:Section|Article|Clause)\s+([0-9IVXLCDM\.]+)\s*[\.\:\-]?\s*([^\n\r]+)",
            re.IGNORECASE | re.MULTILINE,
        ),
        # E.g. "1. INDEMNIFICATION" or "1.1 Limitation of Liability" or "1. SERVICES AND COMPENSATION"
        re.compile(
            r"^([0-9]{1,2}(?:\.[0-9]{1,2})*)\.?\s+([A-Za-z0-9\s\,\/\-\(\)]{3,80})$",
            re.MULTILINE,
        ),
        # E.g. "INDEMNIFICATION AND HOLD HARMLESS:"
        re.compile(
            r"^([A-Z\s]{4,60})\s*[\:\-]\s*$",
            re.MULTILINE,
        ),
    ]

    def segment(self, text: Optional[str]) -> List[RawClause]:
        """
        Segment a document into titled raw clauses.
        Falls back to paragraph chunking if formal headers are absent.
        Guarantees zero null reference crashes on empty or None input.
        """
        safe_text = str(text) if text is not None else ""
        if not safe_text.strip():
            return []

        # Find all candidate header split points
        split_points: List[Tuple[int, str]] = []

        for pattern in self.HEADER_PATTERNS:
            for match in pattern.finditer(safe_text):
                start = match.start()
                groups = match.groups()
                if len(groups) == 2:
                    sec_num, sec_title = groups
                    full_title = f"{sec_num.strip()} {sec_title.strip()}"
                else:
                    full_title = groups[0].strip()
                split_points.append((start, full_title))

        # Sort and deduplicate split points by character index
        split_points.sort(key=lambda x: x[0])
        unique_splits: List[Tuple[int, str]] = []
        last_idx = -9999
        for idx, title in split_points:
            # Enforce minimum distance of 35 characters between successive clause headings
            if idx > last_idx + 35:
                unique_splits.append((idx, title))
                last_idx = idx

        # If formal section headers are detected
        if len(unique_splits) >= 2:
            clauses: List[RawClause] = []
            
            # Check if there is meaningful preamble before the first header (>100 chars & >15 words)
            first_header_idx = unique_splits[0][0]
            preamble_candidate = safe_text[:first_header_idx].strip()
            if len(preamble_candidate) > 100 and len(preamble_candidate.split()) > 15:
                clauses.append(
                    RawClause(
                        clause_id=1,
                        title="Preamble & Recitals",
                        text=preamble_candidate,
                        category=ClauseCategory.GENERAL_BOILERPLATE,
                    )
                )

            for i in range(len(unique_splits)):
                curr_idx, title = unique_splits[i]
                next_idx = (
                    unique_splits[i + 1][0]
                    if i + 1 < len(unique_splits)
                    else len(safe_text)
                )
                clause_text = safe_text[curr_idx:next_idx].strip()
                cat = self._classify_category(title, clause_text)
                clauses.append(
                    RawClause(
                        clause_id=len(clauses) + 1,
                        title=title,
                        text=clause_text,
                        category=cat,
                    )
                )
            return clauses

        # Fallback: Split by clean paragraph breaks
        paragraphs = [p.strip() for p in _PARAGRAPH_SPLIT_PATTERN.split(safe_text) if p.strip()]
        clauses = []
        for i, para in enumerate(paragraphs, 1):
            first_line = para.split("\n")[0][:60].strip()
            cat = self._classify_category(first_line, para)
            clauses.append(
                RawClause(
                    clause_id=i,
                    title=f"Section {i}: {first_line}",
                    text=para,
                    category=cat,
                )
            )
        return clauses

    def _classify_category(self, title: Optional[str], text: Optional[str]) -> ClauseCategory:
        """
        Categorize a clause based on heading and textual semantics using pre-compiled regex unions.
        Evaluates the title and the first 400 characters of the clause text.
        """
        safe_title = str(title).lower() if title else ""
        safe_text = str(text)[:400].lower() if text else ""
        search_corpus = f"{safe_title} {safe_text}"

        for cat, compiled_pat in _COMPILED_CATEGORY_MATCHERS:
            if compiled_pat.search(search_corpus):
                return cat

        return ClauseCategory.GENERAL_BOILERPLATE
