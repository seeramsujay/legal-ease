"""
Unit tests for high-velocity string algorithms, Cython compilation bridge, and fallback Python math.
Verifies numerical equivalence, boundary handling, and algorithmic invariants.
"""

import pytest
from legal_ease import fast_ops_py
from legal_ease import fast_ops_bridge


class TestFastOpsPy:
    """Test pure Python fallback implementation of Levenshtein and Jaccard metrics."""

    def test_fast_levenshtein_identical_strings(self):
        assert fast_ops_py.fast_levenshtein_distance("indemnification", "indemnification") == 0
        assert fast_ops_py.fast_levenshtein_distance("", "") == 0

    def test_fast_levenshtein_empty_and_none(self):
        assert fast_ops_py.fast_levenshtein_distance("liability", "") == len("liability")
        assert fast_ops_py.fast_levenshtein_distance("", "arbitration") == len("arbitration")
        assert fast_ops_py.fast_levenshtein_distance(None, "arbitration") == len("arbitration")
        assert fast_ops_py.fast_levenshtein_distance("arbitration", None) == len("arbitration")

    def test_fast_levenshtein_symmetry(self):
        s1 = "unilateral indemnity"
        s2 = "mutual indemnity agreement"
        assert fast_ops_py.fast_levenshtein_distance(s1, s2) == fast_ops_py.fast_levenshtein_distance(s2, s1)

    def test_fast_token_similarity_bounds(self):
        sim = fast_ops_py.fast_token_similarity("termination for cause", "termination for convenience")
        assert 0.0 <= sim <= 1.0

        # Exact match
        assert fast_ops_py.fast_token_similarity("governing law", "governing law") == 1.0
        # Empty match
        assert fast_ops_py.fast_token_similarity("", "") == 1.0
        assert fast_ops_py.fast_token_similarity(None, None) == 1.0

    def test_fast_token_similarity_disjoint_and_overlap(self):
        s1 = "arbitration confidentiality waiver"
        s2 = "payment invoice compensation"
        assert fast_ops_py.fast_token_similarity(s1, s2) == 0.0

        s3 = "arbitration dispute venue"
        # Intersection: {"arbitration"} (1). Union: 5 words.
        sim = fast_ops_py.fast_token_similarity(s1, s3)
        assert pytest.approx(sim, 0.01) == 1 / 5


class TestFastOpsBridge:
    """Test unified FastOps bridge and runtime acceleration telemetry."""

    def test_bridge_acceleration_info(self):
        info = fast_ops_bridge.get_acceleration_info()
        assert isinstance(info, dict)
        assert "compiled" in info
        assert "engine" in info

    def test_bridge_parity_with_python(self):
        s1 = "consultant agrees to hold harmless"
        s2 = "contractor agrees to defend and hold harmless"

        bridge_dist = fast_ops_bridge.compute_levenshtein(s1, s2)
        py_dist = fast_ops_py.fast_levenshtein_distance(s1, s2)
        assert bridge_dist == py_dist

        bridge_sim = fast_ops_bridge.compute_similarity(s1, s2)
        py_sim = fast_ops_py.fast_token_similarity(s1, s2)
        assert pytest.approx(bridge_sim, 0.001) == py_sim

    def test_bridge_none_safety(self):
        # Defensively handles None without throwing TypeError
        assert fast_ops_bridge.compute_levenshtein(None, None) == 0
        assert fast_ops_bridge.compute_similarity(None, None) == 1.0
