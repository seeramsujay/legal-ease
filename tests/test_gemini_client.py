"""
Unit tests for Google Gemini Flash-Lite client, provider presets,
and environment allowance discovery.
"""

import os
import pytest
from unittest.mock import AsyncMock
from legal_ease.llm_client import NemotronClient, LLMConfig, PROVIDER_PRESETS
from legal_ease.pipeline import LegalAnalysisPipeline


def test_gemini_preset_configuration():
    # Test setting provider to gemini
    client = NemotronClient(
        LLMConfig(
            api_key="AIzaSyTestGeminiKey12345",
            provider="gemini",
            model_name="gemini-2.0-flash-lite",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai",
            enabled=True,
        )
    )
    assert client.is_configured() is True
    status = client.get_status()
    assert status["provider"] == "gemini"
    assert status["model_name"] == "gemini-2.0-flash-lite"
    assert "AIza" in status["masked_key"]
    assert "gemini" in status["available_presets"]


def test_environment_allowance_discovery(monkeypatch):
    # Simulate evaluator passing GEMINI_API_KEY via environment
    monkeypatch.setenv("GEMINI_API_KEY", "AIzaSyEvaluatorProvidedKey999")

    client = NemotronClient()
    assert client.is_configured() is True
    assert client.config.provider == "gemini"
    assert client.config.api_key == "AIzaSyEvaluatorProvidedKey999"
    assert client.config.api_key_source == "environment"
    assert "gemini" in client.config.model_name.lower()


def test_provider_switching_to_nemotron():
    client = NemotronClient()
    client.update_config(provider="nemotron", api_key="nvapi-test-key")
    assert client.config.provider == "nemotron"
    assert "nemotron" in client.config.model_name.lower()
    assert "nvidia" in client.config.base_url.lower()


@pytest.mark.asyncio
async def test_pipeline_escalates_to_gemini():
    """Verify that when local confidence is below threshold, the pipeline escalates to Gemini."""
    mock_llm = NemotronClient(
        LLMConfig(
            api_key="AIzaSyTestKey",
            base_url="https://generativelanguage.googleapis.com/v1beta/openai",
            model_name="gemini-2.0-flash-lite",
            provider="gemini",
            enabled=True,
            confidence_threshold=0.80,
        )
    )

    mock_deep_response = {
        "risk_score": 90,
        "severity": "CRITICAL",
        "detected_traps": ["Ambiguous Disputed Remedy Forfeiture"],
        "plain_english_summary": "Contractor forfeits legal recourse in arbitrary dispute situations.",
        "what_it_means_for_you": "You give up legal claims without judicial trial.",
        "negotiation_tip": "Make indemnification and remedies bilateral.",
        "reasoning": "Unclassified latent forfeiture language.",
    }

    mock_llm.deep_reason_clause = AsyncMock(return_value=mock_deep_response)

    pipeline = LegalAnalysisPipeline(llm_client=mock_llm)
    test_contract = """
    Section 1. Operational Exceptions
    In the event of any operational conflict, the party may forfeit certain damages and waive ordinary remedy.
    """
    result = await pipeline.analyze_async(test_contract, "Gemini Escalation Test")

    assert result.risk_overview.escalated_clauses_count >= 1
    assert "gemini" in result.risk_overview.ai_model_used.lower()
    escalated_clause = result.clauses[0]
    assert escalated_clause.analysis_source == "GEMINI_DEEP_REASONING"


def test_byok_override_and_environment_fallback(monkeypatch):
    """Verify BYOK key overrides environment key, and clearing BYOK restores environment key."""
    monkeypatch.setenv("GEMINI_API_KEY", "AIzaSyDefaultEnvKey")

    client = NemotronClient()
    assert client.is_configured() is True
    assert client.config.api_key == "AIzaSyDefaultEnvKey"
    assert client.config.api_key_source == "environment"

    # 1. User enters personal BYOK key in modal
    client.update_config(api_key="AIzaSyUserPersonalBYOK")
    assert client.config.api_key == "AIzaSyUserPersonalBYOK"
    assert client.config.api_key_source == "user_configured"

    # 2. User clears BYOK key in modal -> seamlessly falls back to env key
    client.update_config(api_key="")
    assert client.config.api_key == "AIzaSyDefaultEnvKey"
    assert client.config.api_key_source == "environment"

    # 3. Test reset_to_environment()
    client.update_config(api_key="AnotherBYOKKey", provider="openai")
    client.reset_to_environment()
    assert client.config.provider == "gemini"
    assert client.config.api_key == "AIzaSyDefaultEnvKey"
    assert client.config.api_key_source == "environment"
