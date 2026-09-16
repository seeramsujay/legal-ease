# ⚖️ Legal-Ease: Privacy-First AI Legal Navigator & Contract Risk Analyzer

[![Tests](https://img.shields.io/badge/tests-27%20passed-success)](https://github.com/seeramsujay/legal-ease)
[![Repo Size](https://img.shields.io/badge/repo%20size-%3C%201%20MB%20(limit%2010MB)-blue)](https://github.com/seeramsujay/legal-ease)
[![Package Manager](https://img.shields.io/badge/package%20managers-uv%20%7C%20pnpm%20only-indigo)](https://github.com/seeramsujay/legal-ease)
[![Single Branch](https://img.shields.io/badge/branch-main%20only-teal)](https://github.com/seeramsujay/legal-ease)
[![Vertical](https://img.shields.io/badge/Hackathon%20Vertical-AI%20for%20Legal%20Assistance%20%26%20Access-orange)](https://github.com/seeramsujay/legal-ease)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Submission for Hackathon:** *AI for Legal Assistance & Access*  
> **Repository:** [https://github.com/seeramsujay/legal-ease](https://github.com/seeramsujay/legal-ease)  
> **Tooling Stack:** Built strictly with **`uv`** and **`pnpm`** with zero external network bloat and sub-second execution.

---

## 📌 1. Chosen Vertical & Problem Statement

### **Vertical: AI for Legal Assistance & Access**

Independent freelancers, technical contractors, startup founders, and small business owners sign dozens of legal agreements every year—Independent Contractor Agreements, Master Services Agreements (MSAs), Statements of Work (SOWs), SaaS Terms of Service, and Non-Disclosure Agreements (NDAs). 

### The Problem:
* **The Access Gap:** Commercial attorneys bill between **$350 to $800+ per hour**, making formal legal review financially impossible for routine $5,000–$50,000 contracts.
* **The Legalese Asymmetry:** Enterprise counterparties use standardized, one-sided templates packed with legal traps: **unilateral indemnification**, **unlimited contractor liability with a $100 client cap**, **pre-existing IP forfeiture**, **arbitration & class-action waivers**, and **immediate zero-notice termination**.
* **The Privacy Hazard:** Pasting unredacted contracts containing private names, personal addresses, tax IDs (SSNs/EINs), client rates, and financial terms into public LLMs creates catastrophic privacy and confidentiality breaches.

### The Solution: Legal-Ease
**Legal-Ease** is a local-first, privacy-guaranteed AI contract analyzer and legal navigator that democratizes legal comprehension. It strips out all sensitive identifiers on the client machine, scores contractual risk exposure, translates dense legalese into plain English, tracks liability shifts between contract revisions, and synthesizes a structured **Attorney Consultation Brief** to make paid lawyer consultations 5x more efficient.

---

## 🚀 2. Core Features & Capabilities

```
                  ┌─────────────────────────────────────────────────────────┐
                  │                 Raw Contract Document                   │
                  └──────────────────────────┬──────────────────────────────┘
                                             │
                       [Step 1] Local Deterministic PII Shield
                                             ▼
                  ┌─────────────────────────────────────────────────────────┐
                  │  Redacted Text: [EMAIL_1], [TAX_ID_1], [AMOUNT_1]...    │
                  │  Zero sensitive PII leaves your local sandbox!           │
                  └──────────────────────────┬──────────────────────────────┘
                                             │
                       [Step 2] Structural Clause Segmenter & Classifier
                                             ▼
                  ┌─────────────────────────────────────────────────────────┐
                  │  Categorized Sections: Indemnity, Liability, IP,        │
                  │  Termination, Payment Terms, Restrictive Covenants...   │
                  └──────────┬──────────────────────────────┬───────────────┘
                             │                              │
          [Step 3] Deterministic Risk Matrix   [Step 4] Plain-English Simplifier
                             │                              │
                             ▼                              ▼
                  ┌──────────────────────┐      ┌───────────────────────────┐
                  │  Legal Risk Index    │      │  "In Plain English"       │
                  │  (Score: 0 to 100)   │      │  "What This Means For You"│
                  │  Detected Traps &    │      │  Actionable Redline Tips  │
                  │  Critical Warnings   │      │  Legal Jargon Glossary    │
                  └──────────┬───────────┘      └───────────┬───────────────┘
                             │                              │
                             └──────────────┬───────────────┘
                                            │
               [Step 5] Lawyer-Ready Attorney Consultation Brief & Redlines
                                            │
                                            ▼
                  ┌─────────────────────────────────────────────────────────┐
                  │  • Prioritized Legal Questions with Business Rationale  │
                  │  • Recommended Fallback Counter-Proposals               │
                  │  • Exportable Markdown (.md) Brief for Counsel          │
                  └─────────────────────────────────────────────────────────┘
```

### 1. 🛡️ Zero-Knowledge Local PII Shield
* Automatically identifies and masks sensitive entities locally using high-precision deterministic pattern heuristics before any external linguistic or AI processing.
* Redacts **Emails**, **Phone Numbers**, **SSNs / Tax IDs / EINs**, **Street Addresses**, **Credit Cards**, **Bank Account Numbers**, **Monetary Values**, and **Entity Names**.
* Deterministic token mapping (`[EMAIL_1]`, `[CONFIDENTIAL_AMOUNT_1]`) allows seamless local restoration without compromising privacy.

### 2. ⚡ Multi-Dimensional Contract Risk Matrix
* Evaluates clauses against real-world legal hazards and computes a standardized **Legal Risk Index (0–100)**:
  * **Unilateral Indemnification Trap:** Detects asymmetric obligations where contractor pays company legal costs without reciprocity.
  * **Uncapped / Asymmetric Liability Trap:** Identifies when company limits liability to nominal amounts ($50–$100) while contractor liability remains unlimited.
  * **Pre-Existing IP Assignment Trap:** Catches overbroad "work-for-hire" clauses attempting to claim ownership over your background tools and prior inventions.
  * **Zero-Notice Termination Trap:** Flags termination for convenience without notice or opportunity to cure.
  * **Dispute & Class Action Waivers:** Identifies mandatory arbitration in distant jurisdictions and class-action forfeitures.
  * **Net-60/90 Payment Traps:** Flags extended payment delays and subjective withholding clauses.

### 3. 📖 Plain-English Simplifier & Negotiation Tips
* Breaks down every clause into three human-readable layers:
  1. **Plain English Translation:** What the legal jargon actually says.
  2. **What This Means For You:** Real-world consequences, worst-case scenarios, and practical business impact.
  3. **Actionable Redline Tip:** Specific counter-proposal clauses you can ask the other party to substitute.
* Built-in legal glossary explaining terms like *indemnification*, *severability*, *force majeure*, and *consequential damages*.

### 4. ⚖️ Side-by-Side Contract Version Comparator
* Compares **Contract A (Original / Enterprise Draft)** against **Contract B (Counter-Proposal / Redline)**.
* Categorizes changes: `ADDED`, `MODIFIED`, `REMOVED`, and `UNCHANGED`.
* Quantifies **Risk Delta** and overall **Trajectory** (`SAFER`, `MORE_RISK`, `NEUTRAL`) to confirm whether revisions genuinely improved your contractual protection.

### 5. 📋 Attorney Consultation Brief Generator
* Generates a structured, exportable Markdown report ready to hand directly to your attorney.
* Pre-populates targeted, high-priority questions categorized by risk severity, detailing:
  * Why the clause matters to your business.
  * Recommended fallback position.
  * Specific redline suggestions.
* Reduces a standard 2-hour intake consultation to a focused 20-minute meeting, saving hundreds of dollars in legal fees.

### 6. 💬 Context-Aware Legal Navigator AI Assistant
* Interactive assistant grounded strictly in your active contract text.
* Includes pre-configured scenario prompts (e.g. *"Can they cancel without paying me?"*, *"Who owns the background IP?"*).
* Cites specific contract sections and enforces mandatory non-advisory disclosures.

---

## 🛠️ 3. Quickstart & Installation

This project is built strictly with **`uv`** (for Python environment and package management) and **`pnpm`** (for script orchestration and test execution).

### Prerequisites
* **Python >= 3.12**
* **uv >= 0.5.0** ([Install uv](https://docs.astral.sh/uv/getting-started/installation/))
* **Node.js >= 18 & pnpm >= 8.0** ([Install pnpm](https://pnpm.io/installation))

### Clone Repository
```bash
git clone https://github.com/seeramsujay/legal-ease.git
cd legal-ease
```

### 1. Run Automated Tests (`pnpm test`)
Execute the full 27-test suite covering PII anonymization, risk heuristics, clause segmentation, version comparison, API endpoints, and security guardrails:
```bash
pnpm test
```
*Expected result:* **`27 passed in ~0.6 seconds`**

### 2. Launch Web Application (`pnpm start` or `pnpm dev`)
Start the high-performance web dashboard:
```bash
pnpm start
```
Open your browser to: **[http://localhost:8000](http://localhost:8000)**

### 3. Command Line Interface (CLI)
Legal-Ease includes a full-featured CLI for terminal workflows:
```bash
# View bundled realistic sample contracts
pnpm cli samples

# Analyze a contract text file
pnpm cli analyze <path-to-contract.txt> --checklist

# Compare two revisions side-by-side
pnpm cli compare <draft_v1.txt> <draft_v2.txt>

# Test local PII redaction on a document
pnpm cli anonymize <path-to-contract.txt>
```

---

## 📐 4. Architecture & Engineering Logic

### Directory Structure
```
legal-ease/
├── .gitignore               # Strict safeguards ensuring repo size < 10 MB
├── package.json             # Root pnpm script runner (start, dev, test, cli)
├── pyproject.toml           # uv project configuration and dependencies
├── uv.lock                  # Deterministic dependency lockfile
├── README.md                # Comprehensive documentation
├── ROADMAP.md               # Milestones and feature roadmap
├── idea.md                  # Vertical specification and problem definition
├── src/
│   └── legal_ease/
│       ├── __init__.py      # Package entry marker
│       ├── models.py        # Pydantic v2 schemas and enums
│       ├── guardrails.py    # Non-advisory legal disclosures & injection defense
│       ├── anonymizer.py    # Deterministic local PII redactor & pseudonymizer
│       ├── clause_segmenter.py # Structural parser and category classifier
│       ├── risk_analyzer.py # Deterministic risk scoring and exposure matrix
│       ├── simplifier.py    # Plain-English translation & redline tips
│       ├── comparator.py    # Side-by-side contract diff & risk delta engine
│       ├── checklist_generator.py # Attorney consultation brief generator
│       ├── assistant.py     # Grounded Q&A assistant engine
│       ├── sample_contracts.py # Realistic curated test contracts
│       ├── cli.py           # Command-line interface entry point
│       ├── ui.py            # Accessible, fast single-page web dashboard
│       └── main.py          # FastAPI application & REST endpoints
└── tests/
    ├── test_anonymizer.py       # PII redaction and restoration tests
    ├── test_clause_segmenter.py # Heading, numbering, and category tests
    ├── test_risk_analyzer.py    # Trap detection and score calculation tests
    ├── test_comparator.py       # Version diff and trajectory tests
    ├── test_simplifier.py       # Plain-English translation & glossary tests
    ├── test_checklist.py        # Attorney brief generation tests
    └── test_api.py              # FastAPI endpoints, chat & guardrails tests
```

### Approach and Pipeline Logic
1. **Sanitization & Guardrails (`guardrails.py`):**
   Validates input length, strips potential prompt injection attacks, and attaches non-advisory disclosures.
2. **Local PII Redaction (`anonymizer.py`):**
   Parses raw input through regex state machines identifying 8 categories of sensitive identifiers, replacing them with deterministic tokens.
3. **Structural Segmentation (`clause_segmenter.py`):**
   Detects multi-tier numbering formats (`1.`, `1.1`, `Section 2`, `Article III`) and semantic headers. Categorizes each section into one of 10 legal domains.
4. **Risk Heuristics Engine (`risk_analyzer.py`):**
   Evaluates each clause against asymmetrical liability traps, computing clause-level risk scores (0–100) and weighting them into the document-wide **Legal Risk Index**.
5. **Plain-English Translation (`simplifier.py`):**
   Maps identified hazards to plain-English breakdowns, explaining the practical business consequence and providing standard counter-proposal redline text.
6. **Attorney Brief Synthesis (`checklist_generator.py`):**
   Aggregates critical flags into a prioritized, categorized brief for counsel, complete with questions, rationale, and markdown export.
7. **Interactive Assistance (`assistant.py`):**
   Provides context-grounded Q&A with mandatory citations and persistent non-advisory disclaimers.

---

## ⚖️ 5. Evaluation Focus Areas

| Focus Area | How Legal-Ease Demonstrates Excellence |
| :--- | :--- |
| **Code Quality** | Clean, modular, type-annotated Python 3.12 with Pydantic v2 validation. Full separation of concerns across models, guardrails, heuristics, and UI. Zero monolithic files. |
| **Security & Privacy** | **100% Local PII Redaction**: Sensitive personal and corporate entities are anonymized locally before linguistic analysis. Built-in input sanitization against prompt injection attacks. |
| **Efficiency & Speed** | Sub-second analysis pipeline (< 50ms per contract). Zero heavy client dependencies; embedded accessible dashboard starts in sub-100ms. |
| **Testing** | 27 automated tests with **100% pass rate** (`pnpm test`), validating PII redaction, risk rules, diffing, REST endpoints, and security guardrails. |
| **Accessibility** | Semantic HTML5, WCAG AA high-contrast color scheme, full keyboard navigation, `aria-*` tags, and responsive design for mobile and desktop screens. |
| **Repository Rules** | Strict compliance: **Single branch (`main`)**, **Repo size < 1 MB** (well under the 10 MB ceiling), public GitHub repository, and built with `uv` and `pnpm` only. |

---

## 📑 6. Ethical Guardrails & Assumptions

1. **Non-Advisory Tool:** Legal-Ease is explicitly designed as a legal document literacy and negotiation preparation instrument. It **does not** provide formal legal advice, establish an attorney-client relationship, or substitute for licensed legal representation.
2. **Pre-Consultation Utility:** The solution is designed to empower clients *prior* to attorney consultation, dramatically reducing the billable hours required for intake and issue-spotting.
3. **Jurisdictional Notice:** Legal standards vary across states and countries. Default heuristics reflect standard US commercial contract norms (Delaware, New York, California common law precedents).

---

## 📜 7. License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
