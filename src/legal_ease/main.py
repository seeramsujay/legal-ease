"""
FastAPI application entry point for Legal-Ease.
Provides REST API endpoints and serves the modern, accessible web dashboard.
"""

from typing import Optional, List, Dict
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from legal_ease.pipeline import LegalAnalysisPipeline
from legal_ease.comparator import ContractComparator
from legal_ease.anonymizer import PIIAnonymizer
from legal_ease.assistant import LegalAssistant
from legal_ease.sample_contracts import get_all_samples
from legal_ease.guardrails import get_standard_disclaimer
from legal_ease.models import (
    ContractAnalysisResponse,
    ContractComparisonResponse,
    AnonymizationResult,
    ChatResponse,
    ChatRequest,
    SampleContract,
)

app = FastAPI(
    title="Legal-Ease API",
    description="Privacy-First AI Legal Navigator & Contract Risk Analyzer",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = LegalAnalysisPipeline()
comparator = ContractComparator()
anonymizer = PIIAnonymizer()
assistant = LegalAssistant()


class AnalyzeRequest(BaseModel):
    text: str
    title: Optional[str] = None


class CompareRequest(BaseModel):
    text_v1: str
    text_v2: str
    title_v1: Optional[str] = "Original Version"
    title_v2: Optional[str] = "Revised Proposal"


class AnonymizeRequest(BaseModel):
    text: str


@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "service": "legal-ease",
        "version": "1.0.0",
        "vertical": "AI for Legal Assistance & Access",
    }


@app.get("/api/samples", response_model=List[SampleContract])
async def get_samples():
    """Retrieve realistic contract samples for demonstration."""
    return get_all_samples()


@app.post("/api/analyze", response_model=ContractAnalysisResponse)
async def analyze_contract(request: AnalyzeRequest):
    """Analyze contract text, redact PII, score risks, and generate attorney brief."""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Contract text cannot be empty.")
    return pipeline.analyze(request.text, document_title=request.title)


@app.post("/api/analyze-file", response_model=ContractAnalysisResponse)
async def analyze_file(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
):
    """Analyze an uploaded contract text file."""
    try:
        content = await file.read()
        text = content.decode("utf-8", errors="replace")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {e}")

    doc_title = title if title else file.filename
    return pipeline.analyze(text, document_title=doc_title)


@app.post("/api/compare", response_model=ContractComparisonResponse)
async def compare_contracts(request: CompareRequest):
    """Compare two contract versions and identify liability deltas."""
    if not request.text_v1.strip() or not request.text_v2.strip():
        raise HTTPException(status_code=400, detail="Both contract versions are required.")
    return comparator.compare(
        request.text_v1,
        request.text_v2,
        title_v1=request.title_v1 or "Original Version",
        title_v2=request.title_v2 or "Revised Proposal",
    )


@app.post("/api/anonymize", response_model=AnonymizationResult)
async def anonymize_text(request: AnonymizeRequest):
    """Perform local PII anonymization preview on raw text."""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")
    return anonymizer.anonymize(request.text)


@app.post("/api/chat", response_model=ChatResponse)
async def chat_contract(request: ChatRequest):
    """Context-aware conversational assistance regarding the contract."""
    return assistant.answer_query(
        query=request.message,
        contract_text=request.contract_text,
        clauses_context=request.context_clauses,
    )


@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    """Serve the modern, responsive, accessible Single Page Application."""
    from legal_ease.ui import get_dashboard_html
    return get_dashboard_html()
