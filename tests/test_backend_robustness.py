"""
Robustness and Edge-Case Backend Tests for Legal-Ease.
Tests core pipeline orchestrator, defensive input sanitization, complex legal patterns,
resilience against malformed inputs, and fallback behavior.
"""

import pytest
from legal_ease.pipeline import LegalAnalysisPipeline
from legal_ease.clause_segmenter import ClauseSegmenter, RawClause
from legal_ease.risk_analyzer import RiskAnalyzer
from legal_ease.simplifier import PlainEnglishSimplifier
from legal_ease.anonymizer import PIIAnonymizer
from legal_ease.comparator import ContractComparator
from legal_ease.models import ClauseCategory, RiskSeverity
from legal_ease.sample_contracts import FREELANCE_HIGH_RISK, FREELANCE_NEGOTIATED, SAAS_TERMS


class TestPipelineRobustness:
    """Test LegalAnalysisPipeline across synchronous and asynchronous execution paths."""

    def test_sync_analyze_standard_contract(self):
        pipeline = LegalAnalysisPipeline()
        res = pipeline.analyze(FREELANCE_HIGH_RISK, document_title="High Risk Agreement")
        assert res is not None
        assert res.risk_overview.total_clauses >= 5
        assert res.risk_overview.legal_risk_index > 50
        assert res.document_id is not None
        assert len(res.clauses) == res.risk_overview.total_clauses
        assert res.attorney_checklist is not None

    def test_sync_analyze_empty_or_whitespace_input(self):
        pipeline = LegalAnalysisPipeline()
        res = pipeline.analyze("", document_title="Empty Doc")
        assert res is not None
        assert res.risk_overview.total_clauses == 0
        assert res.risk_overview.legal_risk_index == 0

        res_spaces = pipeline.analyze("   \n\t   \n  ")
        assert res_spaces.risk_overview.total_clauses == 0

    def test_sync_analyze_none_input(self):
        pipeline = LegalAnalysisPipeline()
        res = pipeline.analyze(None)
        assert res is not None
        assert res.risk_overview.total_clauses == 0

    def test_sync_analyze_null_byte_resilience(self):
        pipeline = LegalAnalysisPipeline()
        poisoned_text = "1. Term.\x00 The agreement lasts for 1 year.\x00\x00"
        res = pipeline.analyze(poisoned_text)
        assert res is not None
        assert res.risk_overview.total_clauses >= 1

    def test_sync_analyze_single_clause_without_numbers(self):
        pipeline = LegalAnalysisPipeline()
        text = "The Contractor agrees to unconditionally indemnify and hold harmless the Client against all third-party claims."
        res = pipeline.analyze(text)
        assert res is not None
        assert res.risk_overview.total_clauses == 1
        assert res.clauses[0].category == ClauseCategory.INDEMNIFICATION

    def test_sync_analyze_very_long_contract(self):
        pipeline = LegalAnalysisPipeline()
        # Construct large repetitive contract
        sections = [
            f"{i}. Section {i}. The contractor shall deliver services according to milestone {i}."
            for i in range(1, 40)
        ]
        large_contract = "\n\n".join(sections)
        res = pipeline.analyze(large_contract, document_title="Long Contract")
        assert res.risk_overview.total_clauses >= 35


class TestClauseSegmenterRobustness:
    """Test clause segmentation against unconventional formatting and numbering schemes."""

    def setup_method(self):
        self.segmenter = ClauseSegmenter()

    def test_roman_numerals_segmentation(self):
        text = (
            "ARTICLE I. DEFINITIONS\n"
            "Confidential information means all non-public data.\n\n"
            "ARTICLE II. OBLIGATIONS\n"
            "Recipient shall protect confidential information with reasonable care.\n\n"
            "ARTICLE III. TERM AND TERMINATION\n"
            "This agreement shall terminate upon 30 days written notice."
        )
        clauses = self.segmenter.segment(text)
        assert len(clauses) == 3
        assert "DEFINITIONS" in clauses[0].title
        assert "OBLIGATIONS" in clauses[1].title
        assert "TERMINATION" in clauses[2].title

    def test_section_symbol_segmentation(self):
        text = (
            "§ 1.0 Services and Scope\n"
            "Consultant agrees to perform the services detailed in Exhibit A.\n\n"
            "§ 2.0 Fees and Reimbursement\n"
            "Client shall pay Consultant within forty-five (45) days of invoice date."
        )
        clauses = self.segmenter.segment(text)
        assert len(clauses) >= 2
        assert any(c.category == ClauseCategory.PAYMENT_TERMS for c in clauses)

    def test_unstructured_paragraphs_fallback(self):
        text = (
            "Here is a contract with no section headings at all.\n"
            "First paragraph says the contractor will build a web app for $10,000.\n\n"
            "Second paragraph specifies that either party can terminate with two weeks notice.\n\n"
            "Third paragraph says consultant forfeits all ownership in pre-existing intellectual property."
        )
        clauses = self.segmenter.segment(text)
        assert len(clauses) >= 3


class TestRiskAnalyzerPredatoryPatterns:
    """Validate detection of nuanced predatory contract traps and compounding risk calculations."""

    def setup_method(self):
        self.analyzer = RiskAnalyzer()

    def test_unilateral_indemnity_vs_mutual_indemnity(self):
        unilateral = RawClause(
            clause_id=1,
            title="Indemnification",
            text="Contractor shall defend, indemnify, and hold harmless Client from any and all claims, liabilities, and expenses.",
            category=ClauseCategory.INDEMNIFICATION,
        )
        res_uni = self.analyzer.evaluate_clause(unilateral)
        assert res_uni.risk_score >= 70
        assert res_uni.severity in (RiskSeverity.CRITICAL, RiskSeverity.HIGH)
        assert any("unilateral" in trap.lower() for trap in res_uni.traps)

        mutual = RawClause(
            clause_id=2,
            title="Mutual Indemnification",
            text="Each party agrees to mutually defend, indemnify, and hold harmless the other party from third-party claims arising from gross negligence.",
            category=ClauseCategory.INDEMNIFICATION,
        )
        res_mut = self.analyzer.evaluate_clause(mutual)
        assert res_mut.risk_score < res_uni.risk_score

    def test_preexisting_ip_assignment_trap(self):
        clause = RawClause(
            clause_id=3,
            title="Intellectual Property Ownership",
            text="Contractor hereby assigns all right, title, and interest in and to all deliverables, including all pre-existing inventions, background technology, and tools.",
            category=ClauseCategory.INTELLECTUAL_PROPERTY,
        )
        res = self.analyzer.evaluate_clause(clause)
        assert res.risk_score >= 65
        assert any("pre-existing" in trap.lower() or "assignment" in trap.lower() for trap in res.traps)

    def test_clawback_and_withholding_trap(self):
        clause = RawClause(
            clause_id=4,
            title="Payment Terms",
            text="Client reserves the unilateral right to withhold payment or claw back previously paid compensation at its sole discretion.",
            category=ClauseCategory.PAYMENT_TERMS,
        )
        res = self.analyzer.evaluate_clause(clause)
        assert res.risk_score >= 50
        assert any("clawback" in trap.lower() or "withhold" in trap.lower() for trap in res.traps)


class TestPIIAnonymizerEdgeCases:
    """Exhaustive testing of PII identification, redaction, and restoration."""

    def setup_method(self):
        self.anon = PIIAnonymizer()

    def test_multiple_overlapping_entities(self):
        text = (
            "Please send tax records for John Doe (SSN: 123-45-6789, EIN: 12-3456789) "
            "to john.doe@consulting.co.uk or call +1 (555) 234-5678. "
            "Address: 742 Evergreen Terrace, Springfield, OR 97477. "
            "Retainer amount is $25,000.00 USD with €5,000 travel deposit."
        )
        result = self.anon.anonymize(text)
        assert "123-45-6789" not in result.redacted_text
        assert "12-3456789" not in result.redacted_text
        assert "john.doe@consulting.co.uk" not in result.redacted_text
        assert "(555) 234-5678" not in result.redacted_text
        assert "$25,000.00" not in result.redacted_text
        assert len(result.entities) >= 5

        # Verify deanonymization restores the original strings
        restored = self.anon.deanonymize(result.redacted_text, result.entities)
        assert "john.doe@consulting.co.uk" in restored
        assert "123-45-6789" in restored

    def test_idempotent_anonymization(self):
        text = "Contact agent at support@domain.com."
        res1 = self.anon.anonymize(text)
        res2 = self.anon.anonymize(res1.redacted_text)
        # Re-anonymizing already redacted text should not introduce duplicate entities
        assert "[EMAIL_1]" in res2.redacted_text
        assert len(res2.entities) == 0

    def test_deanonymization_with_empty_or_modified_text(self):
        empty_restored = self.anon.deanonymize("", [])
        assert empty_restored == ""


class TestComparatorEdgeCases:
    """Exhaustive testing of contract comparison under diverse conditions."""

    def setup_method(self):
        self.comparator = ContractComparator()

    def test_compare_identical_contracts(self):
        text = "1. Term. This agreement expires in 12 months."
        res = self.comparator.compare(text, text)
        assert res.risk_index_delta == 0
        assert res.trajectory == "NEUTRAL"
        assert len(res.clause_diffs) >= 1

    def test_compare_completely_disjoint_contracts(self):
        c1 = "1. Confidentiality. Recipient shall keep secret all business plans."
        c2 = "1. Warranty. The software is provided AS-IS without warranty of any kind."
        res = self.comparator.compare(c1, c2, title_v1="Draft NDA", title_v2="Draft License")
        assert res is not None
        assert len(res.clause_diffs) >= 1

    def test_compare_saas_vs_negotiated(self):
        res = self.comparator.compare(FREELANCE_HIGH_RISK, FREELANCE_NEGOTIATED)
        assert res.risk_index_v1 > res.risk_index_v2
        assert res.risk_index_delta < 0
        assert res.trajectory == "SAFER"
        assert len(res.summary_of_changes) >= 1
