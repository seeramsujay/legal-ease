"""
Core End-to-End Analysis Pipeline Orchestrator.
Sequences local PII anonymization, structural clause segmentation, deterministic risk heuristics,
semantic vector archetype projection, obfuscation detection, confidence evaluation,
and optional LLM escalation routing (Gemini Flash Lite, Nemotron, OpenAI).
"""

from datetime import datetime, timezone
import uuid
from typing import Optional, List, Dict, Any
from legal_ease.models import (
    ContractAnalysisResponse,
    ClauseAnalysis,
    RiskSeverity,
)
from legal_ease.guardrails import get_standard_disclaimer, sanitize_input_text
from legal_ease.anonymizer import PIIAnonymizer
from legal_ease.clause_segmenter import ClauseSegmenter, RawClause
from legal_ease.risk_analyzer import RiskAnalyzer, ClauseRiskEvaluation
from legal_ease.simplifier import PlainEnglishSimplifier
from legal_ease.checklist_generator import AttorneyChecklistGenerator
from legal_ease.llm_client import NemotronClient


class LegalAnalysisPipeline:
    """
    Orchestrates the multi-stage legal document comprehension pipeline.
    Ensures zero PII leakage by anonymizing identifiers before linguistic analysis.
    Applies local-first verification with confidence-based LLM escalation.
    """

    def __init__(self, llm_client: Optional[NemotronClient] = None) -> None:
        self.anonymizer = PIIAnonymizer()
        self.segmenter = ClauseSegmenter()
        self.risk_analyzer = RiskAnalyzer()
        self.simplifier = PlainEnglishSimplifier()
        self.checklist_gen = AttorneyChecklistGenerator()
        self.llm_client = llm_client or NemotronClient()

    async def analyze_async(
        self, raw_text: Optional[str], document_title: Optional[str] = None
    ) -> ContractAnalysisResponse:
        """
        Asynchronously executes the full legal analysis with LLM escalation on low confidence or twisted drafting.
        Guarantees defensive execution against empty, None, or malformed inputs.
        """
        doc_id = str(uuid.uuid4())[:8]
        clean_text = sanitize_input_text(raw_text)

        if not document_title:
            first_line = clean_text.split("\n")[0][:50].strip() if clean_text else ""
            doc_title = first_line if first_line else "Legal Document"
        else:
            doc_title = str(document_title).strip()

        # Step 1: Local PII Anonymization (ZERO PII ever leaves client sandbox)
        anon_result = self.anonymizer.anonymize(clean_text)

        # Step 2: Clause Segmentation (using anonymized text for absolute privacy)
        raw_clauses: List[RawClause] = self.segmenter.segment(anon_result.redacted_text)

        # Step 3: Local Risk Evaluation, Semantic Vector Matching & Confidence Scoring
        clause_evaluations: List[ClauseRiskEvaluation] = []
        analyzed_clauses: List[ClauseAnalysis] = []
        escalated_count = 0

        for c in raw_clauses:
            eval_res = self.risk_analyzer.evaluate_clause(c)
            clause_evaluations.append(eval_res)

            # Check if local confidence is below threshold AND LLM is configured
            is_low_confidence = eval_res.confidence < self.llm_client.config.confidence_threshold
            can_escalate = self.llm_client.is_configured() and is_low_confidence

            deep_data: Optional[Dict[str, Any]] = None
            if can_escalate:
                # Escalate PII-redacted clause to LLM (Gemini Flash Lite / Nemotron / OpenAI)
                deep_data = await self.llm_client.deep_reason_clause(
                    anonymized_text=c.text,
                    section_title=c.title,
                    local_category=c.category.value,
                    local_score=eval_res.risk_score,
                    local_traps=eval_res.traps,
                )

            if deep_data:
                escalated_count += 1
                risk_score = deep_data.get("risk_score", eval_res.risk_score)
                sev_str = deep_data.get("severity", eval_res.severity.value).upper()
                try:
                    severity = RiskSeverity(sev_str)
                except Exception:
                    severity = eval_res.severity

                traps = deep_data.get("detected_traps", eval_res.traps)
                summary = deep_data.get("plain_english_summary") or self.simplifier.simplify(
                    c.category, severity, c.title, c.text, traps
                )[0]
                impact = deep_data.get("what_it_means_for_you") or self.simplifier.simplify(
                    c.category, severity, c.title, c.text, traps
                )[1]
                tip = deep_data.get("negotiation_tip") or self.simplifier.simplify(
                    c.category, severity, c.title, c.text, traps
                )[2]

                if "gemini" in self.llm_client.config.model_name.lower():
                    analysis_source = "GEMINI_DEEP_REASONING"
                elif "openai" in getattr(self.llm_client.config, "provider", "").lower() or "gpt" in self.llm_client.config.model_name.lower():
                    analysis_source = "OPENAI_DEEP_REASONING"
                else:
                    analysis_source = "NEMOTRON_DEEP_REASONING"

                escalation_reason = (
                    f"Local confidence was {int(eval_res.confidence * 100)}% "
                    f"(below {int(self.llm_client.config.confidence_threshold * 100)}% threshold). "
                    f"Deep legal reasoning applied via {self.llm_client.config.model_name}."
                )
                confidence = 0.95
                confidence_label = "HIGH"
                risk_reasons = eval_res.reasons + [f"AI Synthesis: {deep_data.get('reasoning', '')}"]
            else:
                summary, impact, tip = self.simplifier.simplify(
                    c.category, eval_res.severity, c.title, c.text, eval_res.traps
                )
                analysis_source = "LOCAL_HEURISTICS"
                escalation_reason = None
                risk_score = eval_res.risk_score
                severity = eval_res.severity
                traps = eval_res.traps
                confidence = eval_res.confidence
                confidence_label = eval_res.confidence_label
                risk_reasons = eval_res.reasons

            analyzed_clauses.append(
                ClauseAnalysis(
                    id=c.clause_id,
                    section_title=c.title,
                    category=c.category,
                    original_text=c.text,
                    redacted_text=c.text,  # Already segmented from anonymized text
                    risk_score=risk_score,
                    severity=severity,
                    confidence=confidence,
                    confidence_label=confidence_label,
                    analysis_source=analysis_source,
                    escalation_reason=escalation_reason,
                    risk_reasons=risk_reasons,
                    plain_english_summary=summary,
                    what_it_means_for_you=impact,
                    negotiation_tip=tip,
                    detected_traps=traps,
                    is_twisted=eval_res.is_twisted,
                    obfuscation_score=eval_res.obfuscation_score,
                    semantic_archetype_matches=eval_res.archetype_scores,
                    detected_euphemisms=eval_res.detected_euphemisms,
                )
            )

        # Step 4: Overall Document Risk Synthesis
        overview = self.risk_analyzer.calculate_overview(clause_evaluations)
        overview.escalated_clauses_count = escalated_count

        if self.llm_client.is_configured():
            overview.ai_model_used = f"Local Privacy Shield + {self.llm_client.config.model_name}"

        # Step 5: Generate Attorney Brief & Checklist
        attorney_brief = self.checklist_gen.generate(doc_title, overview, analyzed_clauses)

        return ContractAnalysisResponse(
            document_id=doc_id,
            disclaimer=get_standard_disclaimer(),
            anonymization=anon_result,
            risk_overview=overview,
            clauses=analyzed_clauses,
            attorney_checklist=attorney_brief,
            analyzed_at=datetime.now(timezone.utc).isoformat(),
        )

    def analyze(
        self, raw_text: Optional[str], document_title: Optional[str] = None
    ) -> ContractAnalysisResponse:
        """
        Synchronously executes the full legal analysis.
        Convenience wrapper around analyze_async for CLI, scripts, and synchronous workflows.
        Handles both idle thread execution and active event loop contexts safely.
        """
        import asyncio
        import concurrent.futures

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                return pool.submit(
                    asyncio.run, self.analyze_async(raw_text, document_title)
                ).result()
        else:
            return asyncio.run(self.analyze_async(raw_text, document_title))
