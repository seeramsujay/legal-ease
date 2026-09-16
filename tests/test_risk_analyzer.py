"""
Unit tests for the deterministic risk scoring engine.
"""

from legal_ease.clause_segmenter import RawClause
from legal_ease.risk_analyzer import RiskAnalyzer
from legal_ease.models import ClauseCategory, RiskSeverity


def test_unilateral_indemnity_trap_detection():
    analyzer = RiskAnalyzer()
    clause = RawClause(
        clause_id=1,
        title="Indemnification",
        text="Contractor shall indemnify and hold harmless Company from any and all claims, including attorney's fees.",
        category=ClauseCategory.INDEMNIFICATION,
    )
    res = analyzer.evaluate_clause(clause)
    assert res.risk_score >= 70
    assert "Unilateral Indemnification Trap" in res.traps
    assert res.severity in (RiskSeverity.HIGH, RiskSeverity.CRITICAL)


def test_uncapped_liability_disparity():
    analyzer = RiskAnalyzer()
    clause = RawClause(
        clause_id=2,
        title="Limitation of Liability",
        text="Company's total liability shall not exceed $100. Contractor's liability is not limited and shall be unlimited.",
        category=ClauseCategory.LIMITATION_OF_LIABILITY,
    )
    res = analyzer.evaluate_clause(clause)
    assert res.risk_score >= 75
    assert "Uncapped / Asymmetric Liability Trap" in res.traps


def test_arbitration_and_class_action_waiver():
    analyzer = RiskAnalyzer()
    clause = RawClause(
        clause_id=3,
        title="Dispute Resolution",
        text="All disputes subject to mandatory arbitration. User expressly waives any right to a jury trial and class action waiver.",
        category=ClauseCategory.DISPUTE_RESOLUTION,
    )
    res = analyzer.evaluate_clause(clause)
    assert res.risk_score >= 70
    assert "Class Action Waiver" in res.traps
    assert "Mandatory Arbitration Trap" in res.traps


def test_zero_notice_termination_trap():
    analyzer = RiskAnalyzer()
    clause = RawClause(
        clause_id=4,
        title="Termination",
        text="Company may terminate this agreement at any time immediately without prior notice and without opportunity to cure.",
        category=ClauseCategory.TERMINATION,
    )
    res = analyzer.evaluate_clause(clause)
    assert res.risk_score >= 70
    assert "Zero-Notice Termination Trap" in res.traps


def test_document_overview_calculation():
    analyzer = RiskAnalyzer()
    high_eval = analyzer.evaluate_clause(
        RawClause(1, "Indemnity", "Contractor shall indemnify Company from any and all claims with attorney's fees.", ClauseCategory.INDEMNIFICATION)
    )
    low_eval = analyzer.evaluate_clause(
        RawClause(2, "Governing Law", "Governed by the laws of Texas.", ClauseCategory.GOVERNING_LAW)
    )
    overview = analyzer.calculate_overview([high_eval, low_eval])
    assert overview.total_clauses == 2
    assert overview.high_risk_count >= 1
    assert overview.legal_risk_index > 40
    assert len(overview.critical_findings) >= 1
