"""
Core Data Models, Pydantic v2 Schemas, and Enumerations for Legal-Ease.
Provides strict type validation, field documentation, and default factories
to prevent null/None references across all application pipelines.
"""

from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field, field_validator


class RiskSeverity(str, Enum):
    """Enumeration of contractual liability severity levels."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ClauseCategory(str, Enum):
    """Legal classifications for categorized contract provisions."""
    INDEMNIFICATION = "indemnification"
    LIMITATION_OF_LIABILITY = "limitation_of_liability"
    DISPUTE_RESOLUTION = "dispute_resolution"
    TERMINATION = "termination"
    INTELLECTUAL_PROPERTY = "intellectual_property"
    CONFIDENTIALITY = "confidentiality"
    PAYMENT_TERMS = "payment_terms"
    RESTRICTIVE_COVENANTS = "restrictive_covenants"
    WARRANTY_DISCLAIMER = "warranty_disclaimer"
    GOVERNING_LAW = "governing_law"
    GENERAL_BOILERPLATE = "general_boilerplate"


class RedactedEntity(BaseModel):
    """Represents a single sensitive PII entity sanitized by the local privacy shield."""
    entity_type: str = Field(description="PII Category: EMAIL, PHONE, SSN_TAX_ID, FINANCIAL, CREDIT_CARD, ADDRESS, PARTY_NAME")
    original_value: str = Field(description="Original unredacted sensitive entity value")
    token: str = Field(description="Pseudonym token replacement, e.g. [EMAIL_1], [CONFIDENTIAL_AMOUNT_1]")
    start_char: int = Field(ge=0, description="Character start index in original raw text")
    end_char: int = Field(ge=0, description="Character end index in original raw text")


class AnonymizationResult(BaseModel):
    """Output summary of the deterministic local PII redaction pass."""
    redacted_text: str = Field(description="Sanitized text with all sensitive identifiers replaced with tokens")
    entities: List[RedactedEntity] = Field(default_factory=list, description="List of all detected and redacted entities")
    privacy_score: float = Field(default=100.0, ge=0.0, le=100.0, description="Estimated privacy coverage score (0.0 to 100.0)")
    entity_counts: Dict[str, int] = Field(default_factory=dict, description="Redaction counts partitioned by entity type")


class ClauseAnalysis(BaseModel):
    """Comprehensive linguistic, risk, and translation analysis for an individual contract clause."""
    id: int = Field(ge=1, description="Sequential clause identifier")
    section_title: str = Field(default="Untitled Section", description="Extracted heading or section numbering")
    category: ClauseCategory = Field(default=ClauseCategory.GENERAL_BOILERPLATE, description="Classified legal category")
    original_text: str = Field(description="Raw text of the clause as present in document")
    redacted_text: str = Field(description="Privacy-sanitized text of the clause")
    risk_score: int = Field(ge=0, le=100, description="Liability exposure score from 0 (benign) to 100 (catastrophic)")
    severity: RiskSeverity = Field(default=RiskSeverity.LOW, description="Categorized severity level")
    confidence: float = Field(default=0.95, ge=0.0, le=1.0, description="Confidence in the local heuristic assessment")
    confidence_label: str = Field(default="HIGH", description="Categorical confidence tag: HIGH, MEDIUM, LOW")
    analysis_source: str = Field(default="LOCAL_HEURISTICS", description="Engine source: LOCAL_HEURISTICS or GEMINI_DEEP_REASONING")
    escalation_reason: Optional[str] = Field(default=None, description="Diagnostic justification if escalated to remote LLM")
    risk_reasons: List[str] = Field(default_factory=list, description="Specific risk exposures and legal hazards identified")
    plain_english_summary: str = Field(default="", description="Conversational summary demystifying the clause for non-lawyers")
    what_it_means_for_you: str = Field(default="", description="Practical real-world business and personal liability consequences")
    negotiation_tip: str = Field(default="", description="Concrete redline counter-proposal to balance the terms")
    detected_traps: List[str] = Field(default_factory=list, description="Recognized predatory drafting archetypes and traps")
    is_twisted: bool = Field(default=False, description="Flag indicating semantic obfuscation or deceptive euphemisms")
    obfuscation_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Complexity and obfuscation index (0.0 clear to 1.0 disguised)")
    semantic_archetype_matches: Dict[str, float] = Field(default_factory=dict, description="Cosine similarity metrics against predatory archetypes")
    detected_euphemisms: List[str] = Field(default_factory=list, description="Specific deceptive drafting euphemisms flagged")


class RiskOverview(BaseModel):
    """Executive document-level risk synthesis and exposure scorecard."""
    legal_risk_index: int = Field(ge=0, le=100, description="Overall contract hazard score from 0 to 100")
    risk_level: RiskSeverity = Field(default=RiskSeverity.LOW, description="Aggregated risk tier")
    total_clauses: int = Field(default=0, ge=0, description="Total number of segmented clauses")
    high_risk_count: int = Field(default=0, ge=0, description="Count of HIGH and CRITICAL risk clauses")
    medium_risk_count: int = Field(default=0, ge=0, description="Count of MEDIUM risk clauses")
    low_risk_count: int = Field(default=0, ge=0, description="Count of LOW risk clauses")
    critical_findings: List[str] = Field(default_factory=list, description="Prioritized list of top exposures")
    executive_summary: str = Field(default="No content analyzed.", description="Actionable executive assessment for decision makers")
    average_confidence: float = Field(default=0.92, ge=0.0, le=1.0, description="Mean confidence across all evaluated clauses")
    escalated_clauses_count: int = Field(default=0, ge=0, description="Number of clauses escalated to LLM for deep reasoning")
    twisted_clauses_count: int = Field(default=0, ge=0, description="Number of clauses flagged with obfuscated or twisted language")
    ai_model_used: Optional[str] = Field(default="Local Rules + Deterministic Heuristics", description="Active AI engine descriptor")


class AttorneyQuestion(BaseModel):
    """Structured question for a professional attorney consultation."""
    category: str = Field(description="Legal domain or subject area")
    question: str = Field(description="Precise, high-value question to pose to legal counsel")
    why_it_matters: str = Field(description="Explanation of underlying risk and financial exposure")
    recommended_fallback: str = Field(description="Standard fair market fallback position or amendment")
    related_clause_id: Optional[int] = Field(default=None, description="Optional foreign key to originating clause")


class AttorneyChecklist(BaseModel):
    """Comprehensive attorney consultation brief and redline checklist."""
    document_title: str = Field(default="Contract Agreement", description="Document title or reference")
    overall_risk_index: int = Field(ge=0, le=100, description="Overall document risk score")
    questions_for_counsel: List[AttorneyQuestion] = Field(default_factory=list, description="Prioritized questions for legal consultation")
    priority_negotiation_items: List[str] = Field(default_factory=list, description="Checklist of essential counter-proposal amendments")
    markdown_report: str = Field(default="", description="Exportable Markdown formatted brief for counsel")


class DiffChangeType(str, Enum):
    """Status classification for contract revision comparison."""
    ADDED = "ADDED"
    REMOVED = "REMOVED"
    MODIFIED = "MODIFIED"
    UNCHANGED = "UNCHANGED"


class ClauseDiff(BaseModel):
    """Comparative delta analysis between corresponding clauses in two contract revisions."""
    section_title: str = Field(description="Clause heading or identifier")
    category: str = Field(description="Legal subject matter category")
    change_type: DiffChangeType = Field(description="ADDED, REMOVED, MODIFIED, or UNCHANGED")
    text_v1: Optional[str] = Field(default=None, description="Clause text in original draft (v1)")
    text_v2: Optional[str] = Field(default=None, description="Clause text in revised draft (v2)")
    risk_score_v1: Optional[int] = Field(default=None, description="Risk score of original clause")
    risk_score_v2: Optional[int] = Field(default=None, description="Risk score of revised clause")
    risk_delta: int = Field(default=0, description="Risk point trajectory (v2 - v1; negative is safer)")
    analysis_notes: str = Field(default="", description="Explanatory notes on the legal impact of the revision")


class ContractComparisonResponse(BaseModel):
    """Full side-by-side contract comparison response with trajectory analysis."""
    document_title_v1: str = Field(default="Original Draft", description="Title of base agreement")
    document_title_v2: str = Field(default="Revised Draft", description="Title of counter-proposal")
    disclaimer: str = Field(description="Mandatory non-advisory legal disclosure")
    risk_index_v1: int = Field(ge=0, le=100, description="Risk index of original version")
    risk_index_v2: int = Field(ge=0, le=100, description="Risk index of revised version")
    risk_index_delta: int = Field(description="Overall risk index change (negative indicates reduced exposure)")
    trajectory: str = Field(description="Directional assessment: 'SAFER', 'MORE_RISK', or 'NEUTRAL'")
    summary_of_changes: List[str] = Field(default_factory=list, description="Bullet summary of key material alterations")
    clause_diffs: List[ClauseDiff] = Field(default_factory=list, description="Granular clause-by-clause diff breakdown")


class ContractAnalysisResponse(BaseModel):
    """End-to-end response for a complete contract analysis operation."""
    document_id: str = Field(description="Unique deterministic or random document identifier")
    disclaimer: str = Field(description="Mandatory legal disclaimer")
    anonymization: AnonymizationResult = Field(description="PII sanitization telemetry and redacted text")
    risk_overview: RiskOverview = Field(description="High-level risk index, breakdown, and executive summary")
    clauses: List[ClauseAnalysis] = Field(default_factory=list, description="Detailed analysis for every segmented clause")
    attorney_checklist: AttorneyChecklist = Field(description="Structured briefing notes and questions for counsel")
    analyzed_at: str = Field(description="ISO-8601 UTC timestamp of analysis completion")


# Request Schemas
class AnalyzeRequest(BaseModel):
    """Request payload for contract risk and semantic analysis."""
    text: str = Field(description="Raw contract text to analyze")
    title: Optional[str] = Field(default=None, description="Optional custom document title")


class CompareRequest(BaseModel):
    """Request payload for comparing two contract revisions."""
    text_v1: str = Field(description="Text of original contract draft (v1)")
    text_v2: str = Field(description="Text of revised counter-proposal (v2)")
    title_v1: Optional[str] = Field(default="Original Version", description="Label for v1")
    title_v2: Optional[str] = Field(default="Revised Proposal", description="Label for v2")


class AnonymizeRequest(BaseModel):
    """Request payload for deterministic local PII redaction only."""
    text: str = Field(description="Raw contract text containing sensitive identifiers")


class ChatRequest(BaseModel):
    """Request payload for the context-aware grounded legal assistant."""
    message: str = Field(description="User query regarding contract terms")
    contract_text: Optional[str] = Field(default="", description="Optional full contract context")
    context_clauses: Optional[List[Dict[str, Any]]] = Field(default=None, description="Optional pre-analyzed clause context")
    history: Optional[List[Dict[str, str]]] = Field(default=None, description="Optional chat conversation history")


class ChatResponse(BaseModel):
    """Response from the grounded legal assistant."""
    answer: str = Field(description="Contextual answer explaining contract terms")
    disclaimer: str = Field(description="Mandatory non-advisory legal disclaimer")
    referenced_clauses: List[str] = Field(default_factory=list, description="Clauses cited or evaluated in answer")
    risk_warning: Optional[str] = Field(default=None, description="Safety or risk alert if applicable")
    model_used: Optional[str] = Field(default=None, description="Engine or model identifier utilized")


class SampleContract(BaseModel):
    """Curated realistic contract sample for demonstration."""
    id: str = Field(description="Unique sample identifier")
    title: str = Field(description="Human-readable title")
    description: str = Field(description="Overview of contract type and embedded traps")
    category: str = Field(description="Industry category (e.g. Freelance, SaaS, NDA)")
    content: str = Field(description="Full text of contract sample")


class LLMConfigUpdateRequest(BaseModel):
    """Request payload for updating LLM provider settings at runtime."""
    api_key: Optional[str] = Field(default=None, description="API key for provider")
    base_url: Optional[str] = Field(default=None, description="Custom base URL if overriding preset")
    model_name: Optional[str] = Field(default=None, description="Model identifier")
    enabled: Optional[bool] = Field(default=None, description="Whether LLM escalation is active")
    confidence_threshold: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Escalation threshold")
    provider: Optional[str] = Field(default=None, description="Provider preset: 'gemini', 'nemotron', 'openai'")
