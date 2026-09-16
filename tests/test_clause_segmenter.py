"""
Unit tests for the structural contract parser and clause segmenter.
"""

from legal_ease.clause_segmenter import ClauseSegmenter
from legal_ease.models import ClauseCategory


SAMPLE_NUMBERED_CONTRACT = """
1. INDEMNIFICATION AND HOLD HARMLESS
Contractor agrees to indemnify Company from all claims.

2. LIMITATION OF LIABILITY
Neither party shall be liable for indirect damages.

3. TERM AND TERMINATION
Either party may terminate upon thirty days notice.
"""


def test_numbered_clause_segmentation():
    segmenter = ClauseSegmenter()
    clauses = segmenter.segment(SAMPLE_NUMBERED_CONTRACT)
    assert len(clauses) == 3
    assert "INDEMNIFICATION" in clauses[0].title
    assert clauses[0].category == ClauseCategory.INDEMNIFICATION
    assert clauses[1].category == ClauseCategory.LIMITATION_OF_LIABILITY
    assert clauses[2].category == ClauseCategory.TERMINATION


def test_article_format_segmentation():
    text = """
Article I: Dispute Resolution
All claims will be settled through arbitration.

Article II: Intellectual Property
Client owns all deliverables upon creation.
    """
    segmenter = ClauseSegmenter()
    clauses = segmenter.segment(text)
    assert len(clauses) >= 2
    assert any(c.category == ClauseCategory.DISPUTE_RESOLUTION for c in clauses)
    assert any(c.category == ClauseCategory.INTELLECTUAL_PROPERTY for c in clauses)


def test_empty_contract_segmentation():
    segmenter = ClauseSegmenter()
    assert segmenter.segment("") == []
    assert segmenter.segment("   ") == []
