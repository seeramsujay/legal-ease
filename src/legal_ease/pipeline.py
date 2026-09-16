"""
Core end-to-end analysis pipeline orchestrator.
Sequences PII anonymization, clause segmentation, risk heuristics, plain-English translation,
and attorney checklist synthesis.
"""

from datetime import datetime, timezone
import uuid
from typing import Optional
from legal_ease.models import (
    ContractAnalysisResponse,
    ClauseAnalysis,
)
from legal_ease.guardrails import get_standard_disclaimer, sanitize_input_text
from legal_ease.anonymizer import PIIAnonymizer
from legal_ease.clause_segmenter import ClauseSegmenter
from legal_ease.risk_analyzer import RiskAnalyzer
from legal_ease.simplifier import PlainEnglishSimplifier
from legal_ease.checklist_generator import AttorneyChecklistGenerator


class LegalAnalysisPipeline:
    """
    Orchestrates the multi-stage legal document comprehension pipeline.
    Ensures zero PII leakage by anonymizing identifiers before linguistic analysis.
    """

    def __init__(self):
        self.anonymizer = PIIAnonymizer()
        self.segmenter = ClauseSegmenter()
        self.risk_analyzer = RiskAnalyzer()
        self.simplifier = PlainEnglishSimplifier()
        self.checklist_gen = AttorneyChecklistGenerator()

    def analyze(self, raw_text: str, document_title: Optional[str] = None) -> ContractAnalysisResponse:
        """
        Execute full legal analysis on input contract text.
        """
        doc_id = str(uuid.uuid4())[:8]
        clean_text = sanitize_input_text(raw_text)

        if not document_title:
            # Extract first non-empty line or default
            first_line = clean_text.split("\n")[0][:50].strip()
            document_title = first_line if first_line else "Legal Document"

        # Step 1: Local PII Anonymization
        anon_result = self.anonymizer.anonymize(clean_text)

        # Step 2: Clause Segmentation (using anonymized text for privacy)
        raw_clauses = self.segmenter.segment(anon_result.redacted_text)

        # Step 3: Risk Evaluation & Plain-English Translation
        clause_evaluations = []
        analyzed_clauses = []

        for c in raw_clauses:
            evaluation = self.risk_analyzer.evaluate_clause(c)
            clause_evaluations.append(evaluation)

            summary, impact, tip = self.simplifier.simplify(
                category=c.category,
                severity=evaluation.severity,
                title=c.title,
                text=c.text,
                traps=evaluation.traps,
            )

            # Re-hydrate original text for local clause representation
            orig_clause_text = self.anonymizer.deanonymize(c.text, anon_result.entities)

            analyzed_clauses.append(
                ClauseAnalysis(
                    id=c.clause_id,
                    section_title=c.title,
                    category=c.category,
                    original_text=orig_clause_text,
                    redacted_text=c.text,
                    risk_score=evaluation.risk_score,
                    severity=evaluation.severity,
                    risk_reasons=evaluation.reasons,
                    plain_english_summary=summary,
                    what_it_means_for_you=impact,
                    negotiation_tip=tip,
                    detected_traps=evaluation.traps,
                )
            )

        # Step 4: Aggregate Document-Level Risk Overview
        risk_overview = self.risk_analyzer.calculate_overview(clause_evaluations)

        # Step 5: Generate Attorney Briefing Checklist
        attorney_checklist = self.checklist_gen.generate(
            document_title=document_title,
            risk_overview=risk_overview,
            clauses=analyzed_clauses,
        )

        return ContractAnalysisResponse(
            document_id=doc_id,
            disclaimer=get_standard_disclaimer(),
            anonymization=anon_result,
            risk_overview=risk_overview,
            clauses=analyzed_clauses,
            attorney_checklist=attorney_checklist,
            analyzed_at=datetime.now(timezone.utc).isoformat(),
        )
