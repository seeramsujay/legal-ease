"""
Bridge loader for Cython-compiled extensions with zero-overhead fallback.
Exposes Levenshtein distance, token similarity, and engine metadata.
Guarantees null-safe inputs so that None or empty strings never raise TypeErrors.
"""

from typing import Dict, Any, Optional

try:
    from legal_ease.fast_ops import (
        fast_levenshtein_distance,
        fast_token_similarity,
        get_cython_engine_status,
    )
    _IS_CYTHON = True
except ImportError:
    from legal_ease.fast_ops_py import (
        fast_levenshtein_distance,
        fast_token_similarity,
        get_cython_engine_status,
    )
    _IS_CYTHON = False


def is_cython_accelerated() -> bool:
    """Returns True if the native Cython C-extension (.so) is compiled and running."""
    return _IS_CYTHON


def compute_levenshtein(s1: Optional[str], s2: Optional[str]) -> int:
    """
    Computes Levenshtein edit distance between two strings with C-speed or Python fallback.
    Defensively coerces None or non-string arguments to empty strings.
    """
    safe_s1 = str(s1) if s1 is not None else ""
    safe_s2 = str(s2) if s2 is not None else ""
    return fast_levenshtein_distance(safe_s1, safe_s2)


def compute_similarity(s1: Optional[str], s2: Optional[str]) -> float:
    """
    Computes token-level Jaccard similarity (0.0 to 1.0) between two text blocks.
    Defensively coerces None or non-string arguments to empty strings.
    """
    safe_s1 = str(s1) if s1 is not None else ""
    safe_s2 = str(s2) if s2 is not None else ""
    return fast_token_similarity(safe_s1, safe_s2)


def get_acceleration_info() -> Dict[str, Any]:
    """Retrieve runtime compiler acceleration telemetry and optimization flags."""
    return get_cython_engine_status()
