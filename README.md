# ⚖️ Legal-Ease: Privacy-First AI Legal Navigator & Contract Risk Analyzer

[![Tests](https://img.shields.io/badge/tests-32%20passed-success)](https://github.com/seeramsujay/legal-ease)
[![Repo Size](https://img.shields.io/badge/repo%20size-%3C%201%20MB%20(limit%2010MB)-blue)](https://github.com/seeramsujay/legal-ease)
[![Package Manager](https://img.shields.io/badge/package%20managers-uv%20%7C%20pnpm%20only-indigo)](https://github.com/seeramsujay/legal-ease)
[![Single Branch](https://img.shields.io/badge/branch-main%20only-teal)](https://github.com/seeramsujay/legal-ease)
[![Vertical](https://img.shields.io/badge/Hackathon%20Vertical-AI%20for%20Legal%20Assistance%20%26%20Access-orange)](https://github.com/seeramsujay/legal-ease)
[![AI Engine](https://img.shields.io/badge/AI%20Engine-Local%20Heuristics%20%2B%20NVIDIA%20Nemotron-purple)](https://github.com/seeramsujay/legal-ease)
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

## 🧠 2. Local-First Verification + Nemotron Deep Escalation Architecture

Legal-Ease operates on a **hybrid local-first architecture with confidence-based escalation**:

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
                  └──────────────────────────┬──────────────────────────────┘
                                             │
                       [Step 3] Local Heuristics & Confidence Scoring
                                             │
                   ┌─────────────────────────┴─────────────────────────┐
                   ▼                                                   ▼
       Local Confidence >= 75%                             Local Confidence < 75%
      (Standard / Clear Traps)                           (Ambiguity / Edge Cases)
                   │                                                   │
                   │                                       [Step 4] PII-Safe Escalation
                   │                                                   ▼
                   │                                       ┌───────────────────────┐
                   │                                       │    NVIDIA NEMOTRON    │
                   │                                       │  OpenAI-Compatible LLM│
                   │                                       │ (Deep Legal Reasoning)│
                   │                                       └───────────┬───────────┘
                   │                                                   │
                   └─────────────────────────┬─────────────────────────┘
                                             │
                       [Step 5] Synthesized Risk & Translation Layer
                                             ▼
                  ┌─────────────────────────────────────────────────────────┐
                  │  • Standardized Legal Risk Index (0 - 100)               │
                  │  • Plain-English Translation & "What It Means For You"   │
                  │  • Actionable Negotiation Counter-Proposal Tips          │
                  │  • Lawyer-Ready Attorney Consultation Brief (.md)        │
                  └─────────────────────────────────────────────────────────┘
```

### Routing Logic:
1. **Local Heuristics (High Confidence >= 75%):**
   * Instant, sub-millisecond evaluation on your device.
   * Standard clauses and definitive trap patterns (e.g. unilateral indemnity, Delaware AAA arbitration) are resolved locally with zero cloud dependencies.
2. **Nemotron Escalation (Low / Borderline Confidence < 75%):**
   * If a clause has ambiguous phrasing, unclassified latent liability markers, or conflicting remedies, it is flagged for escalation.
   * **Privacy Guarantee:** Only the **already-anonymized** clause is transmitted to the configured OpenAI-compatible Nemotron endpoint (`nvidia/llama-3.1-nemotron-70b-instruct`, OpenRouter, or local vLLM).
   * Nemotron returns deep synthesis: precise risk scores, edge-case trap definitions, and redline counter-proposals.

---

## 🚀 3. Core Features & Capabilities

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
* Supports both local grounded heuristics and OpenAI-compatible **Nemotron conversational synthesis**.
* Includes pre-configured scenario prompts (e.g. *"Can they cancel without paying me?"*, *"Who owns the background IP?"*).
* Cites specific contract sections and enforces mandatory non-advisory disclosures.

---

## 🛠️ 4. Quickstart & Installation

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
Execute the full 32-test suite covering PII anonymization, risk heuristics, clause segmentation, Nemotron client & escalation routing, version comparison, API endpoints, and security guardrails:
```bash
pnpm test
```
*Expected result:* **`32 passed in ~1.4 seconds`**

### 2. Launch Web Application (`pnpm start` or `pnpm dev`)
Start the high-performance web dashboard:
```bash
pnpm start
```
Open your browser to: **[http://localhost:8000](http://localhost:8000)**

### 3. Configuring NVIDIA Nemotron / OpenAI-Compatible API
You can configure Nemotron directly in the Web Dashboard via the **⚙️ AI Model & Nemotron Settings** modal, or by setting environment variables:
```bash
# NVIDIA Nemotron (default model: nvidia/llama-3.1-nemotron-70b-instruct)
export NEMOTRON_API_KEY="nvapi-..."
export OPENAI_BASE_URL="https://integrate.api.nvidia.com/v1"
export OPENAI_MODEL_NAME="nvidia/llama-3.1-nemotron-70b-instruct"

# Or OpenRouter
export OPENAI_API_KEY="sk-or-..."
export OPENAI_BASE_URL="https://openrouter.ai/api/v1"
export OPENAI_MODEL_NAME="nvidia/llama-3.1-nemotron-70b-instruct"

# Or local Ollama / vLLM (Zero API Key required)
export OPENAI_BASE_URL="http://localhost:11434/v1"
export OPENAI_MODEL_NAME="nemotron-mini"
```

### 4. Command Line Interface (CLI)
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

## 📐 5. Architecture & Directory Structure

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
│       ├── llm_client.py    # OpenAI-compatible / Nemotron client & escalation engine
│       ├── assistant.py     # Grounded Q&A assistant engine
│       ├── sample_contracts.py # Realistic curated test contracts
│       ├── cli.py           # Command-line interface entry point
│       ├── ui.py            # Accessible, fast single-page web dashboard
│       └── main.py          # FastAPI application & REST endpoints
└── tests/
    ├── test_anonymizer.py       # PII redaction and restoration tests
    ├── test_clause_segmenter.py # Heading, numbering, and category tests
    ├── test_risk_analyzer.py    # Trap detection and score calculation tests
    ├── test_nemotron.py         # Nemotron client, confidence & escalation tests
    ├── test_comparator.py       # Version diff and trajectory tests
    ├── test_simplifier.py       # Plain-English translation & glossary tests
    ├── test_checklist.py        # Attorney brief generation tests
    └── test_api.py              # FastAPI endpoints, settings & guardrails tests
```

---

## ⚖️ 6. Evaluation Focus Areas

| Focus Area | How Legal-Ease Demonstrates Excellence |
| :--- | :--- |
| **Code Quality** | Clean, modular, type-annotated Python 3.12 with Pydantic v2 validation. Full separation of concerns across models, guardrails, heuristics, LLM client, and UI. Zero monolithic files. |
| **Security & Privacy** | **100% Local PII Redaction**: Sensitive personal and corporate entities are anonymized locally before linguistic analysis or Nemotron escalation. Built-in input sanitization against prompt injection attacks. |
| **Efficiency & Speed** | Sub-second local analysis pipeline (< 50ms per contract). High-confidence items never trigger external network requests, saving latency and API compute. |
| **Testing** | 32 automated tests with **100% pass rate** (`pnpm test`), validating PII redaction, risk rules, Nemotron escalation, diffing, REST endpoints, and security guardrails. |
| **Accessibility & UI** | Sleek modern glassmorphism design, semantic HTML5, WCAG AA high-contrast color scheme, full keyboard navigation, `aria-*` tags, and responsive layout across mobile and desktop. |
| **Repository Rules** | Strict compliance: **Single branch (`main`)**, **Repo size < 1 MB** (well under the 10 MB ceiling), public GitHub repository, and built with `uv` and `pnpm` only. |

---

## 📑 7. Ethical Guardrails & Assumptions

1. **Non-Advisory Tool:** Legal-Ease is explicitly designed as a legal document literacy and negotiation preparation instrument. It **does not** provide formal legal advice, establish an attorney-client relationship, or substitute for licensed legal representation.
2. **Pre-Consultation Utility:** The solution is designed to empower clients *prior* to attorney consultation, dramatically reducing the billable hours required for intake and issue-spotting.
3. **Jurisdictional Notice:** Legal standards vary across states and countries. Default heuristics reflect standard US commercial contract norms (Delaware, New York, California common law precedents).

---

## 📜 8. License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.
