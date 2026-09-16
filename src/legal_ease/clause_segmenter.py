"""
Structural contract parser and clause segmenter.
Splits contracts into discrete articles and clauses with contextual categorization.
"""

import re
from typing import List, Tuple
from legal_ease.models import ClauseCategory


class RawClause:
    def __init__(self, clause_id: int, title: str, text: str, category: ClauseCategory):
        self.clause_id = clause_id
        self.title = title
        self.text = text.strip()
        self.category = category


class ClauseSegmenter:
    """
    Parses unstructured contract text into structural clauses,
    detecting numbered sections, headings, and legal categories.
    """

    HEADER_PATTERNS = [
        # E.g. "Section 1. Indemnification" or "Article 2: Limitation of Liability"
        re.compile(
            r"^(?:Section|Article|Clause)\s+([0-9IVXLCDM\.]+)\s*[\.\:\-]?\s*([^\n\r]+)",
            re.IGNORECASE | re.MULTILINE,
        ),
        # E.g. "1. INDEMNIFICATION" or "1.1 Limitation of Liability" or "1. SERVICES AND COMPENSATION"
        re.compile(
            r"^([0-9]{1,2}(?:\.[0-9]{1,2})*)\.?\s+([A-Za-z0-9\s,\/\-\(\)]{3,80})$",
            re.MULTILINE,
        ),
        # E.g. "INDEMNIFICATION AND HOLD HARMLESS:"
        re.compile(
            r"^([A-Z\s]{4,60})\s*[\:\-]\s*$",
            re.MULTILINE,
        ),
    ]

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

    def segment(self, text: str) -> List[RawClause]:
        """
        Segment a document into titled raw clauses.
        Falls back to paragraph chunking if formal headers are absent.
        """
        if not text.strip():
            return []

        # Find all candidate headers
        split_points: List[Tuple[int, str]] = []

        for pattern in self.HEADER_PATTERNS:
            for match in pattern.finditer(text):
                start = match.start()
                groups = match.groups()
                if len(groups) == 2:
                    sec_num, sec_title = groups
                    full_title = f"{sec_num.strip()} {sec_title.strip()}"
                else:
                    full_title = groups[0].strip()
                split_points.append((start, full_title))

        # Sort and deduplicate split points
        split_points.sort(key=lambda x: x[0])
        unique_splits: List[Tuple[int, str]] = []
        last_idx = -9999
        for idx, title in split_points:
            if idx > last_idx + 35:
                unique_splits.append((idx, title))
                last_idx = idx

        if len(unique_splits) >= 2:
            clauses: List[RawClause] = []
            # Check if there is meaningful preamble before the first header (>100 characters and >10 words)
            first_header_idx = unique_splits[0][0]
            preamble_candidate = text[:first_header_idx].strip()
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
                    else len(text)
                )
                clause_text = text[curr_idx:next_idx].strip()
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

        # Fallback: Split by paragraphs
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", text) if p.strip()]
        clauses: List[RawClause] = []
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

    def _classify_category(self, title: str, text: str) -> ClauseCategory:
        """Categorize a clause based on heading and textual semantics."""
        search_corpus = f"{title.lower()} {text[:400].lower()}"

        for cat, keywords in self.CATEGORY_KEYWORDS.items():
            for kw in keywords:
                if kw in search_corpus:
                    return cat

        return ClauseCategory.GENERAL_BOILERPLATE
