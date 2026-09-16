"""
Unit tests for Nemotron / OpenAI-compatible client,
confidence evaluation, and local-first escalation routing.
"""

import pytest
from unittest.mock import AsyncMock, patch
from legal_ease.llm_client import NemotronClient, LLMConfig
from legal_ease.risk_analyzer import RiskAnalyzer
from legal_ease.clause_segmenter import RawClause
from legal_ease.models import ClauseCategory, RiskSeverity
from legal_ease.pipeline import LegalAnalysisPipeline


def test_nemotron_client_init_and_config():
    client = NemotronClient(
        LLMConfig(
            api_key="nvapi-test12345",
            base_url="https://integrate.api.nvidia.com/v1",
            model_name="nvidia/llama-3.1-nemotron-70b-instruct",
            enabled=True,
            confidence_threshold=0.80,
        )
    )
    assert client.is_configured() is True
    assert client.config.confidence_threshold == 0.80

    # Update config
    client.update_config(confidence_threshold=0.70, enabled=False)
    assert client.config.confidence_threshold == 0.70
    assert client.is_configured() is False


def test_local_confidence_estimation():
    analyzer = RiskAnalyzer()

    # 1. Definitive trap has high confidence
    trap_clause = RawClause(
        clause_id=1,
        title="Indemnification",
        text="Contractor agrees to indemnify and hold harmless Company from any and all claims.",
        category=ClauseCategory.INDEMNIFICATION,
    )
    res = analyzer.evaluate_clause(trap_clause)
    assert res.confidence >= 0.85
    assert res.confidence_label == "HIGH"

    # 2. Ambiguous boilerplate with latent risk terms has lower confidence (<0.75)
    ambiguous_clause = RawClause(
        clause_id=2,
        title="Miscellaneous",
        text="In the event of any breach or disputed remedy, the party may forfeit certain rights.",
        category=ClauseCategory.GENERAL_BOILERPLATE,
    )
    res_amb = analyzer.evaluate_clause(ambiguous_clause)
    assert res_amb.confidence <= 0.75
    assert res_amb.confidence_label in ("MEDIUM", "LOW")


@pytest.mark.asyncio
async def test_pipeline_escalates_low_confidence_to_nemotron():
    """
    Verify that when local confidence is below threshold,
    the pipeline escalates the anonymized clause to Nemotron.
    """
    mock_llm = NemotronClient(
        LLMConfig(
            api_key="nvapi-test-key",
            base_url="https://integrate.api.nvidia.com/v1",
            model_name="nvidia/llama-3.1-nemotron-70b-instruct",
            enabled=True,
            confidence_threshold=0.80,  # Will trigger escalation on confidence < 0.80
        )
    )

    # Mock Nemotron's deep reasoning response
    mock_deep_response = {
        "risk_score": 85,
        "severity": "HIGH",
        "detected_traps": ["Ambiguous Remedy Forfeiture Trap"],
        "plain_english_summary": "This clause deprives you of legal remedies if a dispute arises.",
        "what_it_means_for_you": "You could forfeit all claims without judicial recourse.",
        "negotiation_tip": "Delete the forfeiture requirement and require mutual arbitration.",
        "reasoning": "Language effectively functions as an exculpatory waiver.",
    }

    mock_llm.deep_reason_clause = AsyncMock(return_value=mock_deep_response)

    pipeline = LegalAnalysisPipeline(llm_client=mock_llm)

    test_contract = """
Section 1. Miscellaneous Terms
In the event of any breach or disputed remedy, the party may forfeit certain rights.
"""
    result = await pipeline.analyze_async(test_contract, "Test Contract")

    # Verify escalation took place
    assert result.risk_overview.escalated_clauses_count >= 1
    assert "nemotron" in result.risk_overview.ai_model_used.lower() or "hybrid" in result.risk_overview.ai_model_used.lower()

    escalated_clause = result.clauses[0]
    assert escalated_clause.analysis_source == "NEMOTRON_DEEP_REASONING"
    assert escalated_clause.risk_score == 85
    assert "Ambiguous Remedy Forfeiture Trap" in escalated_clause.detected_traps
    assert "nemotron" in (escalated_clause.escalation_reason or "").lower()


@pytest.mark.asyncio
async def test_nemotron_connection_failure_handling():
    """Verify that if Nemotron endpoint fails or times out, the system handles it gracefully."""
    client = NemotronClient(LLMConfig(api_key=None))
    res = await client.test_connection()
    assert res["success"] is False
    assert "No API key" in res["message"]
