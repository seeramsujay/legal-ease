"""
Plain-English Translation Engine and Actionable Legal Guidance Generator.
Demystifies dense contractual provisions for freelancers, contractors, and SMBs.
Provides direct explanations of operational consequences and redline negotiation tips.
"""

from typing import Tuple, List, Optional
from legal_ease.models import ClauseCategory, RiskSeverity


class PlainEnglishSimplifier:
    """
    Translates complex legalese into clear, conversational language,
    explaining real-world consequences and actionable negotiation strategies.
    Guarantees null-safe execution across all contractual clause categories.
    """

    GLOSSARY = {
        "indemnify": "To financially reimburse the other party for their legal costs, judgments, or damages if someone sues them.",
        "hold harmless": "To promise not to sue or seek financial damages from the other party even if a problem occurs.",
        "consequential damages": "Indirect losses, like lost business revenue, missed opportunities, or reputational harm, separate from the immediate direct damage.",
        "liquidated damages": "A pre-agreed financial penalty that must be paid automatically if a specific breach occurs, without needing to prove actual losses in court.",
        "severability": "A standard rule stating that if one clause is found illegal by a judge, the rest of the contract remains valid and enforceable.",
        "force majeure": "A clause excusing parties from performance obligations due to unforeseeable catastrophic events (e.g. natural disasters, war).",
        "work made for hire": "A legal concept where the hiring company is legally considered the sole original author and owner of everything you create from the moment of creation.",
        "injunctive relief": "A court order forcing a party to immediately stop doing something (like sharing secrets or competing) rather than just paying financial compensation.",
    }

    def simplify(
        self,
        category: ClauseCategory,
        severity: RiskSeverity,
        title: Optional[str],
        text: Optional[str],
        traps: Optional[List[str]],
    ) -> Tuple[str, str, str]:
        """
        Generate (plain_english_summary, what_it_means_for_you, negotiation_tip).
        All returned strings are strictly non-null and conversational.
        """
        lower = text.lower() if text else ""
        trap_list = traps or []

        # 1. Indemnification
        if category == ClauseCategory.INDEMNIFICATION or "indemnif" in lower:
            if "Unilateral Indemnification Trap" in trap_list or severity in (RiskSeverity.HIGH, RiskSeverity.CRITICAL):
                summary = (
                    "You are agreeing to pay all legal defense costs, attorney fees, and settlement payouts "
                    "for the other party if any third party files a claim or lawsuit related to your work."
                )
                impact = (
                    "If someone sues your client because of your deliverables—even if the claim is unfounded—"
                    "you could be forced to pay hundreds of thousands in attorney fees out of your own pocket."
                )
                tip = (
                    "PROPOSE MUTUAL INDEMNITY & LIABILITY CAP: Ask to amend this clause to be mutual, "
                    "limit your indemnity strictly to your gross negligence or willful misconduct, and cap total indemnity "
                    "to the total compensation received under this agreement."
                )
            else:
                summary = (
                    "Outlines mutual protection against third-party claims, requiring each party to cover the other "
                    "if their own fault causes legal liability."
                )
                impact = (
                    "Provides standard defense coverage if your direct actions cause third-party losses."
                )
                tip = (
                    "Confirm the indemnity includes an obligation to provide prompt written notice of claims "
                    "and grants you control over the legal defense."
                )
            return summary, impact, tip

        # 2. Limitation of Liability
        if category == ClauseCategory.LIMITATION_OF_LIABILITY or "liability" in lower:
            if "Uncapped / Asymmetric Liability Trap" in trap_list or severity in (RiskSeverity.HIGH, RiskSeverity.CRITICAL):
                summary = (
                    "The counterparty strictly restricts the maximum damages you can ever collect from them, "
                    "while leaving your personal financial liability completely unlimited."
                )
                impact = (
                    "If they fail to pay or breach the deal, you can barely recover anything. But if they accuse you "
                    "of an issue, they can come after all your personal or business assets."
                )
                tip = (
                    "PROPOSE A MUTUAL AGGREGATE CAP: Insist on a mutual liability cap equal to 1x to 2x the fees "
                    "paid in the preceding 12 months, and delete any one-sided exclusions."
                )
            else:
                summary = (
                    "Caps direct damages and prevents either party from claiming lost profits, speculative losses, "
                    "or consequential damages."
                )
                impact = (
                    "Protects both parties from massive runaway liability beyond the actual contract value."
                )
                tip = "Ensure the cap applies equally to both sides and does not carve out excessive exceptions."
            return summary, impact, tip

        # 3. Dispute Resolution & Arbitration
        if category == ClauseCategory.DISPUTE_RESOLUTION or "arbitrat" in lower:
            if "Class Action Waiver" in trap_list or "Mandatory Arbitration Trap" in trap_list:
                summary = (
                    "Gives up your right to take disputes to a public court of law or jury trial. You must resolve "
                    "all claims through private binding arbitration and agree not to join class actions."
                )
                impact = (
                    "Private arbitration can cost thousands of dollars in administrative fees before a hearing even starts, "
                    "often favoring large corporations with repeat arbitrator relationships."
                )
                tip = (
                    "REQUEST LOCAL VENUE & MEDIATION STEP: Request a mandatory 30-day informal mediation period first, "
                    "and ensure any hearing takes place in your local jurisdiction or virtually over video."
                )
            else:
                summary = "Establishes the legal procedures and location for resolving disagreements between the parties."
                impact = "Sets expectations for where legal battles would take place if disputes escalate."
                tip = "Make sure the chosen jurisdiction and governing law is reasonable and accessible for you."
            return summary, impact, tip

        # 4. Termination
        if category == ClauseCategory.TERMINATION or "terminat" in lower:
            if "Zero-Notice Termination Trap" in trap_list or severity in (RiskSeverity.HIGH, RiskSeverity.CRITICAL):
                summary = (
                    "Allows the other party to cancel the contract at any moment without warning or without giving "
                    "you an opportunity to fix any perceived problem."
                )
                impact = (
                    "You could dedicate months of capacity, only to have the project pulled overnight with zero compensation "
                    "or safety net."
                )
                tip = (
                    "DEMAND A 30-DAY WRITTEN NOTICE & CURE PERIOD: Add terms requiring at least 30 days written notice "
                    "for termination for convenience, an immediate kill-fee covering work completed, and a 15-day cure period for breach."
                )
            else:
                summary = "Defines how either party can formally exit the agreement and specifies required notice periods."
                impact = "Governs the orderly wrap-up, transition of deliverables, and final payments upon project conclusion."
                tip = "Verify that all outstanding invoices are payable immediately upon early termination."
            return summary, impact, tip

        # 5. Intellectual Property
        if category == ClauseCategory.INTELLECTUAL_PROPERTY or "intellectual property" in lower or "work for hire" in lower:
            if "Pre-Existing IP Assignment Trap" in trap_list or severity in (RiskSeverity.HIGH, RiskSeverity.CRITICAL):
                summary = (
                    "Assigns ownership of everything you deliver, including your prior tools, libraries, code templates, "
                    "or trade secrets to the client."
                )
                impact = (
                    "You could legally lose the right to use your own background codebase, reusable design systems, "
                    "or internal tools on future client projects."
                )
                tip = (
                    "EXCLUDE BACKGROUND IP & GRANT A LICENSE: Insert an explicit carve-out for 'Contractor Pre-Existing Materials'. "
                    "Grant the client an irrevocable license to use your pre-existing tools rather than transferring full ownership."
                )
            else:
                summary = "Specifies who owns the custom work products, deliverables, and copyrights created under the contract."
                impact = "Guarantees client ownership of final deliverables upon full payment of all contractual fees."
                tip = "Condition the transfer of IP ownership on full and complete receipt of payment."
            return summary, impact, tip

        # 6. Restrictive Covenants / Non-Compete
        if category == ClauseCategory.RESTRICTIVE_COVENANTS or "non-compete" in lower or "non compete" in lower:
            summary = (
                "Restricts your freedom to work with competing companies, solicit clients, or take on similar "
                "projects in your industry after this contract ends."
            )
            impact = (
                "Could legally bar you from earning a living in your core specialty for months or years in your region."
            )
            tip = (
                "NARROW OR DELETE NON-COMPETE: Seek to eliminate non-compete clauses entirely (often unenforceable against contractors). "
                "If non-solicitation remains, limit it strictly to direct clients you personally worked with, for no more than 6-12 months."
            )
            return summary, impact, tip

        # 7. Payment Terms
        if category == ClauseCategory.PAYMENT_TERMS or "payment" in lower:
            if "Net-60+ Payment Delay Trap" in trap_list or "Discretionary Payment Trap" in trap_list:
                summary = (
                    "Sets prolonged payment terms (e.g. Net-60/90) or allows the counterparty to withhold payments based "
                    "on subjective approval."
                )
                impact = (
                    "Creates severe cash-flow strain by delaying your compensation 2 to 3 months after work is delivered, "
                    "with risk of arbitrary non-payment."
                )
                tip = (
                    "ENFORCE NET-15/30 & DEPOSIT: Insist on standard Net-15 or Net-30 payment terms with a late fee of 1.5% per month, "
                    "and require objective milestone acceptance criteria with a 10-day deemed approval window."
                )
            else:
                summary = "Defines billing schedules, payment methods, invoice terms, and reimbursement for expenses."
                impact = "Dictates how and when you get paid for your work."
                tip = "Ensure expenses require prior written approval and invoices are deemed accepted if not disputed within 10 days."
            return summary, impact, tip

        # 8. General Boilerplate / Default
        clean_title = title.strip() if title else "General Terms"
        summary = f"Standard contractual terms governing {clean_title}."
        impact = "Operational provision setting procedural expectations and administrative guidelines."
        tip = "Review carefully to ensure operational feasibility and absence of hidden obligations."
        return summary, impact, tip
