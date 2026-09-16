"""
Interactive Context-Aware Legal Assistant.
Answers user questions regarding contract terms with mandatory disclaimers,
clause citations, and optional Nemotron LLM conversational intelligence.
"""

import re
from typing import List, Dict, Optional, Any
from legal_ease.models import ChatResponse
from legal_ease.guardrails import get_standard_disclaimer, validate_chat_query
from legal_ease.clause_segmenter import ClauseSegmenter
from legal_ease.risk_analyzer import RiskAnalyzer
from legal_ease.simplifier import PlainEnglishSimplifier
from legal_ease.anonymizer import PIIAnonymizer
from legal_ease.llm_client import NemotronClient


class LegalAssistant:
    """
    Context-aware legal document Q&A engine.
    Finds relevant clauses, explains their implications, highlights risks,
    and enforces strict non-advisory disclaimers.
    Optionally routes queries through Nemotron for deep conversational synthesis.
    """

    def __init__(self, llm_client: Optional[NemotronClient] = None):
        self.segmenter = ClauseSegmenter()
        self.analyzer = RiskAnalyzer()
        self.simplifier = PlainEnglishSimplifier()
        self.anonymizer = PIIAnonymizer()
        self.llm_client = llm_client or NemotronClient()

    async def answer_query_async(
        self,
        query: str,
        contract_text: str = "",
        clauses_context: Optional[List[Dict[str, Any]]] = None,
        history: Optional[List[Dict[str, str]]] = None,
    ) -> ChatResponse:
        """Process user query against contract context and generate grounded response."""
        # 1. Guardrail validation
        validation = validate_chat_query(query)
        if not validation["valid"]:
            return ChatResponse(
                answer=validation["reason"],
                disclaimer=get_standard_disclaimer(),
                referenced_clauses=[],
                risk_warning="Guardrail intervention triggered.",
                model_used="Security Guardrail Engine",
            )

        # Build context if not provided
        if not clauses_context and contract_text.strip():
            raw_clauses = self.segmenter.segment(contract_text)
            clauses_context = []
            for c in raw_clauses:
                eval_res = self.analyzer.evaluate_clause(c)
                summary, impact, tip = self.simplifier.simplify(
                    c.category, eval_res.severity, c.title, c.text, eval_res.traps
                )
                clauses_context.append({
                    "id": c.clause_id,
                    "section_title": c.title,
                    "category": c.category.value,
                    "original_text": c.text,
                    "risk_score": eval_res.risk_score,
                    "plain_english_summary": summary,
                    "what_it_means_for_you": impact,
                    "negotiation_tip": tip,
                })

        # Check if Nemotron is configured for deep conversational reasoning
        if self.llm_client.is_configured() and contract_text.strip():
            # Guarantee 100% PII anonymity before calling Nemotron
            anon_res = self.anonymizer.anonymize(contract_text)
            llm_answer = await self.llm_client.chat_completion(
                query=query,
                anonymized_contract_context=anon_res.redacted_text,
                conversation_history=history,
            )
            if llm_answer:
                # Identify referenced clauses
                referenced = []
                if clauses_context:
                    for c in clauses_context:
                        sec_name = c.get("section_title", "")
                        if sec_name.lower() in llm_answer.lower() or c.get("category", "") in llm_answer.lower():
                            referenced.append(sec_name)
                return ChatResponse(
                    answer=llm_answer,
                    disclaimer=get_standard_disclaimer(),
                    referenced_clauses=list(dict.fromkeys(referenced[:4])),
                    risk_warning=None,
                    model_used=self.llm_client.config.model_name,
                )

        # Local deterministic assistant fallback
        return self._answer_locally(query, clauses_context)

    def _answer_locally(
        self, query: str, clauses_context: Optional[List[Dict[str, Any]]]
    ) -> ChatResponse:
        q_lower = query.lower()
        referenced_clauses: List[str] = []
        findings: List[str] = []
        risk_warning: Optional[str] = None

        # 2. Check for Termination & Payment on Cancellation
        if any(w in q_lower for w in ["terminate", "cancel", "kill", "fire", "quit", "leave", "cure"]):
            if clauses_context:
                term_clauses = [
                    c for c in clauses_context
                    if c.get("category") == "termination" or "terminat" in c.get("section_title", "").lower()
                ]
                for c in term_clauses:
                    referenced_clauses.append(c.get("section_title", "Termination Clause"))
                    findings.append(
                        f"**Regarding Termination ({c.get('section_title')}):** "
                        f"{c.get('plain_english_summary')}\n"
                        f"• *Real-World Consequence:* {c.get('what_it_means_for_you')}\n"
                        f"• *Actionable Tip:* {c.get('negotiation_tip')}"
                    )
                    if c.get("risk_score", 0) >= 60:
                        risk_warning = "CAUTION: This contract contains a high-risk unilateral termination clause."

        # 3. Check for Intellectual Property & Ownership
        if any(w in q_lower for w in ["ip", "intellectual property", "own", "ownership", "code", "invention", "copyright", "patent"]):
            if clauses_context:
                ip_clauses = [
                    c for c in clauses_context
                    if c.get("category") == "intellectual_property" or "intellectual" in c.get("section_title", "").lower()
                ]
                for c in ip_clauses:
                    referenced_clauses.append(c.get("section_title", "IP Clause"))
                    findings.append(
                        f"**Regarding Intellectual Property ({c.get('section_title')}):** "
                        f"{c.get('plain_english_summary')}\n"
                        f"• *Real-World Consequence:* {c.get('what_it_means_for_you')}\n"
                        f"• *Actionable Tip:* {c.get('negotiation_tip')}"
                    )
                    if c.get("risk_score", 0) >= 60:
                        risk_warning = "CAUTION: High risk of assigning your pre-existing tools or background IP."

        # 4. Check for Liability, Lawsuits, & Indemnity
        if any(w in q_lower for w in ["liability", "indemn", "sue", "lawsuit", "damages", "cap", "limit"]):
            if clauses_context:
                liab_clauses = [
                    c for c in clauses_context
                    if c.get("category") in ("indemnification", "limitation_of_liability")
                    or any(k in c.get("section_title", "").lower() for k in ["indemn", "liability"])
                ]
                for c in liab_clauses:
                    referenced_clauses.append(c.get("section_title", "Liability Clause"))
                    findings.append(
                        f"**Regarding Liability & Indemnification ({c.get('section_title')}):** "
                        f"{c.get('plain_english_summary')}\n"
                        f"• *Real-World Consequence:* {c.get('what_it_means_for_you')}\n"
                        f"• *Actionable Tip:* {c.get('negotiation_tip')}"
                    )
                    if c.get("risk_score", 0) >= 70:
                        risk_warning = "CRITICAL WARNING: This document contains an unbalanced indemnification or liability trap."

        # 5. Check for Payment & Compensation
        if any(w in q_lower for w in ["pay", "payment", "money", "fee", "rate", "invoice", "net 30", "net 60", "late"]):
            if clauses_context:
                pay_clauses = [
                    c for c in clauses_context
                    if c.get("category") == "payment_terms" or "pay" in c.get("section_title", "").lower()
                ]
                for c in pay_clauses:
                    referenced_clauses.append(c.get("section_title", "Payment Clause"))
                    findings.append(
                        f"**Regarding Payment Terms ({c.get('section_title')}):** "
                        f"{c.get('plain_english_summary')}\n"
                        f"• *Real-World Consequence:* {c.get('what_it_means_for_you')}\n"
                        f"• *Actionable Tip:* {c.get('negotiation_tip')}"
                    )

        # 6. Check for Arbitration, Court & Disputes
        if any(w in q_lower for w in ["arbitrat", "court", "jury", "dispute", "sue", "venue", "class action"]):
            if clauses_context:
                disp_clauses = [
                    c for c in clauses_context
                    if c.get("category") == "dispute_resolution" or "dispute" in c.get("section_title", "").lower()
                ]
                for c in disp_clauses:
                    referenced_clauses.append(c.get("section_title", "Dispute Resolution"))
                    findings.append(
                        f"**Regarding Dispute Resolution ({c.get('section_title')}):** "
                        f"{c.get('plain_english_summary')}\n"
                        f"• *Real-World Consequence:* {c.get('what_it_means_for_you')}\n"
                        f"• *Actionable Tip:* {c.get('negotiation_tip')}"
                    )

        # 7. Check for Non-Compete & Moonlighting
        if any(w in q_lower for w in ["compete", "non-compete", "moonlight", "solicit", "clients", "other job"]):
            if clauses_context:
                rest_clauses = [
                    c for c in clauses_context
                    if c.get("category") == "restrictive_covenants" or "compete" in c.get("section_title", "").lower()
                ]
                for c in rest_clauses:
                    referenced_clauses.append(c.get("section_title", "Non-Compete Clause"))
                    findings.append(
                        f"**Regarding Non-Compete & Restrictive Covenants ({c.get('section_title')}):** "
                        f"{c.get('plain_english_summary')}\n"
                        f"• *Real-World Consequence:* {c.get('what_it_means_for_you')}\n"
                        f"• *Actionable Tip:* {c.get('negotiation_tip')}"
                    )

        # Build final response text
        if findings:
            answer = "\n\n".join(findings)
        else:
            answer = (
                f"I reviewed your question regarding **\"{query}\"** against the contract terms. "
                "Based on the provisions analyzed, please review the specific sections highlighted in the "
                "clause breakdown. For complex scenario-specific liability determinations, we recommend taking "
                "the questions generated in the Attorney Checklist directly to licensed counsel."
            )

        return ChatResponse(
            answer=answer,
            disclaimer=get_standard_disclaimer(),
            referenced_clauses=list(dict.fromkeys(referenced_clauses)),
            risk_warning=risk_warning,
            model_used="Local Grounded Assistant",
        )

    def answer_query(
        self,
        query: str,
        contract_text: str = "",
        clauses_context: Optional[List[Dict[str, Any]]] = None,
        history: Optional[List[Dict[str, str]]] = None,
    ) -> ChatResponse:
        """Sync wrapper for callers/tests."""
        return self._answer_locally(query, clauses_context)
