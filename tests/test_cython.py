"""
Unit tests for Cython C-extension acceleration and Python fallback parity.
"""

from legal_ease.fast_ops_bridge import (
    compute_levenshtein,
    compute_similarity,
    is_cython_accelerated,
    get_acceleration_info,
)
from legal_ease.fast_ops_py import (
    fast_levenshtein_distance as py_levenshtein,
    fast_token_similarity as py_similarity,
)


def test_cython_engine_telemetry():
    """Verify telemetry correctly identifies engine state."""
    info = get_acceleration_info()
    assert "compiled" in info
    assert "engine" in info
    assert isinstance(is_cython_accelerated(), bool)


def test_levenshtein_parity():
    """Verify C-extension and pure Python calculate identical Levenshtein distances."""
    pairs = [
        ("indemnification", "indemnify"),
        ("limitation of liability", "limitation of liabilities"),
        ("arbitration", "litigation"),
        ("", "non-empty string"),
        ("identical clause", "identical clause"),
    ]

    for s1, s2 in pairs:
        c_val = compute_levenshtein(s1, s2)
        py_val = py_levenshtein(s1, s2)
        assert c_val == py_val, f"Mismatch for '{s1}' vs '{s2}': C={c_val}, Py={py_val}"


def test_token_similarity_parity():
    """Verify token Jaccard similarity returns identical results."""
    t1 = "Contractor agrees to indemnify Company against all third party claims"
    t2 = "Contractor shall indemnify and hold harmless Company from third party claims"

    c_sim = compute_similarity(t1, t2)
    py_sim = py_similarity(t1, t2)

    assert abs(c_sim - py_sim) < 1e-4
    assert 0.0 < c_sim < 1.0


def test_health_reports_cython(test_client=None):
    from fastapi.testclient import TestClient
    from legal_ease.main import app

    client = TestClient(app)
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert "cython_accelerated" in data
    assert "acceleration_info" in data
