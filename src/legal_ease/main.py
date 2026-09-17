"""
FastAPI application entry point for Legal-Ease.
Provides REST API endpoints, LLM escalation management (Google Gemini Flash-Lite,
NVIDIA Nemotron, OpenAI), native Cython compilation telemetry, and serves the modern, accessible web dashboard.
"""

from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from legal_ease.llm_client import NemotronClient, LLMConfig
from legal_ease.pipeline import LegalAnalysisPipeline
from legal_ease.comparator import ContractComparator
from legal_ease.anonymizer import PIIAnonymizer
from legal_ease.assistant import LegalAssistant
from legal_ease.fast_ops_bridge import is_cython_accelerated, get_acceleration_info
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
    description="Privacy-First AI Legal Navigator & Contract Risk Analyzer (Powered by Local Shield + Gemini Flash-Lite / Nemotron + Cython)",
    version="1.3.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global shared client instances
llm_client = NemotronClient()
pipeline = LegalAnalysisPipeline(llm_client=llm_client)
comparator = ContractComparator()
anonymizer = PIIAnonymizer()
assistant = LegalAssistant(llm_client=llm_client)


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


class UpdateLLMConfigRequest(BaseModel):
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model_name: Optional[str] = None
    enabled: Optional[bool] = None
    confidence_threshold: Optional[float] = None
    provider: Optional[str] = None


@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "service": "legal-ease",
        "version": "1.3.0",
        "vertical": "AI for Legal Assistance & Access",
        "provider": llm_client.config.provider,
        "llm_configured": llm_client.is_configured(),
        "api_key_source": llm_client.config.api_key_source,
        "nemotron_configured": llm_client.is_configured(),
        "model": llm_client.config.model_name,
        "cython_accelerated": is_cython_accelerated(),
        "acceleration_info": get_acceleration_info(),
    }


@app.get("/api/settings/llm")
async def get_llm_settings():
    """Retrieve current LLM configuration, provider presets, and environment key status."""
    status = llm_client.get_status()
    # Backwards-compatible aliases for frontend
    status["api_key_configured"] = status["configured"]
    status["masked_api_key"] = status["masked_key"]
    status["cython_active"] = is_cython_accelerated()
    return status


@app.post("/api/settings/llm")
async def update_llm_settings(req: UpdateLLMConfigRequest):
    """Update LLM provider configuration at runtime (Gemini Flash Lite, Nemotron, OpenAI)."""
    llm_client.update_config(
        api_key=req.api_key,
        base_url=req.base_url,
        model_name=req.model_name,
        enabled=req.enabled,
        confidence_threshold=req.confidence_threshold,
        provider=req.provider,
    )
    return {
        "status": "updated",
        "configured": llm_client.is_configured(),
        "provider": llm_client.config.provider,
        "model_name": llm_client.config.model_name,
        "api_key_source": llm_client.config.api_key_source,
    }


@app.post("/api/settings/test")
async def test_llm_connection():
    """Test connection to the active LLM endpoint."""
    res = await llm_client.test_connection()
    return res


@app.get("/api/samples", response_model=List[SampleContract])
async def get_samples():
    """Retrieve realistic contract samples for demonstration."""
    return get_all_samples()


@app.post("/api/analyze", response_model=ContractAnalysisResponse)
async def analyze_contract(request: AnalyzeRequest):
    """Analyze contract text with local privacy shield and confidence-based LLM escalation."""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Contract text cannot be empty.")
    return await pipeline.analyze_async(request.text, document_title=request.title)


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
    return await pipeline.analyze_async(text, document_title=doc_title)


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
    """Context-aware conversational assistance regarding the contract (Local or LLM)."""
    return await assistant.answer_query_async(
        query=request.message,
        contract_text=request.contract_text or "",
        clauses_context=request.context_clauses,
        history=request.history,
    )


@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    """Serve the modern, responsive, accessible Single Page Application."""
    from legal_ease.ui import get_dashboard_html
    return get_dashboard_html()
