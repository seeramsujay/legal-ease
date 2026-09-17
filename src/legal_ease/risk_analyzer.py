"""
Deterministic and semantic contract risk scoring and exposure assessment engine.
Evaluates clauses against real-world legal trap heuristics, computes semantic archetype
vector similarities, detects twisted / obfuscated phrasing, and calculates local confidence.
"""

import re
from typing import List, Tuple, Optional, Dict
from legal_ease.models import (
    ClauseCategory,
    RiskSeverity,
    RiskOverview,
)
from legal_ease.clause_segmenter import RawClause
from legal_ease.semantic_analyzer import get_semantic_model, SemanticClauseInsight


class ClauseRiskEvaluation:
    def __init__(
        self,
        risk_score: int,
        severity: RiskSeverity,
        reasons: List[str],
        traps: List[str],
        confidence: float = 0.95,
        confidence_label: str = "HIGH",
        confidence_reasons: Optional[List[str]] = None,
        is_twisted: bool = False,
        obfuscation_score: float = 0.0,
        archetype_scores: Optional[Dict[str, float]] = None,
        detected_euphemisms: Optional[List[str]] = None,
    ):
        self.risk_score = risk_score
        self.severity = severity
        self.reasons = reasons
        self.traps = traps
        self.confidence = confidence
        self.confidence_label = confidence_label
        self.confidence_reasons = confidence_reasons or []
        self.is_twisted = is_twisted
        self.obfuscation_score = obfuscation_score
        self.archetype_scores = archetype_scores or {}
        self.detected_euphemisms = detected_euphemisms or []


class RiskAnalyzer:
    """
    Evaluates contract clauses using deterministic pattern matching,
    semantic vector archetype matching, obfuscation detection,
    and document-wide risk index calculation.
    """

    def __init__(self):
        self.semantic_model = get_semantic_model()

    def evaluate_clause(self, clause: RawClause) -> ClauseRiskEvaluation:
        """Evaluate a single raw clause and compute its risk score, traps, and confidence."""
        text = clause.text.lower()
        score = 15  # Baseline standard score
        reasons: List[str] = []
        traps: List[str] = []
        confidence_reasons: List[str] = []
        confidence = 0.95  # Default high confidence for straightforward clauses

        # --- Semantic Vector & Obfuscation Analysis ---
        semantic = self.semantic_model.evaluate_semantics(clause.text, clause.title)
        if semantic.is_twisted:
            if semantic.detected_euphemisms:
                traps.append("Twisted / Euphemistic Drafting Trap")
                reasons.append(
                    f"Obfuscated Drafting: Sneaky euphemistic terms identified: {', '.join(semantic.detected_euphemisms)}."
                )
                score += int(semantic.obfuscation_score * 25)
            if semantic.escalation_recommended:
                confidence = min(confidence, 0.66)
                confidence_reasons.append(
                    f"Semantic ambiguity & obfuscation detected ({int(semantic.obfuscation_score * 100)}% complexity). "
                    "Deep AI LLM escalation recommended."
                )

        # 1. Indemnification traps
        if clause.category == ClauseCategory.INDEMNIFICATION or "indemnif" in text or "hold harmless" in text:
            has_contractor_indemnifies = bool(
                re.search(
                    r"(contractor|consultant|employee|vendor|provider|licensee|user)\s+(shall|agrees to)\s+(?:indemnif|hold\s+harmless)",
                    text,
                )
            )
            has_client_indemnifies = bool(
                re.search(
                    r"(client|company|customer|employer|licensor)\s+(shall|agrees to)\s+(?:indemnif|hold\s+harmless)",
                    text,
                )
            )
            has_attorney_fees = bool(
                re.search(r"attorney(?:'s)?\s+fees|legal\s+costs|expenses", text)
            )
            has_any_and_all = bool(
                re.search(r"any\s+and\s+all\s+(?:claims|losses|damages|liabilit)", text)
            )

            if has_contractor_indemnifies and not has_client_indemnifies:
                score += 55
                reasons.append(
                    "Unilateral Indemnification: You are required to indemnify the other party with no reciprocal protection for you."
                )
                traps.append("Unilateral Indemnification Trap")
                confidence = 0.96
                confidence_reasons.append("Definitive match: explicit unilateral indemnification structure.")
            elif "indemnif" in text or "hold harmless" in text:
                score += 25
                reasons.append("Contains indemnification obligations requiring financial defense.")
                # If indemnity is mentioned but unclear who indemnifies whom, confidence lowers
                if not has_contractor_indemnifies and not has_client_indemnifies:
                    confidence = min(confidence, 0.68)
                    confidence_reasons.append("Ambiguous indemnifying party in clause text.")

            if has_attorney_fees:
                score += 15
                reasons.append(
                    "Explicitly includes payment of opposing party's attorney's fees and litigation expenses."
                )

            if has_any_and_all:
                score += 10
                reasons.append(
                    "Overbroad 'any and all' language expands liability beyond gross negligence or intentional breach."
                )

        # 2. Limitation of Liability traps
        if (
            clause.category == ClauseCategory.LIMITATION_OF_LIABILITY
            or "limitation of liability" in text
        ):
            has_disparity = bool(
                re.search(
                    r"(company|client)(?:'s)?\s+(?:total|aggregate)?\s*liability\s+shall\s+(?:not\s+exceed|be\s+limited\s+to)",
                    text,
                )
            )
            has_contractor_unlimited = bool(
                re.search(
                    r"contractor(?:'s)?\s+liability\s+(?:shall\s+be\s+unlimited|is\s+not\s+limited)",
                    text,
                )
            )
            caps_at_nominal = bool(
                re.search(r"limited\s+to\s+(?:\$100|\$500|fees\s+paid\s+in\s+the\s+preceding\s+one\s+month)", text)
            )

            if has_contractor_unlimited or (has_disparity and "mutual" not in text):
                score += 60
                reasons.append(
                    "Asymmetrical Liability: Counterparty strictly limits their damages, while your financial exposure remains uncapped."
                )
                traps.append("Uncapped / Asymmetric Liability Trap")
                confidence = 0.95
                confidence_reasons.append("Definitive match: asymmetric liability cap.")
            elif caps_at_nominal:
                score += 45
                reasons.append(
                    "Nominal Recovery Cap: Recovery against counterparty is capped at a negligible sum (e.g. $100 or 1 month fees)."
                )
                traps.append("Nominal Liability Cap Trap")
                confidence = 0.94
            else:
                score += 20
                reasons.append("Standard exclusion of indirect, special, or consequential damages.")

        # 3. Dispute Resolution, Arbitration & Class Action Waiver
        if (
            clause.category == ClauseCategory.DISPUTE_RESOLUTION
            or "arbitrat" in text
            or "class action" in text
        ):
            has_mandatory_arbitration = bool(
                re.search(r"mandatory\s+arbitration|binding\s+arbitration|shall\s+be\s+settled\s+by\s+arbitration", text)
            )
            has_class_action_waiver = bool(
                re.search(r"class\s+action\s+waiver|waives?\s+(?:any\s+right\s+to\s+participate\s+in\s+a\s+class|class)", text)
            )
            has_jury_waiver = bool(
                re.search(r"waive[s]?\s+(?:all\s+rights?\s+to\s+a\s+)?jury\s+trial", text)
            )

            if has_class_action_waiver:
                score += 35
                reasons.append(
                    "Class Action Waiver: Forfeits the ability to join collective or class-wide claims."
                )
                traps.append("Class Action Waiver")
            if has_mandatory_arbitration:
                score += 30
                reasons.append(
                    "Mandatory Binding Arbitration: Deprives you of public court access; arbitration fees can be substantial."
                )
                traps.append("Mandatory Arbitration Trap")
            if has_jury_waiver:
                score += 15
                reasons.append("Jury Trial Waiver: Relinquishes constitutional right to a jury trial.")

        # 4. Termination traps
        if clause.category == ClauseCategory.TERMINATION or "terminat" in text:
            has_immediate_convenience = bool(
                re.search(
                    r"(?:company|client)\s+may\s+terminate.*?(?:at\s+any\s+time|without\s+cause|immediately)",
                    text,
                )
            )
            has_no_cure = bool(
                re.search(r"without\s+(?:prior\s+notice|opportunity\s+to\s+cure|cure\s+period)", text)
            )

            if (has_immediate_convenience or "immediately" in text) and (has_no_cure or "without prior notice" in text or "without cause" in text):
                score += 55
                reasons.append(
                    "Unilateral Immediate Termination: Counterparty can cancel on a moment's notice without providing a cure period."
                )
                traps.append("Zero-Notice Termination Trap")
                confidence = 0.95
            elif has_immediate_convenience:
                score += 35
                reasons.append(
                    "Termination for Convenience: Counterparty can cancel without cause."
                )
            elif "terminat" in text:
                score += 15
                reasons.append("Defines conditions, notice requirements, and post-termination procedures.")

        # 5. Intellectual Property Overreach
        if (
            clause.category == ClauseCategory.INTELLECTUAL_PROPERTY
            or "work for hire" in text
            or "intellectual property" in text
        ):
            has_prior_ip_grab = bool(
                re.search(
                    r"(?:all|prior|pre-existing)\s+(?:inventions|intellectual\s+property|tools|code|works)",
                    text,
                )
            )
            has_moral_rights_waiver = bool(
                re.search(r"waives?\s+(?:all\s+)?moral\s+rights", text)
            )
            has_work_for_hire = bool(
                re.search(r"work(?:s)?\s+(?:made\s+)?for\s+hire", text)
            )

            if has_prior_ip_grab and "excluding" not in text:
                score += 55
                reasons.append(
                    "Overbroad IP Assignment: Claims rights to your pre-existing tools, libraries, or prior inventions."
                )
                traps.append("Pre-Existing IP Assignment Trap")
                confidence = 0.93
            if has_moral_rights_waiver:
                score += 20
                reasons.append("Moral Rights Waiver: Surrenders right of attribution and integrity of created works.")
            if has_work_for_hire:
                score += 20
                reasons.append("Work-Made-For-Hire: All created deliverables transfer automatically upon creation.")

        # 6. Restrictive Covenants / Non-Compete
        if (
            clause.category == ClauseCategory.RESTRICTIVE_COVENANTS
            or "non-compete" in text
            or "non compete" in text
        ):
            has_long_term = bool(re.search(r"(?:2|3|4|5|two|three)\s+years", text))
            has_broad_geo = bool(re.search(r"worldwide|entire\s+world|any\s+geographic\s+area|nationwide", text))

            score += 45
            traps.append("Restrictive Covenant / Non-Compete Trap")
            if has_long_term:
                score += 25
                reasons.append("Excessive Duration: Restricts competitive employment for 2+ years.")
            if has_broad_geo:
                score += 20
                reasons.append("Excessive Geographic Scope: Purports to restrict competition globally or nationwide.")
            if not reasons:
                reasons.append("Imposes restrictions on client solicitation or competitive business activities.")

        # 7. Payment Terms traps
        if clause.category == ClauseCategory.PAYMENT_TERMS or "payment" in text:
            has_net_90 = bool(re.search(r"net\s+(?:60|90|120)", text))
            has_subjective_approval = bool(
                re.search(r"sole\s+discretion|subjective\s+satisfaction|withhold\s+payment", text)
            )

            if has_net_90:
                score += 35
                reasons.append("Extended Payment Delay: Net 60/90 terms create substantial cash flow delays.")
                traps.append("Net-60+ Payment Delay Trap")
            if has_subjective_approval:
                score += 30
                reasons.append("Subjective Payment Withholding: Client may withhold payment based on sole discretion.")
                traps.append("Discretionary Payment Trap")
            if not reasons:
                score += 10
                reasons.append("Standard invoicing, fee schedules, and milestone delivery terms.")

        # 8. Unclassified Boilerplate with Potential Latent Risk (Confidence Drops)
        if clause.category == ClauseCategory.GENERAL_BOILERPLATE:
            # If boilerplate mentions liability/remedies/waivers without a distinct category, confidence drops
            latent_risk_keywords = ["liable", "liability", "indemn", "waive", "remedy", "breach", "damages", "forfeit"]
            found_latent = [kw for kw in latent_risk_keywords if kw in text]
            if found_latent:
                score += 25
                reasons.append(f"Uncategorized clause contains potential liability triggers: {', '.join(found_latent)}.")
                confidence = min(confidence, 0.65)
                confidence_reasons.append(
                    f"Unclassified clause with legal risk terminology ({', '.join(found_latent)}). Escalation recommended."
                )
            elif not semantic.is_twisted:
                confidence = 0.92
                confidence_reasons.append("Standard general boilerplate.")

        # 9. Latent Trap Detection from Semantic Archetype Similarity
        if semantic.top_archetype_similarity >= 0.42 and not traps:
            arch_name = semantic.top_archetype.replace("_", " ").title()
            traps.append(f"Disguised {arch_name} Trap")
            reasons.append(
                semantic.explanation
                or f"Semantic vector analysis reveals high mathematical alignment with {arch_name} archetype."
            )
            score += 35
            confidence = min(confidence, 0.67)
            confidence_reasons.append("Semantic vectors indicate disguised predatory obligations. LLM escalation recommended.")

        # Ambiguity check: dense text (>120 words) with borderline score (35-55) and no traps
        word_count = len(text.split())
        if word_count > 120 and 35 <= score <= 55 and not traps:
            confidence = min(confidence, 0.70)
            confidence_reasons.append("Dense legal verbiage with indeterminate liability thresholds.")

        # Cap score between 0 and 100
        final_score = max(5, min(98, score))

        if final_score >= 75:
            severity = RiskSeverity.CRITICAL if final_score >= 88 else RiskSeverity.HIGH
        elif final_score >= 45:
            severity = RiskSeverity.MEDIUM
        else:
            severity = RiskSeverity.LOW

        # Confidence label
        if confidence >= 0.85:
            confidence_label = "HIGH"
        elif confidence >= 0.70:
            confidence_label = "MEDIUM"
        else:
            confidence_label = "LOW"

        if not reasons:
            reasons.append("Standard contract provision without elevated liability flags.")

        return ClauseRiskEvaluation(
            risk_score=final_score,
            severity=severity,
            reasons=reasons,
            traps=traps,
            confidence=round(confidence, 2),
            confidence_label=confidence_label,
            confidence_reasons=confidence_reasons,
            is_twisted=semantic.is_twisted,
            obfuscation_score=semantic.obfuscation_score,
            archetype_scores=semantic.archetype_scores,
            detected_euphemisms=semantic.detected_euphemisms,
        )

    def calculate_overview(
        self, evaluations: List[ClauseRiskEvaluation]
    ) -> RiskOverview:
        """Calculate document-wide risk index, average confidence, and executive findings."""
        if not evaluations:
            return RiskOverview(
                legal_risk_index=0,
                risk_level=RiskSeverity.LOW,
                total_clauses=0,
                high_risk_count=0,
                medium_risk_count=0,
                low_risk_count=0,
                critical_findings=["Document is empty or contains no detectable clauses."],
                executive_summary="No content available to evaluate.",
                average_confidence=1.0,
                escalated_clauses_count=0,
                twisted_clauses_count=0,
            )

        total_clauses = len(evaluations)
        high_count = sum(1 for e in evaluations if e.severity in (RiskSeverity.HIGH, RiskSeverity.CRITICAL))
        med_count = sum(1 for e in evaluations if e.severity == RiskSeverity.MEDIUM)
        low_count = sum(1 for e in evaluations if e.severity == RiskSeverity.LOW)
        twisted_count = sum(1 for e in evaluations if getattr(e, "is_twisted", False))

        weighted_sum = sum(
            e.risk_score * (2.2 if e.severity in (RiskSeverity.HIGH, RiskSeverity.CRITICAL) else 1.0)
            for e in evaluations
        )
        total_weight = sum(
            (2.2 if e.severity in (RiskSeverity.HIGH, RiskSeverity.CRITICAL) else 1.0)
            for e in evaluations
        )
        raw_index = int(weighted_sum / max(1.0, total_weight))
        risk_index = max(10, min(98, raw_index))

        avg_conf = sum(e.confidence for e in evaluations) / max(1, total_clauses)

        all_traps: List[str] = []
        for e in evaluations:
            for trap in e.traps:
                if trap not in all_traps:
                    all_traps.append(trap)

        critical_findings: List[str] = []
        if all_traps:
            for trap in all_traps[:5]:
                critical_findings.append(f"Detected {trap} requiring negotiation or legal counsel.")
        else:
            critical_findings.append("No critical legal traps detected. Standard contractual language.")

        if twisted_count > 0:
            critical_findings.append(
                f"Semantic Obfuscation Alert: {twisted_count} clause(s) exhibit twisted or euphemistic legal phrasing."
            )

        if risk_index >= 75:
            overall_severity = RiskSeverity.HIGH
            exec_summary = (
                f"HIGH RISK AGREEMENT ({risk_index}/100): Contains {high_count} high-exposure clauses, "
                f"including {', '.join(all_traps[:2]) if all_traps else 'unbalanced terms'}. "
                "Signing as-is exposes you to significant legal liabilities and financial exposure. "
                "Immediate attorney consultation and counter-proposal recommended."
            )
        elif risk_index >= 45:
            overall_severity = RiskSeverity.MEDIUM
            exec_summary = (
                f"MODERATE RISK AGREEMENT ({risk_index}/100): Contains standard operational clauses "
                f"alongside {med_count} moderate-risk items. Several provisions should be clarified or revised "
                "to ensure mutual fairness before execution."
            )
        else:
            overall_severity = RiskSeverity.LOW
            exec_summary = (
                f"LOW RISK BALANCED AGREEMENT ({risk_index}/100): Contract appears predominantly bilateral "
                "and standard. Ensure specific business deliverables and deadlines align with your expectations."
            )

        return RiskOverview(
            legal_risk_index=risk_index,
            risk_level=overall_severity,
            total_clauses=total_clauses,
            high_risk_count=high_count,
            medium_risk_count=med_count,
            low_risk_count=low_count,
            critical_findings=critical_findings,
            executive_summary=exec_summary,
            average_confidence=round(avg_conf, 2),
            escalated_clauses_count=0,
            twisted_clauses_count=twisted_count,
        )
