"""
Data models and schemas for Legal-Ease.
"""

from enum import Enum
from typing import Dict, List, Optional
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
    RESTRICTIVE_COVENANTS = "restrictive_covenants"
    CONFIDENTIALITY = "confidentiality"
    PAYMENT_TERMS = "payment_terms"
    WARRANTY_DISCLAIMER = "warranty_disclaimer"
    GOVERNING_LAW = "governing_law"
    GENERAL_BOILERPLATE = "general_boilerplate"


class RedactedEntity(BaseModel):
    token: str
    original_value: str
    entity_type: str
    start_char: int
    end_char: int


class AnonymizationResult(BaseModel):
    original_text_length: int
    redacted_text: str
    entities: List[RedactedEntity]
    entity_counts: Dict[str, int]
    privacy_score: float = Field(
        ..., description="Score 0-100 indicating privacy protection level"
    )


class ClauseAnalysis(BaseModel):
    id: int
    section_title: str
    category: ClauseCategory
    original_text: str
    redacted_text: str
    risk_score: int = Field(..., ge=0, le=100, description="Risk score 0-100")
    severity: RiskSeverity
    risk_reasons: List[str]
    plain_english_summary: str
    what_it_means_for_you: str
    negotiation_tip: str
    detected_traps: List[str]


class RiskOverview(BaseModel):
    legal_risk_index: int = Field(
        ..., ge=0, le=100, description="Overall contract risk index (0=Safe, 100=Dangerous)"
    )
    risk_level: RiskSeverity
    total_clauses: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    critical_findings: List[str]
    executive_summary: str


class AttorneyQuestion(BaseModel):
    category: str
    related_clause_id: Optional[int]
    question: str
    why_it_matters: str
    recommended_fallback: str


class AttorneyChecklist(BaseModel):
    document_title: str
    overall_risk_index: int
    top_exposures: List[str]
    questions_for_counsel: List[AttorneyQuestion]
    priority_negotiation_items: List[str]
    markdown_report: str


class ContractAnalysisResponse(BaseModel):
    document_id: str
    disclaimer: str
    anonymization: AnonymizationResult
    risk_overview: RiskOverview
    clauses: List[ClauseAnalysis]
    attorney_checklist: AttorneyChecklist
    analyzed_at: str


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
    risk_delta: int = Field(0, description="Change in risk score (v2 - v1)")
    analysis_notes: str


class ContractComparisonResponse(BaseModel):
    document_title_v1: str
    document_title_v2: str
    disclaimer: str
    risk_index_v1: int
    risk_index_v2: int
    risk_index_delta: int
    trajectory: str  # "SAFER", "MORE_RISK", "NEUTRAL"
    summary_of_changes: List[str]
    clause_diffs: List[ClauseDiff]


class ChatRequest(BaseModel):
    message: str
    contract_text: str
    context_clauses: Optional[List[Dict]] = None


class ChatResponse(BaseModel):
    answer: str
    disclaimer: str
    referenced_clauses: List[str]
    risk_warning: Optional[str] = None


class SampleContract(BaseModel):
    id: str
    title: str
    description: str
    category: str
    content: str
