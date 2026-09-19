"""
Unified LLM Client Supporting Google Gemini (Flash-Lite / Flash 2.0),
NVIDIA Nemotron, and OpenAI-Compatible Endpoints with Local-First
Confidence-Based Escalation Routing and Environment Key Auto-Detection.
"""

import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
import httpx
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


def _load_env_file() -> None:
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
    """Configuration state for remote LLM escalation."""
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
    Reuses connection pools and provides zero-crash error boundaries.
    """

    def __init__(self, config: Optional[LLMConfig] = None) -> None:
        if config:
            self.config = config
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

        # Shared connection limits for high-performance keepalive reuse
        self._limits = httpx.Limits(max_keepalive_connections=10, max_connections=20)

    def _discover_initial_config(self) -> LLMConfig:
        """Automatically detect active API keys from the environment prioritizing user preference or Gemini Flash Lite."""
        _load_env_file()
        threshold = 0.75
        try:
            if "CONFIDENCE_THRESHOLD" in os.environ:
                threshold = float(os.environ["CONFIDENCE_THRESHOLD"])
        except ValueError:
            threshold = 0.75

        preferred_prov = os.getenv("LLM_PROVIDER", "").lower().strip()
        provider_order = ["gemini", "nemotron", "openai"]
        if preferred_prov in provider_order:
            provider_order.remove(preferred_prov)
            provider_order.insert(0, preferred_prov)

        for prov in provider_order:
            preset = PROVIDER_PRESETS[prov]
            vars_to_check = preset["env_vars"] + (["LLM_API_KEY"] if prov == "openai" else [])
            for var in vars_to_check:
                val = os.getenv(var)
                if val and val.strip():
                    return LLMConfig(
                        api_key=val.strip(),
                        base_url=os.getenv(f"{prov.upper()}_BASE_URL", preset["base_url"]),
                        model_name=os.getenv(f"{prov.upper()}_MODEL_NAME", preset["model_name"]),
                        provider=prov,
                        enabled=True,
                        confidence_threshold=threshold,
                        api_key_source="environment",
                    )

        target_prov = preferred_prov if preferred_prov in PROVIDER_PRESETS else "gemini"
        preset = PROVIDER_PRESETS[target_prov]
        return LLMConfig(
            api_key=None,
            base_url=os.getenv(f"{target_prov.upper()}_BASE_URL", preset["base_url"]),
            model_name=os.getenv(f"{target_prov.upper()}_MODEL_NAME", preset["model_name"]),
            provider=target_prov,
            enabled=False,
            confidence_threshold=threshold,
            api_key_source="none",
        )

    def reset_to_environment(self) -> None:
        """Resets runtime configuration back to discovered environment variables."""
        _load_env_file()
        self.config = self._discover_initial_config()

    def is_configured(self) -> bool:
        """Returns True if a valid API key is present and remote escalation is enabled."""
        return bool(self.config.api_key and self.config.enabled)

    def get_status(self) -> Dict[str, Any]:
        """Return clean telemetry regarding current provider, status, and environment allowance."""
        masked_key = None
        if self.config.api_key:
            k = self.config.api_key
            masked_key = f"{k[:4]}...{k[-4:]}" if len(k) > 8 else "***"

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
    ) -> None:
        """Updates provider and endpoint configuration dynamically at runtime."""
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
            cleaned = api_key.strip()
            if cleaned:
                self.config.api_key = cleaned
                self.config.api_key_source = "user_configured"
                if enabled is None:
                    self.config.enabled = True
            else:
                # User cleared BYOK; try to find an environment key for this provider
                env_key = None
                for env_var in PROVIDER_PRESETS.get(self.config.provider, {}).get("env_vars", []):
                    val = os.getenv(env_var)
                    if val and val.strip():
                        env_key = val.strip()
                        break
                if env_key:
                    self.config.api_key = env_key
                    self.config.api_key_source = "environment"
                    if enabled is None:
                        self.config.enabled = True
                else:
                    self.config.api_key = None
                    self.config.api_key_source = "none"
                    if enabled is None:
                        self.config.enabled = False

        if base_url is not None:
            self.config.base_url = base_url.rstrip("/")
        if model_name is not None:
            self.config.model_name = model_name.strip()
        if enabled is not None:
            self.config.enabled = enabled
        if confidence_threshold is not None:
            self.config.confidence_threshold = confidence_threshold

        if self.config.api_key and enabled is None and api_key is not None:
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
                {"role": "system", "content": "Respond with 'OK'." if not self.config.provider == 'gemini' else "OK"},
                {"role": "user", "content": "Ping"},
            ],
            "max_tokens": 10,
            "temperature": 0.1,
        }

        try:
            async with httpx.AsyncClient(timeout=12.0, limits=self._limits) as client:
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
        anonymized_text: Optional[str],
        section_title: Optional[str],
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

        safe_text = str(anonymized_text) if anonymized_text else ""
        safe_title = str(section_title) if section_title else "Untitled Section"

        prompt = f"""You are an expert commercial contract attorney analyzing a specific clause.
The clause has had all PII and sensitive party names anonymized:
Section Title: {safe_title}
Assigned Category: {local_category}
Clause Text:
\"\"\"{safe_text}\"\"\"

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
            async with httpx.AsyncClient(timeout=25.0, limits=self._limits) as client:
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
        query: Optional[str],
        anonymized_contract_context: Optional[str],
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> Optional[str]:
        """Direct conversational query using active LLM with contract context."""
        if not self.is_configured():
            return None

        safe_query = str(query) if query else ""
        safe_context = str(anonymized_contract_context)[:6000] if anonymized_contract_context else ""

        provider_title = self.config.provider.title()
        system_prompt = f"""You are Legal-Ease, an expert AI legal navigator powered by {provider_title} designed to help freelancers, contractors, and small business owners understand contracts.
The contract text below has all personal PII anonymized:
--- CONTRACT CONTEXT ---
{safe_context}
--- END CONTEXT ---

CRITICAL INSTRUCTIONS:
1. Ground your answers strictly in the contract text provided above.
2. Cite specific clauses, section titles, and language when answering.
3. Be candid, direct, and conversational. Highlight hidden risks, unilateral terms, and unfair provisions.
4. Provide concrete negotiation advice or fallback redline proposals where appropriate.
5. NEVER pretend to provide formal legal representation or legal advice. Include informational explanations.
"""
        messages = [{"role": "system", "content": system_prompt}]

        # Append previous conversation history
        if conversation_history:
            for msg in conversation_history[-6:]:
                role = msg.get("role", "user")
                if role in ("user", "assistant"):
                    messages.append({"role": role, "content": msg.get("content", "")})

        messages.append({"role": "user", "content": safe_query})

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
            async with httpx.AsyncClient(timeout=30.0, limits=self._limits) as client:
                res = await client.post(url, headers=headers, json=payload)
                if res.status_code == 200:
                    data = res.json()
                    return data["choices"][0]["message"]["content"].strip()
                else:
                    logger.warning(f"Chat completion error {res.status_code}: {res.text[:150]}")
                    return None
        except Exception as e:
            logger.error(f"Chat completion call failed: {e}")
            return None
