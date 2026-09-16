"""
OpenAI-compatible client with specialized support for NVIDIA Nemotron models
and local-first confidence-based escalation routing.
"""

import os
import json
import logging
from typing import Optional, Dict, Any, List
import httpx
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class LLMConfig(BaseModel):
    api_key: Optional[str] = Field(default=None, description="OpenAI or Nemotron API Key")
    base_url: str = Field(
        default="https://integrate.api.nvidia.com/v1",
        description="OpenAI-compatible API base URL (e.g., NVIDIA Build, OpenRouter, vLLM, Ollama)",
    )
    model_name: str = Field(
        default="nvidia/llama-3.1-nemotron-70b-instruct",
        description="Target model identifier",
    )
    enabled: bool = Field(default=True, description="Whether remote escalation is active")
    confidence_threshold: float = Field(
        default=0.75,
        description="Local confidence score threshold below which analysis is escalated to LLM",
    )


class NemotronClient:
    """
    Client for OpenAI-compatible APIs (specifically tuned for NVIDIA Nemotron models).
    All data sent through this client MUST be PII-anonymized first.
    """

    def __init__(self, config: Optional[LLMConfig] = None):
        if config:
            self.config = config
        else:
            # Fall back to environment variables
            api_key = (
                os.getenv("NEMOTRON_API_KEY")
                or os.getenv("OPENAI_API_KEY")
                or os.getenv("LLM_API_KEY")
            )
            base_url = os.getenv("OPENAI_BASE_URL", "https://integrate.api.nvidia.com/v1")
            model_name = os.getenv(
                "OPENAI_MODEL_NAME", "nvidia/llama-3.1-nemotron-70b-instruct"
            )
            self.config = LLMConfig(
                api_key=api_key,
                base_url=base_url,
                model_name=model_name,
                enabled=bool(api_key),
            )

    def is_configured(self) -> bool:
        return bool(self.config.api_key and self.config.enabled)

    def update_config(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        enabled: Optional[bool] = None,
        confidence_threshold: Optional[float] = None,
    ):
        if api_key is not None:
            self.config.api_key = api_key
        if base_url is not None:
            self.config.base_url = base_url.rstrip("/")
        if model_name is not None:
            self.config.model_name = model_name
        if enabled is not None:
            self.config.enabled = enabled
        if confidence_threshold is not None:
            self.config.confidence_threshold = confidence_threshold

    async def test_connection(self) -> Dict[str, Any]:
        """Verify API key and endpoint health with a minimal prompt."""
        if not self.config.api_key:
            return {
                "success": False,
                "message": "No API key configured. Provide an OpenAI-compatible / Nemotron API key.",
            }

        url = f"{self.config.base_url}/chat/completions"
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
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(url, headers=headers, json=payload)
                if res.status_code == 200:
                    return {
                        "success": True,
                        "model": self.config.model_name,
                        "base_url": self.config.base_url,
                        "message": "Successfully connected to Nemotron / OpenAI-compatible endpoint!",
                    }
                else:
                    return {
                        "success": False,
                        "status_code": res.status_code,
                        "message": f"API returned error: {res.text[:200]}",
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
        Escalates an ambiguous / low-confidence clause to Nemotron for deep legal synthesis.
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
However, local confidence was low or borderline. 

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

        url = f"{self.config.base_url}/chat/completions"
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
                    logger.warning(f"Nemotron API error {res.status_code}: {res.text[:150]}")
                    return None
        except Exception as e:
            logger.error(f"Failed to call Nemotron: {e}")
            return None

    async def chat_completion(
        self,
        query: str,
        anonymized_contract_context: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
    ) -> Optional[str]:
        """Direct conversational query using Nemotron with contract context."""
        if not self.is_configured():
            return None

        system_prompt = f"""You are Legal-Ease, an expert AI legal navigator designed to help freelancers, contractors, and small business owners understand contracts.
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

        url = f"{self.config.base_url}/chat/completions"
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
            logger.error(f"Nemotron chat error: {e}")
            return None
