"""
Deterministic and Semantic Contract Risk Scoring and Exposure Assessment Engine.
Evaluates clauses against real-world legal trap heuristics, computes semantic archetype
vector similarities, detects twisted / obfuscated phrasing, and calculates local confidence.
Optimized with pre-compiled regex objects for high-velocity linear scanning.
"""

import re
from typing import List, Tuple, Optional, Dict, Pattern
from legal_ease.models import (
    ClauseCategory,
    RiskSeverity,
    RiskOverview,
)
from legal_ease.clause_segmenter import RawClause
from legal_ease.semantic_analyzer import get_semantic_model, SemanticClauseInsight

# --- Pre-compiled Heuristic Regex Patterns for Maximum Single-Pass Velocity ---

# Indemnification heuristics
_RE_CONTRACTOR_INDEMNIFIES = re.compile(
    r"(?:contractor|consultant|employee|vendor|provider|licensee|user)\s+(?:shall|agrees to)\s+(?:defend[\w\s\,]*?)?(?:indemnif|hold\s+harmless)",
    re.IGNORECASE,
)
_RE_CLIENT_INDEMNIFIES = re.compile(
    r"(?:client|company|customer|employer|licensor)\s+(?:shall|agrees to)\s+(?:defend[\w\s\,]*?)?(?:indemnif|hold\s+harmless)",
    re.IGNORECASE,
)
_RE_ATTORNEY_FEES = re.compile(
    r"attorney(?:'s)?\s+fees|legal\s+costs|expenses",
    re.IGNORECASE,
)
_RE_ANY_AND_ALL = re.compile(
    r"any\s+and\s+all\s+(?:claims|losses|damages|liabilit)",
    re.IGNORECASE,
)

# Limitation of Liability heuristics
_RE_LIABILITY_DISPARITY = re.compile(
    r"(?:company|client)(?:'s)?\s+(?:total|aggregate)?\s*liability\s+shall\s+(?:not\s+exceed|be\s+limited\s+to)",
    re.IGNORECASE,
)
_RE_CONTRACTOR_UNLIMITED = re.compile(
    r"contractor(?:'s)?\s+liability\s+(?:shall\s+be\s+unlimited|is\s+not\s+limited)",
    re.IGNORECASE,
)
_RE_NOMINAL_CAP = re.compile(
    r"limited\s+to\s+(?:\$100|\$500|fees\s+paid\s+in\s+the\s+preceding\s+one\s+month)",
    re.IGNORECASE,
)

# Dispute Resolution & Waivers heuristics
_RE_MANDATORY_ARBITRATION = re.compile(
    r"mandatory\s+arbitration|binding\s+arbitration|shall\s+be\s+settled\s+by\s+arbitration",
    re.IGNORECASE,
)
_RE_CLASS_ACTION_WAIVER = re.compile(
    r"class\s+action\s+waiver|waives?\s+(?:any\s+right\s+to\s+participate\s+in\s+a\s+class|class)",
    re.IGNORECASE,
)
_RE_JURY_WAIVER = re.compile(
    r"waive[s]?\s+(?:all\s+rights?\s+to\s+a\s+)?jury\s+trial",
    re.IGNORECASE,
)

# Termination heuristics
_RE_IMMEDIATE_CONVENIENCE = re.compile(
    r"(?:company|client)\s+may\s+terminate.*?(?:at\s+any\s+time|without\s+cause|immediately)",
    re.IGNORECASE,
)
_RE_NO_CURE = re.compile(
    r"without\s+(?:prior\s+notice|opportunity\s+to\s+cure|cure\s+period)",
    re.IGNORECASE,
)

# Intellectual Property Overreach heuristics
_RE_PRE_EXISTING_IP = re.compile(
    r"(?:all|prior|pre-existing)\s+(?:inventions|intellectual\s+property|tools|code|works)",
    re.IGNORECASE,
)
_RE_MORAL_RIGHTS = re.compile(
    r"waives?\s+(?:all\s+)?moral\s+rights",
    re.IGNORECASE,
)
_RE_WORK_FOR_HIRE = re.compile(
    r"work(?:s)?\s+(?:made\s+)?for\s+hire",
    re.IGNORECASE,
)

# Restrictive Covenants heuristics
_RE_LONG_TERM_NON_COMPETE = re.compile(
    r"(?:2|3|4|5|two|three)\s+years",
    re.IGNORECASE,
)
_RE_BROAD_GEO_SCOPE = re.compile(
    r"worldwide|entire\s+world|any\s+geographic\s+area|nationwide",
    re.IGNORECASE,
)

# Payment Terms heuristics
_RE_NET_PAYMENT_TERMS = re.compile(
    r"net\s+(?:60|90|120)",
    re.IGNORECASE,
)
_RE_SUBJECTIVE_WITHHOLDING = re.compile(
    r"sole\s+discretion|subjective\s+satisfaction|withhold\s+payment|claw\s*back",
    re.IGNORECASE,
)

# Latent boilerplate risk terminology
LATENT_RISK_KEYWORDS = [
    "liable", "liability", "indemn", "waive", "remedy", "breach", "damages", "forfeit"
]


class ClauseRiskEvaluation:
    """Detailed risk assessment telemetry for a single clause."""
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
    ) -> None:
        self.risk_score = risk_score
        self.severity = severity
        self.reasons = reasons or []
        self.traps = traps or []
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
    semantic vector archetype projection, obfuscation analysis,
    and document-wide risk index calculation.
    """

    def __init__(self) -> None:
        self.semantic_model = get_semantic_model()

    def evaluate_clause(self, clause: Optional[RawClause]) -> ClauseRiskEvaluation:
        """
        Evaluate a single raw clause and compute its risk score, traps, and confidence.
        Guarantees safe handling if clause is None or has empty content.
        """
        if clause is None:
            return ClauseRiskEvaluation(
                risk_score=10,
                severity=RiskSeverity.LOW,
                reasons=["Empty or null clause provided."],
                traps=[],
                confidence=1.0,
                confidence_label="HIGH",
            )

        text = clause.text.lower() if clause.text else ""
        score = 15  # Baseline standard score
        reasons: List[str] = []
        traps: List[str] = []
        confidence_reasons: List[str] = []
        confidence = 0.95  # Default high confidence for straightforward clauses

        # --- Semantic Vector & Obfuscation Analysis ---
        semantic: SemanticClauseInsight = self.semantic_model.evaluate_semantics(clause.text, clause.title)
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
            has_contractor_indemnifies = bool(_RE_CONTRACTOR_INDEMNIFIES.search(text))
            has_client_indemnifies = bool(_RE_CLIENT_INDEMNIFIES.search(text))
            has_attorney_fees = bool(_RE_ATTORNEY_FEES.search(text))
            has_any_and_all = bool(_RE_ANY_AND_ALL.search(text))

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
            has_disparity = bool(_RE_LIABILITY_DISPARITY.search(text))
            has_contractor_unlimited = bool(_RE_CONTRACTOR_UNLIMITED.search(text))
            caps_at_nominal = bool(_RE_NOMINAL_CAP.search(text))

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
            has_mandatory_arbitration = bool(_RE_MANDATORY_ARBITRATION.search(text))
            has_class_action_waiver = bool(_RE_CLASS_ACTION_WAIVER.search(text))
            has_jury_waiver = bool(_RE_JURY_WAIVER.search(text))

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
            has_immediate_convenience = bool(_RE_IMMEDIATE_CONVENIENCE.search(text))
            has_no_cure = bool(_RE_NO_CURE.search(text))

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
            has_prior_ip_grab = bool(_RE_PRE_EXISTING_IP.search(text))
            has_moral_rights_waiver = bool(_RE_MORAL_RIGHTS.search(text))
            has_work_for_hire = bool(_RE_WORK_FOR_HIRE.search(text))

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
            has_long_term = bool(_RE_LONG_TERM_NON_COMPETE.search(text))
            has_broad_geo = bool(_RE_BROAD_GEO_SCOPE.search(text))

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
            has_net_90 = bool(_RE_NET_PAYMENT_TERMS.search(text))
            has_subjective_approval = bool(_RE_SUBJECTIVE_WITHHOLDING.search(text))

            if has_net_90:
                score += 35
                reasons.append("Extended Payment Delay: Net 60/90 terms create substantial cash flow delays.")
                traps.append("Net-60+ Payment Delay Trap")
            if has_subjective_approval:
                score += 30
                reasons.append("Subjective Payment Withholding: Client may withhold payment based on sole discretion.")
                traps.append("Discretionary Payment / Clawback Trap")
            if not reasons:
                score += 10
                reasons.append("Standard invoicing, fee schedules, and milestone delivery terms.")

        # 8. Unclassified Boilerplate with Latent Risks
        if clause.category == ClauseCategory.GENERAL_BOILERPLATE:
            found_latent = [kw for kw in LATENT_RISK_KEYWORDS if kw in text]
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
            arch_name = semantic.top_archetype.replace("_", " ").title() if semantic.top_archetype else "Predatory Term"
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

        # Cap score between 5 and 98 to keep within realistic bounds
        final_score = max(5, min(98, score))

        if final_score >= 75:
            severity = RiskSeverity.CRITICAL if final_score >= 88 else RiskSeverity.HIGH
        elif final_score >= 45:
            severity = RiskSeverity.MEDIUM
        else:
            severity = RiskSeverity.LOW

        # Categorical confidence label
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
        self, evaluations: Optional[List[ClauseRiskEvaluation]]
    ) -> RiskOverview:
        """
        Calculates document-wide risk index, average confidence, and executive findings.
        Applies non-linear weighting (2.2x) to high/critical risk provisions to reflect true hazard.
        """
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
            ai_model_used="Local Privacy Shield & Semantic Heuristics",
        )
