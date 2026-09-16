"""
Deterministic contract risk scoring and exposure assessment engine.
Evaluates clauses against real-world legal trap heuristics.
"""

import re
from typing import List, Tuple
from legal_ease.models import (
    ClauseCategory,
    RiskSeverity,
    RiskOverview,
)
from legal_ease.clause_segmenter import RawClause


class ClauseRiskEvaluation:
    def __init__(
        self,
        risk_score: int,
        severity: RiskSeverity,
        reasons: List[str],
        traps: List[str],
    ):
        self.risk_score = risk_score
        self.severity = severity
        self.reasons = reasons
        self.traps = traps


class RiskAnalyzer:
    """
    Evaluates contract clauses using deterministic pattern matching,
    severity weighing, and document-wide risk index calculation.
    """

    def evaluate_clause(self, clause: RawClause) -> ClauseRiskEvaluation:
        """Evaluate a single raw clause and compute its risk score and identified traps."""
        text = clause.text.lower()
        score = 15  # Baseline standard score
        reasons: List[str] = []
        traps: List[str] = []

        # 1. Indemnification traps
        if clause.category == ClauseCategory.INDEMNIFICATION or "indemnif" in text:
            has_contractor_indemnifies = bool(
                re.search(
                    r"(contractor|consultant|employee|vendor|provider|licensee|user)\s+(shall|agrees to)\s+indemnif",
                    text,
                )
            )
            has_client_indemnifies = bool(
                re.search(
                    r"(client|company|customer|employer|licensor)\s+(shall|agrees to)\s+indemnif",
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
            elif "indemnif" in text:
                score += 25
                reasons.append("Contains indemnification obligations requiring financial defense.")

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
            elif caps_at_nominal:
                score += 45
                reasons.append(
                    "Nominal Recovery Cap: Recovery against counterparty is capped at a negligible sum (e.g. $100 or 1 month fees)."
                )
                traps.append("Nominal Liability Cap Trap")
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
            has_long_term = bool(
                re.search(r"(?:2|3|4|5|two|three)\s+years", text)
            )
            has_broad_geo = bool(
                re.search(r"worldwide|entire\s+world|any\s+geographic\s+area|nationwide", text)
            )

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

        # Cap score between 0 and 100
        final_score = max(5, min(98, score))

        if final_score >= 75:
            severity = RiskSeverity.CRITICAL if final_score >= 88 else RiskSeverity.HIGH
        elif final_score >= 45:
            severity = RiskSeverity.MEDIUM
        else:
            severity = RiskSeverity.LOW

        if not reasons:
            reasons.append("Standard contract provision without elevated liability flags.")

        return ClauseRiskEvaluation(
            risk_score=final_score,
            severity=severity,
            reasons=reasons,
            traps=traps,
        )

    def calculate_overview(
        self, evaluations: List[ClauseRiskEvaluation]
    ) -> RiskOverview:
        """Calculate document-wide risk index and executive findings."""
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
            )

        total_clauses = len(evaluations)
        high_count = sum(1 for e in evaluations if e.severity in (RiskSeverity.HIGH, RiskSeverity.CRITICAL))
        med_count = sum(1 for e in evaluations if e.severity == RiskSeverity.MEDIUM)
        low_count = sum(1 for e in evaluations if e.severity == RiskSeverity.LOW)

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
                f"LOW RISK AGREEMENT ({risk_index}/100): Balanced contractual terms with {low_count} standard "
                "provisions. Minimal unilateral risk detected; terms generally conform to industry best practices."
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
        )
