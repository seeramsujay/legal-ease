"""
Unit tests for the attorney checklist generator.
"""

from legal_ease.checklist_generator import AttorneyChecklistGenerator
from legal_ease.models import (
    RiskOverview,
    RiskSeverity,
    ClauseAnalysis,
    ClauseCategory,
)


def test_attorney_brief_generation():
    generator = AttorneyChecklistGenerator()
    overview = RiskOverview(
        legal_risk_index=85,
        risk_level=RiskSeverity.HIGH,
        total_clauses=2,
        high_risk_count=1,
        medium_risk_count=0,
        low_risk_count=1,
        critical_findings=["Detected Unilateral Indemnification Trap"],
        executive_summary="High risk contract requiring counsel.",
    )
    clauses = [
        ClauseAnalysis(
            id=1,
            section_title="Indemnification",
            category=ClauseCategory.INDEMNIFICATION,
            original_text="Contractor shall indemnify Client.",
            redacted_text="[PERSON_1] shall indemnify [COMPANY_1].",
            risk_score=85,
            severity=RiskSeverity.HIGH,
            risk_reasons=["Unilateral indemnification"],
            plain_english_summary="You pay their lawsuits.",
            what_it_means_for_you="Huge liability.",
            negotiation_tip="Propose mutual cap.",
            detected_traps=["Unilateral Indemnification Trap"],
        )
    ]

    brief = generator.generate("Freelance Agreement", overview, clauses)
    assert brief.overall_risk_index == 85
    assert len(brief.questions_for_counsel) >= 1
    assert "Indemnification" in brief.questions_for_counsel[0].category
    assert len(brief.priority_negotiation_items) >= 1
    assert "# ⚖️ Attorney Consultation Brief" in brief.markdown_report
    assert "LEGAL DISCLAIMER" in brief.markdown_report
