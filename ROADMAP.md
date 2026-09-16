# 🗺️ Product Roadmap & Engineering Lifecycle: Legal-Ease

This document outlines the operational roadmap, milestones, and design choices for the **Legal-Ease** system.

## Phase 1: Core Engine & Privacy Architecture (Milestone 1)
- [x] **Repository Constraints Setup:** Configure strictly lightweight repository assets maintaining total size < 10 MB.
- [x] **PII Anonymization Module:** Implement regex and Named Entity Recognition (NER) pattern matching to mask names, SSNs/Tax IDs, and financial values locally.
- [x] **Document Parser Engine:** Develop clean text extraction utilities for standard `.pdf` and `.docx` formats with structural section chunking.

## Phase 2: Risk Scoring & Comparison Logic (Milestone 2)
- [x] **Clause Classification System:** Build heuristic rule-set to detect unilateral indemnification, binding arbitration, and auto-renewal traps.
- [x] **Semantic Document Comparison:** Build a diff-analysis module to compare legacy vs. revised contracts side-by-side.
- [x] **Structured Prompt Synthesizer:** Implement system instructions enforcing structured JSON outputs for risk scores and attorney briefing summaries.

## Phase 3: Interface & Compliance Guardrails (Milestone 3)
- [x] **User Interface (Streamlit/FastHTML):** Design an accessible dashboard for drag-and-drop document upload, comparative visualization, and risk breakdown.
- [x] **Legal Disclaimer Guardrails:** Enforce automated non-advisory disclosures across all user-facing output channels.
- [x] **Automated Testing Suite:** Develop comprehensive `pytest` test cases for PII redaction accuracy, parser reliability, and risk-scoring edge cases.

## Future Engineering Enhancements (Post-Hackathon)
- [ ] **Multi-Jurisdictional Framework Support:** Toggle risk weighting based on regional contract laws (e.g., US, EU, UK).
- [ ] **Local LLM Offline Execution:** Integrate WebGPU / Ollama backends to allow 100% offline local inference for ultra-sensitive corporate legal teams.
