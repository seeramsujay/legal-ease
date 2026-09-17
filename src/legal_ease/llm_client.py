"""
Unified LLM client supporting Google Gemini (Flash-Lite / Flash 2.0),
NVIDIA Nemotron, and OpenAI-compatible endpoints with local-first
confidence-based escalation routing and environment key auto-detection.
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
import httpx
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


def _load_env_file():
    """Lightweight .env parser to load local environment configuration without external dependencies."""
    env_paths = [
        Path.cwd() / ".env",
        Path(__file__).resolve().parent.parent.parent / ".env",
    ]
    for env_path in env_paths:
        if env_path.is_file():
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#") or "=" not in line:
                            continue
                        key, val = line.split("=", 1)
                        key = key.strip()
                        val = val.strip().strip("'\"")
                        if key not in os.environ:
                            os.environ[key] = val
            except Exception as e:
                logger.debug(f"Failed to load .env from {env_path}: {e}")
            break


_load_env_file()

PROVIDER_PRESETS: Dict[str, Dict[str, Any]] = {
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "model_name": "gemini-2.0-flash-lite",
        "display_name": "Google Gemini 2.0 Flash-Lite (Fast, Efficient)",
        "env_vars": ["GEMINI_API_KEY", "GOOGLE_API_KEY"],
    },
    "nemotron": {
        "base_url": "https://integrate.api.nvidia.com/v1",
        "model_name": "nvidia/llama-3.1-nemotron-70b-instruct",
        "display_name": "NVIDIA Nemotron 70B (High Reasoning)",
        "env_vars": ["NEMOTRON_API_KEY", "NVIDIA_API_KEY"],
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "model_name": "gpt-4o-mini",
        "display_name": "OpenAI GPT-4o-mini",
        "env_vars": ["OPENAI_API_KEY"],
    },
}


class LLMConfig(BaseModel):
    api_key: Optional[str] = Field(default=None, description="API Key for the active provider")
    base_url: str = Field(
        default="https://generativelanguage.googleapis.com/v1beta/openai",
        description="API base URL",
    )
    model_name: str = Field(
        default="gemini-2.0-flash-lite",
        description="Target model identifier",
    )
    provider: str = Field(default="gemini", description="Active provider preset: gemini, nemotron, openai, or custom")
    enabled: bool = Field(default=True, description="Whether remote escalation is active")
    confidence_threshold: float = Field(
        default=0.75,
        description="Local confidence score threshold below which analysis is escalated to LLM",
    )
    api_key_source: str = Field(default="none", description="environment, user_configured, or none")


class NemotronClient:
    """
    Unified client for LLM providers (Google Gemini Flash-Lite, NVIDIA Nemotron, OpenAI).
    All data sent through this client MUST be PII-anonymized first.
    """

    def __init__(self, config: Optional[LLMConfig] = None):
        if config:
            self.config = config
            # Infer provider only if the model or URL strongly indicates a different provider
            # and provider wasn't explicitly matched
            if "nemotron" in self.config.model_name.lower():
                self.config.provider = "nemotron"
            elif "gpt" in self.config.model_name.lower() or (
                "openai.com" in self.config.base_url.lower() and "google" not in self.config.base_url.lower()
            ):
                self.config.provider = "openai"
            elif "gemini" in self.config.model_name.lower() or "googleapis.com" in self.config.base_url.lower():
                self.config.provider = "gemini"
        else:
            self.config = self._discover_initial_config()

    def _discover_initial_config(self) -> LLMConfig:
        """Automatically detect active API keys from the environment prioritizing Gemini Flash Lite."""
        # 1. Check Gemini
        for var in PROVIDER_PRESETS["gemini"]["env_vars"]:
            val = os.getenv(var)
            if val:
                return LLMConfig(
                    api_key=val,
                    base_url=PROVIDER_PRESETS["gemini"]["base_url"],
                    model_name=os.getenv("GEMINI_MODEL_NAME", PROVIDER_PRESETS["gemini"]["model_name"]),
                    provider="gemini",
                    enabled=True,
                    api_key_source="environment",
                )

        # 2. Check Nemotron
        for var in PROVIDER_PRESETS["nemotron"]["env_vars"]:
            val = os.getenv(var)
            if val:
                return LLMConfig(
                    api_key=val,
                    base_url=os.getenv("NEMOTRON_BASE_URL", PROVIDER_PRESETS["nemotron"]["base_url"]),
                    model_name=os.getenv("NEMOTRON_MODEL_NAME", PROVIDER_PRESETS["nemotron"]["model_name"]),
                    provider="nemotron",
                    enabled=True,
                    api_key_source="environment",
                )

        # 3. Check OpenAI / generic
        for var in PROVIDER_PRESETS["openai"]["env_vars"] + ["LLM_API_KEY"]:
            val = os.getenv(var)
            if val:
                return LLMConfig(
                    api_key=val,
                    base_url=os.getenv("OPENAI_BASE_URL", PROVIDER_PRESETS["openai"]["base_url"]),
                    model_name=os.getenv("OPENAI_MODEL_NAME", PROVIDER_PRESETS["openai"]["model_name"]),
                    provider="openai",
                    enabled=True,
                    api_key_source="environment",
                )

        # 4. Fallback default: Gemini Flash-Lite ready for BYOK or local operation
        return LLMConfig(
            api_key=None,
            base_url=PROVIDER_PRESETS["gemini"]["base_url"],
            model_name=PROVIDER_PRESETS["gemini"]["model_name"],
            provider="gemini",
            enabled=False,
            api_key_source="none",
        )

    def is_configured(self) -> bool:
        return bool(self.config.api_key and self.config.enabled)

    def get_status(self) -> Dict[str, Any]:
        """Return clean telemetry regarding current provider, status, and environment allowance."""
        masked_key = None
        if self.config.api_key:
            k = self.config.api_key
            masked_key = f"{k[:4]}...{k[-4:]}" if len(k) > 8 else "***"

        # Check if an environment key exists for quick indicator
        env_available_provider = None
        for prov, info in PROVIDER_PRESETS.items():
            for env_var in info["env_vars"]:
                if os.getenv(env_var):
                    env_available_provider = prov
                    break
            if env_available_provider:
                break

        return {
            "configured": self.is_configured(),
            "provider": self.config.provider,
            "model_name": self.config.model_name,
            "base_url": self.config.base_url,
            "enabled": self.config.enabled,
            "confidence_threshold": self.config.confidence_threshold,
            "api_key_source": self.config.api_key_source,
            "masked_key": masked_key,
            "env_available_provider": env_available_provider,
            "available_presets": {
                k: {"name": v["display_name"], "model": v["model_name"]}
                for k, v in PROVIDER_PRESETS.items()
            },
        }

    def update_config(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        enabled: Optional[bool] = None,
        confidence_threshold: Optional[float] = None,
        provider: Optional[str] = None,
    ):
        if provider and provider in PROVIDER_PRESETS:
            preset = PROVIDER_PRESETS[provider]
            self.config.provider = provider
            if base_url is None:
                self.config.base_url = preset["base_url"]
            if model_name is None:
                self.config.model_name = preset["model_name"]
            # Auto-check environment key for this provider if user didn't pass one
            if api_key is None and not self.config.api_key:
                for env_var in preset["env_vars"]:
                    val = os.getenv(env_var)
                    if val:
                        self.config.api_key = val
                        self.config.api_key_source = "environment"
                        break
        elif provider:
            self.config.provider = provider

        if api_key is not None:
            self.config.api_key = api_key.strip() if api_key else None
            self.config.api_key_source = "user_configured" if api_key else "none"
        if base_url is not None:
            self.config.base_url = base_url.rstrip("/")
        if model_name is not None:
            self.config.model_name = model_name.strip()
        if enabled is not None:
            self.config.enabled = enabled
        if confidence_threshold is not None:
            self.config.confidence_threshold = confidence_threshold

        # If a key exists, auto-enable
        if self.config.api_key and enabled is None:
            self.config.enabled = True

    async def test_connection(self) -> Dict[str, Any]:
        """Verify API key and endpoint health with a minimal prompt."""
        if not self.config.api_key:
            return {
                "success": False,
                "message": (
                    f"No API key active for {self.config.provider.upper()}. Set GEMINI_API_KEY in env "
                    "or enter your key in Settings."
                ),
            }

        url = f"{self.config.base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.config.model_name,
            "messages": [
                {"role": "system", "content": "Respond with 'OK'."},
                {"role": "user", "content": "Ping"},
            ],
            "max_tokens": 10,
            "temperature": 0.1,
        }

        try:
            async with httpx.AsyncClient(timeout=12.0) as client:
                res = await client.post(url, headers=headers, json=payload)
                if res.status_code == 200:
                    return {
                        "success": True,
                        "provider": self.config.provider,
                        "model": self.config.model_name,
                        "base_url": self.config.base_url,
                        "message": f"Successfully connected to {self.config.provider.title()} ({self.config.model_name})!",
                    }
                else:
                    return {
                        "success": False,
                        "status_code": res.status_code,
                        "message": f"API returned error: {res.text[:220]}",
                    }
        except Exception as e:
            return {
                "success": False,
                "message": f"Connection error: {str(e)}",
            }

    async def deep_reason_clause(
        self,
        anonymized_text: str,
        section_title: str,
        local_category: str,
        local_score: int,
        local_traps: List[str],
    ) -> Optional[Dict[str, Any]]:
        """
        Escalates an ambiguous / low-confidence / twisted clause to the active LLM
        (Gemini Flash-Lite / Nemotron / OpenAI) for deep legal synthesis.
        The input text MUST already be PII-redacted.
        """
        if not self.is_configured():
            return None

        prompt = f"""You are an expert commercial contract attorney analyzing a specific clause.
The clause has had all PII and sensitive party names anonymized:
Section Title: {section_title}
Assigned Category: {local_category}
Clause Text:
\"\"\"{anonymized_text}\"\"\"

Local heuristics scored this clause at {local_score}/100 with potential traps: {', '.join(local_traps) if local_traps else 'None identified'}.
However, local confidence was low or borderline due to potential obfuscation or complex drafting.

Provide a rigorous legal synthesis in valid JSON format with the following keys:
- "risk_score": integer from 0 to 100 representing true liability exposure
- "severity": "LOW", "MEDIUM", or "HIGH"
- "detected_traps": list of strings naming specific legal traps or risks
- "plain_english_summary": 2-3 sentences explaining exactly what this clause obligates
- "what_it_means_for_you": 2-3 sentences explaining real-world business risks or worst-case scenarios
- "negotiation_tip": 1-2 sentences with concrete redline/fallback text to balance the clause
- "reasoning": brief explanation of why this risk score was assigned

Respond ONLY with valid JSON.
"""

        url = f"{self.config.base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.config.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a specialized commercial contract risk analysis engine. Always output strict JSON.",
                },
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
            "max_tokens": 800,
        }

        try:
            async with httpx.AsyncClient(timeout=25.0) as client:
                res = await client.post(url, headers=headers, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    content = data["choices"][0]["message"]["content"].strip()
                    # Strip markdown code fences if present
                    if content.startswith("```"):
                        lines = content.splitlines()
                        if lines[0].startswith("```"):
                            lines = lines[1:]
                        if lines and lines[-1].startswith("```"):
                            lines = lines[:-1]
                        content = "\n".join(lines).strip()
                    return json.loads(content)
                else:
                    logger.warning(f"LLM API error {res.status_code}: {res.text[:150]}")
                    return None
        except Exception as e:
            logger.error(f"Failed to call LLM: {e}")
            return None

    async def chat_completion(
        self,
        query: str,
        anonymized_contract_context: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> Optional[str]:
        """Direct conversational query using active LLM with contract context."""
        if not self.is_configured():
            return None

        provider_title = self.config.provider.title()
        system_prompt = f"""You are Legal-Ease, an expert AI legal navigator powered by {provider_title} designed to help freelancers, contractors, and small business owners understand contracts.
The contract text below has all personal PII anonymized:
--- CONTRACT CONTEXT ---
{anonymized_contract_context[:6000]}
--- END CONTEXT ---

Guidelines:
1. Ground your answers strictly in the clauses provided.
2. Explain legal jargon in clear plain English.
3. Highlight risks, hidden traps, and practical consequences.
4. Suggest concrete redline proposals where appropriate.
5. End with a reminder that this is educational literacy and not formal legal advice.
"""

        messages = [{"role": "system", "content": system_prompt}]
        if conversation_history:
            for msg in conversation_history[-4:]:
                messages.append(msg)
        messages.append({"role": "user", "content": query})

        url = f"{self.config.base_url.rstrip('/')}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.config.model_name,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 1000,
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(url, headers=headers, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    return data["choices"][0]["message"]["content"].strip()
                return None
        except Exception as e:
            logger.error(f"LLM chat error: {e}")
            return None


# Backward-compatible alias
LLMClient = NemotronClient
