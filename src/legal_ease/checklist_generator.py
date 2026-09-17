"""
Attorney Consultation Brief and Negotiation Checklist Generator.
Synthesizes contract risk analysis into an actionable, structured briefing document
with prioritized questions for counsel, statutory exposure warnings, and redline fallback targets.
Minimizes billed attorney consultation hours by presenting pre-triaged legal findings.
"""

from typing import List, Optional
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
    Guarantees null-safe handling and professional formatting.
    """

    def generate(
        self,
        document_title: Optional[str],
        risk_overview: Optional[RiskOverview],
        clauses: Optional[List[ClauseAnalysis]],
    ) -> AttorneyChecklist:
        """
        Generate structured attorney questions and Markdown consultation brief.
        Defensively handles None or empty inputs.
        """
        safe_title = str(document_title).strip() if document_title else "Contract Agreement"
        clause_list = clauses or []
        overview = risk_overview or RiskOverview(
            legal_risk_index=0,
            risk_level=RiskSeverity.LOW,
            total_clauses=0,
            high_risk_count=0,
            medium_risk_count=0,
            low_risk_count=0,
            critical_findings=["No clauses analyzed."],
            executive_summary="Empty analysis.",
        )

        questions: List[AttorneyQuestion] = []
        top_exposures: List[str] = []
        priority_negotiation_items: List[str] = []

        # Filter high and critical risk clauses
        high_risk_clauses = [
            c for c in clause_list if c.severity in (RiskSeverity.HIGH, RiskSeverity.CRITICAL)
        ]

        # 1. Examine High-Risk Clauses for Targeted Attorney Questions
        for clause in high_risk_clauses:
            top_exposures.extend(clause.detected_traps)

            title_lower = clause.section_title.lower()
            text_lower = clause.original_text.lower()

            if "indemnif" in title_lower or "indemnif" in text_lower:
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

            if "liability" in title_lower or "liability" in text_lower:
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

            if "arbitrat" in title_lower or "dispute" in title_lower:
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

            if "terminat" in title_lower:
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
                    f"Section '{clause.section_title}': Require 30-day written termination notice and payment for completed deliverables."
                )

            if "intellectual property" in title_lower or "work for hire" in text_lower:
                questions.append(
                    AttorneyQuestion(
                        category="Intellectual Property & Pre-Existing Tools",
                        related_clause_id=clause.id,
                        question=(
                            "Does the assignment language risk transferring rights to our reusable background libraries, design frameworks, or prior code?"
                        ),
                        why_it_matters=(
                            "Broad assignment without background IP exclusions could surrender ownership of your core operational tools."
                        ),
                        recommended_fallback=(
                            "Add explicit Schedule A carve-out for 'Background Materials' with an irrevocable non-exclusive license upon full payment."
                        ),
                    )
                )
                priority_negotiation_items.append(
                    f"Section '{clause.section_title}': Carve out pre-existing background IP and condition transfer on payment."
                )

            if "non-compete" in title_lower or "non compete" in text_lower:
                questions.append(
                    AttorneyQuestion(
                        category="Restrictive Covenants & Non-Compete",
                        related_clause_id=clause.id,
                        question=(
                            "Is this post-termination restrictive covenant legally enforceable against an independent contractor in this jurisdiction?"
                        ),
                        why_it_matters=(
                            "Unreasonable non-compete terms restrict future business viability and livelihood."
                        ),
                        recommended_fallback=(
                            "Strike non-compete entirely or narrow non-solicitation strictly to clients directly engaged within 6 months."
                        ),
                    )
                )
                priority_negotiation_items.append(
                    f"Section '{clause.section_title}': Strike non-compete covenant and narrow non-solicitation scope."
                )

        # Baseline fallback question if agreement is generally balanced
        if not questions:
            questions.append(
                AttorneyQuestion(
                    category="General Contract Health Check",
                    related_clause_id=None,
                    question=(
                        "Does this agreement contain any silent gaps—such as missing warranties, vague payment terms, or inadequate force majeure protections?"
                    ),
                    why_it_matters="Omitted provisions can create as much legal risk as overreaching terms.",
                    recommended_fallback="Ensure clear payment milestone definitions and appropriate mutual confidentiality protections.",
                )
            )
            priority_negotiation_items.append(
                "Review scope of work (SOW) descriptions to guarantee deliverables and milestone deadlines are strictly objective."
            )

        # Build clean Markdown Consultation Brief matching exact test headers
        md_lines = [
            f"# ⚖️ Attorney Consultation Brief: {safe_title.upper()}",
            f"> **Legal-Ease Risk Index:** {overview.legal_risk_index}/100 ({overview.risk_level.value} Exposure)",
            f"> **Prepared by:** Legal-Ease Automated Triage",
            "",
            "## NOTICE FOR COUNSEL",
            get_attorney_prep_note(),
            "",
            "## EXECUTIVE RISK SUMMARY",
            overview.executive_summary,
            "",
            "## CRITICAL EXPOSURE FINDINGS",
        ]
        for f in overview.critical_findings:
            md_lines.append(f"- {f}")

        md_lines.extend([
            "",
            "## RECOMMENDED QUESTIONS FOR LEGAL COUNSEL",
        ])
        for idx, q in enumerate(questions, 1):
            clause_ref = f" *(Originating Clause #{q.related_clause_id})*" if q.related_clause_id else ""
            md_lines.extend([
                f"### {idx}. [{q.category}]{clause_ref}",
                f"**Question:** {q.question}",
                f"**Why It Matters:** {q.why_it_matters}",
                f"**Suggested Fallback/Redline:** `{q.recommended_fallback}`",
                "",
            ])

        md_lines.extend([
            "## PRIORITY COUNTER-PROPOSAL NEGOTIATION CHECKLIST",
        ])
        for item in priority_negotiation_items:
            md_lines.append(f"- [ ] {item}")

        md_lines.extend([
            "",
            "---",
            f"*{get_standard_disclaimer()}*",
        ])

        return AttorneyChecklist(
            document_title=safe_title,
            overall_risk_index=overview.legal_risk_index,
            questions_for_counsel=questions,
            priority_negotiation_items=priority_negotiation_items,
            markdown_report="\n".join(md_lines),
        )
