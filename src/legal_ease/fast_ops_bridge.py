"""
Bridge loader for Cython-compiled extensions with zero-overhead fallback.
Exposes Levenshtein distance, token similarity, and engine metadata.
"""

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
    """Returns True if Cython binary C-extensions are loaded and running."""
    return _IS_CYTHON


def compute_levenshtein(s1: str, s2: str) -> int:
    """Compute string edit distance with C-speed or Python fallback."""
    return fast_levenshtein_distance(s1, s2)


def compute_similarity(s1: str, s2: str) -> float:
    """Compute token Jaccard similarity (0.0 to 1.0)."""
    return fast_token_similarity(s1, s2)


def get_acceleration_info():
    """Retrieve runtime compiler acceleration telemetry."""
    return get_cython_engine_status()
