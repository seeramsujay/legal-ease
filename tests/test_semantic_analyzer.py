"""
Unit tests for the Semantic Vector & Obfuscation Analysis Engine.
"""

import pytest
from legal_ease.semantic_analyzer import get_semantic_model, SemanticArchetype
from legal_ease.clause_segmenter import RawClause
from legal_ease.models import ClauseCategory
from legal_ease.risk_analyzer import RiskAnalyzer


def test_semantic_model_archetype_similarity():
    model = get_semantic_model()

    # Plain text mimicking unilateral indemnity without the word 'indemnify'
    clause_text = (
        "Contractor agrees to hold harmless and defend Company from any and all "
        "liabilities, losses, damages, proceedings, and attorney legal costs arising out of engagement."
    )
    insight = model.evaluate_semantics(clause_text, "Defense Obligations")

    assert insight.top_archetype == SemanticArchetype.UNILATERAL_INDEMNITY
    assert insight.top_archetype_similarity > 0.35
    assert insight.is_twisted is True
    assert "Euphemistic Indemnity Shield" in insight.detected_euphemisms


def test_twisted_language_lowers_local_confidence():
    analyzer = RiskAnalyzer()

    # Highly disguised non-compete using euphemistic language
    sneaky_clause = RawClause(
        clause_id=1,
        title="Post-Engagement Conduct",
        category=ClauseCategory.GENERAL_BOILERPLATE,
        text=(
            "Recipient covenants to abstain from rendering any guidance, advice, or participation "
            "in any enterprise operating across any commercial domain or territory worldwide in perpetuity, "
            "at Company's sole unreviewable discretion without necessity of prior notice."
        ),
    )

    eval_res = analyzer.evaluate_clause(sneaky_clause)

    # Should detect twisted euphemisms
    assert eval_res.is_twisted is True
    assert eval_res.obfuscation_score > 0.40
    # Confidence should drop into the escalation range (< 0.75)
    assert eval_res.confidence < 0.75
    assert any("Twisted / Euphemistic Drafting Trap" in t for t in eval_res.traps)


def test_benign_clause_maintains_high_confidence():
    analyzer = RiskAnalyzer()

    benign_clause = RawClause(
        clause_id=2,
        title="Notices",
        category=ClauseCategory.GENERAL_BOILERPLATE,
        text="All notices under this Agreement shall be in writing and deemed given upon confirmed email receipt.",
    )

    eval_res = analyzer.evaluate_clause(benign_clause)
    assert eval_res.is_twisted is False
    assert eval_res.confidence >= 0.85
    assert eval_res.risk_score < 30
