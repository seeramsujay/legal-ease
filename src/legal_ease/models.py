"""
Data models, schemas, and enums for Legal-Ease.
"""

from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class RiskSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ClauseCategory(str, Enum):
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
    entity_type: str = Field(description="Category of PII/sensitive info (e.g. EMAIL, PHONE, SSN, MONEY, PARTY_NAME)")
    original_value: str = Field(description="Original unredacted sensitive value")
    token: str = Field(description="Pseudonym token replacement, e.g. [EMAIL_1], [CONFIDENTIAL_AMOUNT_1]")
    start_char: int
    end_char: int


class AnonymizationResult(BaseModel):
    redacted_text: str
    entities: List[RedactedEntity]
    privacy_score: float = Field(description="Estimated privacy coverage score (0.0 to 100.0)")
    entity_counts: Dict[str, int] = Field(default_factory=dict)


class ClauseAnalysis(BaseModel):
    id: int
    section_title: str
    category: ClauseCategory
    original_text: str
    redacted_text: str
    risk_score: int = Field(ge=0, le=100, description="Liability exposure score from 0 (benign) to 100 (extreme)")
    severity: RiskSeverity
    confidence: float = Field(default=0.95, ge=0.0, le=1.0, description="Confidence in the local assessment")
    confidence_label: str = Field(default="HIGH", description="Confidence level: HIGH, MEDIUM, LOW")
    analysis_source: str = Field(default="LOCAL_HEURISTICS", description="LOCAL_HEURISTICS or NEMOTRON_DEEP_REASONING")
    escalation_reason: Optional[str] = Field(default=None, description="Reason if escalated to LLM")
    risk_reasons: List[str] = Field(default_factory=list)
    plain_english_summary: str = Field(description="Plain-English explanation without legalese")
    what_it_means_for_you: str = Field(description="Real-world practical business and personal consequences")
    negotiation_tip: str = Field(description="Actionable redline suggestion to propose to counterparty")
    detected_traps: List[str] = Field(default_factory=list)
    is_twisted: bool = Field(default=False, description="Whether twisted, euphemistic, or obfuscated drafting was detected")
    obfuscation_score: float = Field(default=0.0, ge=0.0, le=1.0, description="Semantic ambiguity/obfuscation index (0.0 clear to 1.0 highly disguised)")
    semantic_archetype_matches: Dict[str, float] = Field(default_factory=dict, description="Cosine similarity matches against predatory contract archetypes")
    detected_euphemisms: List[str] = Field(default_factory=list, description="Specific deceptive/euphemistic phrases identified")


class RiskOverview(BaseModel):
    legal_risk_index: int = Field(ge=0, le=100, description="Overall contract hazard score")
    risk_level: RiskSeverity
    total_clauses: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    critical_findings: List[str]
    executive_summary: str
    average_confidence: float = Field(default=0.92, ge=0.0, le=1.0)
    escalated_clauses_count: int = Field(default=0)
    twisted_clauses_count: int = Field(default=0, description="Count of clauses with twisted or obfuscated language")
    ai_model_used: Optional[str] = Field(default="Local Rules + Deterministic Heuristics")


class AttorneyQuestion(BaseModel):
    category: str
    question: str
    why_it_matters: str
    recommended_fallback: str


class AttorneyChecklist(BaseModel):
    document_title: str
    overall_risk_index: int
    questions_for_counsel: List[AttorneyQuestion]
    priority_negotiation_items: List[str]
    markdown_report: str


class DiffChangeType(str, Enum):
    ADDED = "ADDED"
    REMOVED = "REMOVED"
    MODIFIED = "MODIFIED"
    UNCHANGED = "UNCHANGED"


class ClauseDiff(BaseModel):
    section_title: str
    category: str
    change_type: DiffChangeType
    text_v1: Optional[str] = None
    text_v2: Optional[str] = None
    risk_score_v1: Optional[int] = None
    risk_score_v2: Optional[int] = None
    risk_delta: int = Field(default=0, description="Difference in risk points (v2 - v1)")
    analysis_notes: str


class ContractComparisonResponse(BaseModel):
    document_title_v1: str
    document_title_v2: str
    disclaimer: str
    risk_index_v1: int
    risk_index_v2: int
    risk_index_delta: int
    trajectory: str = Field(description="'SAFER', 'MORE_RISK', or 'NEUTRAL'")
    summary_of_changes: List[str]
    clause_diffs: List[ClauseDiff]


class ContractAnalysisResponse(BaseModel):
    document_id: str
    disclaimer: str
    anonymization: AnonymizationResult
    risk_overview: RiskOverview
    clauses: List[ClauseAnalysis]
    attorney_checklist: AttorneyChecklist
    analyzed_at: str


class ChatRequest(BaseModel):
    message: str
    contract_text: Optional[str] = ""
    context_clauses: Optional[List[Dict[str, Any]]] = None
    history: Optional[List[Dict[str, str]]] = None


class ChatResponse(BaseModel):
    answer: str
    disclaimer: str
    referenced_clauses: List[str] = Field(default_factory=list)
    risk_warning: Optional[str] = None
    model_used: Optional[str] = None


class AnonymizeRequest(BaseModel):
    text: str


class AnalyzeRequest(BaseModel):
    text: str
    title: Optional[str] = None


class CompareRequest(BaseModel):
    text_v1: str
    text_v2: str
    title_v1: Optional[str] = "Version 1"
    title_v2: Optional[str] = "Version 2"


class SampleContract(BaseModel):
    id: str
    title: str
    description: str
    category: str
    content: str


class LLMConfigUpdateRequest(BaseModel):
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model_name: Optional[str] = None
    enabled: Optional[bool] = None
    confidence_threshold: Optional[float] = None
    provider: Optional[str] = None  # "gemini", "nemotron", "openai", "custom"
