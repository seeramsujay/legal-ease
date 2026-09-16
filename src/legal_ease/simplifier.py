"""
Plain-English translation engine and actionable legal guidance generator.
Demystifies dense contractual provisions for everyday users.
"""

from legal_ease.models import ClauseCategory, RiskSeverity


class PlainEnglishSimplifier:
    """
    Translates complex legalese into clear, conversational language,
    explaining real-world consequences and actionable negotiation strategies.
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
        title: str,
        text: str,
        traps: list[str],
    ) -> tuple[str, str, str]:
        """
        Generate (plain_english_summary, what_it_means_for_you, negotiation_tip).
        """
        lower = text.lower()

        # 1. Indemnification
        if category == ClauseCategory.INDEMNIFICATION or "indemnif" in lower:
            if "Unilateral Indemnification Trap" in traps or severity in (RiskSeverity.HIGH, RiskSeverity.CRITICAL):
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
            if "Uncapped / Asymmetric Liability Trap" in traps or severity in (RiskSeverity.HIGH, RiskSeverity.CRITICAL):
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
            if "Class Action Waiver" in traps or "Mandatory Arbitration Trap" in traps:
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
            if "Zero-Notice Termination Trap" in traps or severity in (RiskSeverity.HIGH, RiskSeverity.CRITICAL):
                summary = (
                    "Allows the other party to cancel the contract at any moment without warning or without giving "
                    "you a chance to fix any perceived issue."
                )
                impact = (
                    "You could dedicate weeks to planning and staffing this project, only to be dropped instantly "
                    "without compensation for work underway."
                )
                tip = (
                    "DEMAND 30-DAY NOTICE & KILL FEE: Add a clause requiring at least 14 to 30 days written notice "
                    "for termination without cause, full payment for all work performed to date, and a 15-day cure period for breaches."
                )
            else:
                summary = (
                    "Specifies how and when either party can exit the contract, including notice periods and handling of final payments."
                )
                impact = "Provides predictable off-ramps if either party fails to perform or priorities change."
                tip = "Ensure survival clauses clearly specify that payment obligations survive termination."
            return summary, impact, tip

        # 5. Intellectual Property
        if category == ClauseCategory.INTELLECTUAL_PROPERTY or "intellectual property" in lower:
            if "Pre-Existing IP Assignment Trap" in traps or severity in (RiskSeverity.HIGH, RiskSeverity.CRITICAL):
                summary = (
                    "Transfers ownership of everything you deliver, and potentially claims rights to your pre-existing "
                    "knowledge, tools, boilerplates, or code created outside this contract."
                )
                impact = (
                    "You could legally lose the right to reuse your own proprietary templates, libraries, or methodologies "
                    "with other clients in the future."
                )
                tip = (
                    "EXCLUDE BACKGROUND IP: Explicitly state that Contractor retains all rights in pre-existing IP, "
                    "tools, and general know-how, granting the client only an irrevocable license to use deliverables for their business."
                )
            else:
                summary = "Grants the client ownership of custom project deliverables upon full and final payment."
                impact = "Client owns what they specifically paid you to build, which is standard for work-for-hire."
                tip = "Ensure assignment of IP is strictly conditional upon *receipt of full payment*."
            return summary, impact, tip

        # 6. Restrictive Covenants / Non-Compete
        if category == ClauseCategory.RESTRICTIVE_COVENANTS or "non-compete" in lower:
            summary = (
                "Restricts you from working with competing companies or soliciting the client's customers or staff."
            )
            impact = (
                "Can severely block you from accepting jobs or clients in your primary field of expertise for months or years."
            )
            tip = (
                "NARROW SCOPE OR REMOVE: Limit non-solicitation only to direct employees actively engaged in the project, "
                "and push to eliminate non-competes entirely (often unenforceable under modern FTC / state rules)."
            )
            return summary, impact, tip

        # 7. Payment Terms
        if category == ClauseCategory.PAYMENT_TERMS or "payment" in lower:
            if "Net-60+ Payment Delay Trap" in traps:
                summary = (
                    "Requires you to wait 60 to 90+ days after submitting an invoice before receiving payment."
                )
                impact = "Forces you to effectively finance the client's project and strains your operating cash flow."
                tip = "PROPOSE NET-15 OR NET-30: Ask for standard Net 30 terms, with a 1.5% late fee per month on overdue invoices."
            else:
                summary = "Details the compensation rates, billing cadence, and reimbursement for expenses."
                impact = "Sets legal deadlines for invoice submissions and payments."
                tip = "Include milestone milestones with upfront retainer deposit where possible."
            return summary, impact, tip

        # Default fallback for general boilerplate
        summary = (
            f"Defines standard legal terms regarding {title.lower()}, establishing rights and obligations."
        )
        impact = (
            "Sets administrative and legal ground rules governing how the contract is interpreted and enforced."
        )
        tip = "Review carefully to ensure no hidden obligations or unfavorable jurisdiction clauses are buried here."
        return summary, impact, tip
