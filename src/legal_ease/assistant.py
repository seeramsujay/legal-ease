"""
Interactive Context-Aware Legal Assistant.
Answers user questions regarding contract terms with mandatory disclaimers,
clause citations, and optional LLM conversational intelligence (Gemini Flash-Lite, Nemotron, OpenAI).
"""

import re
from typing import List, Dict, Optional, Any
from legal_ease.models import ChatResponse
from legal_ease.guardrails import get_standard_disclaimer, validate_chat_query
from legal_ease.clause_segmenter import ClauseSegmenter, RawClause
from legal_ease.risk_analyzer import RiskAnalyzer
from legal_ease.simplifier import PlainEnglishSimplifier
from legal_ease.anonymizer import PIIAnonymizer
from legal_ease.llm_client import NemotronClient


class LegalAssistant:
    """
    Context-aware legal document Q&A engine.
    Finds relevant clauses, explains their implications, highlights risks,
    and enforces strict non-advisory disclaimers.
    Optionally routes queries through Gemini Flash-Lite / Nemotron / OpenAI for deep conversational synthesis.
    """

    def __init__(self, llm_client: Optional[NemotronClient] = None) -> None:
        self.segmenter = ClauseSegmenter()
        self.analyzer = RiskAnalyzer()
        self.simplifier = PlainEnglishSimplifier()
        self.anonymizer = PIIAnonymizer()
        self.llm_client = llm_client or NemotronClient()

    async def answer_query_async(
        self,
        query: Optional[str],
        contract_text: Optional[str] = "",
        clauses_context: Optional[List[Dict[str, Any]]] = None,
        history: Optional[List[Dict[str, str]]] = None,
    ) -> ChatResponse:
        """
        Processes a user query against contract context and generates a grounded response.
        Guarantees defensive execution against malformed, adversarial, or None inputs.
        """
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

        safe_query = validation.get("sanitized_query", str(query).strip())
        safe_contract_text = str(contract_text).strip() if contract_text else ""

        # Build context if not provided
        if not clauses_context and safe_contract_text:
            raw_clauses: List[RawClause] = self.segmenter.segment(safe_contract_text)
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

        # Check if LLM is configured for deep conversational reasoning
        if self.llm_client.is_configured() and safe_contract_text:
            # Guarantee 100% PII anonymity before calling LLM
            anon_res = self.anonymizer.anonymize(safe_contract_text)
            llm_answer = await self.llm_client.chat_completion(
                query=safe_query,
                anonymized_contract_context=anon_res.redacted_text,
                conversation_history=history,
            )
            if llm_answer:
                # Identify referenced clauses
                referenced: List[str] = []
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
        return self._answer_locally(safe_query, clauses_context)

    def _answer_locally(
        self, query: str, clauses_context: Optional[List[Dict[str, Any]]]
    ) -> ChatResponse:
        """Local rule-based conversational triage when remote LLM is offline."""
        q_lower = query.lower()
        referenced_clauses: List[str] = []
        findings: List[str] = []
        risk_warning: Optional[str] = None

        # 1. Check for Termination & Payment on Cancellation
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
                        f"• *Negotiation Move:* {c.get('negotiation_tip')}"
                    )

        # 2. Check for Lawsuits, Liability, Indemnity & Being Sued
        if any(w in q_lower for w in ["sue", "sued", "lawsuit", "liable", "liability", "indemn", "damage", "fault"]):
            if clauses_context:
                indem_clauses = [
                    c for c in clauses_context
                    if c.get("category") in ("indemnification", "limitation_of_liability")
                    or any(k in c.get("section_title", "").lower() for k in ["indemn", "liabilit"])
                ]
                for c in indem_clauses:
                    referenced_clauses.append(c.get("section_title", "Liability Provision"))
                    findings.append(
                        f"**Regarding Liability & Indemnity ({c.get('section_title')}):** "
                        f"{c.get('plain_english_summary')}\n"
                        f"• *Exposure Level:* {c.get('risk_score', 0)}/100\n"
                        f"• *Impact:* {c.get('what_it_means_for_you')}\n"
                        f"• *Negotiation Move:* {c.get('negotiation_tip')}"
                    )
                if any(c.get("risk_score", 0) >= 75 for c in indem_clauses):
                    risk_warning = "CRITICAL: Contract contains high-exposure unilateral indemnity or uncapped liability provisions."

        # 3. Check for Intellectual Property, Ownership & Deliverables
        if any(w in q_lower for w in ["own", "ownership", "ip", "code", "work for hire", "deliverable", "copyright", "patent"]):
            if clauses_context:
                ip_clauses = [
                    c for c in clauses_context
                    if c.get("category") == "intellectual_property" or "intellectual" in c.get("section_title", "").lower()
                ]
                for c in ip_clauses:
                    referenced_clauses.append(c.get("section_title", "IP Provision"))
                    findings.append(
                        f"**Regarding Intellectual Property ({c.get('section_title')}):** "
                        f"{c.get('plain_english_summary')}\n"
                        f"• *Impact:* {c.get('what_it_means_for_you')}\n"
                        f"• *Negotiation Move:* {c.get('negotiation_tip')}"
                    )

        # 4. Check for Non-Compete & Restrictive Covenants
        if any(w in q_lower for w in ["compete", "competition", "non-compete", "restrict", "solicit"]):
            if clauses_context:
                nc_clauses = [
                    c for c in clauses_context
                    if c.get("category") == "restrictive_covenants" or "compete" in c.get("section_title", "").lower()
                ]
                for c in nc_clauses:
                    referenced_clauses.append(c.get("section_title", "Restrictive Covenant"))
                    findings.append(
                        f"**Regarding Restrictive Covenants ({c.get('section_title')}):** "
                        f"{c.get('plain_english_summary')}\n"
                        f"• *Impact:* {c.get('what_it_means_for_you')}\n"
                        f"• *Negotiation Move:* {c.get('negotiation_tip')}"
                    )

        # 5. Check for Payment & Fees
        if any(w in q_lower for w in ["pay", "payment", "money", "rate", "fee", "invoice", "late", "net 30", "net 60"]):
            if clauses_context:
                pay_clauses = [
                    c for c in clauses_context
                    if c.get("category") == "payment_terms" or "payment" in c.get("section_title", "").lower()
                ]
                for c in pay_clauses:
                    referenced_clauses.append(c.get("section_title", "Payment Terms"))
                    findings.append(
                        f"**Regarding Compensation & Billing ({c.get('section_title')}):** "
                        f"{c.get('plain_english_summary')}\n"
                        f"• *Impact:* {c.get('what_it_means_for_you')}\n"
                        f"• *Negotiation Move:* {c.get('negotiation_tip')}"
                    )

        if findings:
            answer = (
                "Here is an analysis based on the specific clauses in your agreement:\n\n"
                + "\n\n".join(findings)
                + "\n\n*Tip: Connect an LLM (Gemini Flash-Lite / Nemotron / OpenAI) in Settings for freeform conversational reasoning.*"
            )
        else:
            answer = (
                "Based on the agreement provided, I didn't find specific clauses directly answering that query. "
                "You can ask about:\n"
                "• **Liability:** *'Can they sue me?'* or *'Is indemnity mutual?'*\n"
                "• **Termination:** *'Can they cancel without paying me?'*\n"
                "• **Intellectual Property:** *'Do I own my reusable code and tools?'*\n"
                "• **Non-compete:** *'Can I work for competitor clients?'*\n\n"
                "Or enable Gemini 2.0 Flash-Lite in Settings for general conversational document intelligence."
            )

        return ChatResponse(
            answer=answer,
            disclaimer=get_standard_disclaimer(),
            referenced_clauses=list(dict.fromkeys(referenced_clauses)),
            risk_warning=risk_warning,
            model_used="Local Deterministic Heuristic Engine",
        )
