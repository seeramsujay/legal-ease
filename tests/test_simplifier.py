"""
Unit tests for the plain-English translation and guidance engine.
"""

from legal_ease.simplifier import PlainEnglishSimplifier
from legal_ease.models import ClauseCategory, RiskSeverity


def test_indemnification_simplification():
    simplifier = PlainEnglishSimplifier()
    summary, impact, tip = simplifier.simplify(
        category=ClauseCategory.INDEMNIFICATION,
        severity=RiskSeverity.HIGH,
        title="Indemnification",
        text="Contractor shall indemnify Company from any and all claims.",
        traps=["Unilateral Indemnification Trap"],
    )
    assert "You are agreeing to pay all legal defense costs" in summary
    assert "attorney fees" in impact
    assert "PROPOSE MUTUAL INDEMNITY" in tip


def test_glossary_definitions():
    simplifier = PlainEnglishSimplifier()
    assert "indemnify" in simplifier.GLOSSARY
    assert "severability" in simplifier.GLOSSARY
    assert "force majeure" in simplifier.GLOSSARY
