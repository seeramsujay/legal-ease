"""
Attorney Consultation Brief and Negotiation Checklist Generator.
Prepares structured, high-value questions and exposure summaries for legal counsel.
"""

from typing import List
from legal_ease.models import (
    ClauseAnalysis,
    RiskOverview,
    AttorneyChecklist,
    AttorneyQuestion,
    RiskSeverity,
)
from legal_ease.guardrails import get_attorney_prep_note, get_standard_disclaimer


class AttorneyChecklistGenerator:
    """
    Synthesizes clause risk analyses into an actionable, lawyer-ready consultation brief.
    Enables users to walk into a legal consultation prepared, minimizing billed hours.
    """

    def generate(
        self,
        document_title: str,
        risk_overview: RiskOverview,
        clauses: List[ClauseAnalysis],
    ) -> AttorneyChecklist:
        """Generate structured attorney questions and Markdown consultation brief."""
        questions: List[AttorneyQuestion] = []
        top_exposures: List[str] = []
        priority_negotiation_items: List[str] = []

        # Filter high and critical risk clauses
        high_risk_clauses = [
            c for c in clauses if c.severity in (RiskSeverity.HIGH, RiskSeverity.CRITICAL)
        ]

        # 1. Examine High-Risk Clauses for Targeted Attorney Questions
        for clause in high_risk_clauses:
            top_exposures.extend(clause.detected_traps)

            if "indemnif" in clause.section_title.lower() or "indemnif" in clause.original_text.lower():
                questions.append(
                    AttorneyQuestion(
                        category="Indemnification & Third-Party Claims",
                        related_clause_id=clause.id,
                        question=(
                            "Is this indemnification obligation standard for this type of agreement in our jurisdiction, "
                            "and can we safely negotiate it to be mutual and capped to our aggregate fees received?"
                        ),
                        why_it_matters=(
                            "Uncapped unilateral indemnity exposes personal/company assets to defending third-party "
                            "lawsuits even without proven wrongdoing."
                        ),
                        recommended_fallback=(
                            "Propose standard mutual indemnity limited to gross negligence, subject to the overall liability cap."
                        ),
                    )
                )
                priority_negotiation_items.append(
                    f"Section '{clause.section_title}': Convert unilateral indemnity to mutual and insert liability cap."
                )

            if "liability" in clause.section_title.lower() or "liability" in clause.original_text.lower():
                questions.append(
                    AttorneyQuestion(
                        category="Limitation of Liability",
                        related_clause_id=clause.id,
                        question=(
                            "How enforceable is this asymmetric limitation of liability, and what wording would you recommend "
                            "to make the liability cap bilateral?"
                        ),
                        why_it_matters=(
                            "Leaving contractor liability uncapped while counterparty caps at a nominal amount creates catastrophic imbalance."
                        ),
                        recommended_fallback=(
                            "Mutual aggregate liability cap equal to 100% of fees paid under the contract in the preceding 12 months."
                        ),
                    )
                )
                priority_negotiation_items.append(
                    f"Section '{clause.section_title}': Establish an equal, mutual aggregate dollar liability cap."
                )

            if "arbitrat" in clause.section_title.lower() or "dispute" in clause.section_title.lower():
                questions.append(
                    AttorneyQuestion(
                        category="Dispute Resolution & Venue",
                        related_clause_id=clause.id,
                        question=(
                            "Does mandatory arbitration in the counterparty's chosen venue place us at a material procedural disadvantage, "
                            "and should we stipulate informal mediation first?"
                        ),
                        why_it_matters=(
                            "Out-of-state arbitration upfront administrative costs can easily surpass the total value of disputed fees."
                        ),
                        recommended_fallback=(
                            "Add 30-day executive escalation and mediation clause; permit remote virtual arbitration proceedings."
                        ),
                    )
                )
                priority_negotiation_items.append(
                    f"Section '{clause.section_title}': Insert mediation pre-condition and allow remote virtual hearings."
                )

            if "terminat" in clause.section_title.lower():
                questions.append(
                    AttorneyQuestion(
                        category="Termination & Kill Fees",
                        related_clause_id=clause.id,
                        question=(
                            "What standard cure period and notice window should we enforce to prevent arbitrary zero-notice cancellation?"
                        ),
                        why_it_matters=(
                            "Without a notice period or kill fee, time spent reserving capacity and starting work is unprotected."
                        ),
                        recommended_fallback=(
                            "Require 30 days written notice for convenience, immediate payment for work-in-progress, and 15 days cure for breach."
                        ),
                    )
                )
                priority_negotiation_items.append(
                    f"Section '{clause.section_title}': Add 30-day written notice requirement and payment guarantee for work completed."
                )

            if "intellectual" in clause.section_title.lower() or "ip" in clause.section_title.lower():
                questions.append(
                    AttorneyQuestion(
                        category="Intellectual Property Retention",
                        related_clause_id=clause.id,
                        question=(
                            "Does this work-for-hire assignment unintentionally transfer rights to our pre-existing code, tools, and methodologies?"
                        ),
                        why_it_matters=(
                            "Assigning background IP prevents reuse of your own core tools with subsequent clients."
                        ),
                        recommended_fallback=(
                            "Carve out 'Background Technology and Pre-Existing Materials', granting client a non-exclusive license only."
                        ),
                    )
                )
                priority_negotiation_items.append(
                    f"Section '{clause.section_title}': Explicitly carve out background IP and tie deliverable ownership to receipt of full payment."
                )

        # Fallback question if contract is relatively low risk
        if not questions:
            questions.append(
                AttorneyQuestion(
                    category="General Contract Hygiene",
                    related_clause_id=None,
                    question=(
                        "Are there any jurisdiction-specific implied warranties or statutory compliance terms missing from this agreement?"
                    ),
                    why_it_matters="Ensures comprehensive protection under local governing statutes.",
                    recommended_fallback="Standard mutual boilerplate terms.",
                )
            )
            priority_negotiation_items.append("Confirm governing law matches preferred local courts.")

        # Deduplicate top exposures
        unique_exposures = list(dict.fromkeys(top_exposures))
        if not unique_exposures:
            unique_exposures = ["Standard contract provisions; no severe unilateral traps identified."]

        # Generate human-readable Markdown Report
        markdown_lines = [
            f"# ⚖️ Attorney Consultation Brief: {document_title}",
            "",
            f"> **Legal Risk Index:** {risk_overview.legal_risk_index}/100 ({risk_overview.risk_level.value})  ",
            f"> **Date Generated:** Automated Triage  ",
            "",
            "---",
            "",
            "## 🚨 Executive Summary of Document Exposures",
            risk_overview.executive_summary,
            "",
            "### Critical Risk Flags Identified:",
            *[f"- **{flag}**" for flag in risk_overview.critical_findings],
            "",
            "---",
            "",
            "## 💬 Prepared Questions for Your Attorney Consultation",
            "*(Take these prioritized questions into your legal review meeting to maximize productivity)*",
            "",
        ]

        for i, q in enumerate(questions, 1):
            markdown_lines.extend(
                [
                    f"### {i}. [{q.category}]",
                    f"**Question for Counsel:** {q.question}",
                    f"- **Why It Matters:** {q.why_it_matters}",
                    f"- **Recommended Fallback:** `{q.recommended_fallback}`",
                    "",
                ]
            )

        markdown_lines.extend(
            [
                "---",
                "",
                "## 📝 Priority Counter-Proposal Checklist (Redlines)",
                *[f"- [ ] {item}" for item in priority_negotiation_items],
                "",
                "---",
                "",
                f"> **Notice:** {get_attorney_prep_note()}",
                f"> ",
                f"> **Disclaimer:** {get_standard_disclaimer()}",
            ]
        )

        markdown_report = "\n".join(markdown_lines)

        return AttorneyChecklist(
            document_title=document_title,
            overall_risk_index=risk_overview.legal_risk_index,
            top_exposures=unique_exposures,
            questions_for_counsel=questions,
            priority_negotiation_items=priority_negotiation_items,
            markdown_report=markdown_report,
        )
