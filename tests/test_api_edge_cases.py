"""
Comprehensive API Edge-Case and Error Handling Integration Tests for Legal-Ease.
Tests all FastAPI endpoints against invalid inputs, boundary conditions, file uploads,
sanitization defenses, and conversational query routing.
"""

import io
import pytest
from fastapi.testclient import TestClient
from legal_ease.main import app
from legal_ease.sample_contracts import FREELANCE_HIGH_RISK, FREELANCE_NEGOTIATED

client = TestClient(app)


class TestAnalyzeEndpointEdgeCases:
    """Test /api/analyze validation and error branches."""

    def test_analyze_empty_text_returns_400(self):
        res = client.post("/api/analyze", json={"text": ""})
        assert res.status_code == 400
        data = res.json()
        assert data["error"] is True
        assert "Contract text cannot be empty" in data["detail"]

    def test_analyze_whitespace_text_returns_400(self):
        res = client.post("/api/analyze", json={"text": "   \n\t  \n   "})
        assert res.status_code == 400
        assert res.json()["error"] is True

    def test_analyze_missing_body_returns_422(self):
        res = client.post("/api/analyze", json={})
        assert res.status_code == 422

    def test_analyze_auto_title_inference(self):
        contract_text = "MUTUAL CONFIDENTIALITY AND NONDISCLOSURE AGREEMENT\n1. Scope. Parties agree to exchange trade secrets."
        res = client.post("/api/analyze", json={"text": contract_text})
        assert res.status_code == 200
        data = res.json()
        assert res.status_code == 200
        assert "attorney_checklist" in data
        assert "MUTUAL CONFIDENTIALITY" in data["attorney_checklist"]["markdown_report"]


class TestAnalyzeFileEndpointEdgeCases:
    """Test /api/analyze-file multipart upload handling."""

    def test_upload_valid_txt_file(self):
        content = b"1. Term. This agreement shall remain in effect for two years."
        files = {"file": ("contract.txt", io.BytesIO(content), "text/plain")}
        res = client.post("/api/analyze-file", files=files, data={"title": "Custom TXT Title"})
        assert res.status_code == 200
        data = res.json()
        assert data["risk_overview"]["total_clauses"] >= 1
        assert "CUSTOM TXT TITLE" in data["attorney_checklist"]["markdown_report"]

    def test_upload_valid_markdown_file(self):
        content = b"# Independent Contractor Agreement\n\n## 1. Services\nContractor shall build web apps."
        files = {"file": ("agreement.md", io.BytesIO(content), "text/markdown")}
        res = client.post("/api/analyze-file", files=files)
        assert res.status_code == 200
        data = res.json()
        assert data["risk_overview"]["total_clauses"] >= 1

    def test_upload_empty_file_returns_400(self):
        files = {"file": ("empty.txt", io.BytesIO(b"   "), "text/plain")}
        res = client.post("/api/analyze-file", files=files)
        assert res.status_code == 400
        data = res.json()
        assert data["error"] is True
        assert "Uploaded file is empty" in data["detail"]

    def test_upload_latin1_encoded_file(self):
        # Bytes containing Latin-1 characters like © and accented letters
        latin1_bytes = "1. Copyright Notice © 2026 Société Générale.".encode("latin-1")
        files = {"file": ("legal_fr.txt", io.BytesIO(latin1_bytes), "text/plain")}
        res = client.post("/api/analyze-file", files=files)
        assert res.status_code == 200


class TestCompareEndpointEdgeCases:
    """Test /api/compare validation and diffing branches."""

    def test_compare_missing_v1_returns_400(self):
        res = client.post(
            "/api/compare",
            json={"text_v1": "   ", "text_v2": "1. Term. 30 days."},
        )
        assert res.status_code == 400
        data = res.json()
        assert data["error"] is True
        assert "Both original (v1) and revised (v2) texts are required" in data["detail"]

    def test_compare_missing_v2_returns_400(self):
        res = client.post(
            "/api/compare",
            json={"text_v1": "1. Term. 30 days.", "text_v2": ""},
        )
        assert res.status_code == 400
        data = res.json()
        assert data["error"] is True

    def test_compare_increasing_risk_trajectory(self):
        safe_v1 = "1. Indemnification. Each party mutually indemnifies the other for gross negligence."
        dangerous_v2 = (
            "1. Indemnification. Contractor unconditionally defends and indemnifies Company for any and all claims, "
            "including all attorney fees. Company aggregate liability is capped at $50."
        )
        res = client.post(
            "/api/compare",
            json={
                "text_v1": safe_v1,
                "text_v2": dangerous_v2,
                "title_v1": "Safe Draft",
                "title_v2": "Dangerous Redline",
            },
        )
        assert res.status_code == 200
        data = res.json()
        assert data["risk_index_delta"] > 0
        assert data["trajectory"] == "MORE_RISK"


class TestChatEndpointEdgeCases:
    """Test /api/chat interactive legal Q&A and prompt injection barriers."""

    def test_chat_empty_message_returns_400(self):
        res = client.post(
            "/api/chat",
            json={"message": "   ", "contract_text": "1. Term. 1 year."},
        )
        assert res.status_code == 400
        data = res.json()
        assert data["error"] is True
        assert "Query message cannot be empty" in data["detail"]

    def test_chat_liability_and_lawsuits(self):
        res = client.post(
            "/api/chat",
            json={
                "message": "Will I be sued or made to pay damages under this contract?",
                "contract_text": FREELANCE_HIGH_RISK,
            },
        )
        assert res.status_code == 200
        data = res.json()
        assert "Liability" in data["answer"] or "Indemn" in data["answer"]
        assert len(data["referenced_clauses"]) >= 1

    def test_chat_intellectual_property(self):
        res = client.post(
            "/api/chat",
            json={
                "message": "Do I own my code, tools, and background intellectual property?",
                "contract_text": FREELANCE_HIGH_RISK,
            },
        )
        assert res.status_code == 200
        data = res.json()
        assert "Intellectual Property" in data["answer"] or "IP" in data["answer"]

    def test_chat_non_compete_restrictions(self):
        contract_with_nc = (
            "1. Non-Compete. Contractor agrees not to compete with Client anywhere in the world for 3 years.\n"
            "2. Payment. Net 90 payment terms."
        )
        res = client.post(
            "/api/chat",
            json={
                "message": "Can I work for other clients or does this have a non-compete?",
                "contract_text": contract_with_nc,
            },
        )
        assert res.status_code == 200
        data = res.json()
        assert "Restrictive Covenants" in data["answer"] or "Non-Compete" in data["answer"]

    def test_chat_payment_terms_and_delays(self):
        contract_with_pay = "1. Payment. Client shall pay invoices Net 90 days."
        res = client.post(
            "/api/chat",
            json={
                "message": "What are the payment terms and invoice rates?",
                "contract_text": contract_with_pay,
            },
        )
        assert res.status_code == 200
        data = res.json()
        assert "Payment" in data["answer"] or "Compensation" in data["answer"]

    def test_chat_unmatched_query_fallback(self):
        res = client.post(
            "/api/chat",
            json={
                "message": "What is the capital of France?",
                "contract_text": "1. Governing Law. This agreement is governed by the laws of Delaware.",
            },
        )
        assert res.status_code == 200
        data = res.json()
        # Fallback guidance
        assert "didn't find specific clauses" in data["answer"]
        assert "Liability" in data["answer"]


class TestSettingsAndHealthTelemetry:
    """Test telemetry, connection testing, and runtime settings modifications."""

    def test_health_telemetry_keys(self):
        res = client.get("/api/health")
        assert res.status_code == 200
        data = res.json()
        required_keys = [
            "status", "service", "version", "vertical", "provider",
            "llm_configured", "api_key_source", "nemotron_configured",
            "model", "cython_accelerated", "acceleration_info",
        ]
        for key in required_keys:
            assert key in data, f"Missing key '{key}' in /api/health telemetry"

    def test_test_llm_connection_endpoint(self):
        res = client.post("/api/settings/test")
        assert res.status_code == 200
        data = res.json()
        assert "connected" in data or "status" in data or "message" in data

    def test_cors_preflight_headers(self):
        res = client.options(
            "/api/analyze",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "POST",
            },
        )
        assert res.status_code == 200
        assert "access-control-allow-origin" in res.headers
